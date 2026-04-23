# hybrid_stacking_pipeline.py
# Pipeline to generate submission using hybrid stacking
#
# Combines multiple ensemble types:
# - Regression ensembles (two-stage models: LGBM, XGBoost, Ridge)
# - End-to-end ensembles (PyTorch models: EfficientNet, DINOv2, etc.)
#
# Generates OOF predictions for each ensemble type, then stacks all ensemble predictions
# using a Ridge meta-model.

import logging
import numpy as np
import pandas as pd
import torch
from pathlib import Path
from typing import Dict, Optional, Any, Tuple

from config.config import Config
from modeling.ensembling.ensemble import create_ensemble_from_paths
from modeling.ensembling.end_to_end_oof import generate_end_to_end_ensemble_oof
from modeling.testing import expand_predictions_to_submission_format, validate_predictions_shape
from modeling.utils import save_submission_file
from utils.config import validate_pipeline_config
from utils.system import get_device
from utils.notebook.model_selection import (
    resolve_model_paths_from_config,
    validate_model_paths
)

logger = logging.getLogger(__name__)


def hybrid_stacking_pipeline(
    config: Config,
    hybrid_stacking_config: Dict[str, Any],
    base_model_dir: Optional[str] = None
) -> pd.DataFrame:
    """
    Generate submission using hybrid stacking of multiple ensemble types.
    
    Pipeline flow:
    1. Generate OOF predictions for regression ensembles (two-stage models)
    2. Generate OOF predictions for end-to-end ensembles (PyTorch models)
    3. Combine all ensemble OOF predictions
    4. Train Ridge meta-model per target on combined OOF predictions
    5. Generate final test predictions using meta-models
    6. Generate submission file
    
    Args:
        config: Configuration object with model, data, paths, and device settings
        hybrid_stacking_config: Configuration dict with:
            - 'regression_ensembles': Dict with 'model_types' and 'ensemble_configs'
            - 'end_to_end_ensembles': Dict with 'model_name', 'base_model_dir', and 'ensemble_configs'
            - 'meta_model_alpha': Ridge regularization parameter
            - 'n_folds': Number of folds for OOF generation
        base_model_dir: Base directory for regression models (default: '/kaggle/input/csiro-models/')
        
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
    logger.info("Hybrid Stacking Pipeline")
    logger.info("="*60)
    logger.info(f"  Meta-model alpha: {hybrid_stacking_config.get('meta_model_alpha', 10.0)}")
    logger.info(f"  Number of folds: {hybrid_stacking_config.get('n_folds', 5)}")
    
    # Get device
    device = get_device(config.device.device)
    logger.info(f"  Device: {device}")
    
    # Initialize storage for all ensemble OOF and test predictions
    all_ensemble_oof_preds = {}
    all_ensemble_test_preds = {}
    ensemble_names = []
    
    # Process regression ensembles
    regression_ensembles = hybrid_stacking_config.get('regression_ensembles', {})
    if regression_ensembles:
        logger.info("\n" + "="*60)
        logger.info("Processing Regression Ensembles")
        logger.info("="*60)
        
        regression_oof, regression_test = _generate_regression_ensemble_oof(
            config=config,
            regression_ensembles=regression_ensembles,
            hybrid_stacking_config=hybrid_stacking_config,
            base_model_dir=base_model_dir
        )
        
        # Store regression ensemble predictions
        for ensemble_name, oof_preds in regression_oof.items():
            all_ensemble_oof_preds[ensemble_name] = oof_preds
            all_ensemble_test_preds[ensemble_name] = regression_test[ensemble_name]
            ensemble_names.append(ensemble_name)
    
    # Process end-to-end ensembles
    end_to_end_ensembles = hybrid_stacking_config.get('end_to_end_ensembles', {})
    if end_to_end_ensembles:
        logger.info("\n" + "="*60)
        logger.info("Processing End-to-End Ensembles")
        logger.info("="*60)
        
        end_to_end_oof, end_to_end_test = _generate_end_to_end_ensemble_oof(
            config=config,
            end_to_end_ensembles=end_to_end_ensembles,
            hybrid_stacking_config=hybrid_stacking_config,
            device=device
        )
        
        # Store end-to-end ensemble predictions
        for ensemble_name, oof_preds in end_to_end_oof.items():
            all_ensemble_oof_preds[ensemble_name] = oof_preds
            all_ensemble_test_preds[ensemble_name] = end_to_end_test[ensemble_name]
            ensemble_names.append(ensemble_name)
    
    if not all_ensemble_oof_preds:
        raise ValueError("No ensembles created successfully. Check configuration.")
    
    logger.info(f"\n{'='*60}")
    logger.info(f"Total ensembles: {len(ensemble_names)}")
    logger.info(f"Ensemble names: {', '.join(ensemble_names)}")
    logger.info(f"{'='*60}")
    
    # Load training targets for meta-model training
    logger.info("\nLoading training targets...")
    from modeling.feature_extraction.feature_cache import find_feature_cache, load_features
    
    # Get feature filename from first regression ensemble (if available)
    # Otherwise, we'll need to load targets from train CSV
    feature_filename = None
    if regression_ensembles:
        model_types = regression_ensembles.get('model_types', [])
        ensemble_configs = regression_ensembles.get('ensemble_configs', {})
        if model_types and model_types[0] in ensemble_configs:
            first_type = model_types[0]
            first_versions = ensemble_configs[first_type].get('model_versions', [])
            if first_versions:
                first_version = first_versions[0]
                first_model_path = Path(base_model_dir or '/kaggle/input/csiro-models/') / 'scikitlearn' / first_type / str(first_version)
                first_metadata_file = first_model_path / 'model_metadata.json'
                if first_metadata_file.exists():
                    import json
                    with open(first_metadata_file, 'r') as f:
                        metadata = json.load(f)
                    feature_filename = metadata.get('feature_filename')
    
    if feature_filename:
        # Load targets from feature cache
        cache_path = find_feature_cache(feature_filename)
        if cache_path:
            _, all_targets, _, _ = load_features(cache_path)
            logger.info(f"Loaded targets from feature cache: {all_targets.shape}")
        else:
            # Fallback: load from train CSV
            all_targets = _load_targets_from_train_csv(config)
    else:
        # Load targets from train CSV
        all_targets = _load_targets_from_train_csv(config)
    
    # Train meta-models on combined OOF predictions
    logger.info("\n" + "="*60)
    logger.info("Training Meta-Models (Ridge) per Target")
    logger.info("="*60)
    from sklearn.linear_model import Ridge
    
    n_targets = all_targets.shape[1]
    meta_models = {}
    meta_model_alpha = hybrid_stacking_config.get('meta_model_alpha', 10.0)
    
    for target_idx in range(n_targets):
        # Build meta-features: stack OOF predictions from all ensembles for this target
        X_meta = np.column_stack([
            all_ensemble_oof_preds[ensemble_name][:, target_idx]
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
            all_ensemble_oof_preds[ensemble_name][:, target_idx]
            for ensemble_name in ensemble_names
        ])
        oof_combined[:, target_idx] = meta_model.predict(X_meta)
    
    oof_score, _ = calc_metric(oof_combined, all_targets)
    logger.info(f"\nHybrid Stacking OOF Score: {oof_score:.4f}")
    
    # Generate final test predictions
    logger.info("\n" + "="*60)
    logger.info("Generating Final Test Predictions")
    logger.info("="*60)
    
    # Get test predictions from first ensemble to determine shape
    first_ensemble_name = ensemble_names[0]
    test_predictions_shape = all_ensemble_test_preds[first_ensemble_name].shape
    final_predictions = np.zeros((test_predictions_shape[0], n_targets))
    
    for target_idx, meta_model in meta_models.items():
        X_meta = np.column_stack([
            all_ensemble_test_preds[ensemble_name][:, target_idx]
            for ensemble_name in ensemble_names
        ])
        final_predictions[:, target_idx] = meta_model.predict(X_meta)
    
    # Clip negative values
    final_predictions = np.clip(final_predictions, 0, None)
    logger.info(f"Final predictions shape: {final_predictions.shape}")
    
    # Validate predictions shape
    test_csv_path = Path(config.data.data_root) / config.data.test_csv
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
    logger.info("Hybrid Stacking Pipeline Complete")
    logger.info("="*60)
    logger.info(f"  Ensembles: {len(ensemble_names)} ({', '.join(ensemble_names)})")
    logger.info(f"  OOF score: {oof_score:.4f}")
    logger.info(f"  Output: {output_path}")
    
    return submission_df


def _generate_regression_ensemble_oof(
    config: Config,
    regression_ensembles: Dict[str, Any],
    hybrid_stacking_config: Dict[str, Any],
    base_model_dir: Optional[str] = None
) -> Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]:
    """
    Generate OOF predictions for regression ensembles.
    
    Reuses logic from stacking_ensemble_pipeline.py.
    
    Args:
        config: Configuration object
        regression_ensembles: Regression ensemble configuration
        hybrid_stacking_config: Full hybrid stacking configuration
        base_model_dir: Base directory for regression models
        
    Returns:
        Tuple of (oof_preds_dict, test_preds_dict):
        - oof_preds_dict: Dict mapping ensemble_name -> OOF predictions
        - test_preds_dict: Dict mapping ensemble_name -> test predictions
    """
    model_types = regression_ensembles.get('model_types', [])
    ensemble_configs = regression_ensembles.get('ensemble_configs', {})
    
    if not model_types or not ensemble_configs:
        return {}, {}
    
    # Load training features and targets
    logger.info("\nLoading training features and targets...")
    from modeling.feature_extraction.feature_cache import find_feature_cache, load_features
    
    # Find feature file from first ensemble config
    feature_filename = None
    feature_extraction_model_name = None
    
    first_model_type = model_types[0]
    if first_model_type in ensemble_configs:
        first_versions = ensemble_configs[first_model_type].get('model_versions', [])
        if first_versions:
            first_version = first_versions[0]
            first_model_path = Path(base_model_dir or '/kaggle/input/csiro-models/') / 'scikitlearn' / first_model_type / str(first_version)
            first_metadata_file = first_model_path / 'model_metadata.json'
            
            if first_metadata_file.exists():
                import json
                with open(first_metadata_file, 'r') as f:
                    metadata = json.load(f)
                feature_filename = metadata.get('feature_filename')
                if feature_filename:
                    feature_extraction_model_name = 'dinov2_base'  # Default
    
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
    device = get_device(config.device.device)
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
    
    # Generate OOF predictions for each regression ensemble
    ensemble_oof_preds = {}
    ensemble_test_preds = {}
    
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
        logger.info(f"  Generating OOF predictions for {model_type} ensemble...")
        from sklearn.model_selection import KFold
        import pickle
        from modeling.models.regression_head import RegressionModel
        
        n_folds = hybrid_stacking_config.get('n_folds', 5)
        kf = KFold(n_splits=n_folds, shuffle=True, random_state=42)
        
        n_train = all_features.shape[0]
        n_targets = all_targets.shape[1]
        
        # Store OOF predictions from each model in ensemble
        model_oof_preds = []
        model_test_preds = []
        
        # Load all models
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
                
                # Create new model instance for this fold
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
        
        logger.info(f"  {model_type} ensemble OOF predictions shape: {ensemble_oof.shape}")
    
    return ensemble_oof_preds, ensemble_test_preds


def _generate_end_to_end_ensemble_oof(
    config: Config,
    end_to_end_ensembles: Dict[str, Any],
    hybrid_stacking_config: Dict[str, Any],
    device: torch.device
) -> Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]:
    """
    Generate OOF predictions for end-to-end ensembles.
    
    Args:
        config: Configuration object
        end_to_end_ensembles: End-to-end ensemble configuration
        hybrid_stacking_config: Full hybrid stacking configuration
        device: Device for inference
        
    Returns:
        Tuple of (oof_preds_dict, test_preds_dict):
        - oof_preds_dict: Dict mapping ensemble_name -> OOF predictions
        - test_preds_dict: Dict mapping ensemble_name -> test predictions
    """
    model_name = end_to_end_ensembles.get('model_name')
    base_model_dir = end_to_end_ensembles.get('base_model_dir')
    ensemble_configs = end_to_end_ensembles.get('ensemble_configs', {})
    
    if not model_name or not base_model_dir or not ensemble_configs:
        return {}, {}
    
    # Update config model name for ensemble creation
    original_model_name = config.model.name
    try:
        # Set model name for ensemble creation (will be used to determine architecture)
        config.model.name = model_name
        
        ensemble_oof_preds = {}
        ensemble_test_preds = {}
        
        train_csv_path = Path(config.data.data_root) / config.data.train_csv
        test_csv_path = Path(config.data.data_root) / config.data.test_csv
        data_root = config.data.data_root
        n_folds = hybrid_stacking_config.get('n_folds', 5)
        
        for ensemble_name, ensemble_config in ensemble_configs.items():
            model_versions = ensemble_config.get('model_versions', [])
            if not model_versions:
                logger.warning(f"Empty model_versions for {ensemble_name}, skipping")
                continue
            
            logger.info(f"\n  Creating {ensemble_name} ensemble (versions {model_versions})...")
            
            # Resolve model paths
            model_paths = []
            for version in model_versions:
                model_path = Path(base_model_dir) / str(version)
                if not model_path.exists():
                    raise FileNotFoundError(f"Model path not found: {model_path}")
                model_paths.append(str(model_path))
            
            logger.info(f"  Model paths: {model_paths}")
            
            # Create ensemble from paths
            ensemble = create_ensemble_from_paths(
                model_paths=model_paths,
                config=config,
                method=ensemble_config.get('method', 'weighted_average'),
                device=device,
                score_type=ensemble_config.get('score_type', 'cv')
            )
            
            logger.info(f"  Created ensemble with {len(ensemble.models)} models")
            
            # Generate OOF predictions
            logger.info(f"  Generating OOF predictions for {ensemble_name}...")
            oof_preds, test_preds = generate_end_to_end_ensemble_oof(
                ensemble=ensemble,
                train_csv_path=str(train_csv_path),
                test_csv_path=str(test_csv_path),
                data_root=data_root,
                config=config,
                n_folds=n_folds,
                device=device
            )
            
            ensemble_oof_preds[ensemble_name] = oof_preds
            ensemble_test_preds[ensemble_name] = test_preds
            
            logger.info(f"  {ensemble_name} OOF predictions shape: {oof_preds.shape}")
            logger.info(f"  {ensemble_name} test predictions shape: {test_preds.shape}")
        
        return ensemble_oof_preds, ensemble_test_preds
        
    finally:
        # Restore original model name
        config.model.name = original_model_name


def _load_targets_from_train_csv(config: Config) -> np.ndarray:
    """
    Load targets from training CSV file.
    
    Args:
        config: Configuration object
        
    Returns:
        Targets array of shape (N_train, num_targets)
    """
    from dataset_manipulation import aggregate_train_csv
    from config.evaluation_constants import PRIMARY_TARGETS
    
    train_csv_path = Path(config.data.data_root) / config.data.train_csv
    train_df = aggregate_train_csv(str(train_csv_path))
    
    # Extract target columns
    targets = train_df[PRIMARY_TARGETS].values.astype(np.float32)
    
    logger.info(f"Loaded targets from train CSV: {targets.shape}")
    
    return targets
