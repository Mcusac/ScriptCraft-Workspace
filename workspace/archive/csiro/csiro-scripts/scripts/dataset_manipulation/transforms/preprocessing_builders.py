# preprocessing_builders.py
# Preprocessing transform builder registry
# Defines builders for preprocessing transforms (PIL Image transforms before ToTensor)

import torchvision.transforms as transforms
from typing import Dict, Callable, Optional, Any

from config.config import Config
from dataset_manipulation.essential.preprocessing.resizing import get_resize_transform
from dataset_manipulation.nonessential.preprocessing.contrast_enhancement import contrast_enhancement
from dataset_manipulation.nonessential.preprocessing.noise_reduction import noise_reduction

# Type alias for clarity
TransformBuilder = Callable[[Config], Optional[Any]]


def _get_center_crop_transform(config: Config) -> Optional[transforms.CenterCrop]:
    """
    Get CenterCrop transform based on config image_size.
    
    Args:
        config: Configuration object with data.image_size.
    
    Returns:
        CenterCrop transform or None if image_size not set.
    """
    if not config.data.image_size:
        return None
    
    # Handle both tuple and int image_size
    if isinstance(config.data.image_size, (tuple, list)):
        # Use first dimension (height) for square crop
        size = config.data.image_size[0]
    elif isinstance(config.data.image_size, int):
        size = config.data.image_size
    else:
        return None
    
    return transforms.CenterCrop(size)

# Preprocessing transform builders (PIL transforms, before ToTensor)
# Each builder takes a Config and returns a transform or None
# NOTE: Keys must match AVAILABLE_PREPROCESSING (excluding 'normalize' which is always applied)
PREPROCESSING_BUILDERS: Dict[str, TransformBuilder] = {
    'resize': lambda config: get_resize_transform(config.data.image_size) if config.data.image_size else None,
    'center_crop': lambda config: _get_center_crop_transform(config),
    'contrast_enhancement': lambda config: transforms.Lambda(lambda img: contrast_enhancement(img, method='histogram_equalization')),
    'noise_reduction': lambda config: transforms.Lambda(lambda img: noise_reduction(img, method='gaussian_blur')),
}

