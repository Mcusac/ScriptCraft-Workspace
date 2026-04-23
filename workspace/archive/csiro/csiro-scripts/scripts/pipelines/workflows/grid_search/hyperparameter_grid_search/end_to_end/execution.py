# execution.py
# Execution logic for hyperparameter grid search variants

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

from config.config import Config
from pipelines.atomic.train_only import train_pipeline
from utils.system import clear_gpu_memory
from modeling import handle_oom_error_with_retry
from modeling.utils import COMBINATION_ID_FORMAT
from ...utils.constants import MODEL_DIR_HYPERPARAMETER_GRID_SEARCH
from utils.system import ensure_dir
from utils.config import apply_dataset_config_to_config
from modeling.utils import create_grid_search_result_dict, create_grid_search_error_result_dict
from ...utils.hyperparameters import apply_hyperparameters_to_config
# Cleanup now handled by GridSearchBase instance in pipeline
from ...utils.helpers import create_variant_specific_data

logger = logging.getLogger(__name__)


def execute_single_combination(
    idx: int,
    starting_index: int,
    combination: tuple,
    param_names: List[str],
    total_combinations: int,
    config: Config,
    preprocessing_list: List[str],
    augmentation_list: List[str],
    base_model_dir: Path,
    results_file_path: Path,
    keep_top_n: int
) -> Tuple[Optional[Dict[str, Any]], bool]:
    """
    Execute a single hyperparameter combination.
    
    Args:
        idx: Index of combination in grid (0-based within this grid search)
        starting_index: Starting variant_index to ensure sequential numbering across all grid searches
        combination: Hyperparameter combination tuple
        param_names: List of parameter names
        total_combinations: Total number of combinations
        config: Base configuration object
        preprocessing_list: Preprocessing list from metadata
        augmentation_list: Augmentation list from metadata
        base_model_dir: Base model directory
        results_file_path: Path to results file
        keep_top_n: Number of top variants to keep
    
    Returns:
        Tuple of (result_dict, was_skipped). result_dict is None if combination was skipped.
    """
    hyperparameters = dict(zip(param_names, combination))
    
    logger.info("="*60)
    logger.info(f"Combination {idx+1}/{total_combinations}")
    logger.info(f"Hyperparameters: {hyperparameters}")
    logger.info(f"{'='*60}")
    
    # CRITICAL: Clear GPU memory before starting each combination
    clear_gpu_memory(log_memory=True, aggressive=True)
    
    # Calculate sequential variant_index (starting_index + idx ensures global sequential numbering)
    variant_index = starting_index + idx
    
    # Prepare configuration for this combination
    combo_id = COMBINATION_ID_FORMAT.format(index=idx)
    combo_config, combo_model_dir = _prepare_combination_config(
        config, hyperparameters, preprocessing_list, augmentation_list, combo_id, base_model_dir
    )
    
    # Track batch size used (for adaptive reduction on OOM)
    original_batch_size = combo_config.training.batch_size
    current_batch_size = original_batch_size
    batch_size_reduced = False
    oom_retry_count = 0
    
    try:
        # Train with this combination (will use checkpoint resumption for folds)
        cv_score, fold_scores, _ = train_pipeline(combo_config)
        
        # Create result with unified format
        variant_specific_data = create_variant_specific_data(
            config=config,
            preprocessing_list=preprocessing_list,
            augmentation_list=augmentation_list,
            hyperparameters=hyperparameters
        )
        result = create_grid_search_result_dict(
            variant_index=variant_index,
            variant_id=combo_id,
            cv_score=cv_score,
            fold_scores=fold_scores,
            batch_size_used=current_batch_size,
            batch_size_reduced=batch_size_reduced,
            variant_specific_data=variant_specific_data
        )
        
        return result, False
        
    except KeyboardInterrupt:
        logger.warning(f"\n⚠️ KeyboardInterrupt received during combination {combo_id}")
        logger.warning("Saving current progress before exiting...")
        logger.warning("Grid search interrupted. Progress saved. Resume will continue from next combination.")
        raise
    
    except Exception as e:
        # Try to recover from OOM with batch size reduction
        oom_result = handle_oom_error_with_retry(
            error=e,
            config=combo_config,
            current_batch_size=current_batch_size,
            oom_retry_count=oom_retry_count,
            variant_id=combo_id,
            train_func=lambda cfg: train_pipeline(cfg)[:2]  # Return only cv_score, fold_scores
        )
        
        if oom_result is not None:
            # OOM was handled
            if oom_result['success']:
                # Success after retry
                cv_score = oom_result['cv_score']
                fold_scores = oom_result['fold_scores']
                current_batch_size = oom_result['batch_size_used']
                batch_size_reduced = True
                
                # Create result with batch size info
                variant_specific_data = create_variant_specific_data(
                    config=config,
                    preprocessing_list=preprocessing_list,
                    augmentation_list=augmentation_list,
                    hyperparameters=hyperparameters
                )
                result = create_grid_search_result_dict(
                    variant_index=variant_index,
                    variant_id=combo_id,
                    cv_score=cv_score,
                    fold_scores=fold_scores,
                    batch_size_used=current_batch_size,
                    batch_size_reduced=batch_size_reduced,
                    variant_specific_data=variant_specific_data
                )
                
                return result, False
            else:
                # Skipped due to persistent OOM
                variant_specific_data = create_variant_specific_data(
                    config=config,
                    preprocessing_list=preprocessing_list,
                    augmentation_list=augmentation_list,
                    hyperparameters=hyperparameters
                )
                result = create_grid_search_error_result_dict(
                    variant_index=variant_index,
                    variant_id=combo_id,
                    error=oom_result.get('error', 'Persistent OOM'),
                    batch_size_used=oom_result.get('batch_size_used', current_batch_size),
                    batch_size_reduced=batch_size_reduced,
                    variant_specific_data=variant_specific_data,
                    skipped=True
                )
                
                logger.warning(f"Skipped combination {combo_id} due to persistent OOM")
                return result, False
        
        # Not an OOM error or OOM handling returned None - save error result
        logger.error(f"Error training combination {combo_id}: {e}", exc_info=True)
        
        # Create error result
        variant_specific_data = create_variant_specific_data(
            config=config,
            preprocessing_list=preprocessing_list,
            augmentation_list=augmentation_list,
            hyperparameters=hyperparameters
        )
        result = create_grid_search_error_result_dict(
            variant_index=variant_index,
            variant_id=combo_id,
            error=str(e),
            batch_size_used=current_batch_size,
            batch_size_reduced=batch_size_reduced,
            variant_specific_data=variant_specific_data
        )
        
        logger.warning(f"Error result saved to {results_file_path} (combination will be retried on resume)")
        return result, False


