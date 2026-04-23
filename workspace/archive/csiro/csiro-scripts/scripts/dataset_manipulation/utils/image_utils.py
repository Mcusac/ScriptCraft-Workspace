# image_utils.py
# Image conversion utilities for PIL and numpy arrays

import numpy as np
from PIL import Image
from typing import Union, Tuple
import logging

logger = logging.getLogger(__name__)


def pil_to_numpy(image: Union[Image.Image, np.ndarray]) -> Tuple[np.ndarray, bool]:
    """
    Convert PIL Image to numpy array if needed, preserving original type flag.
    
    Args:
        image: PIL Image or numpy array. If numpy array, returned as-is.
        
    Returns:
        Tuple of (numpy_array, was_pil):
        - numpy_array: Numpy array representation of the image
        - was_pil: True if input was PIL Image, False if already numpy array
        
    Raises:
        TypeError: If image is neither PIL Image nor numpy array.
    """
    if isinstance(image, Image.Image):
        return np.array(image), True
    elif isinstance(image, np.ndarray):
        return image, False
    else:
        raise TypeError(
            f"image must be PIL Image or numpy array, got {type(image)}"
        )


def numpy_to_pil(img_array: np.ndarray) -> Image.Image:
    """
    Convert numpy array to PIL Image.
    
    Args:
        img_array: Numpy array of shape (H, W) for grayscale or (H, W, C) for RGB.
                   Should be uint8 dtype.
        
    Returns:
        PIL Image object.
        
    Raises:
        ValueError: If img_array has invalid shape or dtype.
        TypeError: If img_array is not a numpy array.
    """
    if not isinstance(img_array, np.ndarray):
        raise TypeError(f"img_array must be numpy array, got {type(img_array)}")
    
    if img_array.ndim not in (2, 3):
        raise ValueError(
            f"img_array must be 2D (grayscale) or 3D (RGB), got shape {img_array.shape}"
        )
    
    return Image.fromarray(img_array)


def ensure_uint8(img_array: np.ndarray) -> np.ndarray:
    """
    Ensure numpy array is uint8 dtype, converting if necessary.
    
    If array is in range [0, 1], scales to [0, 255] before converting.
    Otherwise, directly converts to uint8.
    
    Args:
        img_array: Numpy array of any dtype. Should be in range [0, 1] or [0, 255].
        
    Returns:
        Numpy array with uint8 dtype, in range [0, 255].
        
    Raises:
        TypeError: If img_array is not a numpy array.
    """
    if not isinstance(img_array, np.ndarray):
        raise TypeError(f"img_array must be numpy array, got {type(img_array)}")
    
    if img_array.dtype == np.uint8:
        return img_array
    
    # Normalize to [0, 255] if needed
    if img_array.max() <= 1.0:
        img_array = (img_array * 255).astype(np.uint8)
        logger.debug("Converted image from [0, 1] range to [0, 255] uint8")
    else:
        img_array = img_array.astype(np.uint8)
        logger.debug(f"Converted image dtype to uint8 (was {img_array.dtype})")
    
    return img_array

