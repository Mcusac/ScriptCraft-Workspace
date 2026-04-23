# checkpoint_cleanup_utils.py
# Utilities for cleaning up old grid search checkpoints

import logging
import shutil
from pathlib import Path
from typing import List, Dict, Tuple

from utils.system.io import load_json_file

logger = logging.getLogger(__name__)


def get_variant_directories(model_base_dir: Path) -> List[Path]:
    """
    Find all variant directories in grid search model directory.
    
    Normalizes the model_base_dir to ensure we don't have nested paths.
    
    Args:
        model_base_dir: Base model directory (e.g., /kaggle/working/models)
        
    Returns:
        List of variant directory paths (e.g., variant_0001, variant_0002, etc.)
    """
    # Normalize base directory - remove trailing 'dataset_grid_search' if present
    normalized_base = model_base_dir
    if normalized_base.name == 'dataset_grid_search':
        normalized_base = normalized_base.parent
    
    grid_search_dir = normalized_base / 'dataset_grid_search'
    if not grid_search_dir.exists():
        return []
    
    variant_dirs = []
    seen_variant_ids = set()
    
    def collect_variants(directory: Path, depth: int = 0):
        """Recursively collect variant directories, handling nested legacy structures."""
        if depth > 5:  # Safety limit to prevent infinite recursion
            return
        
        for item in directory.iterdir():
            if item.is_dir():
                if item.name.startswith('variant_'):
                    # Extract variant_id (e.g., "variant_0001")
                    variant_id = item.name
                    # Only add if we haven't seen this variant_id before (avoid duplicates)
                    if variant_id not in seen_variant_ids:
                        variant_dirs.append(item)
                        seen_variant_ids.add(variant_id)
    
    collect_variants(grid_search_dir)
    
    return sorted(variant_dirs)


def get_variant_scores(results_file: Path) -> Dict[str, float]:
    """
    Load variant scores from results.json.
    
    Args:
        results_file: Path to results.json file
        
    Returns:
        Dictionary mapping variant_id to cv_score (None if no score)
    """
    if not results_file.exists():
        return {}
    
    try:
        results = load_json_file(results_file, expected_type=list, file_type="Results JSON")
        
        variant_scores = {}
        for result in results:
            variant_id = result.get('variant_id')
            cv_score = result.get('cv_score')
            if variant_id:
                variant_scores[variant_id] = cv_score
        
        return variant_scores
    except Exception as e:
        logger.warning(f"Failed to load variant scores from {results_file}: {e}")
        return {}


def calculate_variant_size(variant_dir: Path) -> int:
    """
    Calculate total size of variant directory in bytes.
    
    Args:
        variant_dir: Path to variant directory
        
    Returns:
        Total size in bytes
    """
    total_size = 0
    if not variant_dir.exists():
        return 0
    
    try:
        for file_path in variant_dir.rglob('*'):
            if file_path.is_file():
                total_size += file_path.stat().st_size
    except Exception as e:
        logger.warning(f"Error calculating size for {variant_dir}: {e}")
    
    return total_size


def delete_variant_directory(variant_dir: Path) -> int:
    """
    Delete entire variant directory and return size freed.
    
    Args:
        variant_dir: Path to variant directory to delete
        
    Returns:
        Size freed in bytes
    """
    if not variant_dir.exists():
        return 0
    
    size_freed = calculate_variant_size(variant_dir)
    
    try:
        shutil.rmtree(variant_dir)
        from utils.system.constants import BYTES_PER_MB
        logger.info(f"Deleted variant directory: {variant_dir.name} ({size_freed / BYTES_PER_MB:.2f} MB)")
        return size_freed
    except Exception as e:
        logger.error(f"Failed to delete variant directory {variant_dir}: {e}")
        return 0


def cleanup_grid_search_checkpoints(
    model_base_dir: Path,
    results_file: Path,
    keep_top_n: int = 20,
    always_keep_best: bool = True
) -> Tuple[int, int]:
    """
    Clean up grid search checkpoints, keeping only the best N variants by CV score.
    
    Args:
        model_base_dir: Base model directory
        results_file: Path to results.json file
        keep_top_n: Number of top variants to keep
        always_keep_best: If True, always keep the best variant even if not in top N
        
    Returns:
        Tuple of (variants_deleted, bytes_freed)
    """
    variant_dirs = get_variant_directories(model_base_dir)
    variant_scores = get_variant_scores(results_file)
    
    if not variant_dirs:
        logger.info("No variant directories found for cleanup")
        return 0, 0
    
    # Find best variant ID
    best_variant_id = None
    best_score = -float('inf')
    for variant_id, score in variant_scores.items():
        if score is not None and score > best_score:
            best_score = score
            best_variant_id = variant_id
    
    # Create list of (variant_dir, score, variant_id) tuples
    variant_info = []
    for variant_dir in variant_dirs:
        variant_id = variant_dir.name
        score = variant_scores.get(variant_id)
        variant_info.append((variant_dir, score, variant_id))
    
    # Sort by score (descending), with None scores at the end
    variant_info.sort(key=lambda x: (x[1] is None, -(x[1] or -float('inf'))))
    
    # Determine which variants to keep
    variants_to_keep = set()
    
    # Always keep best variant if requested
    if always_keep_best and best_variant_id:
        variants_to_keep.add(best_variant_id)
        logger.info(f"Always keeping best variant: {best_variant_id} (score: {best_score:.4f})")
    
    # Keep top N variants with valid scores
    valid_variants = [(d, s, vid) for d, s, vid in variant_info if s is not None]
    for variant_dir, score, variant_id in valid_variants[:keep_top_n]:
        variants_to_keep.add(variant_id)
    
    # Delete variants not in keep list
    variants_deleted = 0
    bytes_freed = 0
    
    for variant_dir, score, variant_id in variant_info:
        if variant_id not in variants_to_keep:
            size_freed = delete_variant_directory(variant_dir)
            variants_deleted += 1
            bytes_freed += size_freed
    
    if variants_deleted > 0:
        from utils.system.constants import BYTES_PER_MB
        logger.info(f"Cleanup complete: Deleted {variants_deleted} variants, freed {bytes_freed / BYTES_PER_MB:.2f} MB")
        logger.info(f"Kept {len(variants_to_keep)} variants (top {keep_top_n} + best variant)")
    else:
        logger.info(f"No cleanup needed: {len(variant_dirs)} variants, keeping {len(variants_to_keep)}")
    
    return variants_deleted, bytes_freed


def cleanup_grid_search_checkpoints_retroactive(
    model_base_dir: str,
    results_file: str,
    keep_top_n: int = 20
) -> Tuple[int, int]:
    """
    Retroactively clean up grid search checkpoints from existing results.
    
    This function can be called independently to clean up old checkpoints
    from a completed or interrupted grid search.
    
    Args:
        model_base_dir: Base model directory path (string)
        results_file: Path to results.json file (string)
        keep_top_n: Number of top variants to keep
        
    Returns:
        Tuple of (variants_deleted, bytes_freed)
    """
    return cleanup_grid_search_checkpoints(
        model_base_dir=Path(model_base_dir),
        results_file=Path(results_file),
        keep_top_n=keep_top_n,
        always_keep_best=True
    )

