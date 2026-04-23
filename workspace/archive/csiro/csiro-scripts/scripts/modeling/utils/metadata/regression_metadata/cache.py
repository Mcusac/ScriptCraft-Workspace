# cache.py
# Caching utilities for regression metadata loading

import logging
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple

from utils.system.io import load_json_file
from ..data_manipulation_loader import find_metadata_dir

logger = logging.getLogger(__name__)

# Module-level cache for input metadata files
# Key: regression_model_type, Value: (variants_list, file_mtime, file_path)
_input_metadata_cache: Dict[str, Tuple[List[Dict[str, Any]], float, Path]] = {}
_input_gridsearch_cache: Dict[str, Tuple[List[Dict[str, Any]], float, Path]] = {}


def _load_cached_input_metadata(regression_model_type: str) -> List[Dict[str, Any]]:
    """
    Load input metadata.json with caching based on file modification time.
    
    Caches the input metadata file per regression_model_type to avoid reloading
    on every grid search iteration. Cache is invalidated if file modification time changes.
    
    Args:
        regression_model_type: Type of regression model ('lgbm', 'xgboost', 'ridge')
        
    Returns:
        List of variant dictionaries from input metadata.json, or empty list if file doesn't exist
    """
    # Find input metadata directory
    input_metadata_dir = find_metadata_dir()
    if not input_metadata_dir or not str(input_metadata_dir).startswith('/kaggle/input'):
        return []
    
    input_metadata_file = input_metadata_dir / regression_model_type / 'metadata.json'
    
    if not input_metadata_file.exists():
        return []
    
    # Check cache validity
    cache_key = regression_model_type
    if cache_key in _input_metadata_cache:
        cached_variants, cached_mtime, cached_path = _input_metadata_cache[cache_key]
        if cached_path == input_metadata_file:
            try:
                current_mtime = os.path.getmtime(input_metadata_file)
                if current_mtime == cached_mtime:
                    # Cache is valid, return cached data
                    logger.debug(f"Using cached input metadata for {regression_model_type}")
                    return cached_variants
            except OSError:
                # File may have been deleted, fall through to reload
                pass
    
    # Cache miss or invalid - load from file
    variants = load_json_file(
        input_metadata_file, expected_type=list, file_type="Regression metadata JSON"
    )
    
    # Update cache
    try:
        file_mtime = os.path.getmtime(input_metadata_file)
        _input_metadata_cache[cache_key] = (variants, file_mtime, input_metadata_file)
        logger.info(f"Loaded {len(variants)} variants from input metadata directory (cached)")
    except OSError:
        # If we can't get mtime, still cache but with 0 mtime
        _input_metadata_cache[cache_key] = (variants, 0.0, input_metadata_file)
        logger.info(f"Loaded {len(variants)} variants from input metadata directory (cached, mtime unavailable)")
    
    return variants


def _load_cached_input_gridsearch(regression_model_type: str) -> List[Dict[str, Any]]:
    """
    Load input gridsearch_metadata.json with caching based on file modification time.
    
    Caches the input gridsearch metadata file per regression_model_type to avoid reloading
    on every grid search iteration. Cache is invalidated if file modification time changes.
    
    Args:
        regression_model_type: Type of regression model ('lgbm', 'xgboost', 'ridge')
        
    Returns:
        List of result dictionaries from input gridsearch_metadata.json, or empty list if file doesn't exist
    """
    # Find input metadata directory
    input_metadata_dir = find_metadata_dir()
    if not input_metadata_dir or not str(input_metadata_dir).startswith('/kaggle/input'):
        return []
    
    input_gridsearch_file = input_metadata_dir / regression_model_type / 'gridsearch_metadata.json'
    
    if not input_gridsearch_file.exists():
        return []
    
    # Check cache validity
    cache_key = regression_model_type
    if cache_key in _input_gridsearch_cache:
        cached_results, cached_mtime, cached_path = _input_gridsearch_cache[cache_key]
        if cached_path == input_gridsearch_file:
            try:
                current_mtime = os.path.getmtime(input_gridsearch_file)
                if current_mtime == cached_mtime:
                    # Cache is valid, return cached data
                    logger.debug(f"Using cached input gridsearch metadata for {regression_model_type}")
                    return cached_results
            except OSError:
                # File may have been deleted, fall through to reload
                pass
    
    # Cache miss or invalid - load from file
    results = load_json_file(
        input_gridsearch_file, expected_type=list, file_type="Regression gridsearch metadata JSON"
    )
    
    # Update cache
    try:
        file_mtime = os.path.getmtime(input_gridsearch_file)
        _input_gridsearch_cache[cache_key] = (results, file_mtime, input_gridsearch_file)
        logger.info(f"Loaded {len(results)} results from input gridsearch metadata (cached)")
    except OSError:
        # If we can't get mtime, still cache but with 0 mtime
        _input_gridsearch_cache[cache_key] = (results, 0.0, input_gridsearch_file)
        logger.info(f"Loaded {len(results)} results from input gridsearch metadata (cached, mtime unavailable)")
    
    return results
