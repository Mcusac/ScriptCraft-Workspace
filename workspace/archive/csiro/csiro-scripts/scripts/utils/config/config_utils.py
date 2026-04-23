# config_utils.py
# Configuration utilities - orchestrator module
#
# This module provides a convenience orchestrator function that combines
# validation and application of config updates from CLI arguments.
#
# Design rationale:
# - This is intentionally a thin orchestrator that delegates to focused modules
# - Kept separate to maintain single responsibility in config_validator and config_updater
# - Provides convenient single-entry-point for common pattern (updating config from CLI args)
# - Used primarily in run.py for CLI argument processing
#
# Delegates to focused modules: config_validator, config_updater

from typing import Optional

from config.config import Config

# Import from focused modules
from .config_validator import validate_config_args, validate_pipeline_config
from .config_updater import (
    apply_data_model_overrides,
    apply_preprocessing_augmentation_from_args,
    apply_training_parameter_overrides
)


def update_config_from_args(
    config: Config,
    data_root: Optional[str] = None,
    model_name: Optional[str] = None,
    preprocessing: Optional[str] = None,
    data_augmentation: Optional[str] = None,
    batch_size: Optional[int] = None,
    learning_rate: Optional[float] = None,
    setup_kaggle_paths: bool = True
) -> None:
    """
    Update config from command-line arguments or other sources.
    
    Orchestrates validation and application of all config updates from CLI arguments.
    Delegates to specialized functions for better single responsibility.
    
    Args:
        config: Config object to update. Must not be None and must have all required attributes.
        data_root: Optional data root directory override. Must be non-empty string if provided.
        model_name: Optional model name override. Must be non-empty string if provided.
        preprocessing: Optional comma-separated preprocessing list (e.g., "resize,normalize").
        data_augmentation: Optional comma-separated augmentation list (e.g., "geometric_transformations").
        batch_size: Optional batch size override. Must be positive integer if provided.
        learning_rate: Optional learning rate override. Must be positive float if provided.
        setup_kaggle_paths: If True, automatically set Kaggle paths when on Kaggle (default: True).
        
    Raises:
        ValueError: If config is None, or any parameter has invalid value.
        TypeError: If any parameter has invalid type.
    """
    # Validate config structure (common sections: data, training, model)
    validate_pipeline_config(config)
    
    # Validate argument values
    validate_config_args(data_root, model_name, batch_size, learning_rate)
    
    # Apply Kaggle paths if requested
    if setup_kaggle_paths:
        from ..system.io.paths import apply_kaggle_paths_to_config
        apply_kaggle_paths_to_config(config)
    
    # Apply overrides using focused functions
    apply_data_model_overrides(config, data_root, model_name)
    apply_preprocessing_augmentation_from_args(config, preprocessing, data_augmentation)
    apply_training_parameter_overrides(config, batch_size, learning_rate)

