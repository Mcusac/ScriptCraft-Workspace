# training_components_factory.py
# Factory functions for creating optimizers and schedulers
# Extracted from BaseModelTrainer to improve modularity

import torch
import torch.optim as optim
import logging
from typing import Optional

from config.config import Config

logger = logging.getLogger(__name__)


def create_optimizer(
    model: torch.nn.Module,
    config: Config
) -> optim.Optimizer:
    """
    Create optimizer from config.
    
    Args:
        model: PyTorch model whose parameters will be optimized.
        config: Configuration object with training settings.
               Must have config.training.optimizer, learning_rate, and weight_decay.
        
    Returns:
        Optimizer instance ready for training.
        
    Raises:
        ValueError: If optimizer type is unknown or config is invalid.
    """
    if config.training.optimizer == 'AdamW':
        optimizer = optim.AdamW(
            model.parameters(),
            lr=config.training.learning_rate,
            weight_decay=config.training.weight_decay
        )
    elif config.training.optimizer == 'Adam':
        optimizer = optim.Adam(
            model.parameters(),
            lr=config.training.learning_rate,
            weight_decay=config.training.weight_decay
        )
    elif config.training.optimizer == 'SGD':
        optimizer = optim.SGD(
            model.parameters(),
            lr=config.training.learning_rate,
            weight_decay=config.training.weight_decay,
            momentum=0.9  # Default momentum
        )
    else:
        raise ValueError(f"Unknown optimizer: {config.training.optimizer}")
    
    logger.info(f"Created optimizer: {config.training.optimizer}")
    logger.info(f"  Learning rate: {config.training.learning_rate}")
    logger.info(f"  Weight decay: {config.training.weight_decay}")
    
    return optimizer


def create_scheduler(
    optimizer: optim.Optimizer,
    config: Config
) -> Optional[optim.lr_scheduler._LRScheduler]:
    """
    Create learning rate scheduler from config.
    
    Args:
        optimizer: Optimizer instance to schedule.
        config: Configuration object with training settings.
               Must have config.training.scheduler and related scheduler settings.
        
    Returns:
        Scheduler instance or None if no scheduler configured.
    """
    if config.training.scheduler == 'ReduceLROnPlateau':
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            optimizer,
            mode=config.training.scheduler_mode,
            factor=config.training.scheduler_factor,
            patience=config.training.scheduler_patience,
            verbose=False
        )
        logger.info(f"Created scheduler: {config.training.scheduler}")
        logger.info(f"  Mode: {config.training.scheduler_mode}")
        logger.info(f"  Factor: {config.training.scheduler_factor}")
        logger.info(f"  Patience: {config.training.scheduler_patience}")
    elif config.training.scheduler == 'CosineAnnealingLR':
        scheduler = optim.lr_scheduler.CosineAnnealingLR(
            optimizer,
            T_max=config.training.num_epochs
        )
        logger.info(f"Created scheduler: {config.training.scheduler}")
    else:
        scheduler = None
        logger.info("No scheduler configured")
    
    return scheduler