def _prepare_combination_config(
    config: Config,
    hyperparameters: Dict[str, Any],
    preprocessing_list: List[str],
    augmentation_list: List[str],
    combo_id: str,
    base_model_dir: Path
) -> Tuple[Config, Path]:
    """
    Prepare configuration for a single hyperparameter combination.
    
    Args:
        config: Base configuration.
        hyperparameters: Hyperparameters for this combination.
        preprocessing_list: Preprocessing list to apply.
        augmentation_list: Augmentation list to apply.
        combo_id: Combination ID string.
        base_model_dir: Base model directory.
        
    Returns:
        Tuple of (combo_config, combo_model_dir).
    """
    import copy
    
    # Create config copy for this combination
    combo_config = copy.deepcopy(config)
    
    # Apply dataset configuration (handles default preprocessing automatically)
    apply_dataset_config_to_config(combo_config, preprocessing_list, augmentation_list)
    
    # Apply hyperparameters to config
    apply_hyperparameters_to_config(combo_config, hyperparameters)
    
    # Create unique model directory for this combination
    combo_model_dir = base_model_dir / MODEL_DIR_HYPERPARAMETER_GRID_SEARCH / combo_id
    combo_config.paths.model_dir = str(combo_model_dir)
    ensure_dir(combo_config.paths.model_dir)
    
    return combo_config, combo_model_dir


def _save_hyperparameter_result(
    result: Dict[str, Any],
    results_file_path: Path
) -> None:
    """
    Save hyperparameter combination result to JSON file.
    
    Uses incremental append to avoid losing progress on timeout.
    
    Args:
        result: Result dictionary to save.
        results_file_path: Path to results JSON file.
    """
    from utils.system import append_to_json_list
    
    append_to_json_list(result, results_file_path, file_type="Hyperparameter results")
    logger.info(f"Results saved incrementally to {results_file_path}")

