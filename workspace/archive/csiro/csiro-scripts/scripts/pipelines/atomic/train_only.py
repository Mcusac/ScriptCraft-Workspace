# train_only.py
# Pipeline to train model only

import logging
from pathlib import Path
from typing import Tuple, List, Optional, Dict, Any
import torch

from config.config import Config
from dataset_manipulation import aggregate_train_csv
from modeling.training import create_kfold_splits, get_fold_data
from utils.system import set_seed, ensure_dir, get_device, get_device_info
from utils.system import clear_gpu_memory, recover_from_oom
from utils.system import validate_reproducibility_settings
from modeling.training.utils import is_checkpoint_complete, get_fold_checkpoint_path
from utils.config import validate_pipeline_config

logger = logging.getLogger(__name__)


def train_pipeline(
    config: Config,
    regression_model_hyperparameters: Optional[Dict[str, Any]] = None
) -> Tuple[float, List[float], Optional[str]]:
    """
    Train model with cross-validation.
    
    Args:
        config: Configuration object with training, model, data, cv, paths, and device settings.
                Must have all required attributes configured.
        regression_model_hyperparameters: Optional hyperparameters for regression model
                                        (only used for feature extraction mode).
        
    Returns:
        Tuple of (avg_cv_score, fold_scores, feature_filename):
        - avg_cv_score: Average cross-validation score across all folds (float)
        - fold_scores: List of scores for each fold (List[float], length = n_folds)
        - feature_filename: Feature filename if in feature extraction mode, None otherwise (Optional[str])
        
    Raises:
        ValueError: If config is None or missing required attributes.
        RuntimeError: If training fails for all folds.
    """
    # Validate config
    validate_pipeline_config(config, required_sections=['data', 'training', 'cv', 'paths'])
    
    # Setup seeds and validate reproducibility
    set_seed(config.seed)
    validate_reproducibility_settings(config)
    config.ensure_dirs()
    
    # Load and aggregate data
    train_csv_path = Path(config.data.data_root) / config.data.train_csv
    logger.info(f"Loading train data from {train_csv_path}")
    
    agg_train_df = aggregate_train_csv(train_csv_path)
    
    # Create CV splits
    agg_train_df = create_kfold_splits(
        agg_train_df,
        n_folds=config.cv.n_folds,
        shuffle=config.cv.shuffle,
        random_state=config.cv.random_state
    )
    
    # Device - automatically detect best available
    device = get_device(config.device.device)
    device_info = get_device_info()
    logger.info(f"Device info: {device_info}")
    
    # Pre-extract features for all images if in feature extraction mode
    all_features = None
    all_targets = None
    fold_assignments = None
    feature_filename = None  # Store feature filename for return value
    
    if getattr(config.model, 'feature_extraction_mode', False):
        logger.info("="*60)
        logger.info("Feature Extraction Mode: Pre-extracting features for all images")
        logger.info("="*60)
        
        # Check if we should extract or load from cache
        extract_features = getattr(config.model, 'extract_features', True)
        
        # Generate feature filename using model_id and combo_id
        from modeling.feature_extraction import (
            generate_feature_filename,
            find_feature_cache,
            load_features,
            save_features
        )
        from config.model_constants import get_model_id, get_model_name_from_pretrained
        from modeling import (
            find_metadata_dir,
            get_or_create_combo_id
        )
        
        # Get model_id from feature extraction model name
        # feature_extraction_model_name might be a path, so convert it to model name if needed
        model_name = config.model.feature_extraction_model_name
        if not model_name:
            raise ValueError("config.model.feature_extraction_model_name is required for feature extraction")
        
        # If model_name looks like a path, try to convert it to a model name
        if model_name.startswith('/') or '/' in model_name:
            resolved_name = get_model_name_from_pretrained(model_name)
            if resolved_name:
                model_name = resolved_name
            # If conversion failed, model_name will be used as-is and will raise error in get_model_id
        
        model_id = get_model_id(model_name)
        
        # Get combo_id from preprocessing_list and augmentation_list
        preprocessing_list = getattr(config.data, 'preprocessing_list', []) or []
        augmentation_list = getattr(config.data, 'augmentation_list', []) or []
        
        metadata_dir = find_metadata_dir()
        if not metadata_dir:
            raise FileNotFoundError(
                "csiro-metadata directory not found. Cannot get combo_id for feature extraction. "
                "Expected: /kaggle/input/csiro-metadata (Kaggle) or ../csiro-metadata (local)"
            )
        
        combo_id = get_or_create_combo_id(preprocessing_list, augmentation_list, metadata_dir)
        
        # Generate filename
        filename = generate_feature_filename(model_id, combo_id)
        feature_filename = filename  # Store for return value
        logger.info(f"Feature filename: {filename} (model_id={model_id}, combo_id={combo_id})")
        
        # Try to find existing cache
        cache_path = find_feature_cache(filename)
        
        if not extract_features and cache_path is not None:
            # Try to load from cache
            logger.info(f"Loading all-features cache (filename: {filename})...")
            try:
                all_features, all_targets, fold_assignments, metadata = load_features(cache_path)
                logger.info(f"✅ Successfully loaded all-features cache")
                logger.info(f"  Model: {metadata.get('model_name', 'unknown')}")
                logger.info(f"  Dataset type: {metadata.get('dataset_type', 'unknown')}")
                logger.info(f"  Features: {all_features.shape}, Targets: {all_targets.shape}")
            except (FileNotFoundError, PermissionError, OSError) as e:
                # File system errors - log and extract features
                logger.warning(f"Failed to load cache: {e}. Extracting features...")
                extract_features = True
            except (KeyError, ValueError, TypeError) as e:
                # Data format errors - log and extract features
                logger.warning(f"Cache file format error: {e}. Extracting features...")
                extract_features = True
            except Exception as e:
                # Catch any other unexpected errors
                logger.warning(f"Unexpected error loading cache: {e}. Extracting features...", exc_info=True)
                extract_features = True
        
        if extract_features or all_features is None:
            # Extract features for all images
            logger.info("Extracting features from all images...")
            
            # Create trainer for feature extraction
            from modeling.training import create_trainer
            feature_trainer = create_trainer(config, device, regression_model_hyperparameters=regression_model_hyperparameters)
            
            # Create a single dataloader for all images
            # Use train_data=agg_train_df and val_data=agg_train_df (same data)
            # We'll use the train_loader for extraction
            all_loader, _, (all_dataset, _) = feature_trainer.create_dataloaders(
                train_data=agg_train_df,
                val_data=agg_train_df,  # Same data, we just need one dataloader
                data_root=config.data.data_root
            )
            
            # Extract features and targets using the train_loader
            all_features, all_targets = feature_trainer.extract_all_features(all_loader)
            
            # Get fold assignments from dataframe
            fold_assignments = agg_train_df['fold'].values
            
            # Save to cache
            logger.info(f"Saving all-features cache (filename: {filename})...")
            save_features(
                all_features=all_features,
                all_targets=all_targets,
                fold_assignments=fold_assignments,
                filename=filename,
                config=config,
                use_input_dir=True
            )
            
            # Cleanup
            del all_loader, all_dataset
            del feature_trainer
            clear_gpu_memory(log_memory=False)
            logger.info("=" * 60)
            logger.info("✅ FEATURE EXTRACTION COMPLETE")
            logger.info("=" * 60)
            logger.info(f"Extracted features shape: {all_features.shape}")
            logger.info(f"Targets shape: {all_targets.shape}")
            logger.info("Starting regression head training for all folds...")
            logger.info("=" * 60)
            logger.info("🎯 REGRESSION HEAD TRAINING")
            logger.info("=" * 60)
    
    # Train each fold
    all_scores = []
    model_dir = Path(config.paths.model_dir)
    
    for fold in range(config.cv.n_folds):
        logger.info("="*50)
        logger.info(f"Training fold {fold}/{config.cv.n_folds - 1}")
        logger.info(f"{'='*50}")
        
        # Check if fold is already complete using utility function
        checkpoint_path = get_fold_checkpoint_path(model_dir, fold)
        is_complete, checkpoint_info = is_checkpoint_complete(checkpoint_path)
        
        if is_complete and checkpoint_info:
            # Skip completed fold
            existing_score = checkpoint_info['best_score']
            existing_epochs = len(checkpoint_info['history'])
            logger.info(f"Found complete checkpoint for fold {fold}")
            logger.info(f"  Best score: {existing_score:.4f}")
            logger.info(f"  Trained epochs: {existing_epochs}")
            logger.info(f"Skipping fold {fold} - training already complete")
            all_scores.append(existing_score)
            logger.info(f"Fold {fold} best score: {existing_score:.4f}")
            continue
        elif checkpoint_info:
            # Checkpoint exists but incomplete - will resume
            logger.info(f"Found incomplete checkpoint for fold {fold}, will resume training")
        
        # CRITICAL: Clear GPU memory before starting each fold
        # This ensures clean memory state between folds
        clear_gpu_memory(log_memory=False)
        
        # Create trainer and data loaders - wrap in try to ensure cleanup on OOM
        trainer = None
        train_loader = None
        val_loader = None
        train_dataset = None
        val_dataset = None
        oom_occurred = False
        
        try:
            # Create trainer (factory routes to appropriate trainer based on config)
            from modeling.training import create_trainer
            
            # Use regression-only mode if features are already extracted
            # This avoids recreating the feature extraction model (e.g., DINOv2) for each fold
            regression_only = (
                getattr(config.model, 'feature_extraction_mode', False) 
                and all_features is not None
            )
            
            trainer = create_trainer(
                config, 
                device, 
                regression_model_hyperparameters=regression_model_hyperparameters,
                regression_only=regression_only
            )
            
            # Train (will automatically resume from checkpoint if it exists)
            save_dir = model_dir / f'fold_{fold}'
            ensure_dir(save_dir)
            
            # Resume is enabled by default in trainer.train()
            # For feature extraction mode with pre-extracted features, pass them directly
            if getattr(config.model, 'feature_extraction_mode', False) and all_features is not None:
                # Use pre-extracted features - no need for data loaders
                history = trainer.train(
                    train_loader=None,  # Not needed when using pre-extracted features
                    val_loader=None,   # Not needed when using pre-extracted features
                    save_dir=save_dir,
                    resume=True,
                    extract_features=False,  # Don't extract, use pre-extracted
                    fold=fold,
                    all_features=all_features,
                    all_targets=all_targets,
                    fold_assignments=fold_assignments
                )
            else:
                # Regular training or feature extraction without pre-extraction
                # Get fold data
                train_data = get_fold_data(agg_train_df, fold, train=True)
                val_data = get_fold_data(agg_train_df, fold, train=False)
                
                # Create data loaders (now also returns datasets for cleanup)
                train_loader, val_loader, (train_dataset, val_dataset) = trainer.create_dataloaders(
                    train_data=train_data,
                    val_data=val_data,
                    data_root=config.data.data_root
                )
                
                extract_features = getattr(config.model, 'extract_features', True)
                history = trainer.train(
                    train_loader=train_loader,
                    val_loader=val_loader,
                    save_dir=save_dir,
                    resume=True,  # Explicitly enable resume (default is True)
                    extract_features=extract_features,
                    fold=fold
                )
            
            all_scores.append(trainer.best_score)
            logger.info(f"Fold {fold} best score: {trainer.best_score:.4f}")
            
        except torch.OutOfMemoryError as e:
            # OOM error - mark for aggressive cleanup in finally block
            logger.error(f"CUDA OOM error during fold {fold}: {e}")
            oom_occurred = True
            # Re-raise to allow grid search to handle it
            raise
            
        finally:
            # CRITICAL: Explicitly clean up GPU memory after each fold
            # This runs even if training succeeded or failed
            model_to_cleanup = None
            
            if trainer is not None:
                try:
                    # Extract model reference before deleting trainer
                    # Cleanup operations must not fail - catch all exceptions
                    if hasattr(trainer, 'model') and trainer.model is not None:
                        model_to_cleanup = trainer.model
                        # Clear model reference from trainer
                        trainer.model = None
                except (AttributeError, RuntimeError) as e:
                    # AttributeError: model attribute access issue
                    # RuntimeError: CUDA/device errors during cleanup
                    logger.debug(f"Error extracting model for cleanup (fold {fold}): {e}")
                except Exception as e:
                    # Catch any other unexpected errors during cleanup
                    logger.debug(f"Unexpected error extracting model for cleanup (fold {fold}): {e}", exc_info=True)
                
                try:
                    # Delete optimizer and scheduler references
                    # Cleanup operations must not fail - catch all exceptions
                    if hasattr(trainer, 'optimizer'):
                        trainer.optimizer = None
                    if hasattr(trainer, 'scheduler'):
                        trainer.scheduler = None
                    # Delete trainer
                    del trainer
                except (AttributeError, RuntimeError) as e:
                    logger.debug(f"Error deleting trainer for fold {fold}: {e}")
                except Exception as e:
                    logger.debug(f"Unexpected error deleting trainer for fold {fold}: {e}", exc_info=True)
            
            # Delete data loaders
            # Cleanup operations must not fail - catch all exceptions
            try:
                if train_loader is not None:
                    del train_loader
                    train_loader = None
            except (AttributeError, RuntimeError) as e:
                logger.debug(f"Error deleting train_loader for fold {fold}: {e}")
            except Exception as e:
                logger.debug(f"Unexpected error deleting train_loader for fold {fold}: {e}", exc_info=True)
            try:
                if val_loader is not None:
                    del val_loader
                    val_loader = None
            except (AttributeError, RuntimeError) as e:
                logger.debug(f"Error deleting val_loader for fold {fold}: {e}")
            except Exception as e:
                logger.debug(f"Unexpected error deleting val_loader for fold {fold}: {e}", exc_info=True)
            
            # Delete datasets (important for memory cleanup, especially streaming datasets)
            # Cleanup operations must not fail - catch all exceptions
            try:
                if train_dataset is not None:
                    del train_dataset
                    train_dataset = None
            except (AttributeError, RuntimeError) as e:
                logger.debug(f"Error deleting train_dataset for fold {fold}: {e}")
            except Exception as e:
                logger.debug(f"Unexpected error deleting train_dataset for fold {fold}: {e}", exc_info=True)
            try:
                if val_dataset is not None:
                    del val_dataset
                    val_dataset = None
            except (AttributeError, RuntimeError) as e:
                logger.debug(f"Error deleting val_dataset for fold {fold}: {e}")
            except Exception as e:
                logger.debug(f"Unexpected error deleting val_dataset for fold {fold}: {e}", exc_info=True)
            
            # Clear GPU memory cache
            # Use specialized OOM recovery if OOM occurred
            if oom_occurred:
                # For OOM errors, use specialized recovery function
                # This handles memory fragmentation and resets CUDA stats
                from utils.system import recover_from_oom
                recover_from_oom(
                    model=model_to_cleanup,
                    delay_seconds=2.0,  # Longer delay for OOM recovery
                    cleanup_passes=3
                )
                # Also clean up datasets and loaders
                clear_gpu_memory(
                    log_memory=False,
                    dataset=train_dataset if train_dataset is not None else val_dataset,
                    dataloader=train_loader if train_loader is not None else val_loader,
                    aggressive=False  # Already did aggressive cleanup above
                )
            else:
                # Regular cleanup - pass datasets and loaders for proper cleanup
                clear_gpu_memory(
                    log_memory=False, 
                    model=model_to_cleanup,
                    dataset=train_dataset if train_dataset is not None else val_dataset,
                    dataloader=train_loader if train_loader is not None else val_loader
                )
    
    # Summary
    avg_cv_score = sum(all_scores) / len(all_scores) if all_scores else -float('inf')
    logger.info("="*50)
    logger.info("Cross-validation summary:")
    logger.info(f"Average CV score: {avg_cv_score:.4f}")
    logger.info(f"Individual fold scores: {all_scores}")
    logger.info(f"{'='*50}")
    
    return avg_cv_score, all_scores, feature_filename
