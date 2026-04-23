# tta_builders.py
# TTA (Test-Time Augmentation) variant builders
# Builds deterministic variants of transforms for TTA using same builders as training

import torchvision.transforms as transforms
from typing import List, Any, Optional
import logging

from config.config import Config
from dataset_manipulation.nonessential.constants import (
    AVAILABLE_TTA_VARIANTS,
    DEFAULT_TTA_VARIANTS
)
from dataset_manipulation.nonessential.data_augmentation.color_jittering import get_color_jittering_transform
from dataset_manipulation.nonessential.data_augmentation.noise_addition import get_noise_addition_transform
from dataset_manipulation.nonessential.defaults import DEFAULT_BLUR_SIGMA
from .transform_composition import compose_transform_pipeline
from .transform_composition import build_preprocessing_transforms, build_tensor_transforms

logger = logging.getLogger(__name__)


def get_blurring_transform_deterministic() -> transforms.GaussianBlur:
    """
    Get deterministic Gaussian blur transform for TTA.
    
    Uses fixed sigma value (midpoint of default range) instead of random range.
    This ensures consistent blur application across TTA variants.
    
    Returns:
        GaussianBlur transform with fixed sigma.
    """
    # Use midpoint of default sigma range for deterministic behavior
    sigma_min, sigma_max = DEFAULT_BLUR_SIGMA
    fixed_sigma = (sigma_min + sigma_max) / 2.0
    return transforms.GaussianBlur(kernel_size=5, sigma=(fixed_sigma, fixed_sigma))


def get_color_jittering_transform_deterministic() -> transforms.ColorJitter:
    """
    Get deterministic color jittering transform for TTA.
    
    Uses default parameters but applies them deterministically.
    Note: ColorJitter is already deterministic if parameters are fixed.
    
    Returns:
        ColorJitter transform with default parameters.
    """
    return get_color_jittering_transform()


def get_noise_addition_transform_deterministic():
    """
    Get deterministic noise addition transform for TTA.
    
    Uses default parameters. Noise addition is already deterministic
    (same mean/std each time, but random noise is still applied).
    
    Returns:
        AddGaussianNoise transform with default parameters.
    """
    return get_noise_addition_transform()


def build_tta_variant(
    config: Config,
    base_pil_transforms: List[Any],
    variant: str,
    augmentation_list: List[str]
) -> transforms.Compose:
    """
    Build a single TTA variant by applying augmentations deterministically.
    
    Uses the same augmentation builders as training, but applies them
    deterministically (p=1.0 for random transforms, fixed parameters for others).
    
    Args:
        config: Configuration object with preprocessing_list and augmentation_list.
        base_pil_transforms: Base preprocessing transforms (resize, etc.).
        variant: TTA variant name (e.g., 'h_flip', 'original').
                Must be in AVAILABLE_TTA_VARIANTS.
        augmentation_list: List of augmentation names to apply deterministically.
    
    Returns:
        Composed transform pipeline for this TTA variant.
    
    Raises:
        ValueError: If variant is not in AVAILABLE_TTA_VARIANTS.
    """
    if variant not in AVAILABLE_TTA_VARIANTS:
        raise ValueError(
            f"Unknown TTA variant: {variant}. "
            f"Available variants: {AVAILABLE_TTA_VARIANTS}"
        )
    
    # Start with base preprocessing transforms
    variant_pil_transforms = base_pil_transforms.copy()
    variant_tensor_transforms = []
    
    # Apply deterministic geometric transforms based on variant
    if variant == 'original':
        # No geometric augmentation, but still apply other augmentations
        pass
    elif variant == 'h_flip':
        variant_pil_transforms.append(transforms.RandomHorizontalFlip(p=1.0))
    elif variant == 'v_flip':
        variant_pil_transforms.append(transforms.RandomVerticalFlip(p=1.0))
    elif variant == 'both_flips':
        variant_pil_transforms.append(transforms.RandomHorizontalFlip(p=1.0))
        variant_pil_transforms.append(transforms.RandomVerticalFlip(p=1.0))
    elif variant == 'rotate_90':
        variant_pil_transforms.append(transforms.RandomRotation(degrees=(90, 90)))
    elif variant == 'rotate_270':
        variant_pil_transforms.append(transforms.RandomRotation(degrees=(270, 270)))
    
    # Apply other augmentations from augmentation_list deterministically
    for aug_name in augmentation_list:
        if aug_name == 'blurring':
            variant_pil_transforms.append(get_blurring_transform_deterministic())
        elif aug_name == 'color_jittering':
            variant_pil_transforms.append(get_color_jittering_transform_deterministic())
        elif aug_name == 'noise_addition':
            # Noise addition is a tensor transform (after ToTensor)
            variant_tensor_transforms.append(get_noise_addition_transform_deterministic())
        elif aug_name == 'geometric_transformations':
            # Geometric transforms are already handled by variant-specific transforms above
            # Skip here to avoid double application
            logger.debug(f"Skipping 'geometric_transformations' in augmentation_list for TTA variant '{variant}' "
                        f"(geometric transforms are handled by variant-specific transforms)")
        else:
            logger.warning(f"Unknown augmentation '{aug_name}' in augmentation_list, skipping for TTA")
    
    # Build tensor transforms (normalization)
    tensor_transforms = build_tensor_transforms(config)
    
    # Compose complete transform pipeline
    return compose_transform_pipeline(
        pil_transforms=variant_pil_transforms,
        augmentation_pil_transforms=[],
        augmentation_tensor_transforms=variant_tensor_transforms,
        tensor_transforms=tensor_transforms
    )


