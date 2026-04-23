# cleanup.py
# General GPU memory cleanup functions

import torch
import logging
import gc
import time
from typing import Optional

logger = logging.getLogger(__name__)


def _perform_aggressive_cleanup() -> None:
    """
    Perform aggressive GPU memory cleanup.
    
    Includes resetting memory statistics and multiple cleanup passes
    for thorough memory release, useful for OOM recovery.
    """
    try:
        # Reset peak memory statistics to help allocator release memory
        torch.cuda.reset_peak_memory_stats()
    except RuntimeError as e:
        # CUDA memory stats operations may fail if device is unavailable or in invalid state
        logger.debug(f"Could not reset peak memory stats: {e}")
    
    # Additional aggressive cleanup passes (more passes for OOM recovery)
    for _ in range(5):
        gc.collect()
        try:
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
        except RuntimeError:
            # CUDA operations may fail if device is unavailable or in invalid state
            pass
    
    # Try to collect any remaining CUDA tensors
    try:
        # Force collection of any remaining CUDA objects
        gc.collect()
        torch.cuda.empty_cache()
    except RuntimeError:
        # CUDA operations may fail if device is unavailable or in invalid state
        pass


def cleanup_dataframe_and_memory(
    dataframe: Optional[object] = None,
    dataset: Optional[object] = None,
    dataloader: Optional[object] = None,
    model: Optional[torch.nn.Module] = None,
    aggressive: bool = True,
    delay_seconds: float = 0.5
) -> None:
    """
    Comprehensive cleanup utility for freeing memory after variant completion.
    
    Deletes DataFrame, datasets, dataloaders, and performs GPU memory cleanup.
    This is a convenience function to avoid repeating the cleanup pattern.
    
    Args:
        dataframe: Optional DataFrame to delete
        dataset: Optional dataset to delete
        dataloader: Optional dataloader to delete
        model: Optional model to move to CPU and delete
        aggressive: If True, perform aggressive cleanup
        delay_seconds: Delay after cleanup to allow CUDA time to release memory
    """
    # Store whether dataframe exists before deletion
    had_dataframe = dataframe is not None
    
    # Delete DataFrame if provided
    # Cleanup operations must not fail - catch all exceptions
    if had_dataframe:
        try:
            del dataframe
        except (AttributeError, RuntimeError) as e:
            logger.debug(f"Error deleting dataframe during cleanup: {e}")
        except Exception as e:
            # Catch any other unexpected errors during cleanup
            logger.debug(f"Unexpected error deleting dataframe during cleanup: {e}", exc_info=True)
    
    # Use clear_gpu_memory for the rest
    clear_gpu_memory(
        log_memory=False,
        model=model,
        dataset=dataset,
        dataloader=dataloader,
        aggressive=aggressive,
        delay_seconds=delay_seconds
    )
    
    # Force additional GC passes after deleting DataFrame
    if had_dataframe:
        for _ in range(3):
            gc.collect()
            try:
                torch.cuda.empty_cache()
            except RuntimeError:
                pass


