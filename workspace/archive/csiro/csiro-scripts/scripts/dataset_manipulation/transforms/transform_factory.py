# transform_factory.py
# Factory for creating transform pipelines based on config
# Separates transform composition from training logic

import logging
from typing import List

import torchvision.transforms as transforms

from config.config import Config
from utils.config.config_validator import validate_config_section
from .transform_composition import (
    build_preprocessing_transforms,
    build_augmentation_transforms,
    build_tensor_transforms,
    compose_transform_pipeline
)
from .tta_builders import build_tta_transforms as _build_tta_transforms

logger = logging.getLogger(__name__)


def _build_base_transform(config: Config, include_augmentation: bool = False) -> transforms.Compose:
    """
    Build base transform pipeline from config (shared by train and val).
    
    Transform order:
    1. PIL Image transforms (preprocessing + augmentation if training)
    2. ToTensor (converts PIL Image to tensor)
    3. Tensor transforms (tensor augmentation if training + normalization)
    
    Note: Essential preprocessing operations are always applied automatically:
    - Resize is applied automatically if image_size is set (before optional preprocessing)
    - Normalization is always applied automatically after ToTensor
    
    Args:
        config: Configuration object with preprocessing_list and augmentation_list.
                Must have config.data attribute with preprocessing_list, augmentation_list,
                image_size, imagenet_mean, and imagenet_std.
        include_augmentation: Whether to include augmentation transforms (default: False).
                             Should be True for training, False for validation.
        
    Returns:
        Composed transform pipeline ready for use in DataLoader.
        
    Raises:
        AttributeError: If config is missing required attributes.
        ValueError: If config.data is None or invalid.
    """
    # Validate config
    validate_config_section(config, 'data')
    
    # Get preprocessing list (only optional preprocessing, essential operations are applied automatically)
    # Note: resize and normalize are always applied automatically and should not be in preprocessing_list
    preprocessing_list = config.data.preprocessing_list or []
    
    # Validate preprocessing_list is a list
    if not isinstance(preprocessing_list, list):
        raise ValueError(f"preprocessing_list must be a list, got {type(preprocessing_list)}")
    
    # Build preprocessing transforms (PIL Image transforms before ToTensor)
    pil_transforms = build_preprocessing_transforms(config, preprocessing_list)
    
    # Build augmentation transforms (separate PIL and tensor transforms)
    augmentation_list = config.data.augmentation_list or [] if include_augmentation else []
    augmentation_pil_transforms, augmentation_tensor_transforms = build_augmentation_transforms(
        config, augmentation_list, include_augmentation
    )
    
    # Build tensor transforms (normalization only - augmentation tensor is handled separately)
    tensor_transforms = build_tensor_transforms(config)
    
    # Compose complete transform pipeline
    return compose_transform_pipeline(
        pil_transforms=pil_transforms,
        augmentation_pil_transforms=augmentation_pil_transforms,
        augmentation_tensor_transforms=augmentation_tensor_transforms,
        tensor_transforms=tensor_transforms
    )


def build_train_transform(config: Config) -> transforms.Compose:
    """
    Build training transform pipeline from config with augmentation enabled.
    
    Transform order:
    1. PIL Image transforms (preprocessing + augmentation)
    2. ToTensor
    3. Tensor transforms (tensor augmentation + normalization)
    
    Note: Essential preprocessing (resize, normalize) is always applied automatically.
    
    Args:
        config: Configuration object with preprocessing_list and augmentation_list.
                Must have config.data attribute with preprocessing_list, augmentation_list,
                image_size, imagenet_mean, and imagenet_std.
        
    Returns:
        Composed transform pipeline for training with augmentation applied.
        
    Raises:
        AttributeError: If config is missing required attributes.
        ValueError: If config.data is None or invalid.
    """
    return _build_base_transform(config, include_augmentation=True)


def build_val_transform(config: Config) -> transforms.Compose:
    """
    Build validation transform pipeline from config without augmentation.
    
    Transform order:
    1. PIL Image transforms (preprocessing only, no augmentation)
    2. ToTensor
    3. Tensor transforms (normalization only, no augmentation)
    
    Note: Essential preprocessing (resize, normalize) is always applied automatically.
    
    Args:
        config: Configuration object with preprocessing_list.
                Must have config.data attribute with preprocessing_list,
                image_size, imagenet_mean, and imagenet_std.
                Augmentation_list is ignored for validation.
        
    Returns:
        Composed transform pipeline for validation without augmentation.
        
    Raises:
        AttributeError: If config is missing required attributes.
        ValueError: If config.data is None or invalid.
    """
    return _build_base_transform(config, include_augmentation=False)


def build_tta_transforms(
    config: Config,
    tta_variants: List[str] = None
) -> List[transforms.Compose]:
    """
    Build TTA transforms using same augmentation builders as training.
    
    Creates deterministic variants of transforms for test-time augmentation.
    Each variant applies the same augmentations as training, but deterministically
    (p=1.0 for random transforms, fixed parameters for others).
    
    This function provides a unified interface for TTA that reuses the same
    transform builders as training, eliminating code duplication and ensuring
    consistency between training augmentation and TTA.
    
    Args:
        config: Configuration object with preprocessing_list and augmentation_list.
                Must have config.data attribute with preprocessing_list, augmentation_list,
                image_size, imagenet_mean, and imagenet_std.
        tta_variants: Optional list of TTA variant names. If None, uses defaults.
                     Each variant must be in AVAILABLE_TTA_VARIANTS.
                     Can also be set via config.data.tta_variants.
    
    Returns:
        List of Composed transform pipelines, one per TTA variant.
        Each transform is ready for use in DataLoader.
    
    Raises:
        AttributeError: If config is missing required attributes.
        ValueError: If any variant in tta_variants is not in AVAILABLE_TTA_VARIANTS.
    
    Example:
        ```python
        # Use default TTA variants
        tta_transforms = build_tta_transforms(config)
        
        # Use specific variants
        tta_transforms = build_tta_transforms(
            config,
            tta_variants=['original', 'h_flip', 'v_flip']
        )
        
        # Use variants from config
        tta_transforms = build_tta_transforms(
            config,
            tta_variants=config.data.tta_variants
        )
        ```
    """
    # Use config.data.tta_variants if available and tta_variants not provided
    if tta_variants is None and hasattr(config.data, 'tta_variants') and config.data.tta_variants:
        tta_variants = config.data.tta_variants
    
    return _build_tta_transforms(config, tta_variants)

