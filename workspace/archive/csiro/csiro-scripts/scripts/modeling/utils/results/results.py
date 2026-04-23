# results_utils.py
# Utilities for viewing grid search results and verifying submission files

import logging
import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple

from utils.system.io import get_output_path, load_json_file
from ..metadata.data_manipulation_loader import (
    find_metadata_dir,
    extract_preprocessing_augmentation_from_variant
)

logger = logging.getLogger(__name__)


def view_grid_search_results(
    results_file: Optional[str] = None,
    best_variant_file: Optional[str] = None
) -> None:
    """
    Display best variant from dataset grid search.
    
    Args:
        results_file: Optional path to results.json (default: output/dataset_grid_search/gridsearch_results.json)
        best_variant_file: Optional path to best_dataset_variant.json (default: output/dataset_grid_search/best_dataset_variant.json)
    """
    if results_file is None:
        results_file = str(get_output_path('output/dataset_grid_search/gridsearch_results.json'))
    if best_variant_file is None:
        best_variant_file = str(get_output_path('output/dataset_grid_search/best_dataset_variant.json'))
    
    results_path = Path(results_file)
    best_variant_path = Path(best_variant_file)
    
    if best_variant_path.exists():
        best_data = load_json_file(best_variant_path, expected_type=dict, file_type="Best variant JSON")
        
        logger.info("🏆 Best Grid Search Result:")
        logger.info(f"   Score: {best_data.get('best_score', 'N/A'):.4f}")
        best_variant = best_data.get('best_variant', {})
        
        # Resolve preprocessing_list and augmentation_list from data_manipulation.combo_id
        preprocessing_list = []
        augmentation_list = []
        try:
            metadata_dir = find_metadata_dir()
            if metadata_dir:
                preprocessing_list, augmentation_list = extract_preprocessing_augmentation_from_variant(
                    best_variant, metadata_dir
                )
        except (ValueError, FileNotFoundError) as e:
            logger.debug(f"Could not resolve data_manipulation for display: {e}")
        
        logger.info(f"   Preprocessing: {preprocessing_list if preprocessing_list else '[]'}")
        logger.info(f"   Augmentation: {augmentation_list if augmentation_list else '[]'}")
        logger.info(f"   Variant ID: {best_variant.get('variant_id', 'N/A')}")
        logger.info(f"\n📁 Full results: {results_path}")
    elif results_path.exists():
        logger.warning("⚠️ Best variant file not found, but results exist")
        logger.info(f"   Check: {results_path}")
        logger.info("   You can still use Pipeline C with --results-file to use best variant")
    else:
        logger.warning("⚠️ Grid search not run yet - run Pipeline B first")


def verify_submission_file(
    submission_file: Optional[str] = None
) -> pd.DataFrame:
    """
    Verify submission.csv format and contents.
    
    Args:
        submission_file: Optional path to submission.csv (default: output/submission.csv)
        
    Returns:
        Submission DataFrame if file exists
        
    Raises:
        FileNotFoundError: If submission file doesn't exist
    """
    if submission_file is None:
        submission_file = str(get_output_path('submission.csv'))
    
    submission_path = Path(submission_file)
    
    if not submission_path.exists():
        raise FileNotFoundError(
            f"⚠️ Submission file not found at {submission_path}\n"
            "   Run Pipeline A to generate submission.csv"
        )
    
    submission_df = pd.read_csv(submission_path)
    
    logger.info("✅ Submission file verification:")
    logger.info(f"Path: {submission_path}")
    logger.info(f"Shape: {submission_df.shape}")
    logger.info(f"Columns: {submission_df.columns.tolist()}")
    logger.info(f"\nFirst 10 rows:")
    # Use logger for DataFrame display - convert to string for logging
    logger.info(f"\n{submission_df.head(10).to_string()}")
    logger.info(f"\nTarget value range: [{submission_df['target'].min():.2f}, {submission_df['target'].max():.2f}]")
    logger.info("✅ Submission file is ready!")
    
    return submission_df


