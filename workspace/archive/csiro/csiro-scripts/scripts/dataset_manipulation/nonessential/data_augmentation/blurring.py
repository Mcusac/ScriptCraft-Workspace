# blurring.py
# Blurring the images as a data augmentation technique
# Randomly applying Gaussian blur to simulate different focus conditions.

import torchvision.transforms as transforms
from typing import Tuple
import logging

from utils.system import validate_min_max_tuple
from ..kernel_utils import ensure_odd_kernel_size
from ..defaults import DEFAULT_BLUR_KERNEL_SIZE, DEFAULT_BLUR_SIGMA

logger = logging.getLogger(__name__)


def get_blurring_transform(
    kernel_size: int = DEFAULT_BLUR_KERNEL_SIZE,
    sigma: Tuple[float, float] = DEFAULT_BLUR_SIGMA
) -> transforms.GaussianBlur:
    """
    Get random Gaussian blur augmentation transform.
    
    Args:
        kernel_size: Size of the Gaussian kernel (must be odd, default: 3).
                     Must be positive. If even, will be incremented by 1.
        sigma: Range of sigma values for blur strength as (min, max) tuple (default: (0.1, 2.0)).
               Both values must be non-negative, and min must be <= max.
        
    Returns:
        GaussianBlur transform instance.
        
    Raises:
        ValueError: If kernel_size is invalid or sigma values are invalid.
    """
    # Validate and ensure kernel_size is odd
    kernel_size = ensure_odd_kernel_size(kernel_size)
    
    # Validate sigma tuple
    validate_min_max_tuple(sigma, "sigma", min_val=0.0, allow_equal=True)
    
    return transforms.GaussianBlur(kernel_size=kernel_size, sigma=sigma)