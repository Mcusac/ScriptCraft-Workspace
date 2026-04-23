# saver.py
# Checkpoint saving utilities

import torch
import torch.nn as nn
import torch.optim as optim
import logging
from pathlib import Path
from typing import Optional, Dict, List, Any

logger = logging.getLogger(__name__)


def save_checkpoint(
    model: nn.Module,
    optimizer: optim.Optimizer,
    scheduler: Optional[optim.lr_scheduler._LRScheduler],
    path: Path,
    epoch: int,
    best_score: float,
    history: List[Dict[str, Any]]
) -> None:
    """
    Save a training checkpoint.
    
    Handles DataParallel models by saving the underlying model state (without 'module.' prefix).
    This makes checkpoints compatible with both DataParallel and non-parallel models.
    
    Args:
        model: PyTorch model (may be wrapped in DataParallel)
        optimizer: Optimizer state
        scheduler: Optional scheduler state
        path: Path to save checkpoint
        epoch: Current epoch number
        best_score: Best score achieved so far
        history: Training history
    """
    # Handle DataParallel - save underlying model state (without 'module.' prefix)
    if isinstance(model, nn.DataParallel):
        model_state_dict = model.module.state_dict()
    else:
        model_state_dict = model.state_dict()
    
    checkpoint = {
        'epoch': epoch,
        'model_state_dict': model_state_dict,
        'optimizer_state_dict': optimizer.state_dict(),
        'best_score': best_score,
        'history': history
    }
    
    if scheduler is not None:
        checkpoint['scheduler_state_dict'] = scheduler.state_dict()
    
    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)
    
    torch.save(checkpoint, path)
    logger.debug(f"Saved checkpoint to {path}")
