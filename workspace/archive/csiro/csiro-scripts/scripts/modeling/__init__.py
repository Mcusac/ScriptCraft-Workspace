# __init__.py
# Modeling package
#
# Provides model architectures, training, inference, and grid search functionality.
#
# Sub-packages:
# - models: Model architectures organized by type (end_to_end, regression_head)
# - training: Training logic and cross-validation utilities
# - testing: Inference and submission generation
# - grid_search_configs: Parameter grid definitions for hyperparameter and dataset searches
#
# This package provides a facade for common modeling operations, allowing
# consumers to import frequently-used functions from a single location.

# Models

# Training

# Training utilities (checkpoints, OOM handling, cleanup)

# Feature extraction

# Testing/Inference

# Ensembling

# Grid search configurations

# Evaluation

# Metadata utilities

__all__ = [
    # Models
    'TimmModel',
    'create_model',
    # Training
    'BaseModelTrainer',
    'FeatureExtractionTrainer',
    'create_kfold_splits',
    'get_fold_data',
    # Training utils
    'is_checkpoint_complete',
    'get_fold_checkpoint_path',
    'find_best_fold_from_scores',
    'is_oom_error',
    'handle_oom_error_with_retry',
    'cleanup_grid_search_checkpoints_retroactive',
    'delete_variant_directory',
    # Feature extraction
    'FeatureExtractor',
    # Testing
    'run_inference',
    'expand_predictions_to_submission_format',
    'create_submission',
    # Ensembling
    'Ensemble',
    'create_ensemble_from_results',
    'create_ensemble_from_paths',
    # Grid search configs
    'get_parameter_grid',
    'get_dataset_variant_grid',
    # Evaluation
    'weighted_r2_score',
    'calc_metric',
    'r2_score_per_target',
    'get_loss_function',
    'TARGET_WEIGHTS',
    'TARGET_ORDER',
    'PRIMARY_TARGETS',
    'DERIVED_TARGETS',
    'ALL_TARGETS',
    'compute_derived_target_values',
    # Metadata utilities
    'find_metadata_dir',
    'get_writable_metadata_dir',
    'extract_preprocessing_augmentation_from_variant',
    'get_or_create_combo_id',
    'find_combo_id',
    'get_combo_details',
    'load_data_manipulation_combos'
]

