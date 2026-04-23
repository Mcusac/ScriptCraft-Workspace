# trainer_factory.py
# Factory for creating appropriate trainer based on config mode
# Routes to BaseModelTrainer (end-to-end) or FeatureExtractionTrainer (two-stage)

import torch
from typing import Union, Optional, Dict, Any
import logging

from config.config import Config
from .base_model_trainer import BaseModelTrainer
from .feature_extraction_trainer import FeatureExtractionTrainer

logger = logging.getLogger(__name__)


def create_trainer(
    config: Config,
    device: torch.device,
    model: Optional[torch.nn.Module] = None,
    regression_model_hyperparameters: Optional[Dict[str, Any]] = None,
    regression_only: bool = False
) -> Union[BaseModelTrainer, FeatureExtractionTrainer]:
    """
    Create appropriate trainer based on config mode.
    
    If config.model.feature_extraction_mode is True, creates FeatureExtractionTrainer.
    Otherwise, creates BaseModelTrainer for end-to-end training.
    
    Args:
        config: Configuration object with model settings.
        device: Device to train on.
        model: Optional model instance (only used for end-to-end mode).
        regression_model_hyperparameters: Optional hyperparameters for regression model
                                        (only used for feature extraction mode).
        regression_only: If True and in feature extraction mode, creates a lightweight trainer
                        that only has the regression model (skips feature extraction model creation).
                        Used when features are already extracted and we only need to train regression heads.
    
    Returns:
        BaseModelTrainer or FeatureExtractionTrainer instance.
    """
    if config.model.feature_extraction_mode:
        if regression_only:
            logger.info("Creating FeatureExtractionTrainer (regression-only mode: features already extracted)")
        else:
            logger.info("Creating FeatureExtractionTrainer (two-stage: feature extraction + regression)")
        return FeatureExtractionTrainer(
            config, 
            device, 
            feature_extraction_model=None,
            regression_model_hyperparameters=regression_model_hyperparameters,
            regression_only=regression_only
        )
    else:
        logger.info("Creating BaseModelTrainer (end-to-end training)")
        return BaseModelTrainer(config, device, model=model)

