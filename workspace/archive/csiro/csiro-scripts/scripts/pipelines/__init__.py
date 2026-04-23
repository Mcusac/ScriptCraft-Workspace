# __init__.py
# Pipelines package
#
# High-level pipeline orchestration for training, testing, and grid search.
# Pipelines combine multiple components (data loading, training, evaluation)
# into complete workflows.
#
# Architecture:
# - atomic/: Single-responsibility operations (train, test, export)
# - workflows/: Orchestrations of atomic operations
#
# This module provides a central registry for all pipeline entry points,
# allowing consumers to import pipelines from a single location:
#   from pipelines import train_pipeline, ensemble_pipeline, ...

# Atomic pipelines

# Workflow pipelines

# Grid search pipelines

__all__ = [
    # Atomic
    'train_pipeline',
    'test_pipeline',
    'export_model_pipeline',
    # Workflows
    'train_test_pipeline',
    'train_and_export_pipeline',
    'ensemble_pipeline',
    'ensemble_pipeline_from_paths',
    'regression_ensemble_pipeline',
    'stacking_pipeline',
    'stacking_ensemble_pipeline',
    'hybrid_stacking_pipeline',
    'multi_variant_regression_training_pipeline',
    'submit_best_variant_pipeline',
    'submit_lightweight_pipeline',
    # Grid search
    'dataset_grid_search_pipeline',
    'test_max_augmentation_pipeline',
    'hyperparameter_grid_search_pipeline',
    'regression_grid_search_pipeline',
]
