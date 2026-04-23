# multi_variant_regression_training.py
# Pipeline to train and export multiple regression models in batch
#
# Trains one regression model per variant index, reusing feature extraction.
# Each model exports to best_model_{index}/ folder.

import logging
from pathlib import Path
from typing import List, Optional

from config.config import Config
from pipelines.workflows.train_and_export import train_and_export_pipeline
from utils.config import validate_pipeline_config
from utils.notebook.model_selection import get_variant_info_from_model_id
from utils.system.io import get_output_path
from config.model_constants import get_model_id
from modeling.feature_extraction import generate_feature_filename

logger = logging.getLogger(__name__)


def multi_variant_regression_training_pipeline(
    config: Config,
    model_ids: List[str],
    feature_extraction_model: str,
    regression_model_type: str,
    data_manipulation_combo: Optional[str] = None,
    extract_features: bool = True,
    fresh_train: bool = False
) -> None:
    """
    Train and export multiple regression models, one per model_id.
    
    Pipeline flow:
    1. Extract features once (shared across all models)
    2. For each model_id:
       a. Get variant_id, feature_filename from model_id (from gridsearch_metadata.json)
       b. Load hyperparameters for that variant
       c. Train regression model
       d. Export to best_model_{model_id}/ folder
    3. All models use same feature extraction and data manipulation combo
    
    Args:
        config: Configuration object with model, data, paths, and device settings
        model_ids: List of model_id strings from gridsearch_metadata.json (e.g., ["080", "083", "086"])
        feature_extraction_model: Model name for feature extraction
        regression_model_type: Type of regression model ('lgbm', 'xgboost', 'ridge')
        data_manipulation_combo: Optional combo ID for data manipulation
        extract_features: Whether to extract features from scratch
        fresh_train: Whether to start fresh training (delete existing directories)
        
    Raises:
        ValueError: If configuration is invalid
        FileNotFoundError: If required files not found
        RuntimeError: If pipeline fails
    """
    # Validate config
    validate_pipeline_config(config, required_sections=['data', 'paths', 'model', 'cv'])
    
    logger.info("="*60)
    logger.info("Multi-Variant Regression Training Pipeline")
    logger.info("="*60)
    logger.info(f"  Regression model type: {regression_model_type}")
    logger.info(f"  Feature extraction model: {feature_extraction_model}")
    logger.info(f"  Data manipulation combo: {data_manipulation_combo or 'combo_00 (default)'}")
    logger.info(f"  Model IDs to train: {model_ids}")
    logger.info(f"  Extract features: {extract_features}")
    logger.info(f"  Fresh train: {fresh_train}")
    
    if not model_ids:
        raise ValueError("model_ids cannot be empty")
    
    # Set feature extraction mode
    config.model.feature_extraction_mode = True
    config.model.regression_model_type = regression_model_type
    config.model.feature_extraction_model_name = feature_extraction_model
    config.model.extract_features = extract_features  # Control feature extraction
    
    # Apply data manipulation combo if provided
    if data_manipulation_combo:
        from utils.config.config_updater import apply_combo_to_config, apply_dataset_config_to_config
        try:
            apply_combo_to_config(config, data_manipulation_combo)
            logger.info(f"Applied data manipulation combo: {data_manipulation_combo}")
        except (FileNotFoundError, ValueError) as e:
            logger.warning(f"Could not load data manipulation combo {data_manipulation_combo}: {e}")
            logger.info("Using default (empty preprocessing/augmentation)")
            apply_dataset_config_to_config(config, [], [])
    
    # Generate feature filename for export directory structure
    model_id = get_model_id(feature_extraction_model)
    combo_id = data_manipulation_combo or 'combo_000'
    feature_filename = generate_feature_filename(model_id, combo_id)
    
    # Parse feature filename to get combo numeric part for export path
    # Format: variant_{model_id}{combo_numeric}_features.npz
    # Example: variant_0163_features.npz -> model_id=01, combo_numeric=63
    if feature_filename.startswith('variant_') and '_features.npz' in feature_filename:
        parts = feature_filename.replace('variant_', '').replace('_features.npz', '')
        if len(parts) >= 4:
            combo_numeric = parts[2:4]
        else:
            combo_numeric = combo_id.replace('combo_', '').zfill(2)
    else:
        combo_numeric = combo_id.replace('combo_', '').zfill(2)
    
    # Base export directory structure
    export_base = Path(get_output_path(f'regression_training/{regression_model_type}'))
    export_path_combo = export_base / f"{model_id}_{combo_numeric}"
    
    # Train each model
    logger.info("\n" + "="*60)
    logger.info("Training Regression Models per Model ID")
    logger.info("="*60)
    logger.info(f"  Feature extraction model: {feature_extraction_model}")
    logger.info(f"  Export base: {export_path_combo}")
    
    # Track if features have been extracted (to reuse for subsequent models)
    features_extracted = False
    
    for model_idx, model_id in enumerate(model_ids):
        logger.info("\n" + "-"*60)
        logger.info(f"Model {model_idx + 1}/{len(model_ids)}: model_id {model_id}")
        logger.info("-"*60)
        
        try:
            # Get variant_id, feature_filename from model_id
            variant_id, model_feature_filename, cv_score = get_variant_info_from_model_id(
                regression_model_type, model_id
            )
            logger.info(f"  Model ID: {model_id}")
            logger.info(f"  Variant ID: {variant_id}")
            logger.info(f"  Feature filename: {model_feature_filename}")
            logger.info(f"  CV score: {cv_score:.6f}" if cv_score is not None else "  CV score: N/A")
            
            # Set up export directory for this model
            export_dir = export_path_combo / f"best_model_{model_id}"
            export_dir.mkdir(parents=True, exist_ok=True)
            
            # Set up training directory for this model (unique per model_id)
            base_training_dir = Path(config.paths.model_dir)
            model_training_dir = base_training_dir / f'model_{model_id}_training'
            
            if fresh_train and model_training_dir.exists():
                logger.info(f"  🗑️  Deleting existing training directory for fresh training")
                import shutil
                shutil.rmtree(model_training_dir)
            
            # Temporarily update config model_dir for this model
            original_model_dir = config.paths.model_dir
            config.paths.model_dir = str(model_training_dir)
            
            try:
                # Determine if we should extract features
                # Extract on first model, reuse for subsequent models
                should_extract = extract_features and not features_extracted
                config.model.extract_features = should_extract
                
                if should_extract:
                    logger.info(f"  Extracting features from scratch...")
                elif features_extracted:
                    logger.info(f"  Reusing features from previous model...")
                else:
                    logger.info(f"  Loading features from cache...")
                
                # Train and export using train_and_export_pipeline
                # This handles feature extraction, training, and export in one call
                train_and_export_pipeline(
                    config=config,
                    results_file=None,  # Not using grid search results file
                    variant_id=None,  # Not applicable for regression models
                    export_dir=str(export_dir),  # Custom export directory
                    fresh_train=fresh_train and model_idx == 0,  # Only fresh train on first model
                    export_only=False,
                    regression_model_variant_id=variant_id  # Use specific variant
                )
                
                # Mark features as extracted after first model
                if should_extract:
                    features_extracted = True
                    # Disable feature extraction for subsequent models
                    config.model.extract_features = False
                
                logger.info(f"  ✅ Training and export complete for model_id {model_id}")
                logger.info(f"     Export directory: {export_dir}")
                
            finally:
                # Restore original model_dir
                config.paths.model_dir = original_model_dir
                
        except Exception as e:
            logger.error(f"  ❌ Failed to train model_id {model_id}: {e}")
            logger.exception("Full error traceback:")
            # Continue with next model
            continue
    
    logger.info("\n" + "="*60)
    logger.info("Multi-Variant Regression Training Pipeline Complete")
    logger.info("="*60)
    logger.info(f"  Trained {len(model_ids)} models")
    logger.info(f"  Export base directory: {export_path_combo}")
    logger.info(f"  Export directories:")
    for model_id in model_ids:
        export_dir = export_path_combo / f"best_model_{model_id}"
        logger.info(f"    - best_model_{model_id}/ -> {export_dir}")
    logger.info(f"  Each directory contains: regression_model.pkl, model_metadata.json")
