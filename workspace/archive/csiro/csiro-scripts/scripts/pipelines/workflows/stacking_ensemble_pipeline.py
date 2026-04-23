# stacking_ensemble_pipeline.py
# Pipeline to generate submission using stacking with ensemble base models
#
# Creates ensembles per model type (e.g., ensemble of LGBM versions, ensemble of XGBoost versions),
# then stacks the ensemble outputs using a Ridge meta-model.

import logging
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Optional, Any

from config.config import Config
from modeling.testing import expand_predictions_to_submission_format, validate_predictions_shape
from modeling.utils import save_submission_file
from utils.config import validate_pipeline_config
from utils.system import get_device
from utils.notebook.model_selection import (
    resolve_model_paths_from_config,
    validate_model_paths
)

logger = logging.getLogger(__name__)


def stacking_ensemble_pipeline(
    config: Config,
    stacking_ensemble_config: Dict[str, Any],
    base_model_dir: Optional[str] = None
) -> pd.DataFrame:
    """
    Generate submission using stacking with ensemble base models.
    
    Pipeline flow:
    1. For each model type, create an ensemble of specified versions
    2. Load training features and targets
    3. Generate OOF predictions from each ensemble (using CV)
    4. Train meta-model (Ridge) per target on ensemble OOF predictions
    5. Generate test predictions from ensemble predictions
    6. Generate submission file
    
    Args:
        config: Configuration object with model, data, paths, and device settings
        stacking_ensemble_config: Configuration dict with:
            - 'model_types': List of model types to include
            - 'ensemble_configs': Dict mapping model_type -> ensemble config with:
                - 'model_versions': List of versions to ensemble
                - 'method': Ensembling method
                - 'score_type': Score type for weighting
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
    logger.info("Stacking Pipeline (Ensemble Base Models)")
    logger.info("="*60)
    logger.info(f"  Model types: {stacking_ensemble_config.get('model_types', [])}")
    logger.info(f"  Meta-model alpha: {stacking_ensemble_config.get('meta_model_alpha', 10.0)}")
    logger.info(f"  Number of folds: {stacking_ensemble_config.get('n_folds', 5)}")
    
    model_types = stacking_ensemble_config.get('model_types', [])
    ensemble_configs = stacking_ensemble_config.get('ensemble_configs', {})
    
    if not model_types:
        raise ValueError("model_types cannot be empty in stacking_ensemble_config")
    
    if not ensemble_configs:
        raise ValueError("ensemble_configs cannot be empty in stacking_ensemble_config")
    
    # Get device
    device = get_device(config.device.device)
    logger.info(f"  Device: {device}")
    
    # Load training features and targets
    logger.info("\nLoading training features and targets...")
    from modeling.feature_extraction.feature_cache import find_feature_cache, load_features
    
    # Find feature file from first ensemble config
    feature_filename = None
    feature_extraction_model_name = None
    
    # We'll determine feature filename from the first model we load
    first_model_type = model_types[0]
    if first_model_type in ensemble_configs:
        first_versions = ensemble_configs[first_model_type].get('model_versions', [])
        if first_versions:
            # Load first model to get feature filename
            first_version = first_versions[0]
            first_model_path = Path(base_model_dir or '/kaggle/input/csiro-models/') / 'scikitlearn' / first_model_type / str(first_version)
            first_metadata_file = first_model_path / 'model_metadata.json'
            
            if first_metadata_file.exists():
                import json
                with open(first_metadata_file, 'r') as f:
                    metadata = json.load(f)
                feature_filename = metadata.get('feature_filename')
                if feature_filename:
                    feature_extraction_model_name = 'dinov2_base'  # Default, could be parsed from feature_filename
    
    if not feature_filename:
        raise ValueError("Cannot determine feature filename from model metadata")
    
    # Load features
    cache_path = find_feature_cache(feature_filename)
    if not cache_path:
        raise FileNotFoundError(f"Feature file not found: {feature_filename}")
    
    logger.info(f"Loading features from {cache_path}")
    all_features, all_targets, fold_assignments, metadata = load_features(cache_path)
    
    logger.info(f"Loaded features: {all_features.shape}, targets: {all_targets.shape}")
    
    # Load test features
    logger.info("\nExtracting test features...")
    from modeling.feature_extraction import FeatureExtractor
    from modeling.models import create_model
    from config.model_constants import get_pretrained_weights_path
    from modeling.testing.dataloaders import create_test_dataloader
    
    if not feature_extraction_model_name:
        feature_extraction_model_name = 'dinov2_base'
    
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
    
    # Create ensembles per type and generate OOF predictions
    logger.info("\nCreating ensembles per model type and generating OOF predictions...")
    ensemble_oof_preds = {}
    ensemble_test_preds = {}
    ensemble_names = []
    
    for model_type in model_types:
        if model_type not in ensemble_configs:
            logger.warning(f"No ensemble config for {model_type}, skipping")
            continue
        
        ensemble_config = ensemble_configs[model_type]
        model_versions = ensemble_config.get('model_versions', [])
        
        if not model_versions:
            logger.warning(f"Empty model_versions for {model_type}, skipping")
            continue
        
        logger.info(f"\n  Creating {model_type} ensemble (versions {model_versions})...")
        
        # Resolve model paths for this type
        type_ensemble_config = {
            'model_types': [model_type],
            'model_versions': {model_type: model_versions},
            'method': ensemble_config.get('method', 'weighted_average'),
            'score_type': ensemble_config.get('score_type', 'cv')
        }
        
        model_paths, cv_scores, _ = resolve_model_paths_from_config(
            type_ensemble_config,
            base_model_dir=base_model_dir,
            auto_detect=False
        )
        
        # Validate model paths
        validate_model_paths(model_paths, require_same_feature_model=True)
        
        # Load model configs
        model_configs = []
        for model_path in model_paths:
            metadata_file = Path(model_path) / 'model_metadata.json'
            if metadata_file.exists():
                import json
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                model_configs.append(metadata)
            else:
                model_configs.append({})
        
        # Generate OOF predictions from ensemble using CV
        # Strategy: Generate OOF from each model, then combine using ensemble method
        logger.info(f"  Generating OOF predictions for {model_type} ensemble...")
        from sklearn.model_selection import KFold
        import pickle
        from modeling.models.regression_head import RegressionModel
        
        n_folds = stacking_ensemble_config.get('n_folds', 5)
        kf = KFold(n_splits=n_folds, shuffle=True, random_state=42)
        
        n_train = all_features.shape[0]
        n_targets = all_targets.shape[1]
        
        # Store OOF predictions from each model in ensemble
        model_oof_preds = []
        model_test_preds = []
        
        # For each model in the ensemble, generate OOF predictions
        # First, load all models
        loaded_models = []
        for model_path in model_paths:
            model_file = Path(model_path) / 'regression_model.pkl'
            if not model_file.exists():
                raise FileNotFoundError(f"Model file not found: {model_file}")
            
            with open(model_file, 'rb') as f:
                model = pickle.load(f)
            loaded_models.append(model)
        
        for model_idx, (model_path, model) in enumerate(zip(model_paths, loaded_models)):
            logger.info(f"    Model {model_idx + 1}/{len(model_paths)}: {Path(model_path).name}")
            
            model_oof = np.zeros((n_train, n_targets))
            model_test = np.zeros((test_features.shape[0], n_targets))
            
            for fold, (train_idx, val_idx) in enumerate(kf.split(all_features, all_targets)):
                X_tr, X_val = all_features[train_idx], all_features[val_idx]
                y_tr = all_targets[train_idx]
                
                # Create new model instance for this fold (instead of cloning)
                model_fold = RegressionModel(
                    model_type=model.model_type,
                    model_params=model.model_params,
                    random_state=model.random_state
                )
                model_fold.fit(X_tr, y_tr)
                
                # Predict on validation fold (OOF)
                val_pred = model_fold.predict(X_val)
                if val_pred.ndim == 1:
                    val_pred = val_pred.reshape(-1, 1)
                val_pred = np.clip(val_pred, 0, None)
                model_oof[val_idx] = val_pred
                
                # Predict on test
                test_pred = model_fold.predict(test_features)
                if test_pred.ndim == 1:
                    test_pred = test_pred.reshape(-1, 1)
                test_pred = np.clip(test_pred, 0, None)
                model_test += test_pred / n_folds
            
            model_oof_preds.append(model_oof)
            model_test_preds.append(model_test)
        
        # Combine OOF predictions using ensemble method
        from modeling.ensembling.methods import create_ensembling_method
        ensembling_method = create_ensembling_method(ensemble_config.get('method', 'weighted_average'))
        
        # Get weights if needed
        weights = None
        if ensemble_config.get('score_type') == 'cv' and cv_scores:
            weights = cv_scores
        
        # Combine OOF predictions
        ensemble_oof = ensembling_method.combine(model_oof_preds, weights)
        ensemble_oof = np.clip(ensemble_oof, 0, None)
        
        # Combine test predictions
        ensemble_test = ensembling_method.combine(model_test_preds, weights)
        ensemble_test = np.clip(ensemble_test, 0, None)
        
        ensemble_oof_preds[model_type] = ensemble_oof
        ensemble_test_preds[model_type] = ensemble_test
        ensemble_names.append(model_type)
        
        logger.info(f"  {model_type} ensemble OOF predictions shape: {ensemble_oof.shape}")
    
    if not ensemble_oof_preds:
        raise ValueError("No ensembles created successfully")
    
    # Train meta-model on ensemble OOF predictions
    logger.info("\nTraining meta-models (Ridge) per target on ensemble OOF predictions...")
    from sklearn.linear_model import Ridge
    
    n_targets = all_targets.shape[1]
    meta_models = {}
    meta_model_alpha = stacking_ensemble_config.get('meta_model_alpha', 10.0)
    
    for target_idx in range(n_targets):
        # Build meta-features: stack OOF predictions from all ensembles for this target
        X_meta = np.column_stack([
            ensemble_oof_preds[ensemble_name][:, target_idx]
            for ensemble_name in ensemble_names
        ])
        
        y_meta = all_targets[:, target_idx]
        
        # Train Ridge meta-model
        meta_model = Ridge(alpha=meta_model_alpha, random_state=42)
        meta_model.fit(X_meta, y_meta)
        
        meta_models[target_idx] = meta_model
        
        # Log weights (coefficients)
        coef_str = ', '.join([
            f"{name}: {coef:.3f}"
            for name, coef in zip(ensemble_names, meta_model.coef_)
        ])
        logger.info(f"  Target {target_idx} weights -> {coef_str}")
    
    logger.info(f"Trained {len(meta_models)} meta-models")
    
    # Calculate OOF score for validation
    from modeling.evaluation.metrics import calc_metric
    oof_combined = np.zeros_like(all_targets)
    for target_idx, meta_model in meta_models.items():
        X_meta = np.column_stack([
            ensemble_oof_preds[ensemble_name][:, target_idx]
            for ensemble_name in ensemble_names
        ])
        oof_combined[:, target_idx] = meta_model.predict(X_meta)
    
    oof_score, _ = calc_metric(oof_combined, all_targets)
    logger.info(f"Stacking OOF Score: {oof_score:.4f}")
    
    # Generate final test predictions
    logger.info("\nGenerating final test predictions...")
    final_predictions = np.zeros((test_features.shape[0], n_targets))
    
    for target_idx, meta_model in meta_models.items():
        X_meta = np.column_stack([
            ensemble_test_preds[ensemble_name][:, target_idx]
            for ensemble_name in ensemble_names
        ])
        final_predictions[:, target_idx] = meta_model.predict(X_meta)
    
    # Clip negative values
    final_predictions = np.clip(final_predictions, 0, None)
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
    logger.info("Stacking Ensemble Pipeline Complete")
    logger.info("="*60)
    logger.info(f"  Ensembles: {len(ensemble_names)} ({', '.join(ensemble_names)})")
    logger.info(f"  OOF score: {oof_score:.4f}")
    logger.info(f"  Output: {output_path}")
    
    return submission_df
