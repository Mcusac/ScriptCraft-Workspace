# __init__.py
# Preprocessing package (necessary operations)
#
# Provides necessary image preprocessing operations that must be applied before training.
# These operations are required to prepare images for model input.
#
# Available preprocessing:
# - resizing: Resize images to model input size
# - normalization: ImageNet mean/std normalization (after ToTensor)
#
# Note: Normalization is always automatically applied in transform pipelines.
# Optional preprocessing operations (contrast_enhancement, noise_reduction) are in
# nonessential.preprocessing.
#
# All preprocessing functions support both PIL Images and numpy arrays,
# with automatic conversion handled by utils.py. Functions can be used
# standalone or as part of transform pipelines.


__all__ = [
    'normalize',
    'get_normalize_transform',
    'resize',
    'get_resize_transform'
]