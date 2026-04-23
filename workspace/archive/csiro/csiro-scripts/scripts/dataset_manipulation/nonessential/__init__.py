# __init__.py
# Data manipulation package (nonessential operations)
#
# Provides nonessential image preprocessing, augmentation, and transform composition.
# These operations enhance data quality or provide augmentation, but are not required
# for basic functionality. They are controlled via config flags (preprocessing_list,
# augmentation_list) and can be enabled/disabled as needed.
#
# Purpose:
# This package contains operations that improve model performance through data
# enhancement and augmentation, but are not essential for basic functionality.
# Examples include:
# - Contrast enhancement for better image quality
# - Noise reduction for cleaner images
# - Geometric augmentations (rotation, translation, scaling)
# - Color augmentations (brightness, contrast, saturation)
# - Blur and noise addition for robustness
#
# Sub-packages:
# - preprocessing: Optional preprocessing operations (contrast_enhancement, noise_reduction)
#   These can be enabled via preprocessing_list in config
# - data_augmentation: Training-time augmentations (geometric, color, blur, noise)
#   These can be enabled via augmentation_list in config
# - kernel_utils: Shared utilities for kernel size validation (ensure_odd_kernel_size)
#   Used by blur and noise reduction operations
#
# Note: Transform pipeline composition has been moved to dataset_manipulation.transforms
# (orchestrates both essential and nonessential transforms into complete pipelines)
#
# Boundary Rules:
# - DO put here: Optional enhancements, augmentation, configurable transforms
# - DO NOT put here: Essential operations (loading, resize, normalize, datasets)
#   (Use essential for those)
#
# Note: Necessary preprocessing operations (resize, normalize) are in essential.preprocessing.
# Normalization is always automatically applied and should not be included in preprocessing_list.
#
# Import Guidelines:
# - To avoid circular imports, we do NOT import from transforms here.
# - For transform imports, use direct imports from the transforms package:
#   - from dataset_manipulation.transforms.transform_factory import build_train_transform, build_val_transform, build_tta_transforms


__all__ = [
    'contrast_enhancement',
    'noise_reduction',
    'get_blurring_transform',
    'get_color_jittering_transform',
    'get_geometric_transformations_transform',
    'get_noise_addition_transform',
    'AddGaussianNoise',
    'DEFAULT_PREPROCESSING_LIST',
    'AVAILABLE_PREPROCESSING',
    'AVAILABLE_AUGMENTATION',
    # Default values
    'DEFAULT_BLUR_KERNEL_SIZE',
    'DEFAULT_BLUR_SIGMA',
    'DEFAULT_COLOR_BRIGHTNESS',
    'DEFAULT_COLOR_CONTRAST',
    'DEFAULT_COLOR_SATURATION',
    'DEFAULT_COLOR_HUE',
    'DEFAULT_GEOMETRIC_DEGREES',
    'DEFAULT_GEOMETRIC_TRANSLATE',
    'DEFAULT_GEOMETRIC_SCALE',
    'DEFAULT_GEOMETRIC_SHEAR',
    'DEFAULT_NOISE_MEAN',
    'DEFAULT_NOISE_STD',
    'DEFAULT_NOISE_REDUCTION_KERNEL_SIZE',
    'DEFAULT_NOISE_REDUCTION_METHOD',
    'DEFAULT_CONTRAST_ENHANCEMENT_METHOD'
]

