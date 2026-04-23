# results_loader.py
# Results file loading and top N model selection for ensembling

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from modeling.utils import load_results_json
from utils.system import is_kaggle_environment

logger = logging.getLogger(__name__)


def _find_results_file_in_paths(file_name: str, search_paths: List[Path]) -> Optional[Path]:
    """
    Find a results file in the given search paths.
    
    Checks in order:
    1. Direct file match
    2. File in root of search path
    3. File in common subdirectories (dataset_grid_search, hyperparameter_grid_search)
    4. File in model-specific subdirectories (e.g., dinov2/, resnet50/)
    
    Args:
        file_name: Name of the file to find (e.g., 'gridsearch_results.json')
        search_paths: List of directory paths to search
        
    Returns:
        Path to file if found, None otherwise
    """
    for search_path in search_paths:
        if not search_path.exists():
            continue
        
        # Check if search_path is a file (direct match)
        if search_path.is_file() and search_path.name == file_name:
            return search_path
        
        # Check if search_path is a directory
        if search_path.is_dir():
            # Check root of search path
            potential_file = search_path / file_name
            if potential_file.exists():
                return potential_file
            
            # Check common subdirectories
            for subdir in ['dataset_grid_search', 'hyperparameter_grid_search']:
                subdir_file = search_path / subdir / file_name
                if subdir_file.exists():
                    return subdir_file
            
            # Check model-specific subdirectories (e.g., dinov2/, resnet50/)
            # Only check immediate subdirectories to avoid deep recursion
            try:
                for item in search_path.iterdir():
                    if item.is_dir():
                        model_file = item / file_name
                        if model_file.exists():
                            return model_file
            except (PermissionError, OSError):
                # Skip directories we can't access
                continue
    
    return None


def _get_default_search_paths() -> List[Path]:
    """
    Get default search paths for results files.
    
    Priority:
    1. Kaggle input paths (curated/uploaded results)
    2. Working directory output (in-progress results)
    
    Returns:
        List of Path objects to search
    """
    paths = []
    
    from config.path_constants import KAGGLE_WORKING_OUTPUTS, LOCAL_OUTPUTS, KAGGLE_INPUT
    
    # Kaggle input (highest priority - curated results)
    if is_kaggle_environment():
        input_base = KAGGLE_INPUT
        if input_base.exists():
            # Check for csiro-metadata dataset (with model-specific subfolders)
            metadata_input = input_base / 'csiro-metadata'
            if metadata_input.exists():
                # Add model-specific subdirectories
                for model_dir in metadata_input.iterdir():
                    if model_dir.is_dir():
                        paths.append(model_dir)
            
            # Also check root of any input dataset
            for dataset_dir in input_base.iterdir():
                if dataset_dir.is_dir():
                    paths.append(dataset_dir)
    
    # Working directory (fallback - in-progress results)
    if is_kaggle_environment():
        paths.append(KAGGLE_WORKING_OUTPUTS)
    else:
        paths.append(LOCAL_OUTPUTS)
    
    return paths


