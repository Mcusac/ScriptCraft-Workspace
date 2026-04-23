# losses.py
# Loss function factory

import torch.nn as nn
import logging

logger = logging.getLogger(__name__)

# Valid loss function names (case-insensitive)
VALID_LOSS_FUNCTIONS = {
    'smoothl1loss': nn.SmoothL1Loss,
    'mseloss': nn.MSELoss,
    'l1loss': nn.L1Loss,
}


def get_loss_function(loss_name: str, **kwargs) -> nn.Module:
    """
    Get loss function by name using factory pattern.
    
    Args:
        loss_name: Name of loss function. Case-insensitive.
                   Valid options: 'SmoothL1Loss', 'MSELoss', 'L1Loss'.
        **kwargs: Additional arguments for loss function constructor.
                  Common options: reduction ('mean', 'sum', 'none').
        
    Returns:
        Loss function module instance ready for use in training.
        
    Raises:
        ValueError: If loss_name is not a valid loss function.
        TypeError: If loss_name is not a string.
        
    Example:
        >>> criterion = get_loss_function('SmoothL1Loss', reduction='mean')
        >>> loss = criterion(predictions, targets)
    """
    # Validate input type
    if not isinstance(loss_name, str):
        raise TypeError(f"loss_name must be str, got {type(loss_name)}")
    
    if not loss_name:
        raise ValueError("loss_name cannot be empty")
    
    # Normalize to lowercase for case-insensitive matching
    loss_name_lower = loss_name.lower()
    
    # Get loss function class
    if loss_name_lower not in VALID_LOSS_FUNCTIONS:
        valid_names = ', '.join(sorted(VALID_LOSS_FUNCTIONS.keys()))
        raise ValueError(
            f"Unknown loss function: '{loss_name}'. "
            f"Valid options: {valid_names}"
        )
    
    loss_class = VALID_LOSS_FUNCTIONS[loss_name_lower]
    
    # Create and return loss function instance
    try:
        loss_function = loss_class(**kwargs)
        logger.debug(f"Created loss function: {loss_name} with kwargs: {kwargs}")
        return loss_function
    except TypeError as e:
        raise ValueError(
            f"Invalid arguments for {loss_name}: {e}. "
            f"Check that kwargs are valid for {loss_class.__name__}."
        )

