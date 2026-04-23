# config package
# Configuration utilities
#
# This package handles all configuration-related operations:
# - Loading config from JSON files
# - Validating config structure and CLI arguments
# - Applying config updates (preprocessing, augmentation, overrides)
# - Orchestrating config updates from CLI arguments (convenience function)
#
# Design Notes:
# - config_utils.py provides update_config_from_args() as a convenience orchestrator
#   that combines validation and application of config updates. This is intentionally
#   kept as a thin wrapper to maintain single responsibility in focused modules.
# - validate_config_args() is internal-only (not exported) as it's only used by
#   update_config_from_args(). External code should use validate_pipeline_config().

# Import directly from source modules for clarity
# Import orchestrator function from config_utils

__all__ = [
    'apply_preprocessing_to_config',
    'apply_augmentation_to_config',
    'apply_data_model_overrides',
    'apply_preprocessing_augmentation_from_args',
    'apply_training_parameter_overrides',
    'apply_dataset_config_to_config',
    'apply_combo_to_config',
    'validate_pipeline_config',
    'validate_config_section',
    'update_config_from_args'
]

