"""
Ensemble workflow for combining predictions from multiple models.
Supports both compatible (same dimensions) and incompatible (different dimensions) models.
"""

import time
from pathlib import Path
from typing import List, Dict, Optional
import numpy as np

from config import get_model_config, get_all_ontologies, PREDICTION_SETTINGS, ENSEMBLE_GC_COLLECT_INTERVAL, get_extra_output_name
from utils.ontology_utils import iterate_ontologies_with_check
from utils.logging import setup_logging, get_logger
from prediction.predict_and_submit import load_test_sequences, post_process_submission
from prediction.ensemble import (
    ensemble_predictions,
    check_ensemble_compatibility,
    align_model_features
)
from pipelines.workflows.workflow_paths import setup_workflow_paths
from pipelines.workflows.workflow_features import extract_features_for_model, get_feature_cache_key
from pipelines.workflows.workflow_predictions import write_predictions_to_file
from utils.model_io import load_model
from utils.utils_common import cleanup_memory


logger = get_logger(__name__)


def run_ensemble_prediction_per_ontology(models_per_ontology: Dict[str, List[str]],
                                       ensemble_method: str = 'average',
                                       weights: Optional[List[float]] = None,
                                       padding_strategy: Optional[str] = None,
                                       output_name: Optional[str] = None,
                                       extra_output_name: Optional[str] = None,
                                       **ensemble_kwargs) -> str:
    """
    Run ensemble prediction workflow with per-ontology model specifications.
    
    Args:
        models_per_ontology: Dict mapping ont_code -> list of model config names
                            Example: {'F': ['logistic_v1_1', 'xgboost_v2'], 
                                     'P': ['logistic_v1_1', 'xgboost_v2'],
                                     'C': ['logistic_v1_1', 'xgboost_v1']}
        ensemble_method: Ensemble method ('average', 'weighted_average', etc.)
        weights: Optional weights for weighted_average
        padding_strategy: Strategy for handling dimension mismatches
        output_name: Optional custom output filename
        extra_output_name: Optional filename for a descriptive copy of submission.tsv
        **ensemble_kwargs: Additional kwargs for ensemble methods
        
    Returns:
        str: Path to final submission file
    """
    setup_logging()
    print("🚀 Starting Ensemble Prediction Workflow (Per-Ontology)")
    print("=" * 60)
    
    start_time = time.time()
    
    # Set up paths
    test_dir, output_dir = setup_workflow_paths(test=True)
    
    # Load test sequences
    print(f"\n📂 Loading test sequences...")
    test_seqs, test_proteins = load_test_sequences(test_dir)
    
    # Process in batches to avoid memory issues
    pred_settings = PREDICTION_SETTINGS
    BATCH_SIZE = pred_settings['ensemble_batch_size']
    ontologies = get_all_ontologies()
    temp_submission_path = output_dir / 'temp_ensemble_submission.tsv'
    prediction_threshold = pred_settings['ensemble_prediction_threshold']
    max_preds_per_ont = pred_settings['ensemble_max_preds_per_ont']
    
    print(f"\n💾 Processing in batches of {BATCH_SIZE:,} proteins to manage memory...")
    print(f"   Total test proteins: {len(test_proteins):,}")
    
    with open(temp_submission_path, 'w') as submission_file:
        for ont_code, ont_name in iterate_ontologies_with_check(
            ontologies, 
            models_per_ontology,
            skip_message=" (no models specified)"
        ):
                
            model_names = models_per_ontology[ont_code]
            print(f"\n🔮 Ensembling {ont_name} predictions with {len(model_names)} models...")
            for i, m in enumerate(model_names, 1):
                print(f"   {i}. {m}")
            
            # Load model configurations for this ontology
            model_configs = []
            for model_name in model_names:
                config = get_model_config(model_name)
                model_configs.append(config)
            
            # Check compatibility
            compatible, issues = check_ensemble_compatibility(model_configs)
            if not compatible:
                if padding_strategy is None:
                    print(f"   ⚠️  Compatibility issues for {ont_name}:")
                    for issue in issues:
                        print(f"      - {issue}")
                    print(f"   💡 Use --padding-strategy or fix feature dimensions")
                    raise ValueError(f"Incompatible models for {ont_name} without padding strategy")
                else:
                    print(f"   ⚙️  Using padding strategy: {padding_strategy}")
            
            # Load models (keep in memory, features/predictions processed in batches)
            loaded_models = []
            for i, (model_name, config) in enumerate(zip(model_names, model_configs)):
                print(f"   Loading model {i+1}/{len(model_names)}: {model_name}")
                try:
                    model, mlb, metadata = load_model(
                        ont_code=ont_code,
                        model_type=config['type'],
                        version=config['version']
                    )
                    loaded_models.append((model, mlb, config, model_name))
                    print(f"      ✓ Model loaded: {config['type']} v{config['version']}")
                except Exception as e:
                    logger.exception(f"Failed to load {config['type']} v{config['version']} for {ont_code}: {e}")
                    print(f"      ❌ Failed to load model: {e}")
            
            if not loaded_models:
                print(f"   ⚠️  No models loaded for {ont_name}, skipping")
                continue
            
            # Use first model's MLB (should be same across models)
            mlb = loaded_models[0][1]
            
            # Process in batches
            n_batches = (len(test_proteins) + BATCH_SIZE - 1) // BATCH_SIZE
            print(f"   Processing {n_batches} batches...")
            import time
            
            for batch_idx in range(n_batches):
                batch_start = time.time()
                start_idx = batch_idx * BATCH_SIZE
                end_idx = min(start_idx + BATCH_SIZE, len(test_proteins))
                batch_proteins = test_proteins[start_idx:end_idx]
                batch_seqs = {pid: test_seqs[pid] for pid in batch_proteins}
                
                print(f"      Batch {batch_idx + 1}/{n_batches}: proteins {start_idx:,}-{end_idx:,} ({len(batch_proteins):,} proteins)")
                
                # Cache features by feature signature to avoid re-extraction
                feature_cache = {}
                
                # Get predictions from each model for this batch
                batch_predictions = []
                
                for model_idx, (model, mlp_model, config, model_name) in enumerate(loaded_models):
                    try:
                        # Parse feature configuration using centralized utility
                        from config.features import parse_model_feature_config
                        feature_type, features = parse_model_feature_config(config)
                        
                        # Create cache key based on feature configuration
                        cache_key = get_feature_cache_key(feature_type, features)
                        
                        # Check cache or extract features
                        if cache_key in feature_cache:
                            print(f"         Model {model_idx + 1}/{len(loaded_models)} ({model_name}): using cached features")
                            X_batch = feature_cache[cache_key]
                        else:
                            print(f"         Model {model_idx + 1}/{len(loaded_models)} ({model_name}): extracting {feature_type} features...")
                            feat_start = time.time()
                            
                            X_batch = extract_features_for_model(
                                batch_seqs,
                                batch_proteins,
                                config
                            )
                            
                            # Cache features for reuse
                            feature_cache[cache_key] = X_batch
                            print(f"         ✓ Features extracted: {X_batch.shape} ({time.time() - feat_start:.1f}s)")
                        
                        # Make predictions for batch using unified prediction interface
                        pred_start = time.time()
                        from utils.model_prediction import predict_with_model
                        y_batch = predict_with_model(
                            model=model,
                            X=X_batch,
                            model_config=config
                        )
                        print(f"         ✓ Predictions: {y_batch.shape} ({time.time() - pred_start:.1f}s)")
                        batch_predictions.append(y_batch)
                        
                    except Exception as e:
                        logger.exception(f"Failed to predict with {model_name} for batch {batch_idx + 1}")
                        print(f"         ❌ Error with {model_name}: {str(e)[:100]}")
                        continue
                
                # Clear feature cache after batch (keep predictions for ensembling)
                del feature_cache
                
                if not batch_predictions:
                    print(f"         ⚠️  No predictions for batch, skipping")
                    continue
                
                # Ensemble batch predictions
                ensemble_start = time.time()
                if len(batch_predictions) > 1:
                    batch_ensembled = ensemble_predictions(
                        batch_predictions,
                        method=ensemble_method,
                        weights=weights,
                        **ensemble_kwargs
                    )
                else:
                    batch_ensembled = batch_predictions[0]
                print(f"         ✓ Ensembled: {batch_ensembled.shape} ({time.time() - ensemble_start:.1f}s)")
                
                # Write batch predictions immediately (free memory)
                write_start = time.time()
                predictions_written = write_predictions_to_file(
                    submission_file,
                    batch_proteins,
                    batch_ensembled,
                    mlb,
                    prediction_threshold,
                    max_preds_per_ont
                )
                print(f"         ✓ Wrote {predictions_written:,} predictions ({time.time() - write_start:.1f}s)")
                
                # Clear batch predictions from memory
                del batch_predictions, batch_ensembled
                
                # Force garbage collection periodically
                if batch_idx % ENSEMBLE_GC_COLLECT_INTERVAL == 0:
                    cleanup_memory()
                
                batch_time = time.time() - batch_start
                elapsed_hours = batch_time * n_batches / 3600
                print(f"      ✓ Batch {batch_idx + 1} complete: {batch_time:.1f}s (est. {elapsed_hours:.1f}h total)")
                submission_file.flush()  # Ensure data is written to disk
            
            print(f"   ✓ {ont_name} ensemble complete")
    
    # Post-process submission
    print(f"\n📝 Post-processing submission...")
    # Use config value if extra_output_name not provided
    final_extra_output_name = get_extra_output_name(extra_output_name)
    final_submission_path = post_process_submission(str(temp_submission_path), output_dir, output_name, extra_output_name=final_extra_output_name)
    
    total_time = time.time() - start_time
    print(f"\n✅ Ensemble Prediction Complete!")
    print(f"⏱️  Total time: {total_time:.1f}s")
    print(f"📄 Submission file: {final_submission_path}")
    
    return str(final_submission_path)


