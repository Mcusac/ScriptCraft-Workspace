# parameter_grids.py
# Parameter grid definitions for hyperparameter grid search

from typing import Dict, List, Any
from .result_analysis import analyze_results_for_focused_grid
from config.config import TrainingConfig


def _get_training_defaults() -> Dict[str, Any]:
    """
    Get default training parameter values from TrainingConfig.
    
    Returns:
        Dictionary mapping parameter names to default values from TrainingConfig.
    """
    defaults = TrainingConfig()
    return {
        'learning_rate': defaults.learning_rate,
        'batch_size': defaults.batch_size,
        'optimizer': defaults.optimizer,
        'weight_decay': defaults.weight_decay,
        'loss_function': defaults.loss_function,
        'scheduler': defaults.scheduler,
        'scheduler_factor': defaults.scheduler_factor,
        'scheduler_patience': defaults.scheduler_patience,
        'early_stopping_patience': defaults.early_stopping_patience,
        'num_epochs': defaults.num_epochs
    }


def get_parameter_grid(search_type: str = "quick") -> Dict[str, List[Any]]:
    """
    Get parameter grid for grid search.
    
    Uses dict merge to build grids: base defaults + varied parameters.
    Only varied parameters need to be specified for each search type.
    All search types include ALL 10 parameters. For parameters not being varied,
    a single default value is used to ensure consistent result structure.
    
    Args:
        search_type: Type of grid search ('defaults', 'quick', 'in_depth', 'thorough', 
                    'focused_in_depth', or 'focused_thorough')
            - 'defaults': Single combination with all default hyperparameters (baseline)
            - 'quick': Small grid (varies learning_rate, batch_size, weight_decay)
            - 'in_depth': Medium grid (varies more hyperparameters)
            - 'thorough': Comprehensive grid (varies all hyperparameters)
            - 'focused_in_depth': Focused in-depth grid based on previous results
            - 'focused_thorough': Focused thorough grid based on previous results
    
    Returns:
        Dictionary mapping hyperparameter names to lists of values to try.
        All 10 parameters are always included.
    """
    defaults = _get_training_defaults()
    
    # Base grid: all parameters with single default value
    base_grid = {param: [value] for param, value in defaults.items()}
    
    if search_type == 'defaults':
        # Return base grid as-is (single combination)
        return base_grid
    
    elif search_type == 'quick':
        # Quick search: Vary only key transformer hyperparameters
        varied = {
            'learning_rate': [5e-5, 1e-4, 2e-4],  # Lower LR for transformers
            'batch_size': [8, 16],  # Smaller batch sizes for memory-intensive models
            'weight_decay': [0.01, 0.05],  # Higher weight decay for ViTs
        }
        # Merge: base_grid values overridden by varied values
        return {**base_grid, **varied}
    
    elif search_type == 'in_depth':
        varied = {
            'learning_rate': [1e-5, 5e-5, 1e-4, 5e-4, 1e-3, 5e-3, 1e-2],
            'batch_size': [8, 16, 32, 64, 128],
            'optimizer': ['AdamW', 'Adam', 'SGD'],
            'weight_decay': [0, 1e-5, 1e-4, 1e-3],
            'scheduler_factor': [0.1, 0.5, 0.7],
            'scheduler_patience': [3, 5, 7, 10],
        }
        return {**base_grid, **varied}
    
    elif search_type == 'thorough':
        varied = {
            'learning_rate': [1e-5, 5e-5, 1e-4, 5e-4, 1e-3, 5e-3],
            'batch_size': [16, 32, 64],
            'optimizer': ['AdamW', 'Adam', 'SGD'],
            'weight_decay': [0, 1e-5, 1e-4, 1e-3],
            'loss_function': ['SmoothL1Loss', 'MSELoss'],
            'scheduler': ['ReduceLROnPlateau', 'CosineAnnealingLR'],
            'scheduler_factor': [0.1, 0.5, 0.7],
            'scheduler_patience': [3, 5, 7, 10],
            'early_stopping_patience': [5, 10, 15],
            'num_epochs': [50, 100, 150]
        }
        return {**base_grid, **varied}
    
    elif search_type in {'focused_in_depth', 'focused_thorough'}:
        raise ValueError(
            f"search_type '{search_type}' requires previous_results_file. "
            f"Use get_focused_parameter_grid() instead."
        )
    else:
        raise ValueError(
            f"Unknown search_type: {search_type}. "
            f"Must be 'defaults', 'quick', 'in_depth', 'thorough', "
            f"'focused_in_depth', or 'focused_thorough'"
        )


def get_focused_parameter_grid(
    base_search_type: str,
    previous_results_file: str,
    top_n_results: int = 10,
    range_expansion_factor: float = 1.5,
    min_values_per_param: int = 2
) -> Dict[str, List[Any]]:
    """
    Get focused parameter grid based on previous grid search results.
    
    Analyzes top N results from a previous search and creates a narrowed parameter
    grid around the best-performing combinations. This dramatically reduces the
    search space while maintaining exploration around promising regions.
    
    Args:
        base_search_type: Base search type to use as template ('in_depth' or 'thorough')
            - 'in_depth': Focused version of in_depth search
            - 'thorough': Focused version of thorough search
        previous_results_file: Path to previous results.json file
        top_n_results: Number of top results to analyze (default: 10)
        range_expansion_factor: Factor to expand numeric ranges around top values (default: 1.5)
        min_values_per_param: Minimum values to keep per parameter (default: 2)
        
    Returns:
        Dictionary mapping hyperparameter names to lists of focused values.
        All 10 parameters are always included.
        
    Raises:
        ValueError: If base_search_type is not 'in_depth' or 'thorough'
        FileNotFoundError: If previous_results_file doesn't exist
    """
    if base_search_type not in {'in_depth', 'thorough'}:
        raise ValueError(
            f"base_search_type must be 'in_depth' or 'thorough', got {base_search_type}"
        )
    
    # Get base grid to determine which parameters should be varied
    base_grid = get_parameter_grid(base_search_type)
    
    # Analyze previous results to get focused ranges
    focused_ranges = analyze_results_for_focused_grid(
        results_file=previous_results_file,
        top_n=top_n_results,
        range_expansion_factor=range_expansion_factor,
        min_values_per_param=min_values_per_param
    )
    
    # Merge focused ranges with base grid
    # For parameters in base grid that are being varied, use focused ranges
    # For parameters not in base grid (single default), keep the default
    focused_grid = {}
    
    for param_name in base_grid.keys():
        if param_name in focused_ranges:
            # Use focused range from analysis
            focused_grid[param_name] = focused_ranges[param_name]
        else:
            # Keep base grid value (should be single default for non-varied params)
            focused_grid[param_name] = base_grid[param_name]
    
    # Ensure all parameters from base grid are included
    # (focused_ranges might have additional params, but we stick to base grid structure)
    
    return focused_grid

