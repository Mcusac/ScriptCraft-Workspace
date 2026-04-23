# result_analysis.py
# Result analysis utilities for narrowing parameter grids based on previous results

import logging
from pathlib import Path
from typing import Dict, List, Any, Union
import statistics

from utils.system import load_json_file

logger = logging.getLogger(__name__)

# Parameter types for range calculation
NUMERIC_PARAMS = {
    'learning_rate', 'batch_size', 'weight_decay', 'scheduler_factor',
    'scheduler_patience', 'early_stopping_patience', 'num_epochs'
}

CATEGORICAL_PARAMS = {
    'optimizer', 'loss_function', 'scheduler'
}


def load_results(results_file: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Load grid search results from JSON file.
    
    Results Loading Hierarchy:
    This function is part of a hierarchy of results loading utilities:
    
    1. file_utils.load_json_file (base):
       - Generic JSON file loader with validation
       - Handles file existence, JSON parsing, type validation
       - Used by all higher-level loaders
    
    2. best_variant_utils.load_results_json (simple wrapper):
       - Simple wrapper around file_utils.load_json_file
       - Adds context-specific type validation (expects list)
       - Used for single-file results loading
    
    3. grid_search_configs/result_analysis.load_results (this function - context-specific):
       - Context-specific wrapper for hyperparameter grid search analysis
       - Uses file_utils.load_json_file directly
       - Adds logging and context-specific error messages
       - Used specifically for hyperparameter grid search result analysis
    
    4. ensembling/results_loader.load_results_from_files (complex):
       - Multi-file loader with auto-detection
       - Uses best_variant_utils.load_results_json internally
       - Handles merging, deduplication, fallback paths
    
    This function: Context-specific wrapper that delegates to file_utils.load_json_file
    with hyperparameter grid search analysis context.
    
    Args:
        results_file: Path to results.json file (string or Path object)
        
    Returns:
        List of result dictionaries
        
    Raises:
        FileNotFoundError: If results file doesn't exist
        ValueError: If results file is invalid
        json.JSONDecodeError: If file is not valid JSON
    """
    results = load_json_file(results_file, expected_type=list, file_type="Results JSON")
    logger.info(f"Loaded {len(results)} results from {results_file}")
    return results


def extract_top_results(
    results: List[Dict[str, Any]],
    top_n: int = 10,
    metric_key: str = 'cv_score'
) -> List[Dict[str, Any]]:
    """
    Extract top N performing results sorted by metric.
    
    Args:
        results: List of result dictionaries
        top_n: Number of top results to extract (default: 10)
        metric_key: Key to use for sorting (default: 'cv_score')
        
    Returns:
        List of top N result dictionaries, sorted by metric (descending)
    """
    # Filter results with valid scores
    valid_results = [
        r for r in results
        if r.get(metric_key) is not None and not (isinstance(r.get(metric_key), float) and (r[metric_key] != r[metric_key]))
    ]
    
    if not valid_results:
        raise ValueError(f"No valid results found with {metric_key}")
    
    # Sort by metric (descending - higher is better)
    sorted_results = sorted(
        valid_results,
        key=lambda x: x.get(metric_key, -float('inf')),
        reverse=True
    )
    
    top_results = sorted_results[:top_n]
    logger.info(f"Extracted top {len(top_results)} results (from {len(valid_results)} valid)")
    
    return top_results


def extract_parameter_ranges(
    top_results: List[Dict[str, Any]],
    range_expansion_factor: float = 1.5,
    min_values_per_param: int = 2
) -> Dict[str, List[Any]]:
    """
    Extract parameter ranges from top results.
    
    For numeric parameters: creates a focused range around min/max/median values
    from top results, expanded by range_expansion_factor.
    
    For categorical parameters: keeps only values that appear in top results.
    
    Args:
        top_results: List of top result dictionaries
        range_expansion_factor: Factor to expand numeric ranges (default: 1.5)
        min_values_per_param: Minimum values to keep per parameter (default: 2)
        
    Returns:
        Dictionary mapping parameter names to lists of focused values
    """
    if not top_results:
        raise ValueError("No top results provided")
    
    # Extract all hyperparameters from first result (all should have same structure)
    first_result = top_results[0]
    hyperparameters = first_result.get('hyperparameters', {})
    
    if not hyperparameters:
        raise ValueError("No hyperparameters found in results")
    
    param_names = list(hyperparameters.keys())
    focused_ranges = {}
    
    for param_name in param_names:
        # Extract values for this parameter from top results
        param_values = [
            r.get('hyperparameters', {}).get(param_name)
            for r in top_results
            if r.get('hyperparameters', {}).get(param_name) is not None
        ]
        
        if not param_values:
            logger.warning(f"No values found for parameter {param_name} in top results")
            continue
        
        if param_name in NUMERIC_PARAMS:
            focused_ranges[param_name] = _extract_numeric_range(
                param_values, range_expansion_factor, min_values_per_param, param_name
            )
        elif param_name in CATEGORICAL_PARAMS:
            focused_ranges[param_name] = _extract_categorical_values(
                param_values, min_values_per_param, param_name
            )
        else:
            # Unknown parameter type - keep all values from top results
            unique_values = sorted(list(set(param_values)), key=str)
            focused_ranges[param_name] = unique_values
            logger.debug(
                f"Parameter {param_name}: "
                f"unknown type, keeping {len(unique_values)} values: {unique_values}"
            )
    
    return focused_ranges


def _extract_numeric_range(
    param_values: List[Any],
    range_expansion_factor: float,
    min_values_per_param: int,
    param_name: str
) -> List[float]:
    """
    Extract focused numeric range from parameter values.
    
    Args:
        param_values: List of parameter values from top results
        range_expansion_factor: Factor to expand numeric ranges
        min_values_per_param: Minimum values to keep per parameter
        param_name: Name of parameter (for logging)
        
    Returns:
        Sorted list of focused numeric values
    """
    numeric_values = [float(v) for v in param_values]
    min_val = min(numeric_values)
    max_val = max(numeric_values)
    median_val = statistics.median(numeric_values)
    
    # Calculate expanded range
    range_size = max_val - min_val
    if range_size == 0:
        # All values are the same, create small range around the value
        center = min_val
        expanded_min = center * (1 / range_expansion_factor)
        expanded_max = center * range_expansion_factor
    else:
        # Expand range around min/max
        center = (min_val + max_val) / 2
        half_range = (range_size / 2) * range_expansion_factor
        expanded_min = max(0, center - half_range)  # Ensure non-negative
        expanded_max = center + half_range
    
    # Generate focused values around the range
    # Include min, median, max from top results, plus expanded boundaries
    focused_values = set()
    
    # Add original top values
    focused_values.update(numeric_values)
    
    # Add expanded boundaries if they're different
    if expanded_min < min_val:
        focused_values.add(expanded_min)
    if expanded_max > max_val:
        focused_values.add(expanded_max)
    
    # Convert to sorted list
    focused_list = sorted(list(focused_values))
    
    # Ensure minimum number of values
    if len(focused_list) < min_values_per_param:
        # Add more values around the range
        step = (expanded_max - expanded_min) / (min_values_per_param - 1)
        for i in range(min_values_per_param):
            val = expanded_min + i * step
            focused_values.add(val)
        focused_list = sorted(list(focused_values))
    
    logger.debug(
        f"Parameter {param_name}: "
        f"original range [{min_val:.6f}, {max_val:.6f}], "
        f"expanded to [{expanded_min:.6f}, {expanded_max:.6f}], "
        f"{len(focused_list)} values"
    )
    
    return focused_list


def _extract_categorical_values(
    param_values: List[Any],
    min_values_per_param: int,
    param_name: str
) -> List[Any]:
    """
    Extract unique categorical values from parameter values.
    
    Args:
        param_values: List of parameter values from top results
        min_values_per_param: Minimum values to keep per parameter
        param_name: Name of parameter (for logging)
        
    Returns:
        Sorted list of unique categorical values
    """
    unique_values = sorted(list(set(param_values)))
    
    # Ensure minimum number of values
    if len(unique_values) < min_values_per_param:
        # If we have fewer than minimum, keep all we have
        logger.warning(
            f"Parameter {param_name} has only {len(unique_values)} unique values "
            f"in top results (minimum requested: {min_values_per_param})"
        )
    
    logger.debug(
        f"Parameter {param_name}: "
        f"keeping {len(unique_values)} values from top results: {unique_values}"
    )
    
    return unique_values


def analyze_results_for_focused_grid(
    results_file: str,
    top_n: int = 10,
    range_expansion_factor: float = 1.5,
    min_values_per_param: int = 2,
    metric_key: str = 'cv_score'
) -> Dict[str, List[Any]]:
    """
    Analyze previous grid search results and return focused parameter ranges.
    
    This is the main entry point for result-based grid filtering.
    
    Args:
        results_file: Path to previous results.json file
        top_n: Number of top results to analyze (default: 10)
        range_expansion_factor: Factor to expand numeric ranges (default: 1.5)
        min_values_per_param: Minimum values to keep per parameter (default: 2)
        metric_key: Key to use for sorting results (default: 'cv_score')
        
    Returns:
        Dictionary mapping parameter names to lists of focused values
    """
    # Load results
    results = load_results(results_file)
    
    # Extract top results
    top_results = extract_top_results(results, top_n=top_n, metric_key=metric_key)
    
    # Extract focused parameter ranges
    focused_ranges = extract_parameter_ranges(
        top_results,
        range_expansion_factor=range_expansion_factor,
        min_values_per_param=min_values_per_param
    )
    
    logger.info(f"Generated focused parameter ranges for {len(focused_ranges)} parameters")
    
    return focused_ranges