def run_ensemble_prediction(model_names: List[str],
                           ensemble_method: str = 'average',
                           weights: Optional[List[float]] = None,
                           padding_strategy: Optional[str] = None,
                           output_name: Optional[str] = None,
                           extra_output_name: Optional[str] = None,
                           **ensemble_kwargs) -> str:
    """
    Run ensemble prediction workflow with same models for all ontologies.
    Convenience wrapper that converts input format and calls run_ensemble_prediction_per_ontology.
    
    Args:
        model_names: List of model configuration names to ensemble (same for all ontologies)
        ensemble_method: Ensemble method ('average', 'weighted_average', 'max', 'geometric_mean',
                        'rank_average', 'power_average', 'percentile')
        weights: Optional weights for weighted_average
        padding_strategy: Strategy for handling dimension mismatches ('zeros', 'mean', 'noise', None)
        output_name: Optional custom output filename
        extra_output_name: Optional filename for a descriptive copy of submission.tsv
        **ensemble_kwargs: Additional kwargs for ensemble methods:
            - power (float): Power for power_average method (default: 1.0)
            - percentile (float): Percentile for percentile method (default: 75.0)
        
    Returns:
        str: Path to final submission file
    """
    # Convert to per-ontology format (same models for all ontologies)
    from config import get_all_ontologies
    ontologies = get_all_ontologies()
    models_per_ontology = {ont_code: model_names for ont_code in ontologies.keys()}
    
    # Call main function
    return run_ensemble_prediction_per_ontology(
        models_per_ontology=models_per_ontology,
        ensemble_method=ensemble_method,
        weights=weights,
        padding_strategy=padding_strategy,
        output_name=output_name,
        extra_output_name=extra_output_name,
        **ensemble_kwargs
    )

