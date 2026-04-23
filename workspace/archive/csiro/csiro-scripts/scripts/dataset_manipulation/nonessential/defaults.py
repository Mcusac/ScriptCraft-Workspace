# defaults.py
# Default values for data augmentation and preprocessing operations
#
# Centralizes default parameter values for augmentation and preprocessing functions.
# This ensures consistency and makes it easier to update defaults across the codebase.

from typing import Tuple

# ============================================================================
# Blurring Defaults
# ============================================================================

DEFAULT_BLUR_KERNEL_SIZE: int = 3
DEFAULT_BLUR_SIGMA: Tuple[float, float] = (0.1, 2.0)

# ============================================================================
# Color Jittering Defaults
# ============================================================================

DEFAULT_COLOR_BRIGHTNESS: float = 0.2
DEFAULT_COLOR_CONTRAST: float = 0.2
DEFAULT_COLOR_SATURATION: float = 0.2
DEFAULT_COLOR_HUE: float = 0.1

# ============================================================================
# Geometric Transformations Defaults
# ============================================================================

DEFAULT_GEOMETRIC_DEGREES: float = 15.0
DEFAULT_GEOMETRIC_TRANSLATE: Tuple[float, float] = (0.1, 0.1)
DEFAULT_GEOMETRIC_SCALE: Tuple[float, float] = (0.9, 1.1)
DEFAULT_GEOMETRIC_SHEAR: float = 5.0

# ============================================================================
# Noise Addition Defaults
# ============================================================================

DEFAULT_NOISE_MEAN: float = 0.0
DEFAULT_NOISE_STD: float = 0.01

# ============================================================================
# Preprocessing Defaults
# ============================================================================

DEFAULT_NOISE_REDUCTION_KERNEL_SIZE: int = 5
DEFAULT_NOISE_REDUCTION_METHOD: str = 'gaussian_blur'

DEFAULT_CONTRAST_ENHANCEMENT_METHOD: str = 'histogram_equalization'

