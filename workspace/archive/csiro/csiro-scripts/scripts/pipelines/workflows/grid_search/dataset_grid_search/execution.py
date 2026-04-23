# execution.py
# Variant execution for dataset grid search

import copy
import logging
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional

from config.config import Config
from pipelines.atomic.train_only import train_pipeline
from dataset_manipulation import aggregate_train_csv
from modeling.training import create_kfold_splits
from utils.system import clear_gpu_memory, cleanup_dataframe_and_memory
from utils.config import apply_dataset_config_to_config
from modeling.utils import create_grid_search_result_dict, create_grid_search_error_result_dict, VARIANT_ID_FORMAT
from utils.system import ensure_dir
from ..utils.constants import MODEL_DIR_DATASET_GRID_SEARCH
from ..utils.helpers import create_variant_specific_data

logger = logging.getLogger(__name__)


def run_single_variant(
    variant: Tuple[List[str], List[str]],
    variant_index: int,
    total_variants: int,
    config: Config,
    train_csv_path: Path,
    base_model_dir: Path,
    device: Any,
    results_file: Path
) -> Tuple[Optional[float], Optional[List[float]], Dict[str, Any], Path]:
    """
    Run training for a single variant.
    
    Args:
        variant: Tuple of (preprocessing_list, augmentation_list).
        variant_index: Index of this variant in the grid.
        total_variants: Total number of variants in grid.
        config: Base configuration object.
        train_csv_path: Path to train CSV file.
        base_model_dir: Base model directory.
        device: Device to train on.
        results_file: Path to results JSON file.
        
    Returns:
        Tuple of (cv_score, fold_scores, result_dict, variant_model_dir).
        Returns (None, None, result_dict, variant_model_dir) on error.
    """
    preprocessing_list, augmentation_list = variant
    variant_key = (tuple(sorted(preprocessing_list)), tuple(sorted(augmentation_list)))
    variant_id = VARIANT_ID_FORMAT.format(index=variant_index)
    
    logger.info("="*60)
    logger.info(f"Variant {variant_index+1}/{total_variants}")
    logger.info(f"Preprocessing: {preprocessing_list if preprocessing_list else '[]'}")
    logger.info(f"Augmentation: {augmentation_list if augmentation_list else '[]'}")
    logger.info(f"{'='*60}")
    
    # CRITICAL: Clear GPU memory before starting each variant
    clear_gpu_memory(log_memory=True, aggressive=True)
    
    # CRITICAL: Reload DataFrame for each variant (memory efficiency)
    logger.info(f"Loading train data for variant {variant_index+1}/{total_variants}")
    agg_train_df = aggregate_train_csv(train_csv_path)
    
    # Create CV splits (same splits for all variants, but reloaded fresh)
    agg_train_df = create_kfold_splits(
        agg_train_df,
        n_folds=config.cv.n_folds,
        shuffle=config.cv.shuffle,
        random_state=config.cv.random_state
    )
    
    # Create config copy for this variant
    variant_config = copy.deepcopy(config)
    
    # Apply dataset configuration (handles default preprocessing automatically)
    apply_dataset_config_to_config(variant_config, preprocessing_list, augmentation_list)
    
    # Create unique model directory for this variant
    variant_model_dir = base_model_dir / MODEL_DIR_DATASET_GRID_SEARCH / variant_id
    variant_config.paths.model_dir = str(variant_model_dir)
    ensure_dir(variant_config.paths.model_dir)
    
    # Track batch size used (for adaptive reduction on OOM)
    original_batch_size = variant_config.training.batch_size
    current_batch_size = original_batch_size
    batch_size_reduced = False
    oom_retry_count = 0
    
    try:
        # Train with this variant (will use checkpoint resumption for folds)
        cv_score, fold_scores, _ = train_pipeline(variant_config)
        
        # Create result with unified format
        variant_specific_data = create_variant_specific_data(
            config=config,
            preprocessing_list=preprocessing_list,
            augmentation_list=augmentation_list
        )
        result = create_grid_search_result_dict(
            variant_index=variant_index,
            variant_id=variant_id,
            cv_score=cv_score,
            fold_scores=fold_scores,
            batch_size_used=current_batch_size,
            batch_size_reduced=batch_size_reduced,
            variant_specific_data=variant_specific_data
        )
        
        return cv_score, fold_scores, result, variant_model_dir
        
    except Exception as e:
        # Try to recover from OOM with batch size reduction
        from modeling import handle_oom_error_with_retry
        
        oom_result = handle_oom_error_with_retry(
            error=e,
            config=variant_config,
            current_batch_size=current_batch_size,
            oom_retry_count=oom_retry_count,
            variant_id=variant_id,
            train_func=lambda cfg: train_pipeline(cfg)[:2]  # Return only cv_score, fold_scores
        )
        
        if oom_result is not None:
            # OOM was handled (either retried successfully or skipped)
            if oom_result['success']:
                # Success after retry
                variant_specific_data = create_variant_specific_data(
                    config=config,
                    preprocessing_list=preprocessing_list,
                    augmentation_list=augmentation_list
                )
                result = create_grid_search_result_dict(
                    variant_index=variant_index,
                    variant_id=variant_id,
                    cv_score=oom_result['cv_score'],
                    fold_scores=oom_result['fold_scores'],
                    batch_size_used=oom_result['batch_size_used'],
                    batch_size_reduced=True,
                    variant_specific_data=variant_specific_data
                )
                return oom_result['cv_score'], oom_result['fold_scores'], result, variant_model_dir
            else:
                # Skipped due to persistent OOM
                variant_specific_data = create_variant_specific_data(
                    config=config,
                    preprocessing_list=preprocessing_list,
                    augmentation_list=augmentation_list
                )
                result = create_grid_search_error_result_dict(
                    variant_index=variant_index,
                    variant_id=variant_id,
                    error=oom_result.get('error', 'Persistent OOM'),
                    batch_size_used=oom_result.get('batch_size_used', current_batch_size),
                    batch_size_reduced=batch_size_reduced,
                    variant_specific_data=variant_specific_data,
                    skipped=True,
                    oom_retry_count=oom_result.get('oom_retry_count', oom_retry_count)
                )
                return None, None, result, variant_model_dir
        
        # If oom_result is None, fall through to normal error handling below
        
        # Error handling (either non-OOM error, or OOM that couldn't be resolved)
        logger.error(f"Error training variant {variant_id}: {e}", exc_info=True)
        
        # Save error result (for tracking purposes, but don't mark as completed)
        variant_specific_data = create_variant_specific_data(
            config=config,
            preprocessing_list=preprocessing_list,
            augmentation_list=augmentation_list
        )
        result = create_grid_search_error_result_dict(
            variant_index=variant_index,
            variant_id=variant_id,
            error=str(e),
            batch_size_used=current_batch_size,
            batch_size_reduced=batch_size_reduced,
            variant_specific_data=variant_specific_data
        )
        
        return None, None, result, variant_model_dir
    
    finally:
        # CRITICAL: Delete DataFrame and force memory cleanup after variant completes
        logger.info(f"Cleaning up memory after variant {variant_id}")
        cleanup_dataframe_and_memory(
            dataframe=agg_train_df if 'agg_train_df' in locals() else None,
            aggressive=True,
            delay_seconds=0.5
        )

