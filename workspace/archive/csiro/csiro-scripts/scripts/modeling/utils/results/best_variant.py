# best_variant_utils.py
# Utilities for finding and working with best variants from grid search results

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from ...training.utils.results import find_best_fold_from_scores
from utils.system.io import load_json_file
from ..metadata.data_manipulation_loader import (
    find_metadata_dir,
    extract_preprocessing_augmentation_from_variant
)

logger = logging.getLogger(__name__)


def load_results_json(results_file: Path) -> List[Dict]:
    """
    Load results from JSON file.
    
    Results Loading Hierarchy:
    This function is part of a hierarchy of results loading utilities:
    
    1. file_utils.load_json_file (base):
       - Generic JSON file loader with validation
       - Handles file existence, JSON parsing, type validation
       - Used by all higher-level loaders
    
    2. best_variant_utils.load_results_json (this function - simple wrapper):
       - Simple wrapper around file_utils.load_json_file
       - Adds context-specific type validation (expects list)
       - Used for single-file results loading
    
    3. grid_search_configs/result_analysis.load_results (context-specific):
       - Wrapper for hyperparameter grid search analysis
       - Uses file_utils.load_json_file directly
       - Adds logging and context-specific error messages
    
    4. ensembling/results_loader.load_results_from_files (complex):
       - Multi-file loader with auto-detection
       - Uses best_variant_utils.load_results_json internally
       - Handles merging, deduplication, fallback paths
    
    This function: Simple wrapper that delegates to file_utils.load_json_file
    with results-specific validation.
    
    Args:
        results_file: Path to results.json file
        
    Returns:
        List of variant result dictionaries
        
    Raises:
        FileNotFoundError: If results file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    results = load_json_file(results_file, expected_type=list, file_type="Results JSON")
    return results


def find_best_variant(results: List[Dict]) -> Optional[Dict]:
    """
    Find the best variant from results based on highest cv_score.
    
    Only considers variants with valid cv_score (not None).
    
    Args:
        results: List of variant result dictionaries
        
    Returns:
        Best variant dictionary, or None if no valid variants found
    """
    valid_variants = [r for r in results if r.get('cv_score') is not None]
    
    if not valid_variants:
        logger.warning("No variants with valid cv_score found")
        return None
    
    best_variant = max(valid_variants, key=lambda x: x.get('cv_score', -float('inf')))
    
    return best_variant


def find_variant_by_id(results: List[Dict], variant_id: str) -> Optional[Dict]:
    """
    Find a specific variant by its variant_id.
    
    Args:
        results: List of variant result dictionaries
        variant_id: Variant ID to search for (e.g., "variant_0067")
        
    Returns:
        Variant dictionary if found, None otherwise
    """
    for result in results:
        if result.get('variant_id') == variant_id:
            return result
    
    return None


def get_variant_best_fold(variant: Dict) -> Tuple[int, float]:
    """
    Get the best fold for a variant from its fold_scores.
    
    Args:
        variant: Variant dictionary with 'fold_scores' key
        
    Returns:
        Tuple of (best_fold_index, best_fold_score)
        
    Raises:
        ValueError: If variant doesn't have fold_scores or fold_scores is empty
    """
    fold_scores = variant.get('fold_scores', [])
    
    if not fold_scores:
        raise ValueError(f"Variant {variant.get('variant_id', 'unknown')} has no fold_scores")
    
    return find_best_fold_from_scores(fold_scores)


def get_best_variant_info(
    results_file: Path,
    variant_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get information about the best variant (or specified variant) from results.
    
    Args:
        results_file: Path to results.json file
        variant_id: Optional variant ID to use instead of finding best
        
    Returns:
        Dictionary with keys:
        - 'variant': Variant dictionary
        - 'best_fold': Best fold index
        - 'best_fold_score': Best fold score
        - 'preprocessing_list': List of preprocessing techniques
        - 'augmentation_list': List of augmentation techniques
        - 'cv_score': Cross-validation score
        - 'dataset_type': Dataset type used ('split' or 'full', default: 'split')
        
    Raises:
        FileNotFoundError: If results file doesn't exist
        ValueError: If variant not found or has no valid scores
    """
    results = load_results_json(results_file)
    
    if variant_id:
        variant = find_variant_by_id(results, variant_id)
        if variant is None:
            raise ValueError(f"Variant {variant_id} not found in results")
        if variant.get('cv_score') is None:
            raise ValueError(f"Variant {variant_id} has no valid cv_score (may have failed)")
    else:
        variant = find_best_variant(results)
        if variant is None:
            raise ValueError("No valid variants found in results")
    
    best_fold, best_fold_score = get_variant_best_fold(variant)
    
    # Resolve data_manipulation.combo_id to actual lists
    preprocessing_list = []
    augmentation_list = []
    
    try:
        metadata_dir = find_metadata_dir()
        if metadata_dir:
            preprocessing_list, augmentation_list = extract_preprocessing_augmentation_from_variant(
                variant, metadata_dir
            )
            logger.debug(f"Resolved variant {variant.get('variant_id', 'unknown')} to preprocessing={preprocessing_list}, augmentation={augmentation_list}")
        else:
            logger.warning(f"Metadata directory not found, cannot resolve combo_id for variant {variant.get('variant_id', 'unknown')}")
    except (ValueError, FileNotFoundError) as e:
        logger.warning(f"Failed to resolve data_manipulation for variant {variant.get('variant_id', 'unknown')}: {e}")
    
    return {
        'variant': variant,
        'best_fold': best_fold,
        'best_fold_score': best_fold_score,
        'preprocessing_list': preprocessing_list,
        'augmentation_list': augmentation_list,
        'cv_score': variant.get('cv_score'),
        'variant_id': variant.get('variant_id'),
        'dataset_type': variant.get('dataset_type', 'full')
    }


