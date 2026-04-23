# contrast_enhancement.py
# Contrast enhancement using histogram equalization

import numpy as np
from PIL import Image
import cv2
from typing import Union
import logging

from dataset_manipulation.utils.image_utils import pil_to_numpy, numpy_to_pil, ensure_uint8
from ..defaults import DEFAULT_CONTRAST_ENHANCEMENT_METHOD

logger = logging.getLogger(__name__)

# Valid enhancement methods
VALID_METHODS = {'histogram_equalization', 'clahe'}


def contrast_enhancement(
    image: Union[Image.Image, np.ndarray],
    method: str = DEFAULT_CONTRAST_ENHANCEMENT_METHOD
) -> Union[Image.Image, np.ndarray]:
    """
    Enhance image contrast using histogram equalization or CLAHE.
    
    Args:
        image: PIL Image or numpy array. If numpy array, should be uint8 in range [0, 255].
               Supports grayscale (2D) or RGB (3D) images.
        method: Enhancement method. Must be one of: 'histogram_equalization', 'clahe'.
                Default: 'histogram_equalization'.
        
    Returns:
        Enhanced image of the same type as input (PIL Image or numpy array).
        Output maintains the same dtype and shape as input.
        
    Raises:
        ValueError: If method is not valid.
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
    
    # Handle grayscale vs RGB
    if len(img_array.shape) == 2:
        # Grayscale
        if method == 'histogram_equalization':
            enhanced = cv2.equalizeHist(img_array)
        else:  # method == 'clahe'
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(img_array)
    elif len(img_array.shape) == 3:
        # RGB - apply to each channel
        enhanced = np.zeros_like(img_array)
        if method == 'histogram_equalization':
            for i in range(img_array.shape[2]):
                enhanced[:, :, i] = cv2.equalizeHist(img_array[:, :, i])
        else:  # method == 'clahe'
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            for i in range(img_array.shape[2]):
                enhanced[:, :, i] = clahe.apply(img_array[:, :, i])
    else:
        raise ValueError(
            f"Unsupported image shape: {img_array.shape}. "
            "Expected 2D (grayscale) or 3D (RGB) array."
        )
    
    # Convert back to PIL if input was PIL
    if is_pil:
        return numpy_to_pil(enhanced)
    return enhanced

