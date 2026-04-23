# dataset_cache_utils.py
# Utilities for dataset caching and grid generation

import hashlib
import logging
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any
from itertools import combinations

import pandas as pd

from ..system.io.paths import is_kaggle_environment
from .preprocessing_utils import AVAILABLE_PREPROCESSING, AVAILABLE_AUGMENTATION
from ..system.io.files import save_json_file

logger = logging.getLogger(__name__)


def generate_cache_key(
    preprocessing_list: List[str],
    augmentation_list: List[str],
    image_size: int,
    fold: int
) -> str:
    """
    Create hash-based cache key from preprocessing/augmentation config.
    
    Args:
        preprocessing_list: List of preprocessing technique names
        augmentation_list: List of augmentation technique names
        image_size: Image size (width/height)
        fold: Fold number
        
    Returns:
        Cache key string (hex digest)
    """
    # Sort lists for consistent hashing
    sorted_preprocessing = sorted(preprocessing_list)
    sorted_augmentation = sorted(augmentation_list)
    
    # Create deterministic string representation
    key_str = (
        f"preprocessing:{','.join(sorted_preprocessing)}|"
        f"augmentation:{','.join(sorted_augmentation)}|"
        f"image_size:{image_size}|"
        f"fold:{fold}"
    )
    
    # Generate hash
    key_hash = hashlib.md5(key_str.encode()).hexdigest()
    return key_hash


def get_dataset_cache_dir() -> Path:
    """
    Return cache directory path based on environment.
    
    Returns:
        Path to dataset cache directory
        - Kaggle: /kaggle/working/datasets
        - Local: output/datasets
    """
    from config.path_constants import KAGGLE_WORKING_DATASETS, LOCAL_DATASETS
    
    if is_kaggle_environment():
        cache_dir = KAGGLE_WORKING_DATASETS
    else:
        cache_dir = LOCAL_DATASETS
    
    return cache_dir


def save_dataset_splits(
    train_data: pd.DataFrame,
    val_data: pd.DataFrame,
    cache_key: str,
    metadata: Optional[Dict[str, Any]] = None
) -> Path:
    """
    Save train/val DataFrames to parquet with metadata JSON.
    
    Args:
        train_data: Training DataFrame
        val_data: Validation DataFrame
        cache_key: Cache key for this dataset variant
        metadata: Optional metadata dictionary to save
        
    Returns:
        Path to cache directory for this variant
    """
    cache_dir = get_dataset_cache_dir()
    variant_cache_dir = cache_dir / cache_key
    variant_cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Save DataFrames
    train_path = variant_cache_dir / 'train.parquet'
    val_path = variant_cache_dir / 'val.parquet'
    
    train_data.to_parquet(train_path, index=False)
    val_data.to_parquet(val_path, index=False)
    
    logger.info(f"Saved dataset splits to {variant_cache_dir}")
    logger.info(f"  Train: {len(train_data)} samples")
    logger.info(f"  Val: {len(val_data)} samples")
    
    # Save metadata if provided
    if metadata:
        metadata_path = variant_cache_dir / 'metadata.json'
        save_json_file(metadata, metadata_path, file_type="Dataset metadata JSON")
    
    return variant_cache_dir


