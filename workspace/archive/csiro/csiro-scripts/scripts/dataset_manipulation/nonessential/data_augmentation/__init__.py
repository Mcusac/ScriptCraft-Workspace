# __init__.py
# Data augmentation package
#
# Provides training-time augmentation transforms for data augmentation.
# All transforms return torchvision Transform objects that can be composed
# into transform pipelines.
#
# Available augmentations:
# - blurring: Gaussian blur for simulating different focus conditions
# - color_jittering: Brightness, contrast, saturation, hue adjustments
# - geometric_transformations: Rotation, translation, scaling, shearing
# - noise_addition: Gaussian noise addition (tensor-based, after ToTensor)
#
# Note: Optional preprocessing operations (contrast_enhancement, noise_reduction)
# are in nonessential.preprocessing, not here.
#
# All augmentation functions include parameter validation using utilities
# from utils.system.io.validation. Transforms are designed to be composable and configurable.


__all__ = [
    'get_blurring_transform',
    'get_color_jittering_transform',
    'get_geometric_transformations_transform',
    'get_noise_addition_transform',
    'AddGaussianNoise'
]