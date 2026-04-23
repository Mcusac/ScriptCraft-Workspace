# validation_utils.py
# General validation utilities for common validation patterns

from typing import Tuple, Union, Optional
import logging
import numpy as np

logger = logging.getLogger(__name__)


# ============================================================================
# Numeric Validation
# ============================================================================

def validate_non_negative(value: float, name: str) -> None:
    """
    Validate that a value is non-negative.
    
    Args:
        value: Value to validate.
        name: Name of the parameter for error messages.
        
    Raises:
        ValueError: If value is negative.
        TypeError: If value is not numeric.
    """
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric (int or float), got {type(value)}")
    
    if value < 0:
        raise ValueError(f"{name} must be non-negative, got {value}")


def validate_positive(value: Union[int, float], name: str) -> None:
    """
    Validate that a value is positive (> 0).
    
    Args:
        value: Value to validate.
        name: Name of the parameter for error messages.
        
    Raises:
        ValueError: If value is not positive.
        TypeError: If value is not numeric.
    """
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric (int or float), got {type(value)}")
    
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")


def validate_range(
    value: float,
    min_val: Optional[float] = None,
    max_val: Optional[float] = None,
    name: str = "value"
) -> None:
    """
    Validate that a value is within a specified range.
    
    Args:
        value: Value to validate.
        min_val: Minimum allowed value (inclusive). If None, no minimum check.
        max_val: Maximum allowed value (inclusive). If None, no maximum check.
        name: Name of the parameter for error messages.
        
    Raises:
        ValueError: If value is outside the specified range.
        TypeError: If value is not numeric.
    """
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric (int or float), got {type(value)}")
    
    if min_val is not None and value < min_val:
        raise ValueError(f"{name} must be >= {min_val}, got {value}")
    
    if max_val is not None and value > max_val:
        raise ValueError(f"{name} must be <= {max_val}, got {value}")


def validate_optional_non_negative(value: Optional[float], name: str) -> None:
    """
    Validate that an optional value is non-negative if provided.
    
    Args:
        value: Optional value to validate. Can be None.
        name: Name of the parameter for error messages.
        
    Raises:
        ValueError: If value is provided and is negative.
        TypeError: If value is not None and not numeric.
    """
    if value is not None:
        validate_non_negative(value, name)


# ============================================================================
# Tuple/List Validation
# ============================================================================

def validate_tuple_length(value: Tuple, expected_length: int, name: str) -> None:
    """
    Validate that a tuple has the expected length.
    
    Args:
        value: Tuple to validate.
        expected_length: Expected length of the tuple.
        name: Name of the parameter for error messages.
        
    Raises:
        ValueError: If tuple length doesn't match expected length.
        TypeError: If value is not a tuple or list.
    """
    if not isinstance(value, (tuple, list)):
        raise TypeError(f"{name} must be a tuple or list, got {type(value)}")
    
    if len(value) != expected_length:
        raise ValueError(
            f"{name} must be a tuple of length {expected_length}, got {value} (length {len(value)})"
        )


def validate_min_max_tuple(
    value: Tuple[float, float],
    name: str,
    min_val: Optional[float] = None,
    max_val: Optional[float] = None,
    allow_equal: bool = False
) -> None:
    """
    Validate a (min, max) tuple with range constraints.
    
    Args:
        value: Tuple of (min, max) values.
        name: Name of the parameter for error messages.
        min_val: Minimum allowed value for both min and max (inclusive).
        max_val: Maximum allowed value for both min and max (inclusive).
        allow_equal: If True, allows min == max. If False, requires min < max.
        
    Raises:
        ValueError: If tuple is invalid or values are out of range.
        TypeError: If value is not a tuple or list.
    """
    validate_tuple_length(value, 2, name)
    
    min_value, max_value = value
    
    # Validate individual values
    if min_val is not None:
        validate_range(min_value, min_val=min_val, name=f"{name}[0]")
        validate_range(max_value, min_val=min_val, name=f"{name}[1]")
    
    if max_val is not None:
        validate_range(min_value, max_val=max_val, name=f"{name}[0]")
        validate_range(max_value, max_val=max_val, name=f"{name}[1]")
    
    # Validate min <= max (or min < max if not allowing equal)
    if allow_equal:
        if min_value > max_value:
            raise ValueError(
                f"{name} min ({min_value}) must be <= max ({max_value})"
            )
    else:
        if min_value >= max_value:
            raise ValueError(
                f"{name} min ({min_value}) must be < max ({max_value})"
            )


