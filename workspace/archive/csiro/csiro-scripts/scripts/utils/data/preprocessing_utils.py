# preprocessing_utils.py
# Utilities for parsing and applying preprocessing/augmentation configurations

import logging
from typing import List, Optional

# Import constants from data package (single source of truth)
from dataset_manipulation.nonessential.constants import (
    AVAILABLE_PREPROCESSING,
    AVAILABLE_AUGMENTATION
)

logger = logging.getLogger(__name__)


def _parse_list(list_str: Optional[str]) -> List[str]:
    """
    Parse comma-separated list string.
    
    Args:
        list_str: Comma-separated string (e.g., "resize,normalize") or None/empty string
        
    Returns:
        List of names (empty list if None/empty)
    """
    if not list_str or list_str.strip() == '':
        return []
    
    # Split by comma and strip whitespace
    parsed_list = [name.strip() for name in list_str.split(',')]
    # Remove empty strings
    parsed_list = [name for name in parsed_list if name]
    
    return parsed_list


def parse_preprocessing_list(preprocessing_str: Optional[str]) -> List[str]:
    """
    Parse comma-separated preprocessing list.
    
    Args:
        preprocessing_str: Comma-separated string (e.g., "resize,normalize") or None/empty string
        
    Returns:
        List of preprocessing technique names (empty list if None/empty)
    """
    return _parse_list(preprocessing_str)


def parse_augmentation_list(augmentation_str: Optional[str]) -> List[str]:
    """
    Parse comma-separated augmentation list.
    
    Args:
        augmentation_str: Comma-separated string (e.g., "geometric_transformations,color_jittering") or None/empty string
        
    Returns:
        List of augmentation technique names (empty list if None/empty)
    """
    return _parse_list(augmentation_str)


def _validate_names(names: List[str], available: set, category: str) -> bool:
    """
    Validate technique names against available set.
    
    Args:
        names: List of technique names to validate
        available: Set of available technique names
        category: Category name for error messages (e.g., "preprocessing", "augmentation")
        
    Returns:
        True if all names are valid
        
    Raises:
        ValueError: If any name is invalid
    """
    invalid_names = [name for name in names if name not in available]
    if invalid_names:
        raise ValueError(
            f"Invalid {category} technique(s): {invalid_names}. "
            f"Available: {sorted(available)}"
        )
    return True


def validate_preprocessing_names(names: List[str]) -> bool:
    """
    Validate preprocessing technique names.
    
    Args:
        names: List of preprocessing technique names
        
    Returns:
        True if all names are valid
        
    Raises:
        ValueError: If any name is invalid
    """
    return _validate_names(names, AVAILABLE_PREPROCESSING, "preprocessing")


def validate_augmentation_names(names: List[str]) -> bool:
    """
    Validate augmentation technique names.
    
    Args:
        names: List of augmentation technique names
        
    Returns:
        True if all names are valid
        
    Raises:
        ValueError: If any name is invalid
    """
    return _validate_names(names, AVAILABLE_AUGMENTATION, "augmentation")

