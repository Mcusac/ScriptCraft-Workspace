# augmentation_builders.py
# Augmentation transform builder registry
# Defines builders for augmentation transforms (both PIL and tensor transforms)

from typing import Dict, Callable, Tuple, Any

from config.config import Config
from dataset_manipulation.nonessential.data_augmentation.geometric_transformations import get_geometric_transformations_transform
from dataset_manipulation.nonessential.data_augmentation.color_jittering import get_color_jittering_transform
from dataset_manipulation.nonessential.data_augmentation.blurring import get_blurring_transform
from dataset_manipulation.nonessential.data_augmentation.noise_addition import get_noise_addition_transform

# Type alias for clarity
AugmentationBuilder = Callable[[Config], Tuple[Any, bool]]

# Augmentation transform builders
# Each builder returns (transform, is_tensor_transform) tuple
# is_tensor_transform: True if transform operates on tensors (after ToTensor), False if on PIL Images
# NOTE: Keys must match AVAILABLE_AUGMENTATION
AUGMENTATION_BUILDERS: Dict[str, AugmentationBuilder] = {
    'geometric_transformations': lambda config: (get_geometric_transformations_transform(), False),
    'color_jittering': lambda config: (get_color_jittering_transform(), False),
    'blurring': lambda config: (get_blurring_transform(), False),
    'noise_addition': lambda config: (get_noise_addition_transform(), True),
}

