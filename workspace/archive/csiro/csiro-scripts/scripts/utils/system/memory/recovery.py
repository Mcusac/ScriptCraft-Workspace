# recovery.py
# OOM recovery functions for GPU memory management

import torch
import logging
import gc
import time
from typing import Optional

from .cleanup import _perform_aggressive_cleanup

logger = logging.getLogger(__name__)


def recover_from_oom(
    model: Optional[torch.nn.Module] = None,
    delay_seconds: float = 2.0,
    cleanup_passes: int = 3
) -> None:
    """
    Aggressive memory cleanup specifically for OOM recovery.
    
    Handles memory fragmentation by resetting CUDA stats and performing
    multiple cleanup passes with delays. This is more aggressive than
    regular cleanup and should be used after OutOfMemoryError.
    
    Args:
        model: Optional model to clean up. If provided, attempts to move
               to CPU and delete. If CPU move fails (common after OOM),
               forces deletion anyway.
        delay_seconds: Delay between cleanup passes to allow CUDA allocator
                      time to defragment memory (default: 2.0).
        cleanup_passes: Number of cleanup passes to perform (default: 3).
        
    Raises:
        RuntimeError: If CUDA is not available (returns early).
    """
    if not torch.cuda.is_available():
        return
    
    logger.info("🔄 Starting OOM recovery: aggressive memory cleanup")
    
    # Log memory state before cleanup
    try:
        from utils.system.constants import BYTES_PER_GB
        allocated_before = torch.cuda.memory_allocated() / BYTES_PER_GB
        reserved_before = torch.cuda.memory_reserved() / BYTES_PER_GB
        logger.info(f"   Memory before: {allocated_before:.2f} GB allocated, {reserved_before:.2f} GB reserved")
    except RuntimeError:
        pass
    
    # Handle model cleanup first (before other cleanup)
    if model is not None:
        try:
            # Try to move model to CPU (may fail after OOM)
            if isinstance(model, torch.nn.DataParallel):
                try:
                    model.module.cpu()
                except (RuntimeError, AttributeError) as e:
                    logger.debug(f"Could not move DataParallel model to CPU after OOM: {e}")
            else:
                try:
                    model.cpu()
                except (RuntimeError, AttributeError) as e:
                    logger.debug(f"Could not move model to CPU after OOM: {e}")
        except Exception as e:
            logger.debug(f"Error during model CPU move: {e}")
        
        # Force deletion of model even if CPU move failed
        try:
            # Clear any cached attributes that might hold references
            if hasattr(model, 'module'):
                delattr(model, 'module')
            del model
        except Exception as e:
            logger.debug(f"Error deleting model after OOM: {e}")
    
    # Synchronize all CUDA operations before cleanup
    try:
        torch.cuda.synchronize()
    except RuntimeError:
        pass
    
    # Reset CUDA memory statistics to help allocator defragment
    # This is critical for handling memory fragmentation after OOM
    try:
        torch.cuda.reset_peak_memory_stats()
        logger.debug("   Reset CUDA memory statistics")
    except RuntimeError as e:
        logger.debug(f"Could not reset peak memory stats: {e}")
    
    # Perform multiple cleanup passes with delays
    # Delays allow CUDA allocator time to defragment memory
    for pass_num in range(cleanup_passes):
        if pass_num > 0:
            # Delay between passes (except first)
            time.sleep(delay_seconds)
            logger.debug(f"   Cleanup pass {pass_num + 1}/{cleanup_passes}")
        
        # Force Python garbage collection
        gc.collect()
        
        # Clear CUDA cache
        try:
            torch.cuda.empty_cache()
        except RuntimeError:
            pass
        
        # Synchronize to ensure operations complete
        try:
            torch.cuda.synchronize()
        except RuntimeError:
            pass
    
    # Final aggressive cleanup pass
    _perform_aggressive_cleanup()
    
    # Final delay to allow allocator to fully release memory
    if delay_seconds > 0:
        time.sleep(delay_seconds)
        try:
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
        except RuntimeError:
            pass
    
    # Log memory state after cleanup
    try:
        from utils.system.constants import BYTES_PER_GB
        allocated_after = torch.cuda.memory_allocated() / BYTES_PER_GB
        reserved_after = torch.cuda.memory_reserved() / BYTES_PER_GB
        logger.info(f"   Memory after: {allocated_after:.2f} GB allocated, {reserved_after:.2f} GB reserved")
        
        if allocated_after > 0.1:  # More than 100 MB
            logger.warning(f"   ⚠️ Memory still allocated: {allocated_after:.2f} GB (may indicate fragmentation)")
    except RuntimeError:
        pass
    
    logger.info("✅ OOM recovery complete")

