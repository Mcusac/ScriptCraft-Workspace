# __init__.py
# Grid search configuration package
#
# Provides parameter grid definitions for hyperparameter grid searches.
# This package contains grid definitions and result analysis utilities,
# separate from the grid search pipeline execution logic.
#
# Components:
# - parameter_grids: Hyperparameter grid definitions (get_parameter_grid, get_focused_parameter_grid)
# - regression_parameter_grids: Regression model hyperparameter grid definitions
# - result_analysis: Result analysis for focused grid searches (analyze_results_for_focused_grid)
# - Dataset variant grid: Delegates to dataset_cache_utils for consistency
#
# Grid definitions are separated from pipeline logic to allow easy modification
# of search spaces without changing pipeline code.
#
# Note: Grid search pipeline execution is in pipelines/workflows/grid_search/

from typing import List, Tuple



def get_dataset_variant_grid() -> List[Tuple[List[str], List[str]]]:
    """
    Get dataset variant grid (all preprocessing/augmentation combinations).
    
    Delegates to dataset_cache_utils for consistency.
    
    Returns:
        List of tuples (preprocessing_list, augmentation_list)
    """
    from utils.data.dataset_cache_utils import get_dataset_variant_grid as _get_grid
    return _get_grid()


__all__ = [
    'get_parameter_grid',
    'get_focused_parameter_grid',
    'analyze_results_for_focused_grid',
    'get_dataset_variant_grid'
]

