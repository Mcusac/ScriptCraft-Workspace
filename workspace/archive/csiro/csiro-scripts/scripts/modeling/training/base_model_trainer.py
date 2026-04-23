# base_model_trainer.py
# Base model trainer with training and validation loops

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from typing import Dict, List, Optional, Tuple, Callable
import numpy as np
import pandas as pd
import logging
from pathlib import Path

from modeling.evaluation.metrics import calc_metric
from modeling.evaluation.losses import get_loss_function
from utils.system import ensure_dir
from modeling.training.utils.checkpoint import save_checkpoint as save_checkpoint_util, load_checkpoint as load_checkpoint_util
from utils.system import setup_multi_gpu
from utils.system import ProgressTracker
from modeling.models import create_model
from config.config import Config
from utils.config.config_validator import validate_config_section
from .training_components_factory import create_optimizer, create_scheduler
from .dataloader_factory import create_dataloaders

logger = logging.getLogger(__name__)


class BaseModelTrainer:
    """
    Base trainer class with training and validation loops.
    
    Handles model training with early stopping, checkpoint saving/resuming,
    learning rate scheduling, and metric calculation. Supports both single
    and multi-GPU training via DataParallel.
    """
    
    def __init__(
        self,
        config: Config,
        device: torch.device,
        model: Optional[nn.Module] = None
    ):
        """
        Initialize BaseModelTrainer.
        
        Args:
            config: Configuration object containing training, model, and data settings.
                   Must have training, model, device, and data attributes.
            device: Device to train on (e.g., torch.device('cuda') or torch.device('cpu')).
            model: Optional model instance. If None, creates model using factory from config.
        
        Raises:
            ValueError: If config is None or missing required attributes.
            TypeError: If device is not a torch.device.
        """
        # Validate config
        if config is None:
            raise ValueError("config cannot be None")
        
        validate_config_section(config, 'training')
        validate_config_section(config, 'model')
        validate_config_section(config, 'device')
        
        # Validate device
        if not isinstance(device, torch.device):
            raise TypeError(f"device must be torch.device, got {type(device)}")
        
        self.config = config
        self.device = device
        
        # Set up model
        self.model = self._setup_model(device, model)
        
        # Loss function
        self.criterion = get_loss_function(
            config.training.loss_function,
            reduction='mean'
        )
        
        # Create optimizer
        self.optimizer = create_optimizer(self.model, self.config)
        
        # Create scheduler
        self.scheduler = create_scheduler(self.optimizer, self.config)
        
        # Mixed precision training
        # Auto-enable for transformer models (DINOv2) if not explicitly set
        use_mixed_precision = getattr(config.training, 'use_mixed_precision', False)
        if not use_mixed_precision:
            # Auto-detect transformer models and enable mixed precision
            model_name_lower = config.model.name.lower()
            if 'dinov2' in model_name_lower or 'dinov3' in model_name_lower:
                use_mixed_precision = True
                config.training.use_mixed_precision = True
                logger.info("✅ Auto-enabled mixed precision (FP16) for transformer model")
        
        self.use_mixed_precision = use_mixed_precision
        self.scaler = None
        if self.use_mixed_precision:
            from torch.amp import GradScaler
            self.scaler = GradScaler('cuda')
            logger.info("✅ Mixed precision (FP16) training enabled")
        
        # Training history
        self.history: List[Dict] = []
        self.best_score = -float('inf')
        self.best_epoch = 0
        
        # Dataset type for handling different output formats
        self.dataset_type = getattr(config.data, 'dataset_type', 'split')
    
    def _process_batch_train(self, batch, is_training: bool = True) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Process a single batch for training or validation.
        
        Supports both full image and split dataset formats.
        
        Args:
            batch: Batch from DataLoader - either (images, targets) for 'full' dataset,
                   or (left_img, right_img, targets) for 'split' dataset
            is_training: If True, model is in train mode and gradients are computed
        
        Returns:
            Tuple of (outputs, targets, loss)
        """
        from modeling.utils import process_batch_for_model, extract_batch_data
        
        # Extract batch data and move to device
        _, targets = extract_batch_data(batch, self.dataset_type, self.device)
        
        # Process batch through model
        outputs = process_batch_for_model(batch, self.model, self.device, self.dataset_type)
        
        # Calculate loss
        loss = self.criterion(outputs, targets)
        
        return outputs, targets, loss
    
    def train_epoch(self, train_loader: DataLoader) -> float:
        """
        Train for one epoch.
        
        Args:
            train_loader: Training data loader. Must yield (images, targets) tuples for 'full' dataset,
                         or (left_img, right_img, targets) tuples for 'split' dataset.
                         Images should be tensors of shape (B, C, H, W).
                         Targets should be tensors of shape (B, 3).
        
        Returns:
            Average training loss for the epoch (float).
        
        Raises:
            ValueError: If train_loader is empty.
            RuntimeError: If training fails (e.g., OOM, NaN loss).
        """
        if len(train_loader) == 0:
            raise ValueError("train_loader cannot be empty")
        
        self.model.train()
        total_loss = 0.0
        num_batches = 0
        
        for batch in train_loader:
            # Process batch (handles both dataset types)
            # Use mixed precision autocast if enabled
            if self.use_mixed_precision:
                from torch.amp import autocast
                with autocast('cuda'):
                    outputs, targets, loss = self._process_batch_train(batch, is_training=True)
            else:
                outputs, targets, loss = self._process_batch_train(batch, is_training=True)
            
            # Check for NaN loss
            if torch.isnan(loss):
                raise RuntimeError("NaN loss detected during training")
            
            # Backward pass with scaler if using mixed precision
            self.optimizer.zero_grad()
            if self.scaler:
                self.scaler.scale(loss).backward()
                self.scaler.step(self.optimizer)
                self.scaler.update()
            else:
                loss.backward()
                self.optimizer.step()
            
            total_loss += loss.item()
            num_batches += 1
        
        if num_batches == 0:
            raise ValueError("No batches processed in train_epoch")
        
        return total_loss / num_batches
    
    def validate(
        self,
        val_loader: DataLoader
    ) -> Tuple[float, float, np.ndarray]:
        """
        Validate model on validation set.
        
        Args:
            val_loader: Validation data loader. Must yield (images, targets) tuples for 'full' dataset,
                       or (left_img, right_img, targets) tuples for 'split' dataset.
                       Images should be tensors of shape (B, C, H, W).
                       Targets should be tensors of shape (B, 3).
        
        Returns:
            Tuple of (val_loss, weighted_r2, r2_scores_per_target):
            - val_loss: Average validation loss (float)
            - weighted_r2: Weighted R² score (float)
            - r2_scores_per_target: R² score for each target (np.ndarray, shape (5,))
        
        Raises:
            ValueError: If val_loader is empty.
            RuntimeError: If validation fails.
        """
        if len(val_loader) == 0:
            raise ValueError("val_loader cannot be empty")
        
        self.model.eval()
        total_loss = 0.0
        all_outputs: List[np.ndarray] = []
        all_targets: List[np.ndarray] = []
        num_batches = 0
        
        with torch.no_grad():
            for batch in val_loader:
                # Process batch (handles both dataset types)
                outputs, targets, loss = self._process_batch_train(batch, is_training=False)
                
                # Check for NaN loss
                if torch.isnan(loss):
                    logger.warning("NaN loss detected during validation")
                
                total_loss += loss.item()
                num_batches += 1
                
                all_outputs.append(outputs.detach().cpu().numpy())
                all_targets.append(targets.detach().cpu().numpy())
        
        if num_batches == 0:
            raise ValueError("No batches processed in validate")
        
        # Concatenate all predictions and targets
        outputs = np.concatenate(all_outputs, axis=0)
        targets = np.concatenate(all_targets, axis=0)
        
        # Calculate metrics
        weighted_r2, r2_scores = calc_metric(outputs, targets)
        val_loss = total_loss / num_batches
        
        return val_loss, weighted_r2, r2_scores
    
    def train(
        self,
        train_loader: DataLoader,
        val_loader: DataLoader,
        num_epochs: Optional[int] = None,
        save_dir: Optional[Path] = None,
        resume: bool = True
    ) -> List[Dict]:
        """
        Train model with early stopping.
        
        Args:
            train_loader: Training data loader
            val_loader: Validation data loader
            num_epochs: Number of epochs (default: from config)
            save_dir: Directory to save checkpoints
            resume: If True, resume from existing checkpoint if available
            
        Returns:
            Training history
        """
        if num_epochs is None:
            num_epochs = self.config.training.num_epochs
        
        if save_dir:
            ensure_dir(save_dir)
        
        # Check for existing checkpoint to resume
        start_epoch = 0
        checkpoint_path = None
        if resume and save_dir:
            checkpoint_path = save_dir / 'best_model.pth'
            if checkpoint_path.exists():
                logger.info(f"✅ Found existing checkpoint at {checkpoint_path}")
                logger.info("🔄 Resuming training from checkpoint...")
                try:
                    checkpoint_meta = load_checkpoint_util(
                        self.model,
                        self.optimizer,
                        self.scheduler,
                        checkpoint_path,
                        self.device
                    )
                    # Update trainer state from checkpoint
                    self.best_score = checkpoint_meta['best_score']
                    self.history = checkpoint_meta['history']
                    start_epoch = checkpoint_meta['completed_epochs']  # Resume from next epoch
                    logger.info(f"📊 Resuming from epoch {start_epoch}/{num_epochs}")
                    logger.info(f"🏆 Best score so far: {self.best_score:.4f}")
                except (RuntimeError, EOFError, OSError) as e:
                    # Handle corrupted checkpoint files gracefully
                    logger.warning(f"⚠️  Failed to load checkpoint from {checkpoint_path}: {e}")
                    logger.warning("   Checkpoint appears corrupted. Starting fresh training...")
                    # Delete corrupted checkpoint to prevent retry
                    try:
                        checkpoint_path.unlink()
                        logger.info(f"   Deleted corrupted checkpoint: {checkpoint_path}")
                    except Exception as cleanup_error:
                        logger.warning(f"   Could not delete corrupted checkpoint: {cleanup_error}")
                    # Reset to fresh training
                    self.best_score = -float('inf')
                    self.history = []
                    start_epoch = 0
                    logger.info("🆕 Starting fresh training (checkpoint was corrupted)")
            else:
                logger.info("🆕 No existing checkpoint found - starting fresh training")
        
        patience = self.config.training.early_stopping_patience
        epochs_without_improvement = 0
        
        # If resuming, calculate epochs without improvement from history
        if start_epoch > 0 and len(self.history) > 1:
            # Find last improvement in history
            best_epoch_in_history = max(range(len(self.history)), 
                                       key=lambda i: self.history[i].get('weighted_r2', -float('inf')))
            epochs_without_improvement = len(self.history) - 1 - best_epoch_in_history
        
        logger.info(f"Starting training for {num_epochs} epochs (starting from epoch {start_epoch})")
        
        # Initialize progress tracker for epoch-level progress
        progress_tracker = ProgressTracker(self.config.progress)
        epoch_bar_id = None
        if self.config.progress.show_epoch_progress:
            epoch_bar_id = progress_tracker.create_bar(
                bar_id="training_epochs",
                total=num_epochs,
                desc="Training",
                level=2,  # Nested under grid search if applicable
                unit="epoch",
                initial=start_epoch
            )
        
        try:
            for epoch in range(start_epoch, num_epochs):
                # Train
                train_loss = self.train_epoch(train_loader)
                
                # Validate
                val_loss, weighted_r2, r2_scores = self.validate(val_loader)
                
                # Update scheduler
                if self.scheduler:
                    if self.config.training.scheduler_mode == 'max':
                        self.scheduler.step(weighted_r2)
                    else:
                        self.scheduler.step(val_loss)
                
                # Log progress
                current_lr = self.optimizer.param_groups[0]['lr']
                if epoch % 10 == 0 or epoch == num_epochs - 1:
                    logger.info(
                        f"Epoch [{epoch}/{num_epochs}]: "
                        f"Train Loss: {train_loss:.4f}, "
                        f"Val Loss: {val_loss:.4f}, "
                        f"Weighted R²: {weighted_r2:.4f}, "
                        f"LR: {current_lr:.6f}"
                    )
                
                # Update progress bar
                if epoch_bar_id:
                    progress_tracker.update(
                        epoch_bar_id,
                        n=1,
                        loss=f"{val_loss:.4f}",
                        R2=f"{weighted_r2:.4f}",
                        lr=f"{current_lr:.6f}"
                    )
                
                # Save history
                history_entry = {
                    'epoch': epoch,
                    'train_loss': train_loss,
                    'val_loss': val_loss,
                    'weighted_r2': weighted_r2,
                    'r2_scores': r2_scores.tolist(),
                    'lr': current_lr
                }
                self.history.append(history_entry)
                
                # Check for improvement
                if weighted_r2 > self.best_score:
                    self.best_score = weighted_r2
                    self.best_epoch = epoch
                    epochs_without_improvement = 0
                    
                    # Save best model
                    if save_dir:
                        checkpoint_path = save_dir / 'best_model.pth'
                        save_checkpoint_util(
                            model=self.model,
                            optimizer=self.optimizer,
                            scheduler=self.scheduler,
                            path=checkpoint_path,
                            epoch=epoch,
                            best_score=self.best_score,
                            history=self.history
                        )
                        logger.info(f"Saved best model (R²={weighted_r2:.4f}) to {checkpoint_path}")
                else:
                    epochs_without_improvement += 1
                
                # Early stopping
                if epochs_without_improvement >= patience:
                    logger.info(f"Early stopping: {patience} epochs without improvement")
                    break
        finally:
            # Ensure progress bars are always closed, even on exception
            # This prevents state leakage between training sessions
            if epoch_bar_id:
                progress_tracker.close(epoch_bar_id)
            # Close all progress bars to ensure complete cleanup
            progress_tracker.close_all()
        
        logger.info(f"Training completed. Best weighted R²: {self.best_score:.4f} at epoch {self.best_epoch}")
        
        return self.history
    
    def _setup_model(
        self,
        device: torch.device,
        model: Optional[nn.Module] = None
    ) -> nn.Module:
        """
        Set up model for training: create (if needed), move to device, wrap in DataParallel if needed.
        
        Args:
            device: Device to place model on
            model: Optional existing model instance. If None, creates model using config.
            
        Returns:
            Model ready for training (on device, possibly wrapped in DataParallel)
        """
        # Create or use provided model
        if model is None:
            model = create_model(self.config)
        
        # Move to device
        model = model.to(device)
        
        # Set up multi-GPU if enabled and available
        if (self.config.device.use_multi_gpu and 
            device.type == 'cuda' and 
            torch.cuda.device_count() > 1):
            model = setup_multi_gpu(model)
            logger.info(f"Model wrapped in DataParallel for {torch.cuda.device_count()} GPUs")
        
        logger.info(f"Model setup complete: {self.config.model.name}")
        logger.info(f"Input size: {self.config.data.image_size}")
        
        return model
    
    def create_dataloaders(
        self,
        train_data: pd.DataFrame,
        val_data: pd.DataFrame,
        data_root: str,
        train_transform: Optional[Callable] = None,
        val_transform: Optional[Callable] = None
    ) -> Tuple[DataLoader, DataLoader, Tuple[object, object]]:
        """
        Create training and validation data loaders.
        
        Uses StreamingBiomassDataset for memory-efficient on-demand image loading.
        
        Args:
            train_data: Training DataFrame. Must have 'image_path' column and target columns.
            val_data: Validation DataFrame. Must have 'image_path' column and target columns.
            data_root: Root directory for images (string path).
            train_transform: Optional transform for training (if None, will be built from config).
            val_transform: Optional transform for validation (if None, will be built from config).
        
        Returns:
            Tuple of (train_loader, val_loader, (train_dataset, val_dataset)) DataLoader instances and datasets.
            Datasets are returned for proper cleanup after training.
        
        Raises:
            ValueError: If train_data or val_data are empty or invalid.
            TypeError: If train_data or val_data are not DataFrames.
        """
        return create_dataloaders(
            train_data=train_data,
            val_data=val_data,
            data_root=data_root,
            config=self.config,
            train_transform=train_transform,
            val_transform=val_transform
        )