def clear_gpu_memory(
    log_memory: bool = False, 
    model: Optional[torch.nn.Module] = None,
    aggressive: bool = False,
    delay_seconds: float = 0.0,
    dataset: Optional[object] = None,
    dataloader: Optional[object] = None
) -> None:
    """
    Clear GPU memory cache and force garbage collection.
    
    This is useful when training multiple models in sequence (e.g., grid search)
    to prevent GPU memory from accumulating between iterations.
    
    Args:
        log_memory: If True, log memory usage before and after cleanup
        model: Optional model to move to CPU before cleanup (helps ensure proper deletion)
        dataset: Optional dataset to delete (helps free memory from data references)
        dataloader: Optional dataloader to delete (helps free worker processes)
        aggressive: If True, perform aggressive cleanup including memory stats reset
        delay_seconds: Optional delay after cleanup to allow CUDA time to release memory
    """
    if not torch.cuda.is_available():
        return
    
    if log_memory:
        from utils.system.constants import BYTES_PER_GB
        allocated_before = torch.cuda.memory_allocated() / BYTES_PER_GB
        reserved_before = torch.cuda.memory_reserved() / BYTES_PER_GB
        logger.info(f"GPU memory before cleanup: {allocated_before:.2f} GB allocated, {reserved_before:.2f} GB reserved")
    
    # If model provided, move it to CPU before cleanup
    if model is not None:
        try:
            # Handle DataParallel models
            if isinstance(model, torch.nn.DataParallel):
                try:
                    model.module.cpu()
                except (RuntimeError, AttributeError) as e:
                    # If moving to CPU fails (e.g., after OOM), log and continue to deletion
                    logger.debug(f"Could not move DataParallel model to CPU: {e}")
            else:
                try:
                    model.cpu()
                except (RuntimeError, AttributeError) as e:
                    # If moving to CPU fails (e.g., after OOM), log and continue to deletion
                    logger.debug(f"Could not move model to CPU: {e}")
            
            # Clear any cached attributes that might hold GPU references
            # This helps ensure all GPU memory is released
            try:
                if hasattr(model, 'module'):
                    # For DataParallel, clear the underlying module
                    if hasattr(model.module, '__dict__'):
                        for attr_name in list(model.module.__dict__.keys()):
                            if attr_name.startswith('_') or attr_name in ['training', 'eval']:
                                continue
                            try:
                                attr = getattr(model.module, attr_name, None)
                                if attr is not None and hasattr(attr, 'cpu'):
                                    try:
                                        attr.cpu()
                                    except (RuntimeError, AttributeError):
                                        pass
                            except (AttributeError, RuntimeError):
                                # Ignore errors when clearing individual attributes during cleanup
                                pass
                            except Exception:
                                # Catch any other unexpected errors - log but continue cleanup
                                pass
            except (AttributeError, RuntimeError) as e:
                logger.debug(f"Error clearing model attributes: {e}")
            except Exception as e:
                logger.debug(f"Unexpected error clearing model attributes: {e}", exc_info=True)
            
            # Force deletion of model reference even if CPU move failed
            # This is critical for OOM recovery where CPU move may fail
            # Cleanup operations must not fail - catch all exceptions
            try:
                del model
            except (AttributeError, RuntimeError) as e:
                logger.debug(f"Error deleting model: {e}")
            except Exception as e:
                logger.debug(f"Unexpected error deleting model: {e}", exc_info=True)
        except (AttributeError, RuntimeError) as e:
            logger.debug(f"Error during model cleanup: {e}")
        except Exception as e:
            logger.debug(f"Unexpected error during model cleanup: {e}", exc_info=True)
    
    # If dataloader provided, delete it to free worker processes
    if dataloader is not None:
        try:
            # Close worker processes if they exist
            if hasattr(dataloader, '_iterator'):
                try:
                    # Try to close iterator which may close workers
                    iterator = dataloader._iterator
                    if hasattr(iterator, '_shutdown'):
                        iterator._shutdown()
                except (AttributeError, RuntimeError) as e:
                    logger.debug(f"Error closing dataloader iterator: {e}")
                except Exception as e:
                    logger.debug(f"Unexpected error closing dataloader iterator: {e}", exc_info=True)
            
            # Delete dataloader reference
            # Cleanup operations must not fail - catch all exceptions
            del dataloader
        except (AttributeError, RuntimeError) as e:
            logger.debug(f"Error deleting dataloader during cleanup: {e}")
        except Exception as e:
            logger.debug(f"Unexpected error deleting dataloader during cleanup: {e}", exc_info=True)
    
    # If dataset provided, delete it to free data references
    # Cleanup operations must not fail - catch all exceptions
    if dataset is not None:
        try:
            # Clear any cached data in dataset
            if hasattr(dataset, 'data_rows'):
                del dataset.data_rows
            if hasattr(dataset, 'data'):
                del dataset.data
            # Delete dataset reference
            del dataset
        except (AttributeError, RuntimeError) as e:
            logger.debug(f"Error deleting dataset during cleanup: {e}")
        except Exception as e:
            logger.debug(f"Unexpected error deleting dataset during cleanup: {e}", exc_info=True)
    
    # Synchronize all CUDA operations before clearing cache
    try:
        torch.cuda.synchronize()
    except RuntimeError:
        # CUDA synchronization may fail if device is unavailable or in invalid state
        pass
    
    # Clear CUDA cache
    try:
        torch.cuda.empty_cache()
    except RuntimeError:
        # CUDA cache operations may fail if device is unavailable or in invalid state
        pass
    
    # Force Python garbage collection (multiple passes for thorough cleanup)
    for _ in range(2):
        gc.collect()
        try:
            torch.cuda.empty_cache()
        except RuntimeError:
            # CUDA cache operations may fail if device is unavailable or in invalid state
            pass
    
    # Synchronize again
    try:
        torch.cuda.synchronize()
    except RuntimeError:
        # CUDA synchronization may fail if device is unavailable or in invalid state
        pass
    
    # Aggressive cleanup if requested - use specialized OOM recovery function
    if aggressive:
        # Use recover_from_oom() for aggressive cleanup (handles fragmentation better)
        # Note: model is already deleted above, so pass None
        from .recovery import recover_from_oom
        recover_from_oom(
            model=None,  # Already deleted above
            delay_seconds=max(delay_seconds, 1.0),  # Ensure minimum delay for aggressive cleanup
            cleanup_passes=3
        )
    else:
        # Regular cleanup - just clear cache and collect garbage
        try:
            torch.cuda.empty_cache()
        except RuntimeError:
            pass
        
        # Force garbage collection
        gc.collect()
    
    # Force additional garbage collection after deleting objects
    # This helps ensure worker processes and data references are fully released
    if dataset is not None or dataloader is not None:
        for _ in range(2):  # Reduced from 3 since aggressive cleanup already does multiple passes
            gc.collect()
            try:
                torch.cuda.empty_cache()
            except RuntimeError:
                pass
    
    # Optional delay to allow CUDA time to release memory (only if not aggressive, since aggressive already has delays)
    if not aggressive and delay_seconds > 0:
        time.sleep(delay_seconds)
        try:
            torch.cuda.empty_cache()
        except RuntimeError:
            # CUDA cache operations may fail if device is unavailable or in invalid state
            pass
    
    if log_memory:
        from utils.system.constants import BYTES_PER_GB
        allocated_after = torch.cuda.memory_allocated() / BYTES_PER_GB
        reserved_after = torch.cuda.memory_reserved() / BYTES_PER_GB
        logger.info(f"GPU memory after cleanup: {allocated_after:.2f} GB allocated, {reserved_after:.2f} GB reserved")
        
        # Warn if memory wasn't released (common after OOM)
        MIN_MEMORY_THRESHOLD_GB = 0.1  # 100 MB
        if aggressive and allocated_after > MIN_MEMORY_THRESHOLD_GB:
            logger.warning(f"⚠️ GPU memory still allocated after cleanup: {allocated_after:.2f} GB")
            logger.warning("   This may indicate memory fragmentation or lingering references")
            logger.warning("   The next variant may still encounter OOM - consider reducing batch size")

