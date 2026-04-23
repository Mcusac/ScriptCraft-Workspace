# loader.py
# Checkpoint loading utilities

import torch
import torch.nn as nn
import torch.optim as optim
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from collections import OrderedDict

logger = logging.getLogger(__name__)


def _load_model_state_dict(
    model: nn.Module,
    state_dict: Dict[str, Any]
) -> None:
    """
    Load model state dict, handling DataParallel wrapping/unwrapping.
    
    This helper function handles the complexity of loading state dicts when
    models may or may not be wrapped in DataParallel, ensuring compatibility
    regardless of how the checkpoint was saved.
    
    Args:
        model: PyTorch model (may be wrapped in DataParallel)
        state_dict: State dict to load into model
    """
    is_model_parallel = isinstance(model, nn.DataParallel)
    
    if is_model_parallel:
        # If model is wrapped, state_dict keys may have 'module.' prefix
        if any(key.startswith('module.') for key in state_dict.keys()):
            # State dict already has 'module.' prefix, load directly
            model.load_state_dict(state_dict)
        else:
            # Need to add 'module.' prefix for DataParallel
            new_state_dict = OrderedDict()
            for k, v in state_dict.items():
                name = 'module.' + k if not k.startswith('module.') else k
                new_state_dict[name] = v
            model.load_state_dict(new_state_dict)
    else:
        # Remove 'module.' prefix if present (loading non-parallel model from parallel checkpoint)
        if any(key.startswith('module.') for key in state_dict.keys()):
            new_state_dict = OrderedDict()
            for k, v in state_dict.items():
                name = k[7:] if k.startswith('module.') else k
                new_state_dict[name] = v
            model.load_state_dict(new_state_dict)
        else:
            model.load_state_dict(state_dict)


def load_model_from_checkpoint(
    model: nn.Module,
    path: Path,
    device: torch.device
) -> Dict[str, Any]:
    """
    Load only the model state from a checkpoint (for inference).
    
    This is a simplified version of load_checkpoint that doesn't require
    optimizer or scheduler, making it suitable for inference-only scenarios.
    
    This function is typically called by higher-level orchestrators (e.g., ensembling/model_loader)
    after they have:
    1. Found the checkpoint path (using model_finder_utils)
    2. Created the model instance (using modeling.models.create_model)
    
    Responsibility: Low-level checkpoint I/O - loads PyTorch state dict from file.
    
    Args:
        model: PyTorch model to load state into
        path: Path to checkpoint file
        device: Device to load checkpoint on
        
    Returns:
        Dictionary with checkpoint metadata:
        - 'epoch': Epoch number when checkpoint was saved
        - 'best_score': Best score from checkpoint
        - 'history': Training history
        - 'completed_epochs': Number of completed epochs (from history length)
    """
    # weights_only=False is safe here since we trust our own checkpoints
    checkpoint = torch.load(path, map_location=device, weights_only=False)
    
    # Load model state dict using shared helper
    _load_model_state_dict(model, checkpoint['model_state_dict'])
    
    # Extract metadata
    best_score = checkpoint.get('best_score', -float('inf'))
    history = checkpoint.get('history', [])
    epoch = checkpoint.get('epoch', 0)
    completed_epochs = len(history)
    
    logger.info(f"Loaded model from checkpoint: {path}")
    logger.info(f"  Epoch: {epoch}")
    logger.info(f"  Completed epochs: {completed_epochs}")
    logger.info(f"  Best score: {best_score:.4f}")
    
    return {
        'epoch': epoch,
        'best_score': best_score,
        'history': history,
        'completed_epochs': completed_epochs
    }


def load_checkpoint(
    model: nn.Module,
    optimizer: optim.Optimizer,
    scheduler: Optional[optim.lr_scheduler._LRScheduler],
    path: Path,
    device: torch.device
) -> Dict[str, Any]:
    """
    Load a training checkpoint.
    
    Handles DataParallel model wrapping/unwrapping automatically.
    Returns checkpoint metadata for easy access.
    
    Args:
        model: PyTorch model (may be wrapped in DataParallel)
        optimizer: Optimizer to load state into
        scheduler: Optional scheduler to load state into
        path: Path to checkpoint file
        device: Device to load checkpoint on
        
    Returns:
        Dictionary with checkpoint metadata:
        - 'epoch': Epoch number when checkpoint was saved
        - 'best_score': Best score from checkpoint
        - 'history': Training history
        - 'completed_epochs': Number of completed epochs (from history length)
    """
    # weights_only=False is safe here since we trust our own checkpoints
    checkpoint = torch.load(path, map_location=device, weights_only=False)
    
    # Load model state dict using shared helper
    _load_model_state_dict(model, checkpoint['model_state_dict'])
    
    # Load optimizer and scheduler states
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    if 'scheduler_state_dict' in checkpoint and scheduler is not None:
        scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
    
    # Extract metadata
    best_score = checkpoint.get('best_score', -float('inf'))
    history = checkpoint.get('history', [])
    epoch = checkpoint.get('epoch', 0)
    completed_epochs = len(history)
    
    logger.info(f"Loaded checkpoint from {path}")
    logger.info(f"  Epoch: {epoch}")
    logger.info(f"  Completed epochs: {completed_epochs}")
    logger.info(f"  Best score: {best_score:.4f}")
    
    return {
        'epoch': epoch,
        'best_score': best_score,
        'history': history,
        'completed_epochs': completed_epochs
    }
