# environment_utils.py
# Utilities for environment setup, GPU detection, and weight downloading
#
# This module provides convenience functions that combine multiple environment
# checks and setup operations. The setup_environment() function is intentionally
# a multi-purpose convenience function that orchestrates:
# - Environment detection (Kaggle vs local)
# - GPU availability checking
# - Internet connection checking
# - Optional weight downloading
#
# This design is intentional - it provides a single entry point for common
# environment setup needs while delegating to focused modules for actual work.

import logging
import sys
from typing import Dict, Any, Optional, Tuple

from ..io.paths import is_kaggle_environment
from .device import get_device_info
from .weights import check_internet_connection

logger = logging.getLogger(__name__)


def suppress_kaggle_install_script_error() -> None:
    """
    Suppress harmless install_requirements.sh error from Kaggle environment.
    
    Kaggle tries to execute /kaggle/input/pm-*/install_requirements.sh but the file
    doesn't exist, causing an error message. This function filters stderr to suppress
    this specific error pattern.
    
    Should be called early in the application lifecycle, before any imports that
    might trigger the error.
    """
    if not is_kaggle_environment():
        return
    
    class FilteredStderr:
        """Filter stderr to suppress install_requirements.sh error messages."""
        def __init__(self, original_stderr):
            self.original_stderr = original_stderr
        
        def write(self, message):
            # Filter out install_requirements.sh "No such file" errors
            if 'install_requirements.sh' not in message or 'No such file' not in message:
                self.original_stderr.write(message)
        
        def flush(self):
            self.original_stderr.flush()
    
    # Replace stderr with filtered version
    sys.stderr = FilteredStderr(sys.stderr)


# Call suppression function at module import time so it runs early
# This ensures it's active when the notebook imports this module
suppress_kaggle_install_script_error()


def get_gpu_info(is_kaggle: bool) -> Tuple[bool, Dict[str, Any]]:
    """
    Get GPU availability and information.
    
    Uses get_device_info consistently for both Kaggle and local environments,
    adding Kaggle-specific print statements when needed.
    
    Args:
        is_kaggle: Whether running on Kaggle environment
    
    Returns:
        Tuple of (has_gpu, gpu_info)
    """
    try:
        device_info = get_device_info()
        has_gpu = device_info.get('cuda_available', False)
        
        if has_gpu:
            # Use device_info structure, but add compatibility fields for Kaggle
            gpu_info = device_info.copy()
            
            # Add 'name' and 'device_name' fields for convenience
            if device_info.get('device_names'):
                gpu_name = device_info['device_names'][0]
                gpu_info['name'] = gpu_name
                gpu_info['device_name'] = gpu_name
            
            # Log GPU information (consistent logging format with timestamps)
            gpu_name = device_info.get('device_names', [None])[0] if device_info.get('device_names') else None
            gpu_count = device_info.get('device_count', 0)
            if gpu_name:
                logger.info(f"\n✅ GPU Available:")
                logger.info(f"   Device: {gpu_name}")
                logger.info(f"   Count: {gpu_count}")
                if gpu_count > 1:
                    logger.info(f"   ⚡ Multiple GPUs detected - will use DataParallel")
            else:
                logger.info("\n✅ GPU Available")
        else:
            gpu_info = {}
            logger.warning("\n⚠️ No GPU detected - training will be slower on CPU")
    except Exception as e:
        logger.warning(f"Error checking GPU: {e}")
        has_gpu = False
        gpu_info = {}
    
    return has_gpu, gpu_info


def setup_environment(
    model_name: Optional[str] = None,
    download_weights: bool = True
) -> Dict[str, Any]:
    """
    Setup environment: check Kaggle/local, GPU availability, and configure weight cache.
    
    Note: This function configures the weight cache but does NOT download weights.
    Weight loading happens automatically when the model is created via TimmModel.__init__().
    
    Args:
        model_name: Optional model name for cache configuration (e.g., 'efficientnet_b3')
        download_weights: If True, configure weight cache for model_name.
                         The function uses ensure_weight_cache_ready() internally.
    
    Returns:
        Dictionary with environment info:
        - 'is_kaggle': bool - Whether running on Kaggle
        - 'has_gpu': bool - Whether GPU is available
        - 'gpu_info': dict - GPU information (name, count, etc.)
        - 'has_internet': bool - Whether internet connection is available
        - 'weights_downloaded': bool - Whether weight cache is ready.
    """
    # Detect environment
    is_kaggle = is_kaggle_environment()
    logger.info(f"Running on Kaggle: {is_kaggle}")
    
    # Get GPU info
    has_gpu, gpu_info = get_gpu_info(is_kaggle)
    
    # Check internet availability
    has_internet = check_internet_connection()
    weights_downloaded = False
    
    # Configure weight cache if requested
    # Note: This only configures the cache, actual weight loading happens when model is created
    if download_weights and model_name:
        from .weights import ensure_weight_cache_ready
        cache_ready, _ = ensure_weight_cache_ready(model_name)
        weights_downloaded = cache_ready
    
    return {
        'is_kaggle': is_kaggle,
        'has_gpu': has_gpu,
        'gpu_info': gpu_info,
        'has_internet': has_internet,
        'weights_downloaded': weights_downloaded
    }