# ============================================================================
# NumPy Array Validation
# ============================================================================

def validate_numpy_array(
    array: np.ndarray,
    name: str,
    expected_ndim: Optional[int] = None,
    expected_shape: Optional[Tuple[int, ...]] = None,
    min_samples: int = 1
) -> None:
    """
    Validate numpy array properties.
    
    Args:
        array: Array to validate.
        name: Name of the parameter for error messages.
        expected_ndim: Expected number of dimensions. If None, no check.
        expected_shape: Expected shape tuple. If None, no check.
                       Can use -1 for "any" dimension (e.g., (-1, 3) for any rows, 3 columns).
        min_samples: Minimum number of samples (first dimension) required (default: 1).
        
    Raises:
        TypeError: If array is not a numpy array.
        ValueError: If array doesn't meet shape or size requirements.
    """
    if not isinstance(array, np.ndarray):
        raise TypeError(f"{name} must be numpy array, got {type(array)}")
    
    if expected_ndim is not None and array.ndim != expected_ndim:
        raise ValueError(
            f"{name} must be {expected_ndim}D array, got shape {array.shape}"
        )
    
    if expected_shape is not None:
        if len(expected_shape) != array.ndim:
            raise ValueError(
                f"{name} shape mismatch: expected {expected_ndim}D, got {array.ndim}D"
            )
        
        for i, (expected_dim, actual_dim) in enumerate(zip(expected_shape, array.shape)):
            if expected_dim != -1 and expected_dim != actual_dim:
                raise ValueError(
                    f"{name} shape mismatch at dimension {i}: "
                    f"expected {expected_dim}, got {actual_dim}. "
                    f"Full shape: {array.shape}"
                )
    
    if array.shape[0] < min_samples:
        raise ValueError(
            f"{name} must have at least {min_samples} samples, got {array.shape[0]}"
        )


def validate_matching_arrays(
    array1: np.ndarray,
    array2: np.ndarray,
    name1: str,
    name2: str,
    check_shape: bool = True
) -> None:
    """
    Validate that two numpy arrays have matching properties.
    
    Args:
        array1: First array to validate.
        array2: Second array to validate.
        name1: Name of first array for error messages.
        name2: Name of second array for error messages.
        check_shape: If True, checks that shapes match exactly (default: True).
        
    Raises:
        TypeError: If either array is not a numpy array.
        ValueError: If arrays don't match in shape or number of samples.
    """
    # Validate both are numpy arrays
    validate_numpy_array(array1, name1)
    validate_numpy_array(array2, name2)
    
    # Check number of samples matches
    if array1.shape[0] != array2.shape[0]:
        raise ValueError(
            f"{name1} and {name2} must have same number of samples: "
            f"{name1}={array1.shape[0]}, {name2}={array2.shape[0]}"
        )
    
    # Check full shape matches if requested
    if check_shape and array1.shape != array2.shape:
        raise ValueError(
            f"{name1} and {name2} must have same shape: "
            f"{name1}={array1.shape}, {name2}={array2.shape}"
        )


def validate_array_not_empty(array: np.ndarray, name: str) -> None:
    """
    Validate that array is not empty.
    
    Args:
        array: Array to validate.
        name: Name of the parameter for error messages.
        
    Raises:
        ValueError: If array is empty (has 0 samples).
    """
    if array.size == 0 or (array.ndim > 0 and array.shape[0] == 0):
        raise ValueError(f"{name} cannot be empty")