def load_dataset_splits(cache_key: str) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Load cached splits if available.
    
    Args:
        cache_key: Cache key for this dataset variant
        
    Returns:
        Tuple of (train_data, val_data) if found, None otherwise
    """
    cache_dir = get_dataset_cache_dir()
    variant_cache_dir = cache_dir / cache_key
    
    train_path = variant_cache_dir / 'train.parquet'
    val_path = variant_cache_dir / 'val.parquet'
    
    if not train_path.exists() or not val_path.exists():
        return None
    
    try:
        train_data = pd.read_parquet(train_path)
        val_data = pd.read_parquet(val_path)
        
        logger.info(f"Loaded cached dataset splits from {variant_cache_dir}")
        logger.info(f"  Train: {len(train_data)} samples")
        logger.info(f"  Val: {len(val_data)} samples")
        
        return train_data, val_data
    except Exception as e:
        logger.warning(f"Failed to load cached splits from {variant_cache_dir}: {e}")
        return None


def _generate_power_set(items: List[str]) -> List[Tuple[str, ...]]:
    """
    Generate all possible subsets (power set) of items.
    
    Args:
        items: List of items
        
    Returns:
        List of tuples, each representing a subset (sorted for consistency)
    """
    power_set = []
    n = len(items)
    
    # Generate all combinations of all sizes (0 to n)
    for r in range(n + 1):
        for combo in combinations(items, r):
            power_set.append(tuple(sorted(combo)))
    
    return power_set


def get_max_augmentation_variant() -> Tuple[List[str], List[str]]:
    """
    Get the maximally augmented variant (all preprocessing + all augmentation).
    
    Returns the variant with all optional preprocessing methods and all augmentation
    methods enabled. This is useful for quick testing of maximum augmentation's impact
    on model generalization without running the full grid search.
    
    Note: 'resize' and 'normalize' are always applied automatically and not included
    in the preprocessing list.
    
    Returns:
        Tuple of (preprocessing_list, augmentation_list) with all options enabled.
        Both lists are sorted for consistency.
    """
    # Define always-applied preprocessing methods (not part of grid search)
    ALWAYS_APPLIED_PREPROCESSING = {'resize', 'normalize'}
    
    # Get all preprocessing options and filter out always-applied methods
    all_preprocessing = sorted(list(AVAILABLE_PREPROCESSING))
    # Only include optional preprocessing methods
    preprocessing_options = [
        opt for opt in all_preprocessing 
        if opt not in ALWAYS_APPLIED_PREPROCESSING
    ]
    
    # Get all augmentation options
    augmentation_options = sorted(list(AVAILABLE_AUGMENTATION))
    
    logger.info(f"Max augmentation variant:")
    logger.info(f"  Preprocessing: {preprocessing_options}")
    logger.info(f"  Augmentation: {augmentation_options}")
    
    return (preprocessing_options, augmentation_options)


def get_dataset_variant_grid() -> List[Tuple[List[str], List[str]]]:
    """
    Return grid of all preprocessing/augmentation combinations to test.
    
    Generates combinations for optional preprocessing methods only (excludes 'resize' and 'normalize'
    which are always applied). The number of combinations is computed dynamically based on:
    - Optional preprocessing methods (all methods except 'resize' and 'normalize')
    - All augmentation methods
    
    Each generates a power set (all possible subsets), and the cartesian product gives the total grid.
    
    Note: 'resize' and 'normalize' are always applied automatically and not part of the grid.
    When preprocessing_list is empty, DEFAULT_PREPROCESSING_LIST (which includes 'resize') is used.
    
    Returns:
        List of tuples (preprocessing_list, augmentation_list)
        Each list is sorted for consistency
    """
    # Define always-applied preprocessing methods (not part of grid search)
    ALWAYS_APPLIED_PREPROCESSING = {'resize', 'normalize'}
    
    # Get all preprocessing options and filter out always-applied methods
    all_preprocessing = sorted(list(AVAILABLE_PREPROCESSING))
    # Only include optional preprocessing methods
    preprocessing_options = [
        opt for opt in all_preprocessing 
        if opt not in ALWAYS_APPLIED_PREPROCESSING
    ]
    
    # Get all augmentation options
    augmentation_options = sorted(list(AVAILABLE_AUGMENTATION))
    
    # Generate power sets (all subsets)
    preprocessing_combinations = _generate_power_set(preprocessing_options)
    augmentation_combinations = _generate_power_set(augmentation_options)
    
    # Calculate counts dynamically
    num_optional_preprocessing = len(preprocessing_options)
    num_augmentation = len(augmentation_options)
    num_preprocessing_combinations = len(preprocessing_combinations)
    num_augmentation_combinations = len(augmentation_combinations)
    total_combinations = num_preprocessing_combinations * num_augmentation_combinations
    
    # Generate cartesian product
    grid = []
    for prep_combo in preprocessing_combinations:
        for aug_combo in augmentation_combinations:
            grid.append((list(prep_combo), list(aug_combo)))
    
    logger.info(f"Generated dataset variant grid: {total_combinations} combinations")
    logger.info(f"  Optional preprocessing methods: {num_optional_preprocessing} → {num_preprocessing_combinations} combinations")
    logger.info(f"  Augmentation methods: {num_augmentation} → {num_augmentation_combinations} combinations")
    logger.info(f"  Total: {num_preprocessing_combinations} × {num_augmentation_combinations} = {total_combinations}")
    
    return grid

