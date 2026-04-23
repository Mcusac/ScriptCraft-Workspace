# regression_ensemble_pipeline.py
# Pipeline to generate submission using ensemble of regression models
#
# Handles loading multiple regression models, extracting features once,
# running predictions, combining them, and generating submission file.

import logging
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Optional, Any

from config.config import Config
from modeling.ensembling.regression_ensemble import create_regression_ensemble_from_paths
from modeling.testing import expand_predictions_to_submission_format, validate_predictions_shape
from modeling.utils import save_submission_file
from utils.config import validate_pipeline_config
from utils.system import get_device
from utils.notebook.model_selection import (
    resolve_model_paths_from_config,
    validate_model_paths
)

logger = logging.getLogger(__name__)


def regression_ensemble_pipeline(
    config: Config,
    ensemble_config: Dict[str, Any],
    base_model_dir: Optional[str] = None
) -> pd.DataFrame:
    """
    Generate submission using ensemble of regression models.
    
    Pipeline flow:
    1. Resolve model paths from configuration
    2. Validate all models exist and are consistent
    3. Load all regression models
    4. Extract features once (shared across all models)
    5. Run predictions from each model
    6. Combine predictions using selected method
    7. Generate submission file
    
    Args:
        config: Configuration object with model, data, paths, and device settings
        ensemble_config: Configuration dict with:
            - 'model_types': List of model types to include
            - 'model_indices': Dict mapping model_type -> list of 1-indexed ranks
            - 'method': Ensembling method name
            - 'score_type': Score type for weighting
        base_model_dir: Base directory for models (default: '/kaggle/input/csiro-models/regression/')
        
    Returns:
        Submission DataFrame with columns: sample_id, target
        
    Raises:
        ValueError: If configuration is invalid
        FileNotFoundError: If models not found
        RuntimeError: If inference or submission generation fails
    """
    # Validate config
    validate_pipeline_config(config, required_sections=['data', 'paths', 'model'])
    
    logger.info("="*60)
    logger.info("Regression Ensemble Pipeline")
    logger.info("="*60)
    logger.info(f"  Model types: {ensemble_config.get('model_types', [])}")
    logger.info(f"  Method: {ensemble_config.get('method', 'weighted_average')}")
    logger.info(f"  Score type: {ensemble_config.get('score_type', 'cv')}")
    
    # Resolve model paths from configuration
    logger.info("\nResolving model paths from configuration...")
    logger.info("Using explicit configuration (uploaded models by version)...")
    model_paths, cv_scores, model_types = resolve_model_paths_from_config(
        ensemble_config,
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
            # Try alternative location
            if Path(model_path).suffix == '.pkl':
                metadata_file = Path(model_path).parent / 'model_metadata.json'
        
        if metadata_file.exists():
            import json
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            model_configs.append(metadata)
            
            # Extract feature extraction model name from first model
            if feature_extraction_model_name is None:
                feature_filename = metadata.get('feature_filename')
                if feature_filename:
                    # Parse feature filename to get model name
                    # For now, use a simple approach - this should be improved
                    # Format: variant_XXXX_features.npz
                    # We'll need to look up the model_id from the feature filename
                    # For simplicity, assume dinov2_base for now
                    # TODO: Parse feature_filename properly
                    feature_extraction_model_name = 'dinov2_base'
        else:
            logger.warning(f"Metadata not found for {model_path}, using empty config")
            model_configs.append({})
    
    if not feature_extraction_model_name:
        logger.warning("Could not determine feature extraction model name, using default")
        feature_extraction_model_name = 'dinov2_base'
    
    # Get device
    device = get_device(config.device.device)
    logger.info(f"  Device: {device}")
    
    # Create ensemble
    logger.info(f"\nCreating regression ensemble with {len(model_paths)} models...")
    ensemble = create_regression_ensemble_from_paths(
        model_paths=model_paths,
        model_configs=model_configs,
        method=ensemble_config.get('method', 'weighted_average'),
        feature_extraction_model_name=feature_extraction_model_name,
        cv_scores=cv_scores if ensemble_config.get('score_type') == 'cv' else None
    )
    
    # Extract features once (shared across all models)
    logger.info("\nExtracting features from test images...")
    test_csv_path = Path(config.data.data_root) / config.data.test_csv
    data_root = config.data.data_root
    
    # Use first model to extract features (all use same feature extraction)
    # We'll create a temporary submission to get features, then reuse them
    # Actually, let's extract features directly
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
    
    # Extract features
    feature_extractor = FeatureExtractor(feature_model, device)
    test_loader = create_test_dataloader(
        test_csv_path=str(test_csv_path),
        data_root=data_root,
        config=config
    )
    dataset_type = getattr(config.data, 'dataset_type', 'split')
    features = feature_extractor.extract_features(test_loader, dataset_type, config=config)
    logger.info(f"Extracted features shape: {features.shape}")
    
    # Run ensemble predictions
    logger.info("\nRunning ensemble predictions...")
    predictions = ensemble.predict(features)
    logger.info(f"Ensemble predictions shape: {predictions.shape}")
    
    # Validate predictions shape
    from dataset_manipulation import load_and_validate_test_data
    unique_images = load_and_validate_test_data(str(test_csv_path))
    validate_predictions_shape(predictions, len(unique_images), expected_cols=3)
    
    # Expand to submission format
    logger.info("\nExpanding predictions to submission format...")
    submission_df = expand_predictions_to_submission_format(
        predictions=predictions,
        test_csv_path=str(test_csv_path)
    )
    
    # Save submission
    output_path = save_submission_file(submission_df, config)
    
    logger.info("="*60)
    logger.info("Regression Ensemble Pipeline Complete")
    logger.info("="*60)
    logger.info(f"  Models: {len(model_paths)}")
    logger.info(f"  Method: {ensemble_config.get('method')}")
    logger.info(f"  Output: {output_path}")
    
    return submission_df
