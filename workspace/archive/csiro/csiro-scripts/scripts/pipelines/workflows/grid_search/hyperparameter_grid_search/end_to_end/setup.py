# setup.py
# Setup and configuration for hyperparameter grid search

import logging
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional

from config.config import Config
from utils.system import ensure_dir
from ...utils.constants import (
    GRID_SEARCH_TYPE_HYPERPARAMETER,
    FOCUSED_SEARCH_TYPES,
    SEARCH_TYPE_IN_DEPTH,
    SEARCH_TYPE_THOROUGH
)
from modeling.grid_search_configs import get_parameter_grid, get_focused_parameter_grid
from modeling.utils import load_model_metadata
from modeling.utils import CSIROModelsStrategy

logger = logging.getLogger(__name__)


def _setup_hyperparameter_grid_search_environment(
    config: Config,
    search_type: str,
    metadata_path: Optional[str],
    results_file: Optional[str]
) -> Tuple[Dict[str, Any], List[str], List[str], Path, Path]:
    """
    Setup hyperparameter grid search environment.
    
    Args:
        config: Configuration object.
        search_type: Type of grid search.
        metadata_path: Optional explicit metadata path.
        results_file: Optional explicit results file path.
        
    Returns:
        Tuple of (metadata_dict, preprocessing_list, augmentation_list, train_csv_path, grid_search_dir).
    """
    # Store train CSV path for reloading per variant (memory efficiency)
    train_csv_path = Path(config.data.data_root) / config.data.train_csv
    logger.info(f"Train data will be loaded per variant from {train_csv_path}")
    
    # Apply memory optimization settings for grid search
    if getattr(config.device, 'reduce_workers_for_memory', False):
        config.device.num_workers = 0
        logger.info("Memory optimization: Reduced num_workers to 0")
    if getattr(config.device, 'disable_pin_memory_for_memory', False):
        config.device.pin_memory = False
        logger.info("Memory optimization: Disabled pin_memory")
    
    # Load dataset configuration from metadata (with config fallback)
    metadata_dict, preprocessing_list, augmentation_list = _load_dataset_configuration(
        metadata_path, results_file, config
    )
    
    # Create grid search output directory
    grid_search_dir = Path(config.paths.output_dir) / GRID_SEARCH_TYPE_HYPERPARAMETER
    ensure_dir(grid_search_dir)
    
    return metadata_dict, preprocessing_list, augmentation_list, train_csv_path, grid_search_dir


def _load_dataset_configuration(
    metadata_path: Optional[str],
    results_file: Optional[str],
    config: Optional[Config] = None
) -> Tuple[Dict[str, Any], List[str], List[str]]:
    """
    Load dataset configuration from metadata or results file, or fallback to config.
    
    Args:
        metadata_path: Optional explicit metadata path.
        results_file: Optional explicit results file path.
        config: Optional config object to use as fallback if metadata not found.
        
    Returns:
        Tuple of (metadata_dict, preprocessing_list, augmentation_list).
    """
    logger.info("="*60)
    logger.info("Loading dataset configuration")
    logger.info("="*60)
    
    metadata_path_obj = None
    results_file_obj = None
    
    # Try explicit metadata_path
    if metadata_path:
        metadata_path_obj = Path(metadata_path)
        if metadata_path_obj.exists():
            logger.info(f"Using explicit metadata path: {metadata_path_obj}")
        else:
            logger.warning(f"Explicit metadata path not found: {metadata_path_obj}, will try auto-detect")
            metadata_path_obj = None
    
    # Try explicit results_file
    if results_file and metadata_path_obj is None:
        results_file_obj = Path(results_file)
        if results_file_obj.exists():
            logger.info(f"Using explicit results file: {results_file_obj}")
        else:
            logger.warning(f"Explicit results file not found: {results_file_obj}, will try auto-detect")
            results_file_obj = None
    
    # Auto-detect from Kaggle inputs if not provided
    if metadata_path_obj is None and results_file_obj is None:
        metadata_path_obj, results_file_obj = _auto_detect_metadata()
    
    # Load metadata using utility function
    metadata_dict = load_model_metadata(
        metadata_path=metadata_path_obj,
        results_file=results_file_obj,
        model_path=None
    )
    
    preprocessing_list = metadata_dict.get('preprocessing_list', [])
    augmentation_list = metadata_dict.get('augmentation_list', [])
    
    # Fallback to config if metadata not found
    if not preprocessing_list and not augmentation_list and config is not None:
        logger.info("No metadata found, using dataset configuration from config object")
        preprocessing_list = getattr(config.data, 'preprocessing_list', []) or []
        augmentation_list = getattr(config.data, 'augmentation_list', []) or []
        metadata_dict = {
            'preprocessing_list': preprocessing_list,
            'augmentation_list': augmentation_list
        }
    
    logger.info(f"\nDataset configuration loaded:")
    logger.info(f"  Preprocessing: {preprocessing_list if preprocessing_list else '[]'}")
    logger.info(f"  Augmentation: {augmentation_list if augmentation_list else '[]'}")
    logger.info(f"  (This configuration will be used for all hyperparameter variants)")
    logger.info("="*60 + "\n")
    
    return metadata_dict, preprocessing_list, augmentation_list


