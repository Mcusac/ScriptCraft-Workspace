# constants.py
# Constants for data manipulation operations
#
# Defines available preprocessing and augmentation techniques,
# and default preprocessing configurations.
#
# Note: Essential preprocessing operations (resize, normalize) are always
# automatically applied and should not be included in preprocessing_list.
# Resize is applied automatically when image_size is set.
# Normalization is always applied automatically after ToTensor.

# Default preprocessing list (empty - only nonessential operations should be listed)
# Essential operations (resize, normalize) are always applied automatically
DEFAULT_PREPROCESSING_LIST = []

# Available preprocessing techniques
AVAILABLE_PREPROCESSING = {
    'resize',
    'normalize',
    'center_crop',
    'contrast_enhancement',
    'noise_reduction'
}

# Available augmentation techniques
AVAILABLE_AUGMENTATION = {
    'geometric_transformations',
    'color_jittering',
    'blurring',
    'noise_addition'
}

# Available TTA variants
# These variants apply geometric transforms deterministically (p=1.0)
# Other augmentations from augmentation_list are also applied deterministically
AVAILABLE_TTA_VARIANTS = {
    'original',      # No geometric augmentation (only preprocessing + augmentation_list)
    'h_flip',        # Horizontal flip
    'v_flip',        # Vertical flip
    'both_flips',    # Both horizontal and vertical flips
    'rotate_90',     # 90 degree rotation
    'rotate_270',    # 270 degree rotation
}

# Default TTA variants (subset of available variants)
# Used when tta_variants is not specified in config
DEFAULT_TTA_VARIANTS = [
    'original',
    'h_flip',
    'v_flip',
    'both_flips',
    'rotate_90',
    'rotate_270',
]