def load_results_from_files(
    results_files: Optional[List[str]] = None,
    fallback_paths: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    Load results from multiple files, checking Kaggle input first, then working directory.
    
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
    
    3. grid_search/result_analysis.load_results (context-specific):
       - Context-specific wrapper for hyperparameter grid search analysis
       - Uses file_utils.load_json_file directly
       - Adds logging and context-specific error messages
    
    4. ensembling/results_loader.load_results_from_files (this function - complex):
       - Multi-file loader with auto-detection and merging
       - Uses best_variant_utils.load_results_json internally (which uses file_utils.load_json_file)
       - Handles multiple files, auto-detection, merging, deduplication, fallback paths
       - Most complex loader in the hierarchy
    
    This function: Complex multi-file loader that:
    - Auto-detects results files from common locations
    - Loads multiple files using best_variant_utils.load_results_json
    - Merges and deduplicates results by variant_id
    - Provides fallback path searching
    
    Args:
        results_files: Optional list of explicit results file paths.
                      If None, auto-detects from default locations.
        fallback_paths: Optional list of additional paths to search for files.
                       If None, uses default fallback paths.
        
    Returns:
        Merged list of all variant results from all found files
        
    Raises:
        FileNotFoundError: If no results files are found
        ValueError: If results_files contains invalid paths
    """
    all_results = []
    found_files = []
    
    # Build search paths
    search_paths = _get_default_search_paths()
    if fallback_paths:
        for fallback_path in fallback_paths:
            path_obj = Path(fallback_path)
            if path_obj.exists() and path_obj not in search_paths:
                search_paths.append(path_obj)
    
    # If explicit files provided, use them (but still check they exist)
    if results_files:
        _load_explicit_results_files(results_files, search_paths, found_files, all_results)
    else:
        # Auto-detect: look for common results file names
        _load_auto_detected_results_files(search_paths, found_files, all_results)
    
    if not found_files:
        error_msg = (
            "No results files found.\n"
            "Searched locations (in priority order):\n"
        )
        for idx, path in enumerate(search_paths, 1):
            error_msg += f"  {idx}. {path}\n"
        error_msg += (
            "\nNext steps:\n"
            "  1. Upload results files to Kaggle input dataset (highest priority)\n"
            "  2. Run grid search pipelines to generate results files in working directory\n"
            "  3. Provide explicit --results-files argument"
        )
        raise FileNotFoundError(error_msg)
    
    if not all_results:
        raise ValueError("No valid results found in any results file")
    
    # Merge and deduplicate by variant_id
    merged_results = merge_results([all_results])
    
    logger.info(f"Total unique variants loaded: {len(merged_results)}")
    return merged_results


def _load_explicit_results_files(
    results_files: List[str],
    search_paths: List[Path],
    found_files: List[Path],
    all_results: List[Dict[str, Any]]
) -> None:
    """
    Load results from explicitly provided file paths.
    
    Args:
        results_files: List of explicit results file paths
        search_paths: List of paths to search if file not found directly
        found_files: List to append found file paths to
        all_results: List to extend with loaded results
    """
    for file_path_str in results_files:
        file_path = Path(file_path_str)
        
        if file_path.exists():
            found_files.append(file_path)
            logger.info(f"Loading results from explicit path: {file_path}")
            try:
                results = load_results_json(file_path)
                all_results.extend(results)
                logger.info(f"Loaded {len(results)} variants from {file_path}")
            except Exception as e:
                logger.warning(f"Failed to load {file_path}: {e}")
                continue
        else:
            # Try to find it in search paths
            file_name = file_path.name
            found_path = _find_results_file_in_paths(file_name, search_paths)
            if found_path:
                found_files.append(found_path)
                logger.info(f"Found {file_name} at: {found_path}")
                try:
                    results = load_results_json(found_path)
                    all_results.extend(results)
                    logger.info(f"Loaded {len(results)} variants from {found_path}")
                except Exception as e:
                    logger.warning(f"Failed to load {found_path}: {e}")
                    continue
            else:
                logger.warning(f"Results file not found: {file_path_str}")


def _load_auto_detected_results_files(
    search_paths: List[Path],
    found_files: List[Path],
    all_results: List[Dict[str, Any]]
) -> None:
    """
    Auto-detect and load results files from common locations.
    
    Args:
        search_paths: List of paths to search
        found_files: List to append found file paths to
        all_results: List to extend with loaded results
    """
    # Use unified filename format
    default_file_names = [
        'gridsearch_results.json'  # Unified format
    ]
    
    for file_name in default_file_names:
        found_path = _find_results_file_in_paths(file_name, search_paths)
        if found_path:
            found_files.append(found_path)
            logger.info(f"Auto-detected results file: {found_path}")
            try:
                results = load_results_json(found_path)
                all_results.extend(results)
                logger.info(f"Loaded {len(results)} variants from {found_path}")
            except Exception as e:
                logger.warning(f"Failed to load {found_path}: {e}")
                continue


def merge_results(results_list: List[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """
    Merge results from multiple files, deduplicating by variant_id.
    
    If the same variant_id appears in multiple files, keeps the one with the highest cv_score.
    
    Args:
        results_list: List of result lists (one per file)
        
    Returns:
        Merged and deduplicated list of variant results
    """
    variant_dict: Dict[str, Dict[str, Any]] = {}
    
    for results in results_list:
        for variant in results:
            variant_id = variant.get('variant_id')
            if not variant_id:
                logger.warning(f"Skipping variant without variant_id: {variant.get('variant_index', 'unknown')}")
                continue
            
            # If variant already seen, keep the one with higher cv_score
            if variant_id in variant_dict:
                existing_score = variant_dict[variant_id].get('cv_score')
                new_score = variant.get('cv_score')
                
                if existing_score is None:
                    # Existing has no score, replace with new
                    variant_dict[variant_id] = variant
                elif new_score is not None and new_score > existing_score:
                    # New has higher score, replace
                    variant_dict[variant_id] = variant
            else:
                variant_dict[variant_id] = variant
    
    merged = list(variant_dict.values())
    logger.info(f"Merged {len(merged)} unique variants from {len(results_list)} result sets")
    
    return merged


def find_top_n_models(
    results: List[Dict[str, Any]],
    top_n: int = 3,
    metric_key: str = 'cv_score'
) -> List[Dict[str, Any]]:
    """
    Extract top N models sorted by metric.
    
    Args:
        results: List of variant result dictionaries
        top_n: Number of top models to extract (default: 3)
        metric_key: Key to use for sorting (default: 'cv_score')
        
    Returns:
        List of top N variant dictionaries, sorted by metric (descending)
        
    Raises:
        ValueError: If top_n is invalid or no valid results found
    """
    if not isinstance(top_n, int) or top_n < 1:
        raise ValueError(f"top_n must be positive integer, got {top_n}")
    
    if not results:
        raise ValueError("No results provided")
    
    # Filter results with valid scores
    valid_results = [
        r for r in results
        if r.get(metric_key) is not None
        and not (isinstance(r.get(metric_key), float) and (r[metric_key] != r[metric_key]))  # Not NaN
    ]
    
    if not valid_results:
        raise ValueError(f"No valid results found with {metric_key}")
    
    if len(valid_results) < top_n:
        logger.warning(
            f"Only {len(valid_results)} valid results found, but top_n={top_n}. "
            f"Returning all {len(valid_results)} results."
        )
    
    # Sort by metric (descending - higher is better)
    sorted_results = sorted(
        valid_results,
        key=lambda x: x.get(metric_key, -float('inf')),
        reverse=True
    )
    
    top_results = sorted_results[:top_n]
    
    logger.info(
        f"Selected top {len(top_results)} models (from {len(valid_results)} valid, "
        f"{len(results)} total) by {metric_key}"
    )
    
    # Log selected models
    for idx, result in enumerate(top_results, 1):
        variant_id = result.get('variant_id', 'unknown')
        cv_score = result.get('cv_score', 'N/A')
        logger.info(f"  {idx}. {variant_id}: cv_score={cv_score}")
    
    return top_results

