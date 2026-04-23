# color_jittering.py
# Artificially expanding the dataset by applying color jittering to the images
# Adjusting brightness, contrast, saturation, and hue to simulate different lighting conditions.

import torchvision.transforms as transforms
from typing import Optional
import logging

from utils.system import validate_range, validate_optional_non_negative
from ..defaults import (
    DEFAULT_COLOR_BRIGHTNESS,
    DEFAULT_COLOR_CONTRAST,
    DEFAULT_COLOR_SATURATION,
    DEFAULT_COLOR_HUE
)

logger = logging.getLogger(__name__)


def get_color_jittering_transform(
    brightness: Optional[float] = DEFAULT_COLOR_BRIGHTNESS,
    contrast: Optional[float] = DEFAULT_COLOR_CONTRAST,
    saturation: Optional[float] = DEFAULT_COLOR_SATURATION,
    hue: Optional[float] = DEFAULT_COLOR_HUE
) -> transforms.ColorJitter:
    """
    Get color jittering augmentation transform.
    
    Args:
        brightness: Brightness jitter range (default: 0.2, meaning 0.8-1.2x).
                    Must be non-negative. If None, no brightness jitter is applied.
        contrast: Contrast jitter range (default: 0.2, meaning 0.8-1.2x).
                  Must be non-negative. If None, no contrast jitter is applied.
        saturation: Saturation jitter range (default: 0.2, meaning 0.8-1.2x).
                    Must be non-negative. If None, no saturation jitter is applied.
        hue: Hue jitter range (default: 0.1, meaning -0.1 to 0.1).
             Must be in [0, 0.5]. If None, no hue jitter is applied.
        
    Returns:
        ColorJitter transform instance.
        
    Raises:
        ValueError: If any parameter is out of valid range.
    """
    # Validate optional parameters
    validate_optional_non_negative(brightness, "brightness")
    validate_optional_non_negative(contrast, "contrast")
    validate_optional_non_negative(saturation, "saturation")
    
    # Validate hue (must be in [0, 0.5])
    if hue is not None:
        validate_range(hue, min_val=0.0, max_val=0.5, name="hue")
    
    return transforms.ColorJitter(
        brightness=brightness,
        contrast=contrast,
        saturation=saturation,
        hue=hue
    )