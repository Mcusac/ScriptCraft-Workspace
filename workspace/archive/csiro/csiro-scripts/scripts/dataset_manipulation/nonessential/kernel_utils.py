# kernel_utils.py
# Kernel size utilities for data manipulation operations

import logging

logger = logging.getLogger(__name__)


def ensure_odd_kernel_size(kernel_size: int) -> int:
    """
    Ensure kernel size is odd, adjusting if necessary.
    
    Args:
        kernel_size: Kernel size to validate/adjust. Must be positive.
        
    Returns:
        Odd kernel size (same if already odd, incremented by 1 if even).
        
    Raises:
        ValueError: If kernel_size is not positive.
        TypeError: If kernel_size is not an integer.
    """
    from utils.system import validate_positive
    
    validate_positive(kernel_size, "kernel_size")
    
    if not isinstance(kernel_size, int):
        raise TypeError(f"kernel_size must be integer, got {type(kernel_size)}")
    
    if kernel_size % 2 == 0:
        adjusted = kernel_size + 1
        logger.debug(f"Adjusted kernel_size from {kernel_size} to {adjusted} (must be odd)")
        return adjusted
    
    return kernel_size

