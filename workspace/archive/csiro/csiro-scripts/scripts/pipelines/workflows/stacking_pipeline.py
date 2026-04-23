# stacking_pipeline.py
# Pipeline to generate submission using stacking ensemble
#
# Handles loading base models, generating OOF predictions, training meta-models,
# and generating final submission.

import logging
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Optional, Any

from config.config import Config
from modeling.ensembling.stacking import StackingEnsemble
from modeling.testing import expand_predictions_to_submission_format, validate_predictions_shape
from modeling.utils import save_submission_file
from utils.config import validate_pipeline_config
from utils.system import get_device
from utils.notebook.model_selection import (
    resolve_model_paths_from_config,
    validate_model_paths
)

logger = logging.getLogger(__name__)


def stacking_pipeline(
    config: Config,
    stacking_config: Dict[str, Any],
    base_model_dir: Optional[str] = None
) -> pd.DataFrame:
    """
    Generate submission using stacking ensemble.
    
    Pipeline flow:
    1. Resolve model paths from configuration
    2. Validate all models exist and are consistent
    3. Load all base models
    4. Load training features and targets
    5. Generate OOF predictions using cross-validation
    6. Train meta-models (Ridge) per target
    7. Generate test predictions
    8. Generate submission file
    
    Args:
        config: Configuration object with model, data, paths, and device settings
        stacking_config: Configuration dict with:
            - 'model_types': List of model types to include
            - 'model_indices': Dict mapping model_type -> list of 1-indexed ranks
            - 'meta_model_alpha': Ridge regularization parameter
            - 'n_folds': Number of folds for OOF generation
        base_model_dir: Base directory for models
        
    Returns:
        Submission DataFrame with columns: sample_id, target
        
    Raises:
        ValueError: If configuration is invalid
        FileNotFoundError: If models or data not found
        RuntimeError: If pipeline fails
    """
    # Validate config
    validate_pipeline_config(config, required_sections=['data', 'paths', 'model'])
    
    logger.info("="*60)
    logger.info("Stacking Pipeline (Single Models)")
    logger.info("="*60)
    logger.info(f"  Model types: {stacking_config.get('model_types', [])}")
    logger.info(f"  Meta-model alpha: {stacking_config.get('meta_model_alpha', 10.0)}")
    logger.info(f"  Number of folds: {stacking_config.get('n_folds', 5)}")
    
    # Resolve model paths from configuration
    logger.info("\nResolving model paths from configuration...")
    logger.info("Using explicit configuration (uploaded models by version)...")
    model_paths, cv_scores, model_types = resolve_model_paths_from_config(
        stacking_config,
        base_model_dir=base_model_dir,
        auto_detect=False  # Use explicit model versions
    )
    
    # Validate model paths
    logger.info("\nValidating model paths...")
    validate_model_paths(model_paths, require_same_feature_model=True)
    
    # Load model configs (metadata)
    logger.info("\nLoading model metadata...")
    model_configs = []
    feature_extraction_model_name = None
    
    for model_path in model_paths:
        metadata_file = Path(model_path) / 'model_metadata.json'
        if not metadata_file.exists():
            if Path(model_path).suffix == '.pkl':
                metadata_file = Path(model_path).parent / 'model_metadata.json'
        
        if metadata_file.exists():
            import json
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            model_configs.append(metadata)
            
            if feature_extraction_model_name is None:
                feature_filename = metadata.get('feature_filename')
                if feature_filename:
                    # Parse feature filename to get model name
                    # For now, use default
                    feature_extraction_model_name = 'dinov2_base'
        else:
            model_configs.append({})
    
    if not feature_extraction_model_name:
        feature_extraction_model_name = 'dinov2_base'
    
    # Get device
    device = get_device(config.device.device)
    logger.info(f"  Device: {device}")
    
    # Load training features and targets
    logger.info("\nLoading training features and targets...")
    
    # Find feature file from first model's metadata
    feature_filename = None
    if model_configs and model_configs[0].get('feature_filename'):
        feature_filename = model_configs[0]['feature_filename']
    else:
        raise ValueError("Cannot determine feature filename from model metadata")
    
    # Load features using feature cache utility
    from modeling.feature_extraction.feature_cache import find_feature_cache, load_features
    
    cache_path = find_feature_cache(feature_filename)
    if not cache_path:
        raise FileNotFoundError(f"Feature file not found: {feature_filename}")
    
    logger.info(f"Loading features from {cache_path}")
    all_features, all_targets_from_cache, fold_assignments, metadata = load_features(cache_path)
    
    # Use targets from feature cache (already loaded)
    all_targets = all_targets_from_cache
    
    logger.info(f"Loaded features: {all_features.shape}, targets: {all_targets.shape}")
    
    # Load test features
    logger.info("\nExtracting test features...")
    from modeling.feature_extraction import FeatureExtractor
    from modeling.models import create_model
    from config.model_constants import get_pretrained_weights_path
    from modeling.testing.dataloaders import create_test_dataloader
    
    # Create feature extraction model
    pretrained_weights_path = get_pretrained_weights_path(feature_extraction_model_name)
    original_name = config.model.name
    original_pretrained = config.model.pretrained
    try:
        config.model.name = pretrained_weights_path
        config.model.pretrained = True
        feature_model = create_model(config)
        feature_model.to(device)
        feature_model.eval()
    finally:
        config.model.name = original_name
        config.model.pretrained = original_pretrained
    
    # Extract test features
    test_csv_path = Path(config.data.data_root) / config.data.test_csv
    feature_extractor = FeatureExtractor(feature_model, device)
    test_loader = create_test_dataloader(
        test_csv_path=str(test_csv_path),
        data_root=config.data.data_root,
        config=config
    )
    dataset_type = getattr(config.data, 'dataset_type', 'split')
    test_features = feature_extractor.extract_features(test_loader, dataset_type, config=config)
    logger.info(f"Extracted test features shape: {test_features.shape}")
    
    # Create stacking ensemble
    logger.info(f"\nCreating stacking ensemble with {len(model_paths)} base models...")
    stacking = StackingEnsemble(
        model_paths=model_paths,
        model_configs=model_configs,
        feature_extraction_model_name=feature_extraction_model_name,
        n_folds=stacking_config.get('n_folds', 5),
        meta_model_alpha=stacking_config.get('meta_model_alpha', 10.0)
    )
    
    # Generate OOF predictions
    logger.info("\nGenerating out-of-fold predictions...")
    oof_preds, test_preds = stacking.generate_oof_predictions(
        X_train=all_features,
        y_train=all_targets,
        X_test=test_features
    )
    
    # Train meta-models
    logger.info("\nTraining meta-models...")
    stacking.fit_meta_models(oof_preds, all_targets)
    
    # Calculate OOF score for validation
    from modeling.evaluation.metrics import calc_metric
    oof_combined = stacking.predict(oof_preds)
    oof_score, _ = calc_metric(oof_combined, all_targets)
    logger.info(f"Stacking OOF Score: {oof_score:.4f}")
    
    # Generate final test predictions
    logger.info("\nGenerating final test predictions...")
    final_predictions = stacking.predict(test_preds)
    logger.info(f"Final predictions shape: {final_predictions.shape}")
    
    # Validate predictions shape
    from dataset_manipulation import load_and_validate_test_data
    unique_images = load_and_validate_test_data(str(test_csv_path))
    validate_predictions_shape(final_predictions, len(unique_images), expected_cols=3)
    
    # Expand to submission format
    logger.info("\nExpanding predictions to submission format...")
    submission_df = expand_predictions_to_submission_format(
        predictions=final_predictions,
        test_csv_path=str(test_csv_path)
    )
    
    # Save submission
    output_path = save_submission_file(submission_df, config)
    
    logger.info("="*60)
    logger.info("Stacking Pipeline Complete")
    logger.info("="*60)
    logger.info(f"  Base models: {len(model_paths)}")
    logger.info(f"  OOF score: {oof_score:.4f}")
    logger.info(f"  Output: {output_path}")
    
    return submission_df
