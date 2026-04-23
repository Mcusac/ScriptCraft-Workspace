# weight_cache_utils.py
# Utilities for managing pretrained weight caches for offline Kaggle submissions

import os
import logging
from pathlib import Path
from typing import Optional, Tuple
import socket

logger = logging.getLogger(__name__)


def check_internet_connection(timeout: int = 5) -> bool:
    """
    Check if internet connection is available.
    
    Args:
        timeout: Timeout in seconds for connection attempt
        
    Returns:
        True if internet is available, False otherwise
    """
    try:
        # Try to connect to huggingface.co (where timm weights are hosted)
        socket.create_connection(("huggingface.co", 443), timeout=timeout)
        return True
    except (socket.error, OSError):
        return False


def get_kaggle_working_weights_dir() -> Path:
    """Get the path to weights directory in Kaggle working directory."""
    from config.path_constants import KAGGLE_WORKING_WEIGHTS
    return KAGGLE_WORKING_WEIGHTS


def get_kaggle_input_weights_dir() -> Optional[Path]:
    """
    Find the timm-weights directory in Kaggle input.
    
    Searches for a directory named 'timm-weights' in /kaggle/input/ that contains
    HuggingFace cache structure (models--timm--*). This handles both dataset
    and model uploads which can have different path structures.
    
    Returns:
        Path to timm-weights directory if found, None otherwise
    """
    from config.path_constants import KAGGLE_INPUT
    input_dir = KAGGLE_INPUT
    if not input_dir.exists():
        return None
    
    # Search for 'timm-weights' directory in /kaggle/input/
    # This handles paths like:
    # - /kaggle/input/timm-weights/ (dataset)
    # - /kaggle/input/timm/pytorch/default/1/timm-weights/ (model)
    for path in input_dir.rglob('timm-weights'):
        if path.is_dir():
            # Verify it contains HuggingFace cache structure
            if any(path.glob('models--timm--*')):
                logger.info(f"Found timm-weights directory: {path}")
                return path
    
    return None


def find_available_weights_cache() -> Tuple[Optional[Path], bool]:
    """
    Find available weights cache location with fallback chain.
    
    Checks in order:
    1. Internet available -> use default HuggingFace cache
    2. /kaggle/working/timm_weights/ (downloaded in current session)
    3. /kaggle/input/timm-weights/ (from Kaggle input dataset)
    
    Returns:
        Tuple of (cache_path, has_internet)
        - cache_path: Path to use for cache, or None if no cache available
        - has_internet: Whether internet is available
    """
    has_internet = check_internet_connection()
    
    if has_internet:
        # Internet available - use default HuggingFace cache
        # HuggingFace will download to default location
        logger.info("Internet available - will use default HuggingFace cache")
        return None, True
    
    # No internet - check offline locations
    logger.info("No internet detected - checking offline weight locations...")
    
    # Check /kaggle/working/timm_weights/ (downloaded in current session)
    working_weights = get_kaggle_working_weights_dir()
    if working_weights.exists() and any(working_weights.iterdir()):
        logger.info(f"Found weights in working directory: {working_weights}")
        return working_weights, False
    
    # Check /kaggle/input/ for timm-weights (from Kaggle input dataset/model)
    input_weights = get_kaggle_input_weights_dir()
    if input_weights is not None and input_weights.exists() and any(input_weights.iterdir()):
        logger.info(f"Found weights in input: {input_weights}")
        return input_weights, False
    
    logger.warning("No offline weights found in working or input directories")
    return None, False


def configure_huggingface_cache(cache_path: Optional[Path] = None) -> None:
    """
    Configure HuggingFace cache environment variables.
    
    Args:
        cache_path: Path to use for cache. If None, uses default location.
                    If provided, sets HF_HOME and HUGGINGFACE_HUB_CACHE to this path.
    """
    if cache_path is None:
        # Use default HuggingFace cache (don't override)
        # Clear any existing overrides
        if 'HF_HOME' in os.environ:
            del os.environ['HF_HOME']
        if 'HUGGINGFACE_HUB_CACHE' in os.environ:
            del os.environ['HUGGINGFACE_HUB_CACHE']
        logger.debug("Using default HuggingFace cache location")
    else:
        # Set custom cache location
        cache_path = Path(cache_path)
        cache_path.mkdir(parents=True, exist_ok=True)
        
        # Set both environment variables for compatibility
        os.environ['HF_HOME'] = str(cache_path)
        os.environ['HUGGINGFACE_HUB_CACHE'] = str(cache_path)
        logger.info(f"Configured HuggingFace cache to: {cache_path}")


