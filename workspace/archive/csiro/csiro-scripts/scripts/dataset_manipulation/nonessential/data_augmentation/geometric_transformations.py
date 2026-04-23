# geometric_transformations.py
# Artificially expanding the dataset by applying geometric transformations to the images
# Rotating, scaling, and shearing the images to simulate different viewing angles and distances.

import torchvision.transforms as transforms
from typing import Optional, Tuple
import logging

from utils.system import (
    validate_tuple_length,
    validate_range,
    validate_min_max_tuple
)
from ..defaults import (
    DEFAULT_GEOMETRIC_DEGREES,
    DEFAULT_GEOMETRIC_TRANSLATE,
    DEFAULT_GEOMETRIC_SCALE,
    DEFAULT_GEOMETRIC_SHEAR
)

logger = logging.getLogger(__name__)


def get_geometric_transformations_transform(
    degrees: float = DEFAULT_GEOMETRIC_DEGREES,
    translate: Optional[Tuple[float, float]] = None,
    scale: Optional[Tuple[float, float]] = None,
    shear: Optional[float] = None,
    interpolation: int = transforms.InterpolationMode.BILINEAR,
    fill: int = 0
) -> transforms.RandomAffine:
    """
    Get geometric transformation augmentations (rotation, translation, scaling, shearing).
    
    Args:
        degrees: Rotation range in degrees (default: 15.0). Can be a single float or tuple (min, max).
        translate: Translation range as (max_x, max_y) tuple (default: (0.1, 0.1)).
                   Values should be in [0, 1] representing fraction of image size.
        scale: Scaling range as (min, max) tuple (default: (0.9, 1.1)).
               Both values must be positive, and min should be < max.
        shear: Shearing range in degrees (default: 5.0). Can be a single float or tuple (min, max).
        interpolation: Interpolation mode (default: BILINEAR).
        fill: Fill value for areas outside the image (default: 0).
        
    Returns:
        RandomAffine transform instance.
        
    Raises:
        ValueError: If any parameter is out of valid range.
    """
    # Set defaults
    if translate is None:
        translate = DEFAULT_GEOMETRIC_TRANSLATE
    if scale is None:
        scale = DEFAULT_GEOMETRIC_SCALE
    if shear is None:
        shear = DEFAULT_GEOMETRIC_SHEAR
    
    # Validate translate (values must be in [0, 1])
    validate_tuple_length(translate, 2, "translate")
    translate_x, translate_y = translate
    validate_range(translate_x, min_val=0.0, max_val=1.0, name="translate[0]")
    validate_range(translate_y, min_val=0.0, max_val=1.0, name="translate[1]")
    
    # Validate scale (values must be positive, min < max)
    validate_min_max_tuple(scale, "scale", min_val=0.0, allow_equal=False)
    
    # Validate degrees (can be float or tuple)
    if isinstance(degrees, (list, tuple)):
        validate_min_max_tuple(degrees, "degrees", allow_equal=True)
    
    # Validate shear (can be float or tuple)
    if isinstance(shear, (list, tuple)):
        validate_min_max_tuple(shear, "shear", allow_equal=True)
    
    return transforms.RandomAffine(
        degrees=degrees,
        translate=translate,
        scale=scale,
        shear=shear,
        interpolation=interpolation,
        fill=fill
    )