def _auto_detect_metadata() -> Tuple[Optional[Path], Optional[Path]]:
    """
    Auto-detect metadata from Kaggle inputs.
    
    Returns:
        Tuple of (metadata_path, results_file_path).
    """
    logger.info("Auto-detecting model metadata from Kaggle inputs...")
    strategy = CSIROModelsStrategy()
    model_path, detected_metadata_path = strategy.find_model()
    
    metadata_path_obj = None
    results_file_obj = None
    
    if detected_metadata_path and detected_metadata_path.exists():
        metadata_path_obj = detected_metadata_path
        logger.info(f"Auto-detected metadata: {metadata_path_obj}")
    elif model_path:
        # Try to find dataset grid search results near model
        potential_results = model_path.parent / 'gridsearch_results.json'
        if potential_results.exists():
            results_file_obj = potential_results
            logger.info(f"Auto-detected results file: {results_file_obj}")
    
    return metadata_path_obj, results_file_obj


def _get_hyperparameter_grid(
    search_type: str,
    previous_results_file: Optional[str]
) -> Dict[str, List[Any]]:
    """
    Get hyperparameter grid based on search type.
    
    Args:
        search_type: Type of grid search.
        previous_results_file: Optional previous results file for focused searches.
        
    Returns:
        Parameter grid dictionary.
    """
    if search_type in FOCUSED_SEARCH_TYPES:
        # Use focused grid based on previous results
        base_type = SEARCH_TYPE_IN_DEPTH if search_type == 'focused_in_depth' else SEARCH_TYPE_THOROUGH
        logger.info(f"Using focused grid search (base: {base_type})")
        logger.info(f"Analyzing previous results from: {previous_results_file}")
        
        # Get base grid for comparison
        base_grid = get_parameter_grid(base_type)
        
        # Get focused grid
        param_grid = get_focused_parameter_grid(
            base_search_type=base_type,
            previous_results_file=previous_results_file
        )
        
        # Calculate reduction statistics
        base_combinations = _calculate_grid_size(base_grid)
        focused_combinations = _calculate_grid_size(param_grid)
        
        reduction_ratio = focused_combinations / base_combinations if base_combinations > 0 else 0
        reduction_percent = (1 - reduction_ratio) * 100
        
        logger.info(f"Grid search type: {search_type} (focused)")
        logger.info(f"Base grid combinations: {base_combinations:,}")
        logger.info(f"Focused grid combinations: {focused_combinations:,}")
        logger.info(f"Reduction: {reduction_percent:.1f}% ({base_combinations:,} → {focused_combinations:,})")
        logger.info(f"Parameter grid: {param_grid}")
    else:
        # Use standard grid
        param_grid = get_parameter_grid(search_type)
        logger.info(f"Grid search type: {search_type}")
        logger.info(f"Parameter grid: {param_grid}")
    
    return param_grid


def _calculate_grid_size(param_grid: Dict[str, List[Any]]) -> int:
    """
    Calculate total number of combinations in parameter grid.
    
    Args:
        param_grid: Parameter grid dictionary.
        
    Returns:
        Total number of combinations.
    """
    total = 1
    for values in param_grid.values():
        total *= len(values)
    return total