def setup_weight_cache() -> Tuple[Optional[Path], bool]:
    """
    Setup weight cache for offline/online use.
    
    This function:
    1. Checks internet availability
    2. Finds available cache location
    3. Configures HuggingFace environment variables
    
    Returns:
        Tuple of (cache_path, has_internet)
        - cache_path: Path to cache (None if using default)
        - has_internet: Whether internet is available
    """
    cache_path, has_internet = find_available_weights_cache()
    configure_huggingface_cache(cache_path)
    return cache_path, has_internet


def prepare_weights_download_dir() -> Path:
    """
    Prepare directory for downloading weights in Kaggle working directory.
    
    Returns:
        Path to weights directory in /kaggle/working/timm_weights/
    """
    weights_dir = get_kaggle_working_weights_dir()
    weights_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Prepared weights download directory: {weights_dir}")
    return weights_dir


def ensure_weight_cache_ready(model_name: Optional[str] = None) -> Tuple[bool, Optional[Path]]:
    """
    Ensure weight cache is configured and ready for use.
    
    Configures the HuggingFace cache based on availability:
    - If internet is available, configures cache for downloading weights
    - If no internet, checks for existing weights in input directory and configures cache to use them
    
    Note: This function does NOT download weights. Weight loading happens automatically
    when the model is created via TimmModel.__init__().
    
    Args:
        model_name: Optional model name for informational messages (e.g., 'efficientnet_b3')
    
    Returns:
        Tuple of (cache_ready, cache_path)
        - cache_ready: True if cache is configured and ready (weights available or internet available)
        - cache_path: Path to cache if using offline weights, None if using default/online cache
    """
    has_internet = check_internet_connection()
    
    if has_internet:
        # Internet available - configure cache for downloading
        # Use default HuggingFace cache or working directory
        weights_dir = prepare_weights_download_dir()
        configure_huggingface_cache(weights_dir)
        
        if model_name:
            logger.info(f"\n🌐 Internet available - weights will be downloaded when model is created")
            logger.info(f"   Model: {model_name}")
            logger.info(f"   Cache location: {weights_dir}")
        else:
            logger.info(f"\n🌐 Internet available - weights will be downloaded when model is created")
        return True, weights_dir
    
    # No internet - check for existing weights
    logger.info("\n📴 No internet - checking for existing weights...")
    
    # Check /kaggle/working/timm_weights/ (downloaded in current session)
    working_weights = get_kaggle_working_weights_dir()
    if working_weights.exists() and any(working_weights.iterdir()):
        configure_huggingface_cache(working_weights)
        logger.info(f"✅ Found weights in working directory: {working_weights}")
        if model_name:
            logger.info(f"   Model: {model_name}")
        return True, working_weights
    
    # Check /kaggle/input/ for timm-weights (from Kaggle input dataset/model)
    input_weights = get_kaggle_input_weights_dir()
    if input_weights is not None and input_weights.exists() and any(input_weights.iterdir()):
        configure_huggingface_cache(input_weights)
        logger.info(f"✅ Found weights in input directory: {input_weights}")
        if model_name:
            logger.info(f"   Model: {model_name}")
        return True, input_weights
    
    # No weights found
    logger.warning("⚠️ No weights found in working or input directories")
    logger.info("   Weights will be loaded from internet when model is created (if internet becomes available)")
    logger.info("   Or model will fallback to non-pretrained if download fails")
    if model_name:
        logger.info(f"   Model: {model_name}")
    
    # Still configure cache to working directory for potential future downloads
    weights_dir = prepare_weights_download_dir()
    configure_huggingface_cache(weights_dir)
    return False, weights_dir

