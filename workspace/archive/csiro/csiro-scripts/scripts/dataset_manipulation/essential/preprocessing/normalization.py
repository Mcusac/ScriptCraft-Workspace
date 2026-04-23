# normalization.py
# Image normalization using ImageNet statistics

import torch
import torchvision.transforms as transforms
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

# ImageNet normalization constants (standard defaults)
IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


def normalize(
    tensor: torch.Tensor,
    mean: Tuple[float, float, float] = IMAGENET_MEAN,
    std: Tuple[float, float, float] = IMAGENET_STD
) -> torch.Tensor:
    """
    Normalize tensor using mean and standard deviation per channel.
    
    Normalization formula: (tensor - mean) / std
    
    Args:
        tensor: Input tensor of shape (C, H, W) or (B, C, H, W).
                Expected to be in range [0, 1] (after ToTensor()).
        mean: Mean values for each channel (default: ImageNet mean).
              Must be a tuple of 3 floats.
        std: Standard deviation values for each channel (default: ImageNet std).
             Must be a tuple of 3 floats. All values must be positive.
        
    Returns:
        Normalized tensor of the same shape as input.
        
    Raises:
        ValueError: If mean or std have invalid length or std contains non-positive values.
        TypeError: If tensor is not a torch.Tensor.
    """
    # Validate input type
    if not isinstance(tensor, torch.Tensor):
        raise TypeError(f"tensor must be torch.Tensor, got {type(tensor)}")
    
    # Validate mean
    if len(mean) != 3:
        raise ValueError(f"mean must be a tuple of length 3, got {mean}")
    
    # Validate std
    if len(std) != 3:
        raise ValueError(f"std must be a tuple of length 3, got {std}")
    if any(s <= 0 for s in std):
        raise ValueError(f"std values must be positive, got {std}")
    
    normalize_transform = transforms.Normalize(mean=mean, std=std)
    return normalize_transform(tensor)


def get_normalize_transform(
    mean: Tuple[float, float, float] = IMAGENET_MEAN,
    std: Tuple[float, float, float] = IMAGENET_STD
) -> transforms.Normalize:
    """
    Get a torchvision Normalize transform for use in transform pipelines.
    
    Args:
        mean: Mean values for each channel (default: ImageNet mean).
              Must be a tuple of 3 floats.
        std: Standard deviation values for each channel (default: ImageNet std).
             Must be a tuple of 3 floats. All values must be positive.
        
    Returns:
        Normalize transform instance that can be used in torchvision transform pipelines.
        
    Raises:
        ValueError: If mean or std have invalid length or std contains non-positive values.
    """
    # Validate mean
    if len(mean) != 3:
        raise ValueError(f"mean must be a tuple of length 3, got {mean}")
    
    # Validate std
    if len(std) != 3:
        raise ValueError(f"std must be a tuple of length 3, got {std}")
    if any(s <= 0 for s in std):
        raise ValueError(f"std values must be positive, got {std}")
    
    return transforms.Normalize(mean=mean, std=std)