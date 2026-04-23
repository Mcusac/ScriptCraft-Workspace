# __init__.py
# Grid search utilities package
#
# Provides shared utilities for all grid search types:
# - constants: Grid search constants
# - helpers: Common helper functions
# - hyperparameters: Hyperparameter utilities


__all__ = [
    # Constants
    'GRID_SEARCH_TYPE_DATASET',
    'GRID_SEARCH_TYPE_HYPERPARAMETER',
    'SEARCH_TYPE_DEFAULTS',
    'SEARCH_TYPE_QUICK',
    'SEARCH_TYPE_IN_DEPTH',
    'SEARCH_TYPE_THOROUGH',
    'SEARCH_TYPE_FOCUSED_IN_DEPTH',
    'SEARCH_TYPE_FOCUSED_THOROUGH',
    'VALID_HYPERPARAMETER_SEARCH_TYPES',
    'FOCUSED_SEARCH_TYPES',
    'DATASET_TYPE_FULL',
    'DATASET_TYPE_SPLIT',
    'RESULTS_FILE_GRIDSEARCH',
    'GRID_SEARCH_TYPE_FIELD_DATASET',
    'GRID_SEARCH_TYPE_FIELD_HYPERPARAMETER',
    'BEST_VARIANT_FILE_DATASET',
    'BEST_HYPERPARAMETERS_FILE',
    'MODEL_DIR_DATASET_GRID_SEARCH',
    'MODEL_DIR_HYPERPARAMETER_GRID_SEARCH',
    'DEFAULT_KEEP_TOP_VARIANTS',
    'DEFAULT_CLEANUP_INTERVAL',
    # Helpers
    'create_variant_specific_data',
    'create_variant_key',
    'extract_and_sort_preprocessing_augmentation',
    'create_variant_key_from_result',
    'create_regression_variant_key_from_result',
    # Hyperparameters
    'apply_hyperparameters_to_config',
    'get_default_hyperparameters',
    'GRID_SEARCH_PARAM_MAPPING'
]