def get_top_n_results(
    results: List[Dict[str, Any]],
    top_n: int,
    metric_key: str = 'cv_score'
) -> List[Dict[str, Any]]:
    """
    Get top N results sorted by metric.
    
    Args:
        results: List of result dictionaries.
        top_n: Number of top results to return.
        metric_key: Key to use for sorting (default: 'cv_score').
    
    Returns:
        List of top N results, sorted by metric in descending order.
    """
    if not results:
        return []
    
    # Sort by metric (descending) and take top N
    sorted_results = sorted(
        results,
        key=lambda x: x.get(metric_key, -float('inf')),
        reverse=True
    )
    return sorted_results[:top_n]


def create_grid_search_result_dict(
    variant_index: int,
    variant_id: str,
    cv_score: Optional[float],
    fold_scores: Optional[List[float]],
    batch_size_used: int,
    batch_size_reduced: bool,
    variant_specific_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create result dictionary for a grid search variant.
    
    Args:
        variant_index: Index of variant.
        variant_id: ID of variant.
        cv_score: CV score (None if failed).
        fold_scores: Fold scores (None if failed).
        batch_size_used: Batch size used.
        batch_size_reduced: Whether batch size was reduced.
        variant_specific_data: Dictionary with variant-specific fields (e.g., preprocessing_list, hyperparameters).
    
    Returns:
        Result dictionary.
    """
    result = {
        'variant_index': variant_index,
        'variant_id': variant_id,
        'cv_score': cv_score,
        'fold_scores': fold_scores,
        'batch_size_used': batch_size_used,
        'batch_size_reduced': batch_size_reduced
    }
    result.update(variant_specific_data)
    return result


def create_grid_search_error_result_dict(
    variant_index: int,
    variant_id: str,
    error: str,
    batch_size_used: int,
    batch_size_reduced: bool,
    variant_specific_data: Dict[str, Any],
    skipped: bool = False,
    oom_retry_count: Optional[int] = None
) -> Dict[str, Any]:
    """
    Create error result dictionary for a grid search variant.
    
    Args:
        variant_index: Index of variant.
        variant_id: ID of variant.
        error: Error message.
        batch_size_used: Batch size used.
        batch_size_reduced: Whether batch size was reduced.
        variant_specific_data: Dictionary with variant-specific fields.
        skipped: Whether variant was skipped (default: False).
        oom_retry_count: Optional OOM retry count.
    
    Returns:
        Error result dictionary.
    """
    result = {
        'variant_index': variant_index,
        'variant_id': variant_id,
        'cv_score': None,
        'error': error,
        'batch_size_used': batch_size_used,
        'batch_size_reduced': batch_size_reduced
    }
    if skipped:
        result['skipped'] = True
    if oom_retry_count is not None:
        result['oom_retry_count'] = oom_retry_count
    result.update(variant_specific_data)
    return result


def get_next_variant_index(results: List[Dict[str, Any]]) -> int:
    """
    Calculate next variant_index from existing results.
    
    Ensures sequential numbering across all grid search types by finding
    the maximum existing variant_index and returning max + 1.
    
    Args:
        results: List of existing result dictionaries
        
    Returns:
        Next variant_index to use (0 if no results exist)
    """
    if not results:
        return 0
    
    max_index = -1
    for result in results:
        variant_index = result.get('variant_index')
        if variant_index is not None and isinstance(variant_index, int):
            max_index = max(max_index, variant_index)
    
    return max_index + 1


def update_best_score(
    current_best_score: float,
    new_score: Optional[float],
    new_result: Dict[str, Any]
) -> Tuple[float, Optional[Dict[str, Any]]]:
    """
    Update best score if new score is better.
    
    Args:
        current_best_score: Current best score.
        new_score: New score to compare.
        new_result: Result dictionary for new score.
    
    Returns:
        Tuple of (updated_best_score, best_result_dict or None if not updated).
    """
    if new_score is not None and new_score > current_best_score:
        logger.info(f"New best score: {new_score:.4f}")
        return new_score, new_result
    return current_best_score, None

