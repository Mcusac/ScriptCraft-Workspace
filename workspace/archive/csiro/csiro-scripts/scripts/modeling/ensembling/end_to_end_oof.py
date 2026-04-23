# end_to_end_oof.py
# Out-of-fold prediction generation for end-to-end ensembles
#
# Generates OOF predictions from end-to-end PyTorch models using cross-validation.
# Used in hybrid stacking pipeline to combine end-to-end ensembles with regression ensembles.

import logging
import numpy as np
import pandas as pd
import torch
from typing import Tuple

from config.config import Config
from modeling.ensembling.ensemble import Ensemble
from modeling.training.cv_splits import create_kfold_splits, get_fold_data
from dataset_manipulation import aggregate_train_csv

logger = logging.getLogger(__name__)


def generate_end_to_end_ensemble_oof(
    ensemble: Ensemble,
    train_csv_path: str,
    test_csv_path: str,
    data_root: str,
    config: Config,
    n_folds: int = 5,
    device: torch.device = None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate OOF predictions for end-to-end ensemble using cross-validation.
    
    For each fold:
    1. Split training data into train/val
    2. Run ensemble inference on validation set (OOF predictions)
    3. Run ensemble inference on test set
    4. Average test predictions across folds
    
    Args:
        ensemble: Ensemble of end-to-end models (already loaded and ready for inference)
        train_csv_path: Path to training CSV file
        test_csv_path: Path to test CSV file
        data_root: Root directory for images
        config: Configuration object
        n_folds: Number of CV folds (default: 5)
        device: Device for inference (default: ensemble.device)
        
    Returns:
        Tuple of (oof_predictions, test_predictions):
        - oof_predictions: (N_train, num_targets) - OOF predictions for training samples
        - test_predictions: (N_test, num_targets) - Averaged test predictions across folds
        
    Raises:
        FileNotFoundError: If train_csv_path or test_csv_path doesn't exist
        ValueError: If training data is empty or invalid
        RuntimeError: If inference fails
    """
    if device is None:
        device = ensemble.device
    
    logger.info(f"Generating OOF predictions for end-to-end ensemble using {n_folds}-fold CV...")
    logger.info(f"  Ensemble has {len(ensemble.models)} models")
    logger.info(f"  Device: {device}")
    
    # Load training data
    logger.info(f"\nLoading training data from {train_csv_path}...")
    train_df = aggregate_train_csv(train_csv_path)
    logger.info(f"Loaded {len(train_df)} training samples")
    
    # Create fold assignments
    logger.info(f"\nCreating {n_folds}-fold CV splits...")
    train_df_with_folds = create_kfold_splits(
        data=train_df,
        n_folds=n_folds,
        shuffle=True,
        random_state=42
    )
    
    # Get number of targets (from config or infer from data)
    from config.evaluation_constants import NUM_PRIMARY_TARGETS
    num_targets = NUM_PRIMARY_TARGETS
    
    # Initialize OOF prediction array (one prediction per training sample)
    n_train = len(train_df_with_folds)
    oof_predictions = np.zeros((n_train, num_targets), dtype=np.float32)
    
    # Initialize test prediction accumulator (will average across folds)
    # First, we need to know how many test samples there are
    from dataset_manipulation import load_and_validate_test_data
    test_images = load_and_validate_test_data(test_csv_path)
    n_test = len(test_images)
    test_predictions_accumulator = np.zeros((n_test, num_targets), dtype=np.float32)
    
    logger.info(f"Initialized OOF predictions: {oof_predictions.shape}")
    logger.info(f"Initialized test predictions accumulator: {test_predictions_accumulator.shape}")
    
    # Process each fold
    for fold in range(n_folds):
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing fold {fold + 1}/{n_folds}")
        logger.info(f"{'='*60}")
        
        # Get train/val split for this fold
        val_data = get_fold_data(train_df_with_folds, fold=fold, train=False)
        train_data = get_fold_data(train_df_with_folds, fold=fold, train=True)
        
        logger.info(f"  Train samples: {len(train_data)}")
        logger.info(f"  Val samples: {len(val_data)}")
        
        if len(val_data) == 0:
            logger.warning(f"  No validation data for fold {fold}, skipping")
            continue
        
        # Create validation dataloader
        # Note: We use val_transform for validation data (no augmentation)
        # The ensemble will handle model-specific preprocessing via predict_with_individual_preprocessing
        logger.info(f"  Creating validation dataloader...")
        
        # For OOF, we need to run inference on validation set
        # The ensemble's predict_with_individual_preprocessing expects a CSV path
        # So we'll create a temporary CSV for the validation set
        import tempfile
        import os
        
        # Create temporary CSV for validation set
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
            val_data.to_csv(tmp_file.name, index=False)
            val_csv_path = tmp_file.name
        
        try:
            # Run ensemble inference on validation set (OOF predictions)
            logger.info(f"  Running ensemble inference on validation set...")
            val_predictions = ensemble.predict_with_individual_preprocessing(
                test_csv_path=val_csv_path,
                data_root=data_root,
                config=config,
                return_individual=False
            )
            
            # Store OOF predictions for validation samples
            # Map validation samples back to their original indices
            val_indices = val_data.index.values
            oof_predictions[val_indices] = val_predictions
            
            logger.info(f"  Stored OOF predictions for {len(val_data)} validation samples")
            logger.info(f"  OOF predictions shape: {val_predictions.shape}")
            
            # Run ensemble inference on test set
            logger.info(f"  Running ensemble inference on test set...")
            test_pred_fold = ensemble.predict_with_individual_preprocessing(
                test_csv_path=test_csv_path,
                data_root=data_root,
                config=config,
                return_individual=False
            )
            
            # Accumulate test predictions (will average later)
            test_predictions_accumulator += test_pred_fold
            logger.info(f"  Test predictions shape: {test_pred_fold.shape}")
            
        finally:
            # Clean up temporary CSV file
            if os.path.exists(val_csv_path):
                os.unlink(val_csv_path)
    
    # Average test predictions across folds
    test_predictions = test_predictions_accumulator / n_folds
    logger.info(f"\nAveraged test predictions across {n_folds} folds")
    
    # Clip negative values (biomass cannot be negative)
    oof_predictions = np.clip(oof_predictions, 0, None)
    test_predictions = np.clip(test_predictions, 0, None)
    
    logger.info(f"\n✅ OOF generation complete")
    logger.info(f"  OOF predictions: {oof_predictions.shape}")
    logger.info(f"  Test predictions: {test_predictions.shape}")
    
    return oof_predictions, test_predictions
