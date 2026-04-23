# oom_handling_utils.py
# Shared utilities for handling Out of Memory (OOM) errors during training
#
# Provides centralized OOM error handling logic to avoid code duplication
# across different grid search pipelines.

# Standard library imports
import logging
from typing import Dict, Any, Optional, Callable, Tuple, List

# Third-party imports
import torch

# Local imports
from config.config import Config
from utils.system import recover_from_oom

logger = logging.getLogger(__name__)


def is_oom_error(error: Exception) -> bool:
    """
    Check if an exception is an Out of Memory error.
    
    Args:
        error: Exception to check
        
    Returns:
        True if error is OOM-related, False otherwise
    """
    return 'out of memory' in str(error).lower() or isinstance(error, torch.OutOfMemoryError)


def handle_oom_error_with_retry(
    error: Exception,
    config: Config,
    current_batch_size: int,
    oom_retry_count: int,
    variant_id: str,
    train_func: Callable[[Config], Tuple[float, List[float]]]
) -> Optional[Dict[str, Any]]:
    """
    Handle OOM error with automatic batch size reduction and retry.
    
    This function implements the standard OOM recovery pattern:
    1. Check if error is OOM and retries are available
    2. Reduce batch size according to config
    3. Perform OOM recovery cleanup
    4. Retry training with reduced batch size
    5. Return result or None if should fall through to error handling
    
    Args:
        error: The exception that occurred
        config: Configuration object (will be modified with new batch size)
        current_batch_size: Current batch size that caused OOM
        oom_retry_count: Current retry count
        variant_id: Identifier for logging (e.g., variant_id or combination_id)
        train_func: Function to call for training, takes Config and returns (cv_score, fold_scores)
        
    Returns:
        Dictionary with result if OOM was handled, None if should fall through to error handling.
        Result dict contains:
        - 'success': bool - True if retry succeeded, False if skipped
        - 'cv_score': Optional[float] - CV score if successful
        - 'fold_scores': Optional[List[float]] - Fold scores if successful
        - 'batch_size_used': int - Batch size used
        - 'oom_retry_count': int - Final retry count
        - 'error': Optional[str] - Error message if skipped
    """
    # Check if this is an OOM error
    if not is_oom_error(error):
        return None  # Not an OOM error, fall through to normal error handling
    
    # Get OOM handling config
    min_batch_size = config.grid_search.min_batch_size
    batch_size_reduction_factor = config.grid_search.batch_size_reduction_factor
    max_oom_retries = config.grid_search.max_oom_retries
    
    # Check if we can retry
    if oom_retry_count >= max_oom_retries or current_batch_size <= min_batch_size:
        # Can't retry - skip this variant/combination
        logger.warning(
            f"⚠️ Persistent OOM error after {oom_retry_count} retries with batch_size={current_batch_size}"
        )
        logger.warning(f"   Skipping {variant_id} - can retry later with different settings")
        
        return {
            'success': False,
            'cv_score': None,
            'fold_scores': None,
            'batch_size_used': current_batch_size,
            'oom_retry_count': oom_retry_count,
            'error': f"Persistent OOM after {oom_retry_count} retries (batch_size={current_batch_size})"
        }
    
    # Calculate new batch size
    new_batch_size = max(min_batch_size, current_batch_size // batch_size_reduction_factor)
    oom_retry_count += 1
    
    logger.warning(
        f"⚠️ CUDA OOM error detected with batch_size={current_batch_size} "
        f"(retry {oom_retry_count}/{max_oom_retries})"
    )
    logger.info(f"   Retrying with reduced batch_size={new_batch_size}")
    
    # Perform OOM recovery
    logger.info("   Performing OOM recovery before retry...")
    recover_from_oom(
        model=None,
        delay_seconds=2.0,
        cleanup_passes=3
    )
    
    # Update config with new batch size
    config.training.batch_size = new_batch_size
    
    try:
        # Retry training with reduced batch size
        cv_score, fold_scores = train_func(config)
        
        # Success!
        logger.info(f"✅ Successfully completed with reduced batch_size={new_batch_size}")
        
        return {
            'success': True,
            'cv_score': cv_score,
            'fold_scores': fold_scores,
            'batch_size_used': new_batch_size,
            'oom_retry_count': oom_retry_count
        }
        
    except Exception as retry_error:
        # Check if retry also failed with OOM
        if is_oom_error(retry_error):
            # Recursive call to handle nested OOM
            return handle_oom_error_with_retry(
                error=retry_error,
                config=config,
                current_batch_size=new_batch_size,
                oom_retry_count=oom_retry_count,
                variant_id=variant_id,
                train_func=train_func
            )
        else:
            # Other error during retry - fall through to error handling
            logger.error(f"Error persists even with batch_size={new_batch_size}: {retry_error}")
            return None  # Fall through to normal error handling

