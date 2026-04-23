# progress.py
# Progress tracking and utility functions for grid search

import logging
from typing import Dict, List, Any, Optional, Tuple

logger = logging.getLogger(__name__)


def clear_gpu_memory_before_variant() -> None:
    """
    Clear GPU memory before starting a variant.
    
    Should be called at the start of each variant execution.
    """
    from utils.system import clear_gpu_memory
    clear_gpu_memory(log_memory=True, aggressive=True)


def log_variant_header(
    variant_index: int,
    total_variants: int,
    variant_info: str
) -> None:
    """
    Log header for variant execution.
    
    Args:
        variant_index: Index of variant (0-based)
        total_variants: Total number of variants
        variant_info: String describing the variant
    """
    logger.info("="*60)
    logger.info(f"Variant {variant_index+1}/{total_variants}")
    logger.info(f"{variant_info}")
    logger.info(f"{'='*60}")


def create_result_dict(
    variant_index: int,
    variant_id: str,
    cv_score: Optional[float],
    fold_scores: Optional[List[float]],
    batch_size_used: int,
    batch_size_reduced: bool,
    variant_specific_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create result dictionary for a variant.
    
    Args:
        variant_index: Index of variant
        variant_id: ID of variant
        cv_score: CV score (None if failed)
        fold_scores: Fold scores (None if failed)
        batch_size_used: Batch size used
        batch_size_reduced: Whether batch size was reduced
        variant_specific_data: Dictionary with variant-specific fields
    
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


def create_error_result_dict(
    variant_index: int,
    variant_id: str,
    error: str,
    batch_size_used: int,
    batch_size_reduced: bool,
    variant_specific_data: Dict[str, Any],
    skipped: bool = False
) -> Dict[str, Any]:
    """
    Create error result dictionary for a variant.
    
    Args:
        variant_index: Index of variant
        variant_id: ID of variant
        error: Error message
        batch_size_used: Batch size used
        batch_size_reduced: Whether batch size was reduced
        variant_specific_data: Dictionary with variant-specific fields
        skipped: Whether variant was skipped (default: False)
    
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
    result.update(variant_specific_data)
    return result


def update_best_score_helper(
    current_best_score: float,
    new_score: Optional[float],
    new_result: Dict[str, Any],
    best_result_key: str = 'best_variant'
) -> Tuple[float, Optional[Dict[str, Any]]]:
    """
    Update best score if new score is better.
    
    Args:
        current_best_score: Current best score
        new_score: New score to compare
        new_result: Result dictionary for new score
        best_result_key: Key to use for best result in return (for logging context)
    
    Returns:
        Tuple of (updated_best_score, best_result_dict or None).
    """
    if new_score is not None and new_score > current_best_score:
        logger.info(f"New best score: {new_score:.4f}")
        return new_score, new_result
    return current_best_score, None
