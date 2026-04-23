# __init__.py
# Training package
#
# Provides core training logic and cross-validation utilities.
#
# Components:
# - BaseModelTrainer: Core training loop with early stopping, checkpointing,
#   learning rate scheduling, and metric calculation. Supports single and
#   multi-GPU training via DataParallel.
# - cv_splits: K-fold cross-validation splitting with optional
#   stratification. Handles data aggregation and fold assignment.
#
# The trainer is designed to be reusable across different model architectures
# and training configurations, with all hyperparameters provided via Config.


__all__ = [
    'BaseModelTrainer',
    'FeatureExtractionTrainer',
    'create_trainer',
    'create_kfold_splits',
    'get_fold_data',
    'create_optimizer',
    'create_scheduler',
    'create_dataloaders'
]