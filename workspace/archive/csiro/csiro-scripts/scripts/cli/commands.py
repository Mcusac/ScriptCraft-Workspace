# commands.py
# Command definitions for CLI routing

from enum import Enum


class Command(Enum):
    """Enumeration of valid CLI commands."""
    TRAIN = 'train'
    TEST = 'test'
    TRAIN_TEST = 'train_test'
    DATASET_GRID_SEARCH = 'dataset_grid_search'
    HYPERPARAMETER_GRID_SEARCH = 'hyperparameter_grid_search'
    CLEANUP_GRID_SEARCH = 'cleanup_grid_search'
    SUBMIT_BEST = 'submit_best'
    TRAIN_AND_EXPORT = 'train_and_export'
    EXPORT_MODEL = 'export_model'
    SUBMIT = 'submit'
    ENSEMBLE = 'ensemble'
    REGRESSION_GRID_SEARCH = 'regression_grid_search'
    REGRESSION_ENSEMBLE = 'regression_ensemble'
    STACKING = 'stacking'
    STACKING_ENSEMBLE = 'stacking_ensemble'
    HYBRID_STACKING = 'hybrid_stacking'
    MULTI_VARIANT_REGRESSION_TRAIN = 'multi_variant_regression_train'
    
    @classmethod
    def from_string(cls, value: str) -> 'Command':
        """
        Get Command enum from string value.
        
        Args:
            value: String command name.
            
        Returns:
            Command enum value.
            
        Raises:
            ValueError: If value is not a valid command.
        """
        try:
            return cls(value)
        except ValueError:
            valid_commands = ', '.join([cmd.value for cmd in cls])
            raise ValueError(
                f"Unknown command: '{value}'. "
                f"Valid commands: {valid_commands}"
            )

