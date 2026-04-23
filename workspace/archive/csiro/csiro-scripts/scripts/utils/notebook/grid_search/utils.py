# utils.py
# Grid search utilities
#
# Provides utilities for grid search operations:
# - calculate_focused_grid_size: Calculate focused grid size before running search
# - auto_detect_grid_search_results: Auto-detect grid search results files

import logging
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

from utils.system.io.paths import get_output_path, is_kaggle_environment
from ..core import calculate_total_combinations

logger = logging.getLogger(__name__)

# Import from modeling package (absolute import - modeling is at same level as utils)
# This import is optional and only used in calculate_focused_grid_size()
# Wrap in try/except to allow utils.system to be imported even if modeling isn't available yet
# (e.g., when utils is imported before scripts/ is added to sys.path)
try:
    from modeling.grid_search_configs import get_parameter_grid, get_focused_parameter_grid
    _MODELING_AVAILABLE = True
except ImportError:
    # Graceful fallback - modeling will be imported lazily when needed
    _MODELING_AVAILABLE = False
    get_parameter_grid = None
    get_focused_parameter_grid = None


def calculate_focused_grid_size(
    base_search_type: str,
    previous_results_file: str,
    top_n_results: int = 10,
    range_expansion_factor: float = 1.5,
    min_values_per_param: int = 2
) -> Tuple[Dict[str, List[Any]], int, Optional[int]]:
    """
    Calculate focused grid size before running search.
    
    Args:
        base_search_type: Base search type ('in_depth' or 'thorough')
        previous_results_file: Path to previous results.json file
        top_n_results: Number of top results to analyze (default: 10)
        range_expansion_factor: Factor to expand numeric ranges (default: 1.5)
        min_values_per_param: Minimum values to keep per parameter (default: 2)
        
    Returns:
        Tuple of (focused_grid, focused_combinations, base_combinations)
        base_combinations is None if base_search_type is invalid
    """
    try:
        # Lazy import if not available at module load time
        if not _MODELING_AVAILABLE:
            from modeling.grid_search_configs import get_parameter_grid, get_focused_parameter_grid
        
        # Get base grid for comparison
        base_grid = get_parameter_grid(base_search_type)
        base_combinations = calculate_total_combinations(base_grid)
        
        # Get focused grid
        focused_grid = get_focused_parameter_grid(
            base_search_type=base_search_type,
            previous_results_file=previous_results_file,
            top_n_results=top_n_results,
            range_expansion_factor=range_expansion_factor,
            min_values_per_param=min_values_per_param
        )
        focused_combinations = calculate_total_combinations(focused_grid)
        
        return focused_grid, focused_combinations, base_combinations
    except Exception as e:
        logger.warning(f"⚠️ Error calculating focused grid size: {e}")
        return {}, 0, None


def auto_detect_grid_search_results(dataset_type: str = 'split', model_name: Optional[str] = None) -> str:
    """
    Auto-detect grid search results files from Kaggle input directory.
    
    Priority: hyperparameter results (includes both dataset config and hyperparameters) > dataset results
    
    Checks /kaggle/input/ FIRST (curated/uploaded results), then /kaggle/working/output/ (in-progress results).
    Uses flat folder structure: output/{grid_search_type}/{filename_with_dataset_type}.json
    
    Args:
        dataset_type: Dataset type ('full' or 'split')
        model_name: Optional model name for model-specific folder structure.
                   If provided, checks {model_name}/ folder first, then root.
        
    Returns:
        Path to best available results file
        
    Raises:
        FileNotFoundError: If no results files are found
    """
    checked_paths = []
    
    if is_kaggle_environment():
        # Check /kaggle/input/ FIRST (curated/uploaded metadata)
        base_dir = Path('/kaggle/input/csiro-metadata')
        
        # Try model-specific folder first if model_name provided
        if model_name:
            model_specific_dir = base_dir / model_name
            # Check metadata.json file
            metadata_file = model_specific_dir / 'metadata.json'
            checked_paths.append(str(metadata_file))
            if metadata_file.exists():
                results_file = str(metadata_file)
                logger.info(f"✅ Found model metadata in model-specific folder: {results_file}")
                return results_file
        
        # Then check /kaggle/working/output/ (in-progress grid search)
        # Check unified format first (new)
        working_unified_hyperparam = Path(f'/kaggle/working/output/hyperparameter_grid_search/gridsearch_results.json')
        working_unified_dataset = Path(f'/kaggle/working/output/dataset_grid_search/gridsearch_results.json')
        checked_paths.append(str(working_unified_hyperparam))
        checked_paths.append(str(working_unified_dataset))
        
        if working_unified_hyperparam.exists():
            logger.info(f"✅ Found in-progress unified hyperparameter grid search: {working_unified_hyperparam}")
            logger.info("   (Includes both dataset and hyperparameter results)")
            return str(working_unified_hyperparam)
        elif working_unified_dataset.exists():
            logger.info(f"✅ Found in-progress unified dataset grid search: {working_unified_dataset}")
            logger.info("   (Includes both dataset and hyperparameter results)")
            return str(working_unified_dataset)
    else:
        # Local fallback to working directory output
        # Check unified format first (new)
        unified_hyperparam_file = Path(get_output_path('output/hyperparameter_grid_search/gridsearch_results.json'))
        unified_dataset_file = Path(get_output_path('output/dataset_grid_search/gridsearch_results.json'))
        checked_paths.append(str(unified_hyperparam_file))
        checked_paths.append(str(unified_dataset_file))
        
        if unified_hyperparam_file.exists():
            results_file = str(unified_hyperparam_file)
            logger.info(f"✅ Found unified hyperparameter grid search results: {results_file}")
            logger.info("   (Includes both dataset and hyperparameter results)")
            return results_file
        elif unified_dataset_file.exists():
            results_file = str(unified_dataset_file)
            logger.info(f"✅ Found unified dataset grid search results: {results_file}")
            logger.info("   (Includes both dataset and hyperparameter results)")
            return results_file
    
    # Build error message with all checked locations in order
    error_msg = (
        "No grid search results found.\n"
        "Checked paths (in order):\n"
    )
    for idx, path in enumerate(checked_paths, 1):
        status = "❌"
        error_msg += f"  {idx}. {path} {status}\n"
    
    error_msg += (
        "\nNext steps:\n"
        "  - Upload grid search results to Kaggle input dataset\n"
        "  - Or run grid search pipeline to generate new results\n"
    )
    
    raise FileNotFoundError(error_msg)

