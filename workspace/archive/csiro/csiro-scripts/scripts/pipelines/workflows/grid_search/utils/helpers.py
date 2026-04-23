# helpers.py
# Common helper functions for grid search pipelines
# Eliminates code duplication across dataset, hyperparameter, and regression grid searches

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

from config.config import Config
from .constants import DATASET_TYPE_FULL
from modeling import (
    find_metadata_dir,
    get_or_create_combo_id,
    extract_preprocessing_augmentation_from_variant
)

logger = logging.getLogger(__name__)


def create_variant_specific_data(
    config: Config,
    preprocessing_list: Optional[List[str]] = None,
    augmentation_list: Optional[List[str]] = None,
    hyperparameters: Optional[Dict[str, Any]] = None,
    feature_filename: Optional[str] = None,
    metadata_dir: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Create variant-specific data dictionary for grid search results.
    
    This function centralizes the creation of variant_specific_data dictionaries
    used in result dictionaries. It handles different grid search types:
    - Dataset/Hyperparameter searches: includes combo_id in data_manipulation
    - Regression searches: includes feature_filename instead
    
    Args:
        config: Configuration object.
        preprocessing_list: Optional list of preprocessing techniques (for dataset/hyperparameter searches).
        augmentation_list: Optional list of augmentation techniques (for dataset/hyperparameter searches).
        hyperparameters: Optional dictionary of hyperparameters. If None, uses default hyperparameters.
        feature_filename: Optional feature filename (for regression searches).
        metadata_dir: Optional metadata directory path. If None, will find automatically.
    
    Returns:
        Dictionary with variant-specific data:
        - dataset_type: Dataset type ('full' or 'split')
        - data_manipulation: Dict with combo_id (for dataset/hyperparameter searches)
        - hyperparameters: Hyperparameters dict
        - feature_filename: Feature filename (for regression searches only)
    
    Raises:
        FileNotFoundError: If metadata_dir is required but not found.
    """
    dataset_type = getattr(config.data, 'dataset_type', DATASET_TYPE_FULL)
    variant_specific_data = {
        'dataset_type': dataset_type
    }
    
    # Handle dataset/hyperparameter searches (need combo_id)
    if preprocessing_list is not None and augmentation_list is not None:
        if metadata_dir is None:
            metadata_dir = find_metadata_dir()
        
        if not metadata_dir:
            raise FileNotFoundError(
                "csiro-metadata directory not found. Cannot create combo_id for variant. "
                "Expected: /kaggle/input/csiro-metadata (Kaggle) or ../csiro-metadata (local)"
            )
        
        combo_id = get_or_create_combo_id(preprocessing_list, augmentation_list, metadata_dir)
        variant_specific_data['data_manipulation'] = {
            'combo_id': combo_id
        }
    
    # Handle hyperparameters
    if hyperparameters is not None:
        variant_specific_data['hyperparameters'] = hyperparameters
    else:
        # Use default hyperparameters if not provided
        from .hyperparameters import get_default_hyperparameters
        variant_specific_data['hyperparameters'] = get_default_hyperparameters()
    
    # Handle regression searches (need feature_filename)
    if feature_filename is not None:
        variant_specific_data['feature_filename'] = feature_filename
    
    return variant_specific_data


def create_variant_key(
    config: Config,
    preprocessing_list: List[str],
    augmentation_list: List[str],
    hyperparameters: Dict[str, Any]
) -> Tuple[str, Tuple[str, ...], Tuple[str, ...], Tuple[Tuple[str, Any], ...]]:
    """
    Create variant key for deduplication in grid searches.
    
    The variant key is a tuple that uniquely identifies a variant based on:
    - Dataset type
    - Preprocessing list (sorted)
    - Augmentation list (sorted)
    - Hyperparameters (sorted items)
    
    Args:
        config: Configuration object.
        preprocessing_list: List of preprocessing techniques.
        augmentation_list: List of augmentation techniques.
        hyperparameters: Dictionary of hyperparameters.
    
    Returns:
        Tuple of (dataset_type, prep_key, aug_key, hyperparams_key) where:
        - dataset_type: String ('full' or 'split')
        - prep_key: Sorted tuple of preprocessing techniques
        - aug_key: Sorted tuple of augmentation techniques
        - hyperparams_key: Sorted tuple of (key, value) pairs from hyperparameters
    """
    dataset_type = getattr(config.data, 'dataset_type', DATASET_TYPE_FULL)
    prep_key = tuple(sorted(preprocessing_list))
    aug_key = tuple(sorted(augmentation_list))
    hyperparams_key = tuple(sorted(hyperparameters.items()))
    variant_key = (dataset_type, prep_key, aug_key, hyperparams_key)
    
    return variant_key


def extract_and_sort_preprocessing_augmentation(
    result: Dict[str, Any],
    metadata_dir: Optional[Path] = None
) -> Optional[Tuple[Tuple[str, ...], Tuple[str, ...]]]:
    """
    Extract and sort preprocessing/augmentation lists from a result dictionary.
    
    This function extracts preprocessing and augmentation lists from a grid search
    result, sorts them, and returns them as tuples. This is used for creating
    variant keys from existing results for deduplication.
    
    Args:
        result: Result dictionary from grid search results file.
        metadata_dir: Optional metadata directory path. If None, will find automatically.
    
    Returns:
        Tuple of (prep_tuple, aug_tuple) if successful, None if extraction fails.
        Both tuples are sorted for consistent comparison.
    
    Raises:
        ValueError: If result format is invalid.
        FileNotFoundError: If metadata directory not found.
    """
    if metadata_dir is None:
        metadata_dir = find_metadata_dir()
    
    if not metadata_dir:
        logger.warning("Metadata directory not found, cannot extract preprocessing/augmentation")
        return None
    
    try:
        prep_list, aug_list = extract_preprocessing_augmentation_from_variant(result, metadata_dir)
        prep_tuple = tuple(sorted(prep_list))
        aug_tuple = tuple(sorted(aug_list))
        return prep_tuple, aug_tuple
    except (ValueError, FileNotFoundError) as e:
        variant_id = result.get('variant_id', 'unknown')
        logger.warning(f"Skipping result {variant_id}: {e}")
        return None


def create_variant_key_from_result(
    result: Dict[str, Any],
    config: Optional[Config] = None
) -> Optional[Tuple[str, Tuple[str, ...], Tuple[str, ...], Tuple[Tuple[str, Any], ...]]]:
    """
    Create variant key from result dictionary for dataset/hyperparameter grid searches.
    
    This function extracts all necessary information from a result dictionary to create
    a variant key for deduplication. It handles the dataset/hyperparameter search pattern
    where variant keys are: (dataset_type, prep_key, aug_key, hyperparams_key)
    
    Args:
        result: Result dictionary from grid search results file.
        config: Optional configuration object. If None, uses DATASET_TYPE_FULL as default.
    
    Returns:
        Variant key tuple (dataset_type, prep_key, aug_key, hyperparams_key) if successful,
        None if result is invalid or extraction fails.
    """
    if 'data_manipulation' not in result or 'hyperparameters' not in result:
        return None
    
    # Extract dataset_type
    if config is not None:
        dataset_type = getattr(config.data, 'dataset_type', DATASET_TYPE_FULL)
    else:
        dataset_type = result.get('dataset_type', DATASET_TYPE_FULL)
    
    # Extract and sort preprocessing/augmentation
    prep_aug_result = extract_and_sort_preprocessing_augmentation(result)
    if prep_aug_result is None:
        return None
    
    prep_key, aug_key = prep_aug_result
    
    # Extract and sort hyperparameters
    hyperparams_key = tuple(sorted(result.get('hyperparameters', {}).items()))
    
    # Create variant key
    variant_key = (dataset_type, prep_key, aug_key, hyperparams_key)
    
    return variant_key


def create_regression_variant_key_from_result(
    result: Dict[str, Any]
) -> Optional[Tuple[str, Tuple[Tuple[str, Any], ...]]]:
    """
    Create variant key from result dictionary for regression grid searches.
    
    This function extracts all necessary information from a result dictionary to create
    a variant key for deduplication. It handles the regression search pattern where
    variant keys are: (feature_filename, hyperparams_key)
    
    Args:
        result: Result dictionary from regression grid search results file.
    
    Returns:
        Variant key tuple (feature_filename, hyperparams_key) if successful,
        None if result is invalid or missing required fields.
    """
    if 'hyperparameters' not in result:
        return None
    
    feature_filename = result.get('feature_filename')
    if feature_filename is None:
        return None
    
    # Extract and sort hyperparameters
    hyperparams_key = tuple(sorted(result.get('hyperparameters', {}).items()))
    
    # Create variant key
    variant_key = (feature_filename, hyperparams_key)
    
    return variant_key
