# __init__.py
# Preprocessing package (optional operations)
#
# Provides optional image preprocessing operations that can be applied before training.
# These operations improve image quality but are not required for model input.
#
# Available preprocessing:
# - contrast_enhancement: Histogram equalization, CLAHE
# - noise_reduction: Gaussian blur, bilateral filtering, median filtering
#
# Note: Necessary preprocessing operations (resize, normalize) are in essential.preprocessing.
# Normalization is always automatically applied and should not be included in preprocessing_list.
#
# All preprocessing functions support both PIL Images and numpy arrays,
# with automatic conversion handled by utils. Functions can be used
# standalone or as part of transform pipelines.


__all__ = [
    'contrast_enhancement',
    'noise_reduction'
]

