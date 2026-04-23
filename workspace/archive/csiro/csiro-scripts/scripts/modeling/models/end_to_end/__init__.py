# end_to_end package
# End-to-end model architectures with built-in regression heads
#
# This package contains complete model architectures that include both feature extraction
# backbones and regression heads. These models are used for end-to-end training where
# the entire model (backbone + head) is trained together.
#
# Components:
# - base: Base class for end-to-end models (BaseFeatureExtractionModel)
# - timm_model: Wrapper for timm models (EfficientNet, etc.) with regression head.
#   Handles pretrained weight loading with fallback to non-pretrained models
#   when network access is unavailable. Supports weight caching for offline use.
# - dinov2_model: DINOv2 model wrapper with feature fusion support and regression head.
# - weight_loader: Pretrained weight loading utilities for timm models.
# - create_model: Factory function for creating end-to-end model instances from configuration.
#
# The model wrappers provide a unified interface for different architectures
# while allowing custom output dimensions for regression tasks.

import logging
from typing import Union, TYPE_CHECKING, Dict, Callable

from .base import BaseFeatureExtractionModel
from .timm_model import TimmModel
from .dinov2_model import DINOv2Model

if TYPE_CHECKING:
    from config import Config

logger = logging.getLogger(__name__)


def _is_regression_model_type(model_name: str) -> bool:
    """
    Check if a model name is actually a regression model type, not a feature extraction model.
    
    Args:
        model_name: Model name to check
        
    Returns:
        True if model_name is a regression model type (lgbm, xgboost, ridge), False otherwise
    """
    regression_types = {'lgbm', 'xgboost', 'xgb', 'ridge'}
    return model_name.lower() in regression_types


def detect_model_type(config: 'Config') -> str:
    """
    Detect model type from configuration or model name.
    
    Automatically detects model type from config.model.model_type or model name.
    Supports both timm and DINOv2 architectures.
    
    Args:
        config: Configuration object with model settings
        
    Returns:
        Model type string: 'dinov2' or 'timm'
    """
    # Get explicit model_type from config
    model_type = getattr(config.model, 'model_type', None)
    
    # Auto-detect from model name if model_type not explicitly set
    if model_type is None or model_type == 'auto':
        model_name_lower = config.model.name.lower()
        if 'dinov2' in model_name_lower or 'dinov3' in model_name_lower:
            model_type = 'dinov2'
            logger.info(f"Auto-detected DINOv2 model type from name: {config.model.name}")
        elif '/' in config.model.name or config.model.name.startswith('/'):
            # Path-like model name (e.g., '/kaggle/input/dinov2/pytorch/base/1') - likely DINOv2
            # Check if it contains dinov2 in the path
            if 'dinov2' in model_name_lower or 'dinov3' in model_name_lower:
                model_type = 'dinov2'
                logger.info(f"Auto-detected DINOv2 model type from path: {config.model.name}")
            else:
                # Path but not clearly DINOv2 - default to timm but warn
                model_type = 'timm'
                logger.warning(
                    f"Path-like model name detected but not clearly DINOv2: {config.model.name}. "
                    f"Defaulting to timm model type. If this is incorrect, set model_type explicitly."
                )
        else:
            # Default to timm for other model names
            model_type = 'timm'
            logger.info(f"Auto-detected timm model type from name: {config.model.name}")
    
    return model_type


def _create_dinov2_model(config: 'Config') -> DINOv2Model:
    """
    Create DINOv2 model instance from configuration.
    
    Args:
        config: Configuration object with model settings
        
    Returns:
        DINOv2Model instance
    """
    return DINOv2Model(
        model_name=config.model.name,
        pretrained=config.model.pretrained,
        num_classes=config.model.num_classes,
        input_size=config.model.input_size,
        use_tiles=getattr(config.model, 'use_tiles', False),
        tile_grid_size=getattr(config.model, 'tile_grid_size', 2)
    )


def _create_timm_model(config: 'Config') -> TimmModel:
    """
    Create TimmModel instance from configuration.
    
    Args:
        config: Configuration object with model settings
        
    Returns:
        TimmModel instance
    """
    return TimmModel(
        model_name=config.model.name,
        pretrained=config.model.pretrained,
        num_classes=config.model.num_classes,
        input_size=config.model.input_size
    )


MODEL_FACTORIES: Dict[str, Callable[['Config'], Union[TimmModel, DINOv2Model]]] = {
    'dinov2': _create_dinov2_model,
    'timm': _create_timm_model
}


def create_model(config: 'Config') -> Union[TimmModel, DINOv2Model]:
    """
    Create model instance based on configuration.
    
    Automatically detects model type from config.model.model_type or model name.
    Supports both EfficientNet (timm) and DINOv2 architectures.
    
    Args:
        config: Configuration object with model settings
        
    Returns:
        TimmModel or DINOv2Model instance depending on configuration
        
    Raises:
        ValueError: If model name is a regression model type (lgbm, xgboost, ridge)
        
    Side effects:
        Updates config.model.input_size and config.data.image_size with model's input size
    """
    # Validate that model name is not a regression model type
    if _is_regression_model_type(config.model.name):
        raise ValueError(
            f"Invalid model name '{config.model.name}': This is a regression model type, "
            f"not a feature extraction model. "
            f"Regression models (lgbm, xgboost, ridge) cannot be used as feature extraction models. "
            f"Please provide a valid feature extraction model name (e.g., 'dinov2', 'efficientnet_b3')."
        )
    
    # Detect model type from config or model name
    model_type = detect_model_type(config)
    
    # Create model using factory registry
    factory = MODEL_FACTORIES.get(model_type)
    if factory is None:
        raise ValueError(
            f"Unknown model type '{model_type}'. "
            f"Valid types are: {list(MODEL_FACTORIES.keys())}"
        )
    model = factory(config)
    
    # Update config with model input size
    input_size = model.get_input_size()
    config.model.input_size = input_size
    config.data.image_size = input_size
    
    # Set default preprocessing for DINOv2 models (CenterCrop)
    # Note: Resize is always applied automatically when image_size is set
    if model_type == 'dinov2':
        if 'center_crop' not in (config.data.preprocessing_list or []):
            # Initialize preprocessing_list if None
            if config.data.preprocessing_list is None:
                config.data.preprocessing_list = []
            # Add center_crop (resize is applied automatically)
            config.data.preprocessing_list.append('center_crop')
            logger.info("Added 'center_crop' to preprocessing_list for DINOv2 (resize is applied automatically)")
    
    logger.info(f"Created {model_type} model: {config.model.name} (input size: {input_size})")
    
    return model


__all__ = [
    'BaseFeatureExtractionModel',
    'TimmModel',
    'DINOv2Model',
    'create_model',
    '_is_regression_model_type'
]