def build_tta_transforms(
    config: Config,
    tta_variants: Optional[List[str]] = None
) -> List[transforms.Compose]:
    """
    Build TTA transforms using same augmentation builders as training.
    
    Creates deterministic variants of transforms for test-time augmentation.
    Each variant applies the same augmentations as training, but deterministically
    (p=1.0 for random transforms, fixed parameters for others).
    
    Args:
        config: Configuration object with preprocessing_list and augmentation_list.
        tta_variants: List of TTA variant names. If None, uses DEFAULT_TTA_VARIANTS.
                     Each variant must be in AVAILABLE_TTA_VARIANTS.
    
    Returns:
        List of Composed transform pipelines, one per TTA variant.
        Each transform is ready for use in DataLoader.
    
    Raises:
        ValueError: If any variant in tta_variants is not in AVAILABLE_TTA_VARIANTS.
        AttributeError: If config is missing required attributes.
    """
    # Use default variants if not specified
    if tta_variants is None:
        tta_variants = DEFAULT_TTA_VARIANTS.copy()
    
    # Validate all variants
    invalid_variants = set(tta_variants) - AVAILABLE_TTA_VARIANTS
    if invalid_variants:
        raise ValueError(
            f"Invalid TTA variants: {invalid_variants}. "
            f"Available variants: {AVAILABLE_TTA_VARIANTS}"
        )
    
    # Get preprocessing list (only optional preprocessing, resize is applied automatically)
    preprocessing_list = config.data.preprocessing_list or []
    
    # Build base preprocessing transforms (shared by all variants)
    base_pil_transforms = build_preprocessing_transforms(config, preprocessing_list)
    
    # Get augmentation list
    augmentation_list = config.data.augmentation_list or []
    
    # Build TTA variants
    tta_transform_list = []
    for variant in tta_variants:
        variant_transform = build_tta_variant(
            config=config,
            base_pil_transforms=base_pil_transforms,
            variant=variant,
            augmentation_list=augmentation_list
        )
        tta_transform_list.append(variant_transform)
    
    logger.info(f"Built {len(tta_transform_list)} TTA variants: {', '.join(tta_variants)}")
    if augmentation_list:
        logger.info(f"Applying augmentations deterministically: {', '.join(augmentation_list)}")
    
    return tta_transform_list

