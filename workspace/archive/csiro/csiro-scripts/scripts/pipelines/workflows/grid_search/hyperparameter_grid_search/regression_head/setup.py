# setup.py
# Setup and configuration for regression grid search

import logging
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from itertools import product

from config.config import Config
from utils.system import set_seed, ensure_dir
from utils.system import load_json_file
from utils.config import validate_pipeline_config
from modeling.grid_search_configs.regression_parameter_grids import get_regression_parameter_grid
from modeling.feature_extraction import find_feature_cache, load_features
from modeling.utils.metadata.regression_metadata import (
    initialize_working_metadata_files
)

logger = logging.getLogger(__name__)


def setup_regression_grid_search(
    config: Config,
    feature_filename: str,
    regression_model_type: str,
    search_type: str,
    grid_search_dir: Optional[Path] = None
) -> Tuple[
    np.ndarray,  # all_features
    np.ndarray,  # all_targets
    np.ndarray,  # fold_assignments
    Dict[str, Any],  # feature_metadata
    str,  # feature_filename
    Path,  # grid_search_dir
    Dict[str, List[Any]],  # param_grid
    List[tuple],  # all_combinations
    int  # starting_index
]:
    """
    Set up regression grid search environment.
    
    Args:
        config: Base configuration object
        feature_filename: Feature filename (e.g., "variant_0100_features.npz")
        regression_model_type: Type of regression model ('lgbm', 'xgboost', 'ridge')
        search_type: Type of grid search ('defaults', 'quick', 'in_depth', 'thorough')
    
    Returns:
        Tuple of setup data needed for grid search execution, including starting_index
        for sequential variant numbering
    """
    # Validate config
    validate_pipeline_config(config, required_sections=['data', 'cv', 'paths', 'grid_search'])
    
    # Validate regression model type
    valid_model_types = {'lgbm', 'xgboost', 'xgb', 'ridge'}
    if regression_model_type not in valid_model_types:
        raise ValueError(
            f"regression_model_type must be one of {valid_model_types}, got {regression_model_type}"
        )
    
    # Normalize model type (xgb -> xgboost)
    if regression_model_type == 'xgb':
        regression_model_type = 'xgboost'
    
    # Validate search type
    valid_search_types = {'defaults', 'quick', 'in_depth', 'thorough'}
    if search_type not in valid_search_types:
        raise ValueError(
            f"search_type must be one of {valid_search_types}, got {search_type}"
        )
    
    # Setup
    set_seed(config.seed)
    config.ensure_dirs()
    
    # Initialize working metadata files (copy from input if needed)
    logger.info("="*60)
    logger.info("Initializing working metadata files")
    logger.info("="*60)
    try:
        metadata_file, gridsearch_file = initialize_working_metadata_files(regression_model_type)
        logger.info(f"Working metadata file: {metadata_file}")
        logger.info(f"Working gridsearch file: {gridsearch_file}")
    except Exception as e:
        logger.warning(f"Failed to initialize working metadata files: {e}. Continuing anyway...")
    
    # Load features from file
    logger.info("="*60)
    logger.info("Loading features from file")
    logger.info("="*60)
    logger.info(f"Feature filename: {feature_filename}")
    
    feature_cache_path = find_feature_cache(feature_filename)
    if feature_cache_path is None:
        raise FileNotFoundError(
            f"Feature cache not found for filename: {feature_filename}\n"
            f"Searched in input and working directories."
        )
    
    logger.info(f"Found feature cache: {feature_cache_path}")
    
    # Load features and metadata
    all_features, all_targets, fold_assignments, feature_metadata = load_features(feature_cache_path)
    
    logger.info(f"Loaded features: {all_features.shape}")
    logger.info(f"Loaded targets: {all_targets.shape}")
    logger.info(f"Feature metadata: {feature_metadata}")
    
    # Feature filename is already provided as parameter
    logger.info("="*60 + "\n")
    
    # Get hyperparameter grid
    param_grid = get_regression_parameter_grid(regression_model_type, search_type)
    
    # Calculate total combinations
    param_names = list(param_grid.keys())
    param_values = list(param_grid.values())
    total_combinations = 1
    for values in param_values:
        total_combinations *= len(values)
    
    logger.info(f"Regression model type: {regression_model_type}")
    logger.info(f"Search type: {search_type}")
    logger.info(f"Total hyperparameter combinations: {total_combinations:,}")
    logger.info(f"Parameter grid: {param_grid}")
    
    # Create grid search output directory (if not provided)
    if grid_search_dir is None:
        grid_search_dir = Path(config.paths.output_dir) / 'regression_grid_search' / regression_model_type
        ensure_dir(grid_search_dir)
    
    # Calculate starting variant_index to ensure sequential numbering
    # Use metadata.json as source of truth for variant definitions
    starting_index = 0
    try:
        from modeling.utils.metadata.regression_metadata import get_writable_metadata_dir
        from utils.system.io import load_json_file
        working_dir = get_writable_metadata_dir() / regression_model_type
        metadata_file = working_dir / 'metadata.json'
        if metadata_file.exists():
            variants = load_json_file(
                metadata_file, expected_type=list, file_type="Regression metadata JSON"
            )
            if variants:
                max_metadata_index = max(
                    (v.get('variant_index', -1) for v in variants if v.get('variant_index') is not None),
                    default=-1
                )
                starting_index = max_metadata_index + 1
                logger.info(f"Found {len(variants)} variants in metadata.json, max variant_index: {max_metadata_index}")
    except Exception as e:
        logger.warning(f"Failed to check metadata.json for variant_index: {e}. Starting from 0.")
    
    logger.info(f"Starting variant_index from {starting_index} (ensuring sequential numbering)")
    
    # Generate all combinations
    all_combinations = list(product(*param_values))
    
    return (
        all_features,
        all_targets,
        fold_assignments,
        feature_metadata,
        feature_filename,
        grid_search_dir,
        param_grid,
        all_combinations,
        starting_index
    )