def get_regression_variant_info(
    results_file: Path,
    regression_model_type: str,
    feature_filename: str,
    variant_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get information about a regression variant (or best variant) from regression grid search results.
    
    Filters results by regression_model_type and feature_filename,
    then selects either the specified variant_id or the best scoring variant.
    
    Args:
        results_file: Path to regression grid search results JSON file
        regression_model_type: Type of regression model ('lgbm', 'xgboost', 'ridge')
        feature_filename: Feature filename used for training (e.g., 'variant_0100_features.npz')
        variant_id: Optional variant ID to use instead of finding best
        
    Returns:
        Dictionary with keys:
        - 'variant': Variant dictionary
        - 'variant_id': Variant ID
        - 'cv_score': Cross-validation score
        - 'hyperparameters': Hyperparameters dictionary
        - 'feature_filename': Feature filename used for training
        
    Raises:
        FileNotFoundError: If results file doesn't exist
        ValueError: If variant not found or has no valid scores, or no matching results found
    """
    if not results_file.exists():
        raise FileNotFoundError(f"Regression grid search results file not found: {results_file}")
    
    results = load_results_json(results_file)
    
    # Filter results matching regression_model_type and feature_filename
    matching_results = []
    for result in results:
        # Check regression_model_type (may be in result or inferred from file location)
        result_model_type = result.get('regression_model_type')
        if result_model_type and result_model_type != regression_model_type:
            continue
        
        # Check feature filename
        r_feature_filename = result.get('feature_filename')
        if r_feature_filename is None:
            continue
        
        if r_feature_filename == feature_filename:
            matching_results.append(result)
    
    if not matching_results:
        raise ValueError(
            f"No matching regression variants found for:\n"
            f"  Regression model type: {regression_model_type}\n"
            f"  Feature filename: {feature_filename}\n"
            f"  Results file: {results_file}"
        )
    
    # Select variant
    if variant_id:
        variant = find_variant_by_id(matching_results, variant_id)
        if variant is None:
            raise ValueError(
                f"Regression variant {variant_id} not found in matching results.\n"
                f"  Available variant IDs: {[r.get('variant_id') for r in matching_results]}"
            )
        if variant.get('cv_score') is None:
            raise ValueError(f"Regression variant {variant_id} has no valid cv_score (may have failed)")
        
        logger.info(f"✅ Using SPECIFIED regression variant: {variant_id}")
    else:
        variant = find_best_variant(matching_results)
        if variant is None:
            raise ValueError("No valid regression variants found in matching results")
        
        variant_id = variant.get('variant_id')
        logger.info(f"✅ Using BEST regression variant: {variant_id}")
        logger.info(f"   (Highest CV score: {variant.get('cv_score', 0):.4f})")
    
    cv_score = variant.get('cv_score')
    hyperparameters = variant.get('hyperparameters', {})
    variant_feature_filename = variant.get('feature_filename')
    
    logger.info(f"  Variant ID: {variant_id}")
    logger.info(f"  CV Score: {cv_score:.4f}")
    logger.info(f"  Hyperparameters: {hyperparameters}")
    logger.info(f"  Feature Filename: {variant_feature_filename}")
    
    return {
        'variant': variant,
        'variant_id': variant_id,
        'cv_score': cv_score,
        'hyperparameters': hyperparameters,
        'feature_filename': variant_feature_filename
    }

