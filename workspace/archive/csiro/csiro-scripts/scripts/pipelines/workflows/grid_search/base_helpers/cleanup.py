# cleanup.py
# Checkpoint cleanup utilities for grid search

import logging
from pathlib import Path
from typing import Optional

from modeling.training.utils import cleanup_grid_search_checkpoints

logger = logging.getLogger(__name__)


def cleanup_checkpoints_helper(
    config,
    base_model_dir: Path,
    results_file: Path,
    variant_model_dir: Path,
    cv_score: Optional[float],
    variant_id: str
) -> None:
    """
    Clean up checkpoints if configured and needed.
    
    Args:
        config: Configuration object
        base_model_dir: Base model directory
        results_file: Results file path
        variant_model_dir: Model directory for this variant
        cv_score: CV score for this variant (None if failed)
        variant_id: ID of the variant
    """
    # Immediate deletion after variant completes (if configured)
    delete_variant_checkpoints_immediately(config, variant_model_dir, cv_score, variant_id)
    
    # Immediate cleanup after each successful variant (keep only top N)
    cleanup_top_variants(config, base_model_dir, results_file, cv_score)
    
    # Periodic cleanup (every N variants)
    run_periodic_cleanup(config, base_model_dir, results_file, get_completed_count(results_file))


def delete_variant_checkpoints_immediately(
    config,
    variant_model_dir: Path,
    cv_score: Optional[float],
    variant_id: str
) -> None:
    """
    Delete variant checkpoints immediately after completion if configured.
    
    Args:
        config: Configuration object
        variant_model_dir: Model directory for this variant
        cv_score: CV score for this variant (None if failed)
        variant_id: ID of the variant
    """
    if cv_score is not None and getattr(config.grid_search, 'delete_checkpoints_after_completion', True):
        logger.info(f"Deleting checkpoints for variant {variant_id} (results saved to results.json)")
        try:
            from modeling import delete_variant_directory
            from utils.system.constants import BYTES_PER_MB
            bytes_freed = delete_variant_directory(variant_model_dir)
            logger.info(f"Deleted variant checkpoints, freed {bytes_freed / BYTES_PER_MB:.2f} MB")
        except Exception as e:
            logger.warning(f"Failed to delete variant checkpoints: {e}")


def cleanup_top_variants(
    config,
    base_model_dir: Path,
    results_file: Path,
    cv_score: Optional[float]
) -> None:
    """
    Clean up variants, keeping only top N.
    
    Args:
        config: Configuration object
        base_model_dir: Base model directory
        results_file: Results file path
        cv_score: CV score for this variant (None if failed)
    """
    if config.grid_search.enable_cleanup and cv_score is not None:
        variants_deleted, bytes_freed = cleanup_grid_search_checkpoints(
            model_base_dir=base_model_dir,
            results_file=results_file,
            keep_top_n=config.grid_search.keep_top_variants,
            always_keep_best=True
        )
        if variants_deleted > 0:
            from utils.system.constants import BYTES_PER_MB
            logger.info(f"Immediate cleanup: Deleted {variants_deleted} variants, freed {bytes_freed / BYTES_PER_MB:.2f} MB")


def run_periodic_cleanup(
    config,
    base_model_dir: Path,
    results_file: Path,
    completed_count: int
) -> None:
    """
    Run periodic cleanup if configured and interval reached.
    
    Args:
        config: Configuration object
        base_model_dir: Base model directory
        results_file: Results file path
        completed_count: Number of completed variants
    """
    if not config.grid_search.enable_cleanup:
        return
    
    if completed_count > 0 and completed_count % config.grid_search.cleanup_interval == 0:
        logger.info("="*60)
        logger.info(f"Running periodic checkpoint cleanup (every {config.grid_search.cleanup_interval} variants)")
        logger.info(f"{'='*60}")
        variants_deleted, bytes_freed = cleanup_grid_search_checkpoints(
            model_base_dir=base_model_dir,
            results_file=results_file,
            keep_top_n=config.grid_search.keep_top_variants,
            always_keep_best=True
        )
        if variants_deleted > 0:
            from utils.system.constants import BYTES_PER_MB
            logger.info(f"Cleanup: Deleted {variants_deleted} variants, freed {bytes_freed / BYTES_PER_MB:.2f} MB")
        logger.info(f"{'='*60}\n")


def get_completed_count(results_file: Path) -> int:
    """
    Get count of completed variants from results file.
    
    Args:
        results_file: Path to results file
    
    Returns:
        Number of completed variants.
    """
    if results_file and results_file.exists():
        from utils.system import load_json_file
        all_results = load_json_file(results_file, expected_type=list, file_type="Results JSON")
        return len([r for r in all_results if r.get('cv_score') is not None])
    return 0


def run_final_cleanup_helper(config, base_model_dir: Path, results_file: Path) -> None:
    """
    Run final cleanup at the end of grid search.
    
    Args:
        config: Configuration object
        base_model_dir: Base model directory
        results_file: Results file path
    """
    if not config.grid_search.enable_cleanup or not results_file:
        return
    
    logger.info("="*60)
    logger.info("Running final checkpoint cleanup")
    logger.info(f"{'='*60}")
    variants_deleted, bytes_freed = cleanup_grid_search_checkpoints(
        model_base_dir=base_model_dir,
        results_file=results_file,
        keep_top_n=config.grid_search.keep_top_variants,
        always_keep_best=True
    )
    if variants_deleted > 0:
        from utils.system.constants import BYTES_PER_MB
        logger.info(f"Final cleanup: Deleted {variants_deleted} variants, freed {bytes_freed / BYTES_PER_MB:.2f} MB")
    logger.info(f"{'='*60}")
