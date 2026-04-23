# seed_utils.py
# Utilities for setting random seeds for reproducibility

import random
import numpy as np
import torch
import os
import logging

logger = logging.getLogger(__name__)


def set_seed(seed: int = 42) -> None:
    """
    Set random seeds for reproducibility across Python, NumPy, and PyTorch.
    
    Sets seeds for all random number generators and configures PyTorch for
    deterministic behavior. Note: deterministic mode may impact performance.
    
    Args:
        seed: Random seed value (default: 42). Must be a valid integer.
              Typically a non-negative integer, but negative values are allowed.
        
    Raises:
        TypeError: If seed is not an integer.
    """
    if not isinstance(seed, int):
        raise TypeError(f"seed must be integer, got {type(seed)}")
    
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    
    # Ensure deterministic behavior (may impact performance)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    
    # Enable deterministic algorithms if available (PyTorch 1.8+)
    try:
        torch.use_deterministic_algorithms(True, warn_only=True)
    except AttributeError:
        # Older PyTorch versions don't have this function
        logger.debug("PyTorch version does not support use_deterministic_algorithms() - skipping (expected for PyTorch < 1.8)")
    except RuntimeError as e:
        # Some operations may not support deterministic mode
        logger.warning(f"⚠️ Some operations may not support deterministic mode: {e}")
    
    # Set CUBLAS_WORKSPACE_CONFIG for deterministic CuBLAS operations (required for CUDA >= 10.2)
    # This suppresses the warning about non-deterministic CuBLAS operations
    if 'CUBLAS_WORKSPACE_CONFIG' not in os.environ:
        os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':4096:8'
    
    # Set environment variable for additional reproducibility
    os.environ['PYTHONHASHSEED'] = str(seed)
    
    logger.info(f"✅ Random seeds set to {seed} with deterministic mode enabled")


def validate_reproducibility_settings(config=None) -> None:
    """
    Validate that reproducibility settings are correctly configured.
    
    Checks:
    - Seeds are set
    - CUDA deterministic flags
    - Warns about potential non-deterministic operations
    
    Args:
        config: Optional Config object to check seed values from
    """
    warnings = []
    
    # Check CUDA deterministic settings
    if not torch.backends.cudnn.deterministic:
        warnings.append("⚠️ torch.backends.cudnn.deterministic is False - operations may be non-deterministic")
    
    if torch.backends.cudnn.benchmark:
        warnings.append("⚠️ torch.backends.cudnn.benchmark is True - may cause non-deterministic behavior")
    
    # Check config if provided
    if config is not None:
        if not hasattr(config, 'seed') or config.seed is None:
            warnings.append("⚠️ config.seed is not set")
        
        if hasattr(config, 'cv') and hasattr(config.cv, 'random_state'):
            if config.cv.random_state is None:
                warnings.append("⚠️ config.cv.random_state is not set - CV splits may be non-deterministic")
    
    # Check environment variable
    if 'PYTHONHASHSEED' not in os.environ:
        warnings.append("⚠️ PYTHONHASHSEED environment variable not set")
    
    if warnings:
        logger.warning("Reproducibility warnings:")
        for warning in warnings:
            logger.warning(f"  {warning}")
    else:
        logger.info("✅ All reproducibility settings validated")

