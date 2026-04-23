"""
Prediction workflow: Load Models -> Predict -> Submit.
Loads saved models and generates submission file.
"""

import time

from typing import Dict, Tuple, Optional
from config import PREDICTION_SETTINGS, get_model_config
from config.features import parse_model_feature_config
from prediction.predict_and_submit import load_test_sequences, make_predictions, post_process_submission
from pipelines.workflows.workflow_paths import setup_workflow_paths
from pipelines.workflows.workflow_features import (
    make_hashable_for_comparison, 
    compare_feature_configs_across_ontologies,
    infer_features_from_input_dim,
    calculate_expected_dimension
)
from utils.model_io import load_model
from utils.cli_utils import get_model_config_safe


def run_predict_from_saved(model_specs: Dict[str, Tuple[str, str]], 
                          output_name: Optional[str] = None, 
                          models_source: str = 'both',
                          apply_goa_filter: bool = True) -> str:
    """
    Run prediction using saved models: Load Models -> Predict -> Submit.
    
    Args:
        model_specs: dict mapping ont_code -> (model_type, version) or model config name
        output_name: Optional custom output filename
        models_source: Where to load models from - 'input', 'working', or 'both' (default: 'both')
        apply_goa_filter: If True, apply GOA negative propagation filtering (default: True)
        
    Returns:
        str: Path to final submission file
    """
    print("🔮 Starting Prediction from Saved Models")
    print("=" * 60)
    
    start_time = time.time()
    
    # Set up paths (environment-aware)
    test_dir, output_dir = setup_workflow_paths(test=True)
    
    # Load saved models (MLP is saved with each model, so no need for training data)
    print("\n📂 [STEP 1] Loading Saved Models...")
    print(f"   Models source: {models_source}")
    load_start = time.time()
    
    models = {}
    mlb_dict = {}
    model_configs_per_ont = {}
    model_metadata_per_ont = {}  # Store metadata for each ontology
    optimal_thresholds = {}  # Store optimal thresholds per ontology
    
    for ont_code, model_spec in model_specs.items():
        # model_spec is always a tuple (model_type, version) from parse_model_spec
        model_type, version = model_spec
        
        # Get model config to determine feature settings
        config = get_model_config_safe(model_type, version, ont_code=ont_code)
        
        print(f"   Loading {model_type} v{version} for {ont_code}...")
        model, mlb, metadata = load_model(ont_code, model_type, version, models_source=models_source)
        models[ont_code] = model
        mlb_dict[ont_code] = mlb
        model_configs_per_ont[ont_code] = config
        model_metadata_per_ont[ont_code] = metadata
        
        # Check for optimal threshold in metadata
        if metadata and 'optimal_threshold' in metadata:
            optimal_thresholds[ont_code] = metadata['optimal_threshold']
            print(f"      ✓ Using optimal threshold: {metadata['optimal_threshold']:.3f}")
    
    print(f"   ⏱️  Model loading time: {time.time() - load_start:.1f}s")
    
    # Determine feature configuration from models using centralized utility
    # Check for dimension mismatches and override if needed
    feature_configs = {}
    for ont_code, config in model_configs_per_ont.items():
        feature_type, features = parse_model_feature_config(config)
        
        # Check if model metadata indicates different input dimension
        metadata = model_metadata_per_ont.get(ont_code)
        if metadata:
            # Get actual input dimension from metadata
            actual_input_dim = metadata.get('n_features') or metadata.get('input_dim')
            
            if actual_input_dim is not None:
                # Calculate expected dimension from config
                expected_dim = calculate_expected_dimension(feature_type, features)
                
                if expected_dim is not None and abs(actual_input_dim - expected_dim) > 10:
                    # Dimension mismatch detected - infer correct features
                    print(f"\n   ⚠️  Dimension mismatch detected for {ont_code}:")
                    print(f"      Config expects: {expected_dim} dims ({feature_type}: {features})")
                    print(f"      Model expects: {actual_input_dim} dims (from metadata)")
                    print(f"      Inferring correct feature configuration...")
                    
                    inferred_config = infer_features_from_input_dim(actual_input_dim)
                    if inferred_config:
                        inferred_feature_type, inferred_features = inferred_config
                        feature_type = inferred_feature_type
                        features = inferred_features
                        print(f"      ✓ Overriding with: {feature_type}: {inferred_features}")
                    else:
                        print(f"      ⚠️  Could not infer features from dimension {actual_input_dim}")
                        print(f"      Using config-based features (may cause errors)")
        
        feature_configs[ont_code] = (feature_type, features)
    
    # Check if all ontologies use the same feature config
    all_same, feature_type, features = compare_feature_configs_across_ontologies(feature_configs)
    
    if all_same:
        print(f"\n   Feature configuration: {feature_type}")
        if features:
            print(f"   Features: {features}")
    else:
        # Different per ontology - pass per-ontology configs to make_predictions
        print(f"\n   Mixed feature configurations per ontology:")
        for ont_code, (ft, fe) in feature_configs.items():
            print(f"   {ont_code}: {ft} {fe if fe else ''}")
        print(f"   ✓ Per-ontology feature extraction will be used")
    
    # Make Predictions
    print("\n🔮 [STEP 2] Making Predictions...")
    pred_start = time.time()
    
    test_seqs, test_proteins = load_test_sequences(test_dir)
    pred_settings = PREDICTION_SETTINGS
    
    # Use optimal thresholds if available, otherwise use default
    default_threshold = pred_settings.get('prediction_threshold')
    if optimal_thresholds:
        # Use average of optimal thresholds if all are the same, otherwise use default
        threshold_values = list(optimal_thresholds.values())
        if len(set(threshold_values)) == 1:
            threshold_to_use = threshold_values[0]
            print(f"   Using optimal threshold from models: {threshold_to_use:.3f}")
        else:
            threshold_to_use = default_threshold
            print(f"   ⚠️  Mixed optimal thresholds found, using default: {threshold_to_use:.3f}")
    else:
        threshold_to_use = default_threshold
    
    # Filter settings to only include parameters that make_predictions() accepts
    # make_predictions() accepts: batch_size, prediction_threshold, max_preds_per_ont, write_batch_size
    filtered_settings = {
        'batch_size': pred_settings.get('batch_size'),
        'prediction_threshold': threshold_to_use,
        'max_preds_per_ont': pred_settings.get('max_preds_per_ont'),
        'write_batch_size': pred_settings.get('write_batch_size'),
        'propagate_predictions': pred_settings.get('propagate_predictions', False)
    }
    
    # Pass per-ontology feature configs if mixed, otherwise pass single config
    if all_same:
        temp_submission_path = make_predictions(
            models=models,
            mlb_dict=mlb_dict,
            test_seqs=test_seqs,
            test_proteins=test_proteins,
            output_dir=output_dir,
            feature_type=feature_type,
            features=features,
            **filtered_settings
        )
    else:
        # Pass per-ontology feature configs
        temp_submission_path = make_predictions(
            models=models,
            mlb_dict=mlb_dict,
            test_seqs=test_seqs,
            test_proteins=test_proteins,
            output_dir=output_dir,
            per_ontology_feature_configs=feature_configs,
            **filtered_settings
        )
    
    final_submission_path = post_process_submission(
        temp_submission_path, 
        output_dir,
        apply_goa_filter=apply_goa_filter
    )
    
    print(f"   ⏱️  Prediction time: {time.time() - pred_start:.1f}s")
    
    total_time = time.time() - start_time
    print(f"\n✅ Prediction Pipeline Complete!")
    print(f"⏱️  Total time: {total_time:.1f}s")
    print(f"📄 Submission file: {final_submission_path}")
    
    return str(final_submission_path)
