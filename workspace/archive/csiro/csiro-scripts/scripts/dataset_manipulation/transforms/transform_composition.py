# transform_composition.py
# Transform composition logic for building transform pipelines
# Separates composition logic from factory functions

import torchvision.transforms as transforms
import logging
from typing import List, Any, Tuple

from config.config import Config
from dataset_manipulation.essential.preprocessing.normalization import get_normalize_transform
from dataset_manipulation.essential.preprocessing.resizing import get_resize_transform
from dataset_manipulation.nonessential.constants import (
    AVAILABLE_PREPROCESSING,
    AVAILABLE_AUGMENTATION
)
from .preprocessing_builders import PREPROCESSING_BUILDERS
from .augmentation_builders import AUGMENTATION_BUILDERS

logger = logging.getLogger(__name__)


def build_preprocessing_transforms(config: Config, preprocessing_list: List[str]) -> List[Any]:
    """
    Build preprocessing transforms (PIL Image transforms before ToTensor).
    
    Essential preprocessing operations (resize, normalize) are always applied automatically:
    - Resize is applied automatically if image_size is set (before optional preprocessing)
    - Normalize is always applied automatically after ToTensor (handled in build_tensor_transforms)
    
    Args:
        config: Configuration object.
        preprocessing_list: List of optional preprocessing technique names.
                          Essential operations (resize, normalize) should not be included.
        
    Returns:
        List of preprocessing transform objects (resize first, then optional preprocessing).
    """
    pil_transforms: List[Any] = []
    
    # Always apply resize automatically if image_size is set (essential operation)
    # Resize must be applied first, before any optional preprocessing
    if config.data.image_size:
        try:
            resize_transform = get_resize_transform(config.data.image_size)
            if resize_transform is not None:
                pil_transforms.append(resize_transform)
                logger.debug("Resize always applied automatically (essential preprocessing)")
        except Exception as e:
            logger.error(f"Error building resize transform: {e}")
            raise
    else:
        logger.debug("Resize skipped - image_size not set in config")
    
    # Apply optional preprocessing in order
    for prep_name in preprocessing_list:
        # Skip 'normalize' if present in list (it's always applied automatically)
        if prep_name == 'normalize':
            logger.info("'normalize' in preprocessing_list is ignored - normalization is always applied automatically")
            continue
        
        # Skip 'resize' if present in list (it's always applied automatically)
        if prep_name == 'resize':
            logger.info("'resize' in preprocessing_list is ignored - resize is always applied automatically when image_size is set")
            continue
        
        # Validate against available set first (consistent with config validation)
        if prep_name not in AVAILABLE_PREPROCESSING:
            logger.warning(f"Unknown preprocessing technique: {prep_name}, skipping")
            continue
        
        # Build transform if builder exists
        if prep_name in PREPROCESSING_BUILDERS:
            try:
                transform = PREPROCESSING_BUILDERS[prep_name](config)
                if transform is not None:
                    pil_transforms.append(transform)
            except Exception as e:
                logger.error(f"Error building preprocessing transform '{prep_name}': {e}")
                raise
        else:
            # Known but not implemented (e.g., 'normalize' is handled separately)
            logger.debug(f"Preprocessing '{prep_name}' is known but handled separately (e.g., normalize is always applied)")
    
    return pil_transforms


def build_augmentation_transforms(config: Config, augmentation_list: List[str], include_augmentation: bool) -> Tuple[List[Any], List[Any]]:
    """
    Build augmentation transforms, separating PIL and tensor transforms.
    
    Args:
        config: Configuration object.
        augmentation_list: List of augmentation technique names.
        include_augmentation: Whether to include augmentation (should match training mode).
        
    Returns:
        Tuple of (pil_transforms, tensor_transforms).
    """
    augmentation_pil_transforms: List[Any] = []
    augmentation_tensor_transforms: List[Any] = []
    
    if not include_augmentation:
        return augmentation_pil_transforms, augmentation_tensor_transforms
    
    if not augmentation_list:
        return augmentation_pil_transforms, augmentation_tensor_transforms
    
    # Validate augmentation_list is a list
    if not isinstance(augmentation_list, list):
        raise ValueError(f"augmentation_list must be a list, got {type(augmentation_list)}")
    
    logger.info(f"Applying augmentation: {', '.join(augmentation_list)}")
    
    for aug_name in augmentation_list:
        # Validate against available set first (consistent with config validation)
        if aug_name not in AVAILABLE_AUGMENTATION:
            logger.warning(f"Unknown augmentation technique: {aug_name}, skipping")
            continue
        
        # Build transform if builder exists
        if aug_name in AUGMENTATION_BUILDERS:
            try:
                transform, is_tensor_transform = AUGMENTATION_BUILDERS[aug_name](config)
                if is_tensor_transform:
                    augmentation_tensor_transforms.append(transform)
                else:
                    augmentation_pil_transforms.append(transform)
            except Exception as e:
                logger.error(f"Error building augmentation transform '{aug_name}': {e}")
                raise
        else:
            logger.warning(f"Augmentation '{aug_name}' is in AVAILABLE_AUGMENTATION but has no builder implementation")
    
    return augmentation_pil_transforms, augmentation_tensor_transforms


def build_tensor_transforms(config: Config) -> List[Any]:
    """
    Build tensor transforms (normalization only).
    
    Tensor-based augmentation transforms are handled separately in composition.
    This function only builds the normalization transform which is always applied.
    
    Args:
        config: Configuration object.
        
    Returns:
        List containing normalization transform.
    """
    tensor_transforms: List[Any] = []
    
    # Always add normalization (required for pretrained models)
    # Normalization is always applied regardless of preprocessing_list
    try:
        normalize_transform = get_normalize_transform(
            mean=config.data.imagenet_mean,
            std=config.data.imagenet_std
        )
        tensor_transforms.append(normalize_transform)
        logger.debug("Normalization always applied (ImageNet mean/std)")
    except Exception as e:
        logger.error(f"Error building normalization transform: {e}")
        raise
    
    return tensor_transforms


def compose_transform_pipeline(
    pil_transforms: List[Any],
    augmentation_pil_transforms: List[Any],
    augmentation_tensor_transforms: List[Any],
    tensor_transforms: List[Any]
) -> transforms.Compose:
    """
    Compose a complete transform pipeline from component transforms.
    
    Transform order:
    1. PIL Image transforms (preprocessing + augmentation PIL)
    2. ToTensor (converts PIL Image to tensor)
    3. Tensor transforms (augmentation tensor + normalization)
    
    Args:
        pil_transforms: Preprocessing PIL transforms
        augmentation_pil_transforms: Augmentation PIL transforms
        augmentation_tensor_transforms: Augmentation tensor transforms
        tensor_transforms: Final tensor transforms (normalization)
        
    Returns:
        Composed transform pipeline ready for use in DataLoader.
    """
    transform_list: List[Any] = []
    
    # Combine PIL transforms (preprocessing + augmentation PIL)
    pil_transforms.extend(augmentation_pil_transforms)
    transform_list.extend(pil_transforms)
    
    # Convert to tensor (required before normalization and tensor augmentations)
    transform_list.append(transforms.ToTensor())
    
    # Add tensor-based augmentation before normalization
    transform_list.extend(augmentation_tensor_transforms)
    
    # Add final tensor transforms (normalization)
    transform_list.extend(tensor_transforms)
    
    # Ensure we have at least ToTensor
    if not transform_list:
        logger.warning("No transforms specified, adding ToTensor only")
        transform_list = [transforms.ToTensor()]
    
    return transforms.Compose(transform_list)

