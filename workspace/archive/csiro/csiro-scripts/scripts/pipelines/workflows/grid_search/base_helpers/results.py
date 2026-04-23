# results.py
# Result loading and saving utilities for grid search

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set, Callable

from utils.system import load_json_file, append_to_json_list
from modeling.utils import get_top_n_results, get_next_variant_index

logger = logging.getLogger(__name__)


def load_completed_variants_helper(
    results_file: Optional[Path],
    keep_top_n: int,
    create_variant_key_from_result_fn: Callable[[Dict[str, Any]], Optional[Any]]
) -> Tuple[Set[Any], Set[Any], List[Dict[str, Any]], int]:
    """
    Load completed and skipped variants from results file.
    
    Args:
        results_file: Path to results file
        keep_top_n: Number of top variants to keep in memory
        create_variant_key_from_result_fn: Function to create variant key from result dict
        
    Returns:
        Tuple of (completed_variants_set, skipped_variants_set, top_variants_list, starting_index).
    """
    completed_variants = set()
    skipped_variants = set()
    top_variants = []
    
    if not results_file or not results_file.exists():
        return completed_variants, skipped_variants, top_variants, 0
    
    logger.info(f"Loading completed variant keys from {results_file}")
    all_results = load_json_file(results_file, expected_type=list, file_type="Results JSON")
    
    successful_count = 0
    skipped_count = 0
    failed_count = 0
    
    for r in all_results:
        variant_key = create_variant_key_from_result_fn(r)
        if variant_key is not None:
            if r.get('cv_score') is not None:
                completed_variants.add(variant_key)
                successful_count += 1
                top_variants.append(r)
            elif r.get('skipped', False):
                skipped_variants.add(variant_key)
                skipped_count += 1
            else:
                failed_count += 1
    
    # Sort by score and keep only top N
    top_variants = get_top_n_results(top_variants, keep_top_n, metric_key='cv_score')
    
    # Calculate starting_index to ensure sequential numbering
    starting_index = get_next_variant_index(all_results)
    
    logger.info(f"Found {successful_count} successfully completed variants")
    if skipped_count > 0:
        logger.info(f"Found {skipped_count} skipped variants (persistent OOM - can retry later)")
    if failed_count > 0:
        logger.info(f"Found {failed_count} failed variants (will be retried)")
    logger.info(f"Tracking top {len(top_variants)} variant metadata in memory")
    logger.info(f"Starting variant_index from {starting_index} (ensuring sequential numbering across all grid searches)")
    
    return completed_variants, skipped_variants, top_variants, starting_index


def save_variant_result_helper(result: Dict[str, Any], results_file: Path) -> None:
    """
    Save variant result to results file (incremental append).
    
    Args:
        result: Variant result dictionary
        results_file: Path to results file
    """
    append_to_json_list(result, results_file, file_type="Variant results")
    
    variant_id = result.get('variant_id', result.get('combination_id', 'unknown'))
    variant_index = result.get('variant_index', result.get('combination_index', 'unknown'))
    logger.info(f"Results saved incrementally to {results_file} (variant {variant_id}, index {variant_index})")
