"""
Ensemble method configuration for CAFA 6 protein function prediction.
Provides default values and parameter validation ranges for ensemble methods.

Versioning: Changing default parameter values creates a new ensemble config version.
Track changes in version comments or git commits.
"""

from typing import List

# Ensemble config version (increment when changing defaults)
ENSEMBLE_CONFIG_VERSION = "1.0"

# Default ensemble method
DEFAULT_ENSEMBLE_METHOD = "average"

# Merge method (for 2 submissions)
MERGE_METHOD = "merge"  # Special method name for outer merge strategy

# Default parameter values for tunable ensemble methods
# Change these values to create new ensemble config versions (e.g., v1.1, v1.2)
ENSEMBLE_DEFAULTS = {
    "power_average": {
        "power": 1.5  # Default power value (v1.0)
    },
    "percentile": {
        "percentile": 75.0  # Default percentile value (v1.0)
    }
}

# Parameter validation ranges (for CLI validation and error messages)
ENSEMBLE_PARAM_RANGES = {
    "power_average": {
        "power": (0.1, 5.0)  # Min, max power value
    },
    "percentile": {
        "percentile": (0.0, 100.0)  # Min, max percentile value
    }
}


def get_ensemble_default(method: str, param: str) -> float:
    """
    Get default value for ensemble method parameter.
    
    Args:
        method: Ensemble method name
        param: Parameter name
        
    Returns:
        float: Default parameter value
        
    Raises:
        KeyError: If method or parameter not found
    """
    if method not in ENSEMBLE_DEFAULTS:
        raise KeyError(f"No defaults available for method '{method}'")
    if param not in ENSEMBLE_DEFAULTS[method]:
        raise KeyError(f"No default for parameter '{param}' in method '{method}'")
    return ENSEMBLE_DEFAULTS[method][param]


def get_available_ensemble_methods() -> List[str]:
    """
    Get list of available ensemble methods.
    
    Returns:
        list[str]: List of ensemble method names
    """
    return [
        'average',
        'weighted_average',
        'max',
        'geometric_mean',
        'rank_average',
        'power_average',
        'percentile'
    ]


def validate_ensemble_param(method: str, param: str, value: float) -> bool:
    """
    Validate ensemble method parameter value.
    
    Args:
        method: Ensemble method name
        param: Parameter name
        value: Parameter value to validate
        
    Returns:
        bool: True if value is valid
        
    Raises:
        KeyError: If method or parameter not found
        ValueError: If value is out of range
    """
    if method not in ENSEMBLE_PARAM_RANGES:
        raise KeyError(f"No validation ranges for method '{method}'")
    if param not in ENSEMBLE_PARAM_RANGES[method]:
        raise KeyError(f"No validation range for parameter '{param}' in method '{method}'")
    
    min_val, max_val = ENSEMBLE_PARAM_RANGES[method][param]
    if not (min_val <= value <= max_val):
        msg = (f"Parameter '{param}' for method '{method}' must be in range "
               f"[{min_val}, {max_val}], got {value}")
        raise ValueError(msg)
    return True

