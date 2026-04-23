# data package
# Data-related utilities
#
# This package contains utilities for data processing:
# - Preprocessing/augmentation parsing and validation
# - Dataset variant caching and grid generation
#
# Cross-package dependency:
# - config_updater imports from this package to validate preprocessing/augmentation names
#   This is acceptable as config operations need to validate data-related settings.

# image_utils and loading_utils moved to dataset_manipulation.utils

__all__ = [
    'parse_preprocessing_list',
    'parse_augmentation_list',
    'validate_preprocessing_names',
    'validate_augmentation_names',
    'DEFAULT_PREPROCESSING_LIST',
    'AVAILABLE_PREPROCESSING',
    'AVAILABLE_AUGMENTATION',
    'generate_cache_key',
    'get_dataset_cache_dir',
    'save_dataset_splits',
    'load_dataset_splits',
    'get_dataset_variant_grid',
    'get_max_augmentation_variant',
]

