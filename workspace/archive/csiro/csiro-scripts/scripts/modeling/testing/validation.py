# validation.py
# Prediction validation utilities

import numpy as np
import logging
from config.evaluation_constants import NUM_PRIMARY_TARGETS

logger = logging.getLogger(__name__)


def validate_predictions_shape(
    predictions: np.ndarray,
    expected_count: int,
    expected_cols: int = NUM_PRIMARY_TARGETS
) -> None:
    """
    Validate predictions array shape and count.
    
    Args:
        predictions: Predictions array to validate. Must be 2D numpy array.
        expected_count: Expected number of rows (number of images).
        expected_cols: Expected number of columns (default: NUM_PRIMARY_TARGETS for primary targets).
        
    Raises:
        ValueError: If predictions have invalid shape or count doesn't match.
        TypeError: If predictions is not a numpy array.
    """
    if not isinstance(predictions, np.ndarray):
        raise TypeError(f"predictions must be numpy array, got {type(predictions)}")
    
    if predictions.ndim != 2:
        raise ValueError(f"Predictions must be 2D array, got shape {predictions.shape}")
    
    if predictions.shape[1] != expected_cols:
        raise ValueError(
            f"Predictions must have {expected_cols} columns (got {predictions.shape[1]}). "
            f"Expected {expected_cols} primary targets"
        )
    
    if predictions.shape[0] != expected_count:
        raise ValueError(
            f"Predictions count ({predictions.shape[0]}) doesn't match "
            f"expected count ({expected_count})"
        )
