# noise_reduction.py
# Noise reduction techniques for image preprocessing

import numpy as np
from PIL import Image
import cv2
from typing import Union, Optional
import logging

from dataset_manipulation.utils.image_utils import pil_to_numpy, numpy_to_pil, ensure_uint8
from ..kernel_utils import ensure_odd_kernel_size
from ..defaults import (
    DEFAULT_NOISE_REDUCTION_METHOD,
    DEFAULT_NOISE_REDUCTION_KERNEL_SIZE
)

logger = logging.getLogger(__name__)

# Valid denoising methods
VALID_METHODS = {'gaussian_blur', 'bilateral', 'median'}


def noise_reduction(
    image: Union[Image.Image, np.ndarray],
    method: str = DEFAULT_NOISE_REDUCTION_METHOD,
    kernel_size: int = DEFAULT_NOISE_REDUCTION_KERNEL_SIZE,
    sigma: Optional[float] = None
) -> Union[Image.Image, np.ndarray]:
    """
    Reduce noise in image using various filtering techniques.
    
    Args:
        image: PIL Image or numpy array. If numpy array, should be uint8 in range [0, 255].
               Supports grayscale (2D) or RGB (3D) images.
        method: Denoising method. Must be one of: 'gaussian_blur', 'bilateral', 'median'.
                Default: 'gaussian_blur'.
        kernel_size: Kernel size for filtering (default: 5). Must be positive.
                    Will be adjusted to odd if even. For median filter, must be odd.
        sigma: Standard deviation for Gaussian blur (default: None, auto-calculated).
               Must be positive if provided. Only used for 'gaussian_blur' method.
        
    Returns:
        Denoised image of the same type as input (PIL Image or numpy array).
        Output maintains the same dtype and shape as input.
        
    Raises:
        ValueError: If method is not valid, or parameters are out of valid range.
        TypeError: If image type is not PIL Image or numpy array.
    """
    # Validate method
    if method not in VALID_METHODS:
        raise ValueError(
            f"Invalid method '{method}'. Must be one of: {', '.join(VALID_METHODS)}"
        )
    
    # Convert PIL to numpy if needed (pil_to_numpy validates input type)
    img_array, is_pil = pil_to_numpy(image)
    
    # Ensure uint8 for cv2 operations
    img_array = ensure_uint8(img_array)
    
    # Ensure kernel size is odd (required for some methods)
    kernel_size = ensure_odd_kernel_size(kernel_size)
    
    # Validate sigma if provided
    if sigma is not None and sigma <= 0:
        raise ValueError(f"sigma must be positive, got {sigma}")
    
    # Apply denoising method
    if method == 'gaussian_blur':
        if sigma is None:
            sigma = kernel_size / 6.0
        denoised = cv2.GaussianBlur(img_array, (kernel_size, kernel_size), sigma)
    
    elif method == 'bilateral':
        denoised = cv2.bilateralFilter(
            img_array, 
            d=kernel_size, 
            sigmaColor=75, 
            sigmaSpace=75
        )
    
    else:  # method == 'median'
        # Median filter requires odd kernel size (already ensured above)
        denoised = cv2.medianBlur(img_array, kernel_size)
    
    # Convert back to PIL if input was PIL
    if is_pil:
        return numpy_to_pil(denoised)
    return denoised

