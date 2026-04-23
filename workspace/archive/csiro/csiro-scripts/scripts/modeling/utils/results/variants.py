# variant_utils.py
# Utilities for variant ID and key operations
#
# This module consolidates variant-related operations that were previously
# scattered across grid search execution files. It provides centralized
# functions for creating variant IDs, variant keys, and parsing variant information.

import logging
from typing import List, Tuple, Optional

logger = logging.getLogger(__name__)

# Variant ID formats (moved here to avoid circular imports)
VARIANT_ID_FORMAT = 'variant_{index:04d}'
COMBINATION_ID_FORMAT = 'combo_{index:04d}'


def create_variant_id(index: int, is_combination: bool = False) -> str:
    """
    Create variant ID from index.
    
    Args:
        index: Variant/combination index (0-based)
        is_combination: If True, uses combo format (combo_0000), else variant format (variant_0000)
        
    Returns:
        Variant ID string (e.g., "variant_0000" or "combo_0000")
    """
    if is_combination:
        return COMBINATION_ID_FORMAT.format(index=index)
    else:
        return VARIANT_ID_FORMAT.format(index=index)


def create_variant_key(
    preprocessing_list: List[str],
    augmentation_list: List[str]
) -> Tuple[Tuple[str, ...], Tuple[str, ...]]:
    """
    Create variant key from preprocessing and augmentation lists.
    
    Variant key is used for deduplication and comparison. Lists are sorted
    to ensure consistent keys regardless of input order.
    
    Args:
        preprocessing_list: List of preprocessing technique names
        augmentation_list: List of augmentation technique names
        
    Returns:
        Tuple of (sorted_preprocessing_tuple, sorted_augmentation_tuple)
    """
    return (
        tuple(sorted(preprocessing_list)),
        tuple(sorted(augmentation_list))
    )


def parse_variant_id(variant_id: str) -> Tuple[Optional[int], bool]:
    """
    Parse variant ID to extract index and type.
    
    Args:
        variant_id: Variant ID string (e.g., "variant_0000", "combo_0001")
        
    Returns:
        Tuple of (index, is_combination):
        - index: Extracted index (0-based) or None if parsing fails
        - is_combination: True if combo format, False if variant format
        
    Examples:
        >>> parse_variant_id("variant_0000")
        (0, False)
        >>> parse_variant_id("combo_0001")
        (1, True)
        >>> parse_variant_id("invalid")
        (None, False)
    """
    try:
        if variant_id.startswith('combo_'):
            index_str = variant_id.replace('combo_', '')
            index = int(index_str)
            return index, True
        elif variant_id.startswith('variant_'):
            index_str = variant_id.replace('variant_', '')
            index = int(index_str)
            return index, False
        else:
            logger.warning(f"Unknown variant ID format: {variant_id}")
            return None, False
    except (ValueError, AttributeError) as e:
        logger.warning(f"Failed to parse variant ID {variant_id}: {e}")
        return None, False


def is_valid_variant_id(variant_id: str) -> bool:
    """
    Check if variant ID has valid format.
    
    Args:
        variant_id: Variant ID string to validate
        
    Returns:
        True if valid format, False otherwise
    """
    index, _ = parse_variant_id(variant_id)
    return index is not None


def normalize_variant_id(variant_id: str) -> Optional[str]:
    """
    Normalize variant ID to standard format.
    
    Handles common variations like "variant_0" -> "variant_0000"
    
    Args:
        variant_id: Variant ID string (may be in non-standard format)
        
    Returns:
        Normalized variant ID string, or None if cannot be normalized
    """
    index, is_combination = parse_variant_id(variant_id)
    if index is None:
        return None
    
    return create_variant_id(index, is_combination)

