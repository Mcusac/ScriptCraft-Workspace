# grid_search_utils.py
# Shared utilities for grid search pipelines

import logging
from typing import Dict, Any

from config.config import Config

logger = logging.getLogger(__name__)

# Mapping from grid search parameter names to config paths (section.attribute)
GRID_SEARCH_PARAM_MAPPING = {
    'learning_rate': ('training', 'learning_rate'),
    'batch_size': ('training', 'batch_size'),
    'optimizer': ('training', 'optimizer'),
    'weight_decay': ('training', 'weight_decay'),
    'loss_function': ('training', 'loss_function'),
    'scheduler': ('training', 'scheduler'),
    'scheduler_factor': ('training', 'scheduler_factor'),
    'scheduler_patience': ('training', 'scheduler_patience'),
    'early_stopping_patience': ('training', 'early_stopping_patience'),
    'num_epochs': ('training', 'num_epochs'),
}


def apply_hyperparameters_to_config(config: Config, hyperparameters: Dict[str, Any]) -> None:
    """
    Apply hyperparameters from grid search to config using update_from_dict.
    
    Args:
        config: Configuration object to update. Must not be None.
        hyperparameters: Dictionary of hyperparameter names to values.
                        Keys must be valid hyperparameter names from GRID_SEARCH_PARAM_MAPPING.
        
    Raises:
        ValueError: If config is None or hyperparameters dict is invalid.
        TypeError: If hyperparameters is not a dict.
    """
    # Validate inputs
    if config is None:
        raise ValueError("config cannot be None")
    
    if not isinstance(hyperparameters, dict):
        raise TypeError(f"hyperparameters must be dict, got {type(hyperparameters)}")
    
    # Convert flat hyperparameters to nested config structure
    config_updates: Dict[str, Dict[str, Any]] = {}
    
    for param_name, param_value in hyperparameters.items():
        if param_name in GRID_SEARCH_PARAM_MAPPING:
            section, attribute = GRID_SEARCH_PARAM_MAPPING[param_name]
            if section not in config_updates:
                config_updates[section] = {}
            config_updates[section][attribute] = param_value
        else:
            logger.warning(f"Unknown hyperparameter: {param_name}, skipping")
    
    # Apply updates using config's update_from_dict method
    if config_updates:
        config.update_from_dict(config_updates)


def get_default_hyperparameters() -> Dict[str, Any]:
    """
    Get default training hyperparameters from TrainingConfig.
    
    Returns:
        Dictionary mapping hyperparameter names to default values.
    """
    from config.config import TrainingConfig
    defaults = TrainingConfig()
    return {
        'learning_rate': defaults.learning_rate,
        'batch_size': defaults.batch_size,
        'optimizer': defaults.optimizer,
        'weight_decay': defaults.weight_decay,
        'loss_function': defaults.loss_function,
        'scheduler': defaults.scheduler,
        'scheduler_factor': defaults.scheduler_factor,
        'scheduler_patience': defaults.scheduler_patience,
        'early_stopping_patience': defaults.early_stopping_patience,
        'num_epochs': defaults.num_epochs
    }

