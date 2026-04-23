# setup.py
# Environment and directory setup utilities for grid search

import logging
from pathlib import Path
from typing import Tuple, Any

from utils.system import set_seed, get_device, get_device_info, ensure_dir

logger = logging.getLogger(__name__)


def setup_environment_helper(config, grid_search_type_fn) -> Tuple[Any, Path, Path, Any]:
    """
    Set up grid search environment.
    
    Args:
        config: Configuration object
        grid_search_type_fn: Function that returns grid search type string
    
    Returns:
        Tuple of (device, base_model_dir, grid_search_dir, device_info).
    """
    # Setup seeds
    set_seed(config.seed)
    config.ensure_dirs()
    
    # Apply memory optimization settings
    apply_memory_optimizations(config)
    
    # Device setup
    device = get_device(config.device.device)
    device_info = get_device_info()
    logger.info(f"Device info: {device_info}")
    
    # Normalize base model directory
    base_model_dir = normalize_base_model_dir(config, grid_search_type_fn())
    
    # Create grid search output directory
    grid_search_dir = create_grid_search_dir(config, grid_search_type_fn())
    
    return device, base_model_dir, grid_search_dir, device_info


def apply_memory_optimizations(config) -> None:
    """
    Apply memory optimization settings for grid search.
    
    Reduces num_workers and disables pin_memory if configured.
    """
    if getattr(config.device, 'reduce_workers_for_memory', False):
        config.device.num_workers = 0
        logger.info("Memory optimization: Reduced num_workers to 0")
    if getattr(config.device, 'disable_pin_memory_for_memory', False):
        config.device.pin_memory = False
        logger.info("Memory optimization: Disabled pin_memory")


def normalize_base_model_dir(config, grid_search_type: str) -> Path:
    """
    Normalize base model directory to prevent path nesting.
    
    Args:
        config: Configuration object
        grid_search_type: Grid search type string
    
    Returns:
        Normalized base model directory path.
    """
    base_model_dir = Path(config.paths.model_dir)
    if base_model_dir.name == grid_search_type:
        base_model_dir = base_model_dir.parent
        logger.info(f"Normalized base model directory: {base_model_dir} (removed trailing '{grid_search_type}')")
    return base_model_dir


def create_grid_search_dir(config, grid_search_type: str) -> Path:
    """
    Create grid search output directory.
    
    Args:
        config: Configuration object
        grid_search_type: Grid search type string
    
    Returns:
        Path to grid search directory.
    """
    dataset_type = getattr(config.data, 'dataset_type', 'split')
    grid_search_dir = Path(config.paths.output_dir) / f'{grid_search_type}_{dataset_type}'
    ensure_dir(grid_search_dir)
    return grid_search_dir
