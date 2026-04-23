# __init__.py
# Configuration package
#
# Provides dataclass-based configuration management with validation.
#
# Components:
# - config: Main Config dataclass combining all configuration sections.
#   Supports dynamic updates from dictionaries and command-line arguments.
#   Includes validation and directory management utilities.
#
# Configuration sections:
# - ModelConfig: Model architecture, pretrained weights, input size, num_classes
# - TrainingConfig: Batch size, learning rate, epochs, early stopping, optimizer
# - DataConfig: Data paths, preprocessing/augmentation lists, image size
# - CVConfig: Cross-validation settings (n_folds, shuffle, random_state)
# - PathConfig: Output directories (model, output, log, submission)
# - EvaluationConfig: Metric and loss function settings
# - DeviceConfig: GPU/CPU device preferences
# - GridSearchConfig: Grid search parameters
#
# Configuration can be set via CLI arguments, JSON files, or programmatically.
# All paths are automatically adjusted for Kaggle vs local environments.


# Re-export configuration utilities from utils.config for convenience

# Re-export CSIRO-specific config from contest.csiro for convenience

__all__ = [
    'Config',
    'get_default_config',
    'default_config',
    'ModelConfig',
    'TrainingConfig',
    'DataConfig',
    'CVConfig',
    'PathConfig',
    'EvaluationConfig',
    'DeviceConfig',
    'GridSearchConfig',
    'ProgressConfig',
    'ProgressVerbosity',
    # Evaluation constants
    'TARGET_WEIGHTS',
    # Model constants
    'MODEL_NAME_TO_PRETRAINED',
    'get_pretrained_weights_path',
    'get_model_name_from_pretrained',
    # Path constants
    'KAGGLE_WORKING',
    'KAGGLE_INPUT',
    'KAGGLE_WORKING_OUTPUTS',
    'KAGGLE_WORKING_MODELS',
    'KAGGLE_WORKING_LOGS',
    'KAGGLE_WORKING_DATASETS',
    'KAGGLE_WORKING_BEST_MODEL',
    'KAGGLE_WORKING_SUBMISSION',
    'KAGGLE_WORKING_WEIGHTS',
    'KAGGLE_INPUT_SCRIPTS',
    'KAGGLE_INPUT_BIOMASS',
    'KAGGLE_INPUT_CSIRO_MODELS',
    'KAGGLE_INPUT_WEIGHTS',
    'LOCAL_OUTPUTS',
    'LOCAL_MODELS',
    'LOCAL_LOGS',
    'LOCAL_DATASETS',
    'LOCAL_BIOMASS',
    'LOCAL_SCRIPTS',
    'SUBMISSION_FILE_NAME',
    'BEST_MODEL_DIR_NAME',
    'RESULTS_FILE_NAME',
    'METADATA_FILE_NAME',
    'BEST_MODEL_FILE_NAME',
    # Configuration utilities
    'apply_preprocessing_to_config',
    'apply_augmentation_to_config',
    'update_config_from_args',
    'validate_pipeline_config',
    # CSIRO-specific config
    'CSIROConfig',
    'get_csiro_config'
]