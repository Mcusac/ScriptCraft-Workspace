# __init__.py
# Grid search pipelines package
#
# Provides unified access to all grid search pipeline execution:
# - Dataset grid search: Tests preprocessing/augmentation combinations
# - Hyperparameter grid search (end-to-end): Tests hyperparameter combinations with fixed dataset config
# - Regression grid search: Tests hyperparameter combinations for regression models with pre-extracted features
#
# All grid search pipelines share common infrastructure via GridSearchBase.
#
# Note: Parameter grid definitions are in modeling/grid_search_configs/
# This package contains the execution/orchestration logic.


__all__ = [
    # Pipeline functions
    'dataset_grid_search_pipeline',
    'hyperparameter_grid_search_pipeline',
    'regression_grid_search_pipeline',
    # Base class
    'GridSearchBase',
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
    'BEST_VARIANT_FILE_DATASET',
    'BEST_HYPERPARAMETERS_FILE',
    'MODEL_DIR_DATASET_GRID_SEARCH',
    'MODEL_DIR_HYPERPARAMETER_GRID_SEARCH',
    'VARIANT_ID_FORMAT',
    'COMBINATION_ID_FORMAT',
    'DEFAULT_KEEP_TOP_VARIANTS',
    'DEFAULT_CLEANUP_INTERVAL'
]

