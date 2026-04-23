# feature_extraction_trainer.py
# Two-stage trainer for feature extraction mode
# Stage 1: Extract features from images using feature extraction model
# Stage 2: Train regression model on extracted features

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from typing import Dict, List, Optional, Tuple, Callable, Any
import numpy as np
import pandas as pd
import logging
import os
from pathlib import Path

from modeling.evaluation.metrics import calc_metric
from modeling.feature_extraction import FeatureExtractor
from modeling.models import RegressionModel
from utils.system import ensure_dir
from modeling.models import create_model
from config.config import Config
from utils.config.config_validator import validate_config_section

logger = logging.getLogger(__name__)


def split_features_by_fold(
    all_features: np.ndarray,
    all_targets: np.ndarray,
    fold_assignments: np.ndarray,
    current_fold: int
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split all features and targets by fold assignment.
    
    Args:
        all_features: All features array (N_total, feat_dim).
        all_targets: All targets array (N_total, 3).
        fold_assignments: Fold assignments array (N_total,) with values 0 to n_folds-1.
        current_fold: Current fold number to split for.
    
    Returns:
        Tuple of (train_features, val_features, train_targets, val_targets):
        - train_features: Features for all folds except current_fold
        - val_features: Features for current_fold only
        - train_targets: Targets for all folds except current_fold
        - val_targets: Targets for current_fold only
    
    Raises:
        ValueError: If arrays have mismatched shapes or invalid fold assignments.
    """
    if all_features.shape[0] != all_targets.shape[0] or all_features.shape[0] != fold_assignments.shape[0]:
        raise ValueError(
            f"Array length mismatch: all_features={all_features.shape[0]}, "
            f"all_targets={all_targets.shape[0]}, fold_assignments={fold_assignments.shape[0]}"
        )
    
    if current_fold < 0:
        raise ValueError(f"current_fold must be >= 0, got {current_fold}")
    
    # Create masks
    train_mask = fold_assignments != current_fold
    val_mask = fold_assignments == current_fold
    
    # Check that validation set is not empty
    if not np.any(val_mask):
        raise ValueError(f"No samples found for fold {current_fold}")
    
    # Split features and targets
    train_features = all_features[train_mask]
    val_features = all_features[val_mask]
    train_targets = all_targets[train_mask]
    val_targets = all_targets[val_mask]
    
    logger.debug(f"Split features for fold {current_fold}: train {train_features.shape}, val {val_features.shape}")
    
    return train_features, val_features, train_targets, val_targets


class FeatureExtractionTrainer:
    """
    Two-stage trainer for feature extraction mode.
    
    Stage 1: Extract features from images using a feature extraction model
    Stage 2: Train a regression model (LGBM/XGB/Ridge) on the extracted features
    
    This approach is useful for small datasets where end-to-end training
    may overfit, or when using large pretrained models for feature extraction.
    """
    
    def __init__(
        self,
        config: Config,
        device: torch.device,
        feature_extraction_model: Optional[nn.Module] = None,
        regression_model_hyperparameters: Optional[Dict[str, Any]] = None,
        regression_only: bool = False
    ):
        """
        Initialize FeatureExtractionTrainer.
        
        Args:
            config: Configuration object with feature_extraction_mode=True.
                   Must have model.feature_extraction_model_name and
                   model.regression_model_type set.
            device: Device to run feature extraction on.
            feature_extraction_model: Optional feature extraction model instance.
                                    If None and regression_only=False, creates from config.
            regression_model_hyperparameters: Optional hyperparameters dict for regression model.
                                            If None, uses default parameters.
            regression_only: If True, skip creating feature extraction model (for fold training
                           when features are already extracted). Only creates regression model.
        
        Raises:
            ValueError: If config is invalid or missing required attributes.
        """
        # Validate config
        if config is None:
            raise ValueError("config cannot be None")
        
        validate_config_section(config, 'model')
        validate_config_section(config, 'device')
        
        if not config.model.feature_extraction_mode:
            raise ValueError(
                "FeatureExtractionTrainer requires config.model.feature_extraction_mode=True"
            )
        
        if not regression_only:
            # Only require feature_extraction_model_name if we're creating the model
            if not config.model.feature_extraction_model_name:
                raise ValueError(
                    "FeatureExtractionTrainer requires config.model.feature_extraction_model_name"
                )
        
        if not config.model.regression_model_type:
            raise ValueError(
                "FeatureExtractionTrainer requires config.model.regression_model_type"
            )
        
        # Validate device
        if not isinstance(device, torch.device):
            raise TypeError(f"device must be torch.device, got {type(device)}")
        
        self.config = config
        self.device = device
        self.dataset_type = getattr(config.data, 'dataset_type', 'split')
        self.regression_only = regression_only
        
        # Create or use provided feature extraction model (skip if regression_only)
        if regression_only:
            # Regression-only mode: skip feature extraction model creation
            self.feature_extractor = None
        else:
            # Create or use provided feature extraction model
            if feature_extraction_model is None:
                # Create feature extraction model (no regression head)
                feature_extraction_model = self._create_feature_extraction_model()
            
            self.feature_extractor = FeatureExtractor(feature_extraction_model, device)
        
        # Create regression model
        self.regression_model = RegressionModel(
            model_type=config.model.regression_model_type,
            model_params=regression_model_hyperparameters,
            random_state=config.seed
        )
        
        # Training state
        self.best_score = -float('inf')
        self.best_epoch = 0
        self.history: List[Dict] = []
    
    def _create_feature_extraction_model(self) -> nn.Module:
        """
        Create feature extraction model from config.
        
        Creates a model configured for feature extraction only (no regression head).
        Uses the model's backbone for feature extraction.
        """
        # Temporarily modify config to create feature extraction model
        original_name = self.config.model.name
        original_num_classes = self.config.model.num_classes
        
        # Use feature extraction model name
        self.config.model.name = self.config.model.feature_extraction_model_name
        # Keep num_classes as 3 (model will create head, but we'll use backbone only)
        # This ensures model creation works correctly
        
        try:
            # Create model (will have backbone and head, but we'll use backbone for feature extraction)
            model = create_model(self.config)
            
            # For DINOv2, we can use the backbone directly for feature extraction
            # The model's _extract_hf_features method will be available
            # For other models, we might need to access backbone
            if hasattr(model, 'backbone'):
                # Create a wrapper that uses backbone but exposes feature extraction methods
                # Check if model has _extract_hf_features method (DINOv2)
                if hasattr(model, '_extract_hf_features'):
                    # Use model directly (it has feature extraction method)
                    feature_model = model
                else:
                    # Use backbone only
                    feature_model = model.backbone
            else:
                # Model doesn't have separate backbone, use as-is
                # Check if it has feature extraction method
                if hasattr(model, '_extract_hf_features') or hasattr(model, 'extract_features'):
                    feature_model = model
                else:
                    # Fallback: use model as-is (FeatureExtractor will handle it)
                    feature_model = model
            
            logger.info(f"Created feature extraction model: {self.config.model.feature_extraction_model_name}")
            return feature_model
            
        finally:
            # Restore original config
            self.config.model.name = original_name
            self.config.model.num_classes = original_num_classes
    
    def extract_all_features(
        self,
        all_loader: DataLoader
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Extract features and targets from all images (not split by fold).
        
        Args:
            all_loader: DataLoader containing ALL images (no fold split).
        
        Returns:
            Tuple of (all_features, all_targets):
            - all_features: Features array of shape (N_total, feat_dim)
            - all_targets: Targets array of shape (N_total, 3)
        """
        logger.info("Extracting features from all images...")
        
        # Extract features (TTA enabled via config)
        all_features = self.feature_extractor.extract_features(
            all_loader,
            dataset_type=self.dataset_type,
            config=self.config
        )
        
        # Extract targets
        all_targets = self._extract_targets(all_loader)
        
        logger.info(f"Extracted features: {all_features.shape}, targets: {all_targets.shape}")
        
        return all_features, all_targets
    
    def train(
        self,
        train_loader: Optional[DataLoader] = None,
        val_loader: Optional[DataLoader] = None,
        num_epochs: Optional[int] = None,
        save_dir: Optional[Path] = None,
        resume: bool = True,
        extract_features: bool = True,
        fold: Optional[int] = None,
        all_features: Optional[np.ndarray] = None,
        all_targets: Optional[np.ndarray] = None,
        fold_assignments: Optional[np.ndarray] = None
    ) -> List[Dict]:
        """
        Train regression model on extracted features.
        
        This is a two-stage process:
        1. Extract features from train/val images (or load from cache, or use pre-extracted features)
        2. Train regression model on features
        
        Args:
            train_loader: DataLoader for training images. Required if all_features is None.
            val_loader: DataLoader for validation images. Required if all_features is None.
            num_epochs: Not used (regression models don't use epochs).
            save_dir: Directory to save trained regression model.
            resume: Not used (regression models train in one pass).
            extract_features: If True, extract features from scratch. If False, try to load from cache.
            fold: Optional fold number for cross-validation (used in cache key).
            all_features: Pre-extracted features for all images (N_total, feat_dim). If provided, 
                         will split by fold instead of extracting.
            all_targets: Pre-extracted targets for all images (N_total, 3). Required if all_features provided.
            fold_assignments: Fold assignments array (N_total,). Required if all_features provided.
        
        Returns:
            Training history (single entry for regression model training).
        """
        # Extract fold number from save_dir if not provided
        if fold is None and save_dir is not None:
            # Try to extract fold from save_dir path (e.g., "fold_0", "fold_1")
            import re
            fold_match = re.search(r'fold[_\s]?(\d+)', str(save_dir), re.IGNORECASE)
            if fold_match:
                fold = int(fold_match.group(1))
        
        # Check if we're using pre-extracted features
        if all_features is not None:
            # Use pre-extracted features - split by fold
            if all_targets is None:
                raise ValueError("all_targets is required when all_features is provided")
            if fold_assignments is None:
                raise ValueError("fold_assignments is required when all_features is provided")
            if fold is None:
                raise ValueError("fold is required when using pre-extracted features")
            
            logger.info(f"Using pre-extracted features, splitting for fold {fold}...")
            train_features, val_features, train_targets, val_targets = split_features_by_fold(
                all_features, all_targets, fold_assignments, fold
            )
            logger.info(f"Split features: train {train_features.shape}, val {val_features.shape}")
        else:
            # This should not happen in normal flow - all features should be pre-extracted
            # But keep as fallback for edge cases
            raise ValueError(
                "all_features must be provided. Features should be pre-extracted before training folds. "
                "Per-fold feature extraction is no longer supported."
            )
        
        logger.info(f"Features: train {train_features.shape}, val {val_features.shape} | Targets: train {train_targets.shape}, val {val_targets.shape}")
        
        # Train regression model
        logger.info(f"Training {self.config.model.regression_model_type} regression model on extracted features...")
        self.regression_model.fit(train_features, train_targets)
        
        # Evaluate on validation set
        val_predictions = self.regression_model.predict(val_features)
        weighted_r2, r2_scores = calc_metric(val_predictions, val_targets)
        val_score = weighted_r2
        
        logger.info(f"✅ Regression model training complete")
        logger.info(f"📊 Validation Score: {val_score:.4f}")
        
        # Update best score BEFORE saving (so metadata has correct score)
        self.best_score = val_score
        self.best_epoch = 0  # Regression models don't have epochs
        
        # Save model if save_dir provided
        if save_dir:
            ensure_dir(save_dir)
            self._save_model(save_dir)
        
        # Create history entry
        history_entry = {
            'epoch': 0,
            'train_loss': None,  # Regression models don't use loss in same way
            'val_loss': None,
            'val_score': val_score
        }
        self.history = [history_entry]
        
        return self.history
    
    def _extract_targets(self, dataloader: DataLoader) -> np.ndarray:
        """
        Extract targets from dataloader.
        
        Args:
            dataloader: DataLoader with targets.
        
        Returns:
            Targets array of shape (N, 3) for primary targets.
        """
        all_targets = []
        
        for batch in dataloader:
            if self.dataset_type == 'split':
                _, _, targets = batch
            else:
                _, targets = batch
            
            all_targets.append(targets.numpy())
        
        targets_array = np.concatenate(all_targets, axis=0)
        return targets_array
    
    def _save_model(self, save_dir: Path) -> None:
        """
        Save trained regression model and metadata.
        
        Args:
            save_dir: Directory to save model to.
        """
        import pickle
        import json
        
        # Save regression model
        model_path = save_dir / 'regression_model.pkl'
        with open(model_path, 'wb') as f:
            pickle.dump(self.regression_model, f)
        
        logger.info(f"Saved regression model to {model_path}")
        
        # Save metadata file (similar to checkpoint info for export pipeline)
        metadata_path = save_dir / 'regression_model_info.json'
        metadata = {
            'best_score': float(self.best_score),  # Ensure it's a float, not numpy type
            'val_score': float(self.best_score),
            'history': self.history,
            'epoch': 0,  # Regression models don't have epochs
            'exists': True,
            'model_type': 'regression',
            'regression_model_type': self.config.model.regression_model_type
        }
        try:
            # Ensure directory exists
            ensure_dir(save_dir)
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
                f.flush()  # Ensure data is written to disk
                os.fsync(f.fileno())  # Force write to disk
            logger.info(f"Saved regression model metadata to {metadata_path}")
        except Exception as e:
            logger.error(f"Failed to save regression model metadata to {metadata_path}: {e}")
            raise
    
    def create_dataloaders(
        self,
        train_data: pd.DataFrame,
        val_data: pd.DataFrame,
        data_root: str,
        train_transform: Optional[Callable] = None,
        val_transform: Optional[Callable] = None,
        dataset_type: Optional[str] = None
    ) -> Tuple[DataLoader, DataLoader, Tuple[object, object]]:
        """
        Create data loaders for feature extraction.
        
        Delegates to shared dataloader factory.
        """
        return _create_dataloaders(
            train_data=train_data,
            val_data=val_data,
            data_root=data_root,
            config=self.config,
            train_transform=train_transform,
            val_transform=val_transform,
            dataset_type=dataset_type
        )

