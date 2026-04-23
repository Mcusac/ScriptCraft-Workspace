# config_validator.py
# Configuration validation utilities

from typing import Optional, List
from config.config import Config
from ..system.io.validation import validate_positive


def validate_config_args(
    data_root: Optional[str] = None,
    model_name: Optional[str] = None,
    batch_size: Optional[int] = None,
    learning_rate: Optional[float] = None
) -> None:
    """
    Validate command-line argument values.
    
    Args:
        data_root: Optional data root directory override.
        model_name: Optional model name override.
        batch_size: Optional batch size override.
        learning_rate: Optional learning rate override.
        
    Raises:
        ValueError: If any parameter has invalid value.
        TypeError: If any parameter has invalid type.
    """
    if data_root is not None:
        if not isinstance(data_root, str) or not data_root:
            raise ValueError(f"data_root must be non-empty string, got {data_root}")
    
    if model_name is not None:
        if not isinstance(model_name, str) or not model_name:
            raise ValueError(f"model_name must be non-empty string, got {model_name}")
    
    if batch_size is not None:
        if not isinstance(batch_size, int):
            raise TypeError(f"batch_size must be integer, got {type(batch_size)}")
        validate_positive(batch_size, "batch_size")
    
    if learning_rate is not None:
        validate_positive(learning_rate, "learning_rate")


def validate_config_section(config: Config, section_name: str) -> None:
    """
    Validate that a config object has a specific section that is not None.
    
    Common validation pattern used across multiple files to check for
    required config sections.
    
    Args:
        config: Configuration object to validate. Must not be None.
        section_name: Name of the section to validate (e.g., 'data', 'training').
        
    Raises:
        ValueError: If config is None, section is missing, or section is None.
    """
    if config is None:
        raise ValueError("config cannot be None")
    
    if not hasattr(config, section_name):
        raise ValueError(f"config.{section_name} is missing")
    
    section_value = getattr(config, section_name)
    if section_value is None:
        raise ValueError(f"config.{section_name} cannot be None")


def validate_pipeline_config(
    config: Config,
    required_sections: Optional[List[str]] = None
) -> None:
    """
    Validate that a config object has all required sections for pipeline execution.
    
    Common validation pattern used across all pipelines to ensure config
    has necessary attributes before execution.
    
    Consolidates previous validate_config_structure functionality:
    - If required_sections is None, validates common structure: ['data', 'training', 'model']
    - Otherwise validates the explicitly provided sections
    
    Args:
        config: Configuration object to validate.
        required_sections: List of required section names (e.g., ['data', 'paths', 'training']).
                          If None, validates common structure: ['data', 'training', 'model'].
        
    Raises:
        ValueError: If config is None or missing required sections.
    """
    if config is None:
        raise ValueError("config cannot be None")
    
    if required_sections is None:
        required_sections = ['data', 'training', 'model']
    
    for section_name in required_sections:
        validate_config_section(config, section_name)

