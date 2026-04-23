# train_and_export.py
# Pipeline to train model and export it for submission (Pipeline C)
#
# This is a workflow that orchestrates atomic operations:
# - atomic.train_only: Core training logic
# - atomic.export_model: Core export logic

import logging
from pathlib import Path
from typing import Optional

from config.config import Config
from pipelines.atomic.train_only import train_pipeline
from pipelines.atomic.export_model import export_model_pipeline
from .grid_search.utils.hyperparameters import apply_hyperparameters_to_config
from modeling.utils import get_best_variant_info
from modeling import find_metadata_dir, find_combo_id
from utils.config import apply_dataset_config_to_config, validate_pipeline_config
from utils.system import is_kaggle_environment
from modeling.training.utils import has_incomplete_folds

logger = logging.getLogger(__name__)


def train_and_export_pipeline(
    config: Config,
    results_file: Optional[str] = None,
    variant_id: Optional[str] = None,
    export_dir: Optional[str] = None,
    fresh_train: bool = True,
    export_only: bool = False,
    regression_model_variant_id: Optional[str] = None
) -> None:
    """
    Train model and export it for submission.
    
    Pipeline C: Orchestrates training and export operations.
    
    Modes:
    1. Export only (export_only=True):
       - Finds and exports existing model from grid search or CSIRO models location
       - No training performed (regardless of fresh_train setting)
    2. Train then export (export_only=False):
       - If fresh_train=True: Delete directory if all folds complete, start fresh training
       - If fresh_train=False: Preserve directory, resume from checkpoints if incomplete folds exist
       - Exports the trained model
    
    Args:
        config: Configuration object with training, model, data, cv, paths, and device settings.
                Must have all required attributes configured.
        results_file: Optional path to grid search results.json to use best variant.
                     If provided, applies best variant's config for training or export.
        export_dir: Optional export directory (default: uses get_best_model_path()).
                   Parent directory will be created if it doesn't exist.
        fresh_train: If True, delete directory when all folds complete and start fresh.
                    If False, preserve directory to allow resume from checkpoints.
                    Only applies when export_only=False. Default: True.
        export_only: If True, skip training entirely and just export existing model.
                    If False, perform training (either fresh or resume based on fresh_train).
                    Default: False.
        regression_model_variant_id: Optional regression model variant ID to use instead of best
                                    (only used for feature extraction mode).
                                    If None, uses variant with highest CV score.
        
    Returns:
        None. Exports model checkpoint, metadata, and results.json to export_dir.
        
    Raises:
        ValueError: If config is None or missing required attributes.
        FileNotFoundError: If results_file doesn't exist or model checkpoint not found.
        RuntimeError: If training or export fails.
    """
    # Validate config
    validate_pipeline_config(config, required_sections=['training', 'paths'])
    
    if results_file is not None and not isinstance(results_file, str):
        raise TypeError(f"results_file must be string, got {type(results_file)}")
    
    if export_dir is not None and not isinstance(export_dir, str):
        raise TypeError(f"export_dir must be string, got {type(export_dir)}")
    
    # Determine export directory
    if export_dir is None:
        from utils.system import get_best_model_path
        export_dir = get_best_model_path()
    
    # Mode 1: Export existing model (no training)
    if export_only:
        logger.info("🔄 Export mode: Reusing existing model (export_only=True)")
        logger.info("   Delegating to atomic.export_model_pipeline()...")
        
        # Check for existing training directory (for both regular and feature extraction modes)
        training_model_dir = Path(config.paths.model_dir) / 'best_model_training'
        model_dir_to_export = None
        
        if training_model_dir.exists():
            # Check if directory has any trained models
            has_models = False
            for fold_dir in training_model_dir.iterdir():
                if fold_dir.is_dir() and fold_dir.name.startswith('fold_'):
                    # Check for either PyTorch checkpoint or regression model
                    if (fold_dir / 'best_model.pth').exists() or (fold_dir / 'regression_model.pkl').exists():
                        has_models = True
                        break
            
            if has_models:
                model_dir_to_export = str(training_model_dir)
                logger.info(f"   Found existing trained models in: {model_dir_to_export}")
        
        # Delegate ALL export logic to atomic.export_model
        export_model_pipeline(
            config=config,
            results_file=results_file,
            model_dir=model_dir_to_export,  # Pass training directory if found
            export_dir=export_dir
        )
        return
    
    # Mode 2: Train then export
    if fresh_train:
        logger.info("🆕 Train mode: Training fresh model (fresh_train=True)")
    else:
        logger.info("🔄 Train mode: Resuming from checkpoints (fresh_train=False)")
    
    # Initialize variant_info for export metadata
    export_variant_info = None
    variant_id_used = None
    
    # Apply config from results_file if provided
    if results_file:
        results_path = Path(results_file)
        
        if not results_path.exists():
            raise FileNotFoundError(f"Results file not found: {results_path}")
        
        # Get variant info (specified variant_id or best variant)
        if variant_id:
            logger.info(f"Loading specified variant '{variant_id}' from grid search results: {results_file}")
        else:
            logger.info(f"Loading best variant from grid search results: {results_file}")
        
        variant_info = get_best_variant_info(results_path, variant_id=variant_id)
        variant = variant_info['variant']
        preprocessing_list = variant_info['preprocessing_list']
        augmentation_list = variant_info['augmentation_list']
        variant_id_used = variant_info['variant_id']
        hyperparameters = variant.get('hyperparameters')
        
        # Store variant_info for export metadata (will update with training results later)
        export_variant_info = variant_info.copy()
        
        if variant_id:
            logger.info(f"✅ Using SPECIFIED variant: {variant_id_used}")
            logger.info(f"   (Manually selected via SELECTED_VARIANT_ID config)")
        else:
            logger.info(f"✅ Using BEST variant: {variant_id_used}")
            logger.info(f"   (Highest CV score: {variant_info['cv_score']:.4f})")
        logger.info(f"  Variant ID: {variant_id_used}")
        logger.info(f"  CV Score: {variant_info['cv_score']:.4f}")
        logger.info(f"  Preprocessing: {preprocessing_list}")
        logger.info(f"  Augmentation: {augmentation_list}")
        if hyperparameters:
            logger.info(f"  Hyperparameters: {hyperparameters}")
        
        # Get dataset_type: command-line argument takes precedence over results file
        dataset_type_from_results = variant_info.get('dataset_type')
        dataset_type_from_config = getattr(config.data, 'dataset_type', 'split')
        
        if dataset_type_from_config != 'full' or dataset_type_from_results is None:
            dataset_type = dataset_type_from_config
            if dataset_type_from_results and dataset_type_from_results != dataset_type:
                logger.warning(
                    f"⚠️  Dataset type override detected:\n"
                    f"   Grid search results: dataset_type='{dataset_type_from_results}'\n"
                    f"   Command-line override: dataset_type='{dataset_type}'\n"
                    f"   Using command-line value for training and export.\n"
                    f"   Note: This may differ from the best-scoring configuration in grid search."
                )
        else:
            dataset_type = dataset_type_from_results
        
        config.data.dataset_type = dataset_type
        logger.info(f"  Dataset type: {dataset_type}")
        
        # Apply dataset configuration
        apply_dataset_config_to_config(config, preprocessing_list, augmentation_list)
        
        # Apply hyperparameters if present
        if hyperparameters:
            logger.info("Applying best hyperparameters to config...")
            apply_hyperparameters_to_config(config, hyperparameters)
    else:
        # Use specified config (single training)
        preprocessing_list = config.data.preprocessing_list or []
        augmentation_list = config.data.augmentation_list or []
        
        # Apply dataset configuration
        apply_dataset_config_to_config(config, preprocessing_list, augmentation_list)
        
        logger.info("Starting single training run...")
        logger.info(f"  Preprocessing: {preprocessing_list if preprocessing_list else '[]'}")
        logger.info(f"  Augmentation: {augmentation_list if augmentation_list else '[]'}")
    
    # Handle training directory based on fresh_train flag
    training_model_dir = Path(config.paths.model_dir) / 'best_model_training'
    
    if fresh_train:
        # Delete directory if it exists to ensure fresh training
        if training_model_dir.exists():
            logger.info(f"🗑️  Deleting existing training directory for fresh training")
            import shutil
            shutil.rmtree(training_model_dir)
        else:
            logger.info(f"📁 Training directory doesn't exist - will create fresh")
    else:
        # Preserve directory to allow resume
        if training_model_dir.exists():
            n_folds = config.cv.n_folds
            has_incomplete = has_incomplete_folds(training_model_dir, n_folds)
            if has_incomplete:
                logger.info(f"✅ Training directory has incomplete folds - will resume automatically")
            else:
                logger.info(f"ℹ️  All folds complete - training will skip completed folds")
        else:
            logger.info(f"📁 Training directory doesn't exist - will start fresh training")
    
    config.paths.model_dir = str(training_model_dir)
    
    # Load regression model hyperparameters from grid search results if in feature extraction mode
    regression_model_hyperparameters = None
    if config.model.feature_extraction_mode and config.model.regression_model_type:
        logger.info("="*60)
        logger.info("Loading regression model hyperparameters")
        logger.info("="*60)
        
        # Priority 1: Try loading from metadata file if variant_id is provided
        if regression_model_variant_id:
            try:
                from modeling.utils.metadata.regression_metadata import load_regression_variant_from_metadata
                
                logger.info(f"Attempting to load variant '{regression_model_variant_id}' from metadata file...")
                regression_variant_info = load_regression_variant_from_metadata(
                    regression_model_type=config.model.regression_model_type,
                    variant_id=regression_model_variant_id
                )
                regression_model_hyperparameters = regression_variant_info.get('hyperparameters')
                logger.info(f"✅ Loaded regression model hyperparameters from metadata file")
                logger.info(f"   Variant ID: {regression_variant_info.get('variant_id')}")
                logger.info(f"   Metadata source: csiro-metadata/{config.model.regression_model_type}/metadata.json")
            except (FileNotFoundError, ValueError) as e:
                logger.warning(
                    f"⚠️  Could not load regression hyperparameters from metadata file: {e}\n"
                    f"   Falling back to grid search results..."
                )
                regression_variant_info = None
        
        # Final fallback message if no hyperparameters were loaded
        if not regression_model_hyperparameters:
            logger.warning(
                f"⚠️  No regression model hyperparameters loaded.\n"
                f"   Will use default hyperparameters for regression model."
            )
        
        logger.info("="*60 + "\n")
    
    # Train with best variant's config
    logger.info("Starting training with best variant configuration...")
    cv_score, fold_scores, feature_filename = train_pipeline(config, regression_model_hyperparameters=regression_model_hyperparameters)
    
    # Find best fold
    from modeling.training.utils import find_best_fold_from_scores
    best_fold, best_fold_score = find_best_fold_from_scores(fold_scores)
    logger.info(f"\nBest fold: {best_fold} with score: {best_fold_score:.4f}")
    
    # Create export_variant_info if it doesn't exist (e.g., when training fresh without results_file)
    if export_variant_info is None:
        export_variant_info = {}
    
    # Update variant_info with training results
    export_variant_info['cv_score'] = cv_score
    export_variant_info['fold_scores'] = fold_scores
    export_variant_info['best_fold'] = best_fold
    export_variant_info['best_fold_score'] = best_fold_score
    
    # Add regression model info if in feature extraction mode
    if config.model.feature_extraction_mode:
        if config.model.regression_model_type:
            export_variant_info['regression_model_type'] = config.model.regression_model_type
        
        # Ensure variant_id and variant_index are set for regression models
        if 'variant_id' not in export_variant_info:
            # If variant_id not set, try to get from regression_variant_info or set default
            if regression_model_variant_id:
                export_variant_info['variant_id'] = regression_model_variant_id
            else:
                # Default variant_id for single model export
                export_variant_info['variant_id'] = 'variant_0000'
                logger.info("No variant_id found, using default: variant_0000")
        
        # Set variant_index if not present
        if 'variant_index' not in export_variant_info:
            # Try to get from regression_variant_info if available
            if 'regression_variant_info' in locals() and regression_variant_info:
                export_variant_info['variant_index'] = regression_variant_info.get('variant', {}).get('variant_index', 0)
            else:
                export_variant_info['variant_index'] = 0
                logger.info("No variant_index found, using default: 0")
        
        # Use feature_filename from train_pipeline() if available, otherwise try to construct it
        if feature_filename:
            export_variant_info['feature_filename'] = feature_filename
            logger.info(f"Using feature_filename from training: {feature_filename}")
        elif 'feature_filename' not in export_variant_info:
            # Fallback: try to construct if not provided by training
            try:
                from config.model_constants import get_model_id, get_model_name_from_pretrained
                from modeling.feature_extraction import generate_feature_filename
                
                # Get feature extraction model name from config
                feature_extraction_model_name = config.model.feature_extraction_model_name
                if not feature_extraction_model_name:
                    raise ValueError("config.model.feature_extraction_model_name is required to construct feature_filename")
                
                if '/' in feature_extraction_model_name or feature_extraction_model_name.startswith('/'):
                    # Convert path to model name
                    resolved_name = get_model_name_from_pretrained(feature_extraction_model_name)
                    if resolved_name:
                        feature_extraction_model_name = resolved_name
                
                # Get combo_id from preprocessing/augmentation
                preprocessing_list = config.data.preprocessing_list or []
                augmentation_list = config.data.augmentation_list or []
                
                metadata_dir = find_metadata_dir()
                if metadata_dir:
                    combo_id = find_combo_id(preprocessing_list, augmentation_list, metadata_dir)
                    if combo_id:
                        model_id = get_model_id(feature_extraction_model_name)
                        constructed_filename = generate_feature_filename(model_id, combo_id)
                        export_variant_info['feature_filename'] = constructed_filename
                        logger.info(f"Constructed feature_filename for export: {constructed_filename}")
                    else:
                        logger.warning(
                            f"Could not resolve combo_id for preprocessing={preprocessing_list}, "
                            f"augmentation={augmentation_list}. Feature filename may be missing."
                        )
                else:
                    logger.warning("Metadata directory not found. Feature filename may be missing.")
            except Exception as e:
                logger.warning(f"Could not construct feature_filename for export: {e}")
    
    # Export trained model - delegate to atomic.export_model
    # Pass variant_info to ensure metadata includes correct variant_id and all variant details
    logger.info("Exporting trained model...")
    export_model_pipeline(
        config=config,
        model_dir=str(training_model_dir),  # Just-trained location
        export_dir=export_dir,
        variant_id=variant_id_used,  # Pass variant_id (None if not from results_file)
        variant_info=export_variant_info  # Pass complete variant_info for accurate metadata
    )
    
    # Copy results.json for reference if available
    if results_file:
        results_path = Path(results_file)
        if results_path.exists():
            import shutil
            export_path = Path(export_dir)
            dest_results = export_path / 'results.json'
            shutil.copy2(results_path, dest_results)
            logger.info(f"Copied results.json to: {dest_results}")
    
    logger.info("="*60)
    logger.info("✅ Model trained and exported successfully!")
    if results_file and 'variant_id_used' in locals():
        logger.info(f"   Variant ID: {variant_id_used}")
        if variant_id:
            logger.info(f"   Selection: Manually specified variant")
        else:
            logger.info(f"   Selection: Best variant (highest CV score)")
    logger.info(f"   CV Score: {cv_score:.4f}")
    logger.info(f"   Best Fold: {best_fold} (score: {best_fold_score:.4f})")
    logger.info(f"   Export directory: {export_dir}")
    logger.info(f"   Metadata: model_metadata.json contains variant information")
    logger.info(f"{'='*60}")
    
    # Print summary for Kaggle
    if is_kaggle_environment():
        logger.info("\n📥 Next steps:")
        logger.info("   1. Download the 'best_model' folder from /kaggle/working/")
        logger.info("   2. Create a Kaggle dataset and upload the entire best_model folder")
        logger.info("   3. Add the dataset to your submission notebook as input")
        logger.info(f"   4. Make sure your submission notebook uses MODEL = '{config.model.name}'")
