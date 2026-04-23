# commands package
# Command builders for notebook cells
#
# Provides functions to build CLI command lists for various pipelines:
# - grid_search: Grid search command builders
# - ensemble: Ensemble command builders
# - submission: Submission command builders


__all__ = [
    'build_hyperparameter_grid_search_command',
    'build_dataset_grid_search_command',
    'build_regression_grid_search_command',
    'build_ensemble_command',
    'build_regression_ensemble_command',
    'build_stacking_command',
    'build_stacking_ensemble_command',
    'build_hybrid_stacking_command',
    'build_end_to_end_submission_command',
    'build_regression_submission_command',
    'detect_submission_model_path',
    'build_train_and_export_command',
    'build_feature_extraction_train_command',
    'build_multi_variant_regression_train_command'
]

