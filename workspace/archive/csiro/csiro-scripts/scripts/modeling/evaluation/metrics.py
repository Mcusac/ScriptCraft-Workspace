# metrics.py
# Evaluation metrics including weighted R² from competition

import numpy as np
from typing import Dict, Tuple, Optional
import logging

from config.evaluation_constants import (
    TARGET_WEIGHTS, 
    TARGET_ORDER, 
    NUM_PRIMARY_TARGETS,
    NUM_TOTAL_TARGETS
)
from utils.system import validate_numpy_array, validate_matching_arrays, validate_array_not_empty

logger = logging.getLogger(__name__)


def _validate_metric_inputs(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    expected_ndim: int = 2,
    expected_shape: Optional[Tuple[int, ...]] = None
) -> None:
    """
    Validate inputs for metric calculation functions.
    
    Args:
        y_true: True values array to validate
        y_pred: Predicted values array to validate
        expected_ndim: Expected number of dimensions (default: 2)
        expected_shape: Optional expected shape tuple. Can use -1 for "any" dimension.
        
    Raises:
        ValueError: If inputs have invalid shapes or are empty.
        TypeError: If inputs are not numpy arrays.
    """
    validate_numpy_array(y_true, "y_true", expected_ndim=expected_ndim, expected_shape=expected_shape)
    validate_numpy_array(y_pred, "y_pred", expected_ndim=expected_ndim, expected_shape=expected_shape)
    validate_matching_arrays(y_true, y_pred, "y_true", "y_pred", check_shape=True)
    validate_array_not_empty(y_true, "y_true")


def _compute_derived_targets(primary_targets: np.ndarray) -> np.ndarray:
    """
    Compute derived targets (GDM_g and Dry_Total_g) from primary targets.
    
    Args:
        primary_targets: Array of shape (N, NUM_PRIMARY_TARGETS) with primary target values
        
    Returns:
        Array of shape (N, NUM_TOTAL_TARGETS) with all targets (primary + derived)
    """
    return np.column_stack((
        primary_targets,  # Primary targets
        primary_targets[:, :2].sum(axis=1),  # GDM_g = Dry_Green_g + Dry_Clover_g
        primary_targets.sum(axis=1),  # Dry_Total_g = sum of all primary targets
    ))


def calc_metric(
    outputs: np.ndarray,
    targets: np.ndarray
) -> Tuple[float, np.ndarray]:
    """
    Calculate weighted R² from primary target model outputs.
    
    Model outputs NUM_PRIMARY_TARGETS values (primary targets).
    Computes derived targets, then calculates weighted R².
    
    Args:
        outputs: Model predictions, shape (N, NUM_PRIMARY_TARGETS) - primary targets.
                 Must be numpy array with 2 dimensions.
        targets: True values, shape (N, NUM_PRIMARY_TARGETS) - primary targets.
                 Must be numpy array with 2 dimensions, same shape as outputs.
        
    Returns:
        Tuple of (weighted_r2, r2_scores_per_target):
        - weighted_r2: Single weighted R² score (float)
        - r2_scores_per_target: R² score for each target (np.ndarray, shape (NUM_TOTAL_TARGETS,))
        
    Raises:
        ValueError: If outputs or targets have invalid shapes or types.
        TypeError: If inputs are not numpy arrays.
    """
    # Validate inputs
    _validate_metric_inputs(outputs, targets, expected_ndim=2, expected_shape=(-1, NUM_PRIMARY_TARGETS))
    
    # Compute GDM and Total for predictions and targets
    y_pred = _compute_derived_targets(outputs)
    y_true = _compute_derived_targets(targets)
    
    # Calculate weighted R²
    weighted_r2, r2_scores = weighted_r2_score(y_true, y_pred)
    
    return weighted_r2, r2_scores


def weighted_r2_score(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    weights: Optional[Dict[str, float]] = None
) -> Tuple[float, np.ndarray]:
    """
    Calculate weighted R² score matching competition formula exactly.
    
    Competition formula:
    R² = 1 - (RSS / TSS)
    where:
    - RSS = Σ w_i * (y_true_i - y_pred_i)² (weighted residual sum of squares)
    - TSS = Σ w_i * (y_true_i - y_mean)² (weighted total sum of squares)
    - y_mean = global weighted mean of all ground-truth values
    
    This is different from calculating per-target R² then weighting them.
    This calculates a single R² over all (image, target) pairs with weights.
    
    Args:
        y_true: True values, shape (N, NUM_TOTAL_TARGETS) - all targets in TARGET_ORDER.
                Must be numpy array with 2 dimensions, NUM_TOTAL_TARGETS columns.
        y_pred: Predicted values, shape (N, NUM_TOTAL_TARGETS) - same order as y_true.
                Must be numpy array with 2 dimensions, NUM_TOTAL_TARGETS columns, same shape as y_true.
        weights: Optional dict of target weights (default: TARGET_WEIGHTS).
                 Must contain all keys from TARGET_ORDER. Values must be non-negative.
        
    Returns:
        Tuple of (weighted_r2, r2_scores_per_target):
        - weighted_r2: Single weighted R² score (competition metric, float)
        - r2_scores_per_target: R² score for each target (np.ndarray, shape (NUM_TOTAL_TARGETS,))
        
    Raises:
        ValueError: If inputs have invalid shapes, or weights are invalid.
        TypeError: If inputs are not numpy arrays.
    """
    # Validate inputs
    _validate_metric_inputs(y_true, y_pred, expected_ndim=2, expected_shape=(-1, NUM_TOTAL_TARGETS))
    
    # Validate and set weights
    if weights is None:
        weights = TARGET_WEIGHTS
    
    if not isinstance(weights, dict):
        raise TypeError(f"weights must be dict, got {type(weights)}")
    
    # Validate weights contain all required keys
    missing_keys = set(TARGET_ORDER) - set(weights.keys())
    if missing_keys:
        raise ValueError(f"weights missing required keys: {missing_keys}")
    
    # Validate weight values are non-negative
    for key, value in weights.items():
        if value < 0:
            raise ValueError(f"weight for '{key}' must be non-negative, got {value}")
    
    # Convert weights dict to array matching target order
    try:
        weight_array = np.array([weights[t] for t in TARGET_ORDER])
    except KeyError as e:
        raise ValueError(f"weights missing key: {e}")
    
    # Flatten to all (image, target) pairs
    y_true_flat = y_true.flatten()
    y_pred_flat = y_pred.flatten()
    
    # Create weight array for each pair (repeat weights for each image)
    n_images = y_true.shape[0]
    weights_flat = np.tile(weight_array, n_images)
    
    # Calculate global weighted mean
    y_mean = np.average(y_true_flat, weights=weights_flat)
    
    # Calculate weighted RSS
    rss = np.sum(weights_flat * (y_true_flat - y_pred_flat) ** 2)
    
    # Calculate weighted TSS
    tss = np.sum(weights_flat * (y_true_flat - y_mean) ** 2)
    
    # Calculate weighted R²
    if tss > 0:
        weighted_r2 = 1 - (rss / tss)
    else:
        weighted_r2 = 0.0
    
    # Also calculate per-target R² for analysis
    r2_scores = r2_score_per_target(y_true, y_pred)
    
    return weighted_r2, r2_scores


def r2_score_per_target(
    y_true: np.ndarray,
    y_pred: np.ndarray
) -> np.ndarray:
    """
    Calculate R² score for each target separately.
    
    Args:
        y_true: True values, shape (N, M) where M is number of targets.
                Must be numpy array with 2 dimensions.
        y_pred: Predicted values, shape (N, M) - same shape as y_true.
                Must be numpy array with 2 dimensions.
        
    Returns:
        Array of R² scores, shape (M,) where M is number of targets.
        Each value is in range (-∞, 1], where 1 is perfect prediction.
        
    Raises:
        ValueError: If inputs have invalid shapes or are empty.
        TypeError: If inputs are not numpy arrays.
    """
    # Validate inputs
    _validate_metric_inputs(y_true, y_pred, expected_ndim=2)
    
    r2_scores = []
    
    for i in range(y_true.shape[1]):
        y_t = y_true[:, i]
        y_p = y_pred[:, i]
        
        ss_res = np.sum((y_t - y_p) ** 2)
        ss_tot = np.sum((y_t - np.mean(y_t)) ** 2)
        
        if ss_tot > 0:
            r2 = 1 - (ss_res / ss_tot)
        else:
            # If total sum of squares is 0, all values are the same
            # R² is undefined, return 0.0 (or could return 1.0 if predictions match)
            if ss_res == 0:
                r2 = 1.0  # Perfect prediction when all values are constant
            else:
                r2 = 0.0  # Cannot explain variance when target has no variance
        
        r2_scores.append(r2)
    
    return np.array(r2_scores)


def rmse_per_target(
    y_true: np.ndarray,
    y_pred: np.ndarray
) -> np.ndarray:
    """
    Calculate RMSE (Root Mean Squared Error) for each target separately.
    
    Args:
        y_true: True values, shape (N, M) where M is number of targets.
                Must be numpy array with 2 dimensions.
        y_pred: Predicted values, shape (N, M) - same shape as y_true.
                Must be numpy array with 2 dimensions.
        
    Returns:
        Array of RMSE values, shape (M,) where M is number of targets.
        Each value is non-negative (>= 0).
        
    Raises:
        ValueError: If inputs have invalid shapes or are empty.
        TypeError: If inputs are not numpy arrays.
    """
    # Validate inputs
    _validate_metric_inputs(y_true, y_pred, expected_ndim=2)
    
    rmse_scores = []
    
    for i in range(y_true.shape[1]):
        rmse = np.sqrt(np.mean((y_true[:, i] - y_pred[:, i]) ** 2))
        rmse_scores.append(rmse)
    
    return np.array(rmse_scores)


def mae_per_target(
    y_true: np.ndarray,
    y_pred: np.ndarray
) -> np.ndarray:
    """
    Calculate MAE (Mean Absolute Error) for each target separately.
    
    Args:
        y_true: True values, shape (N, M) where M is number of targets.
                Must be numpy array with 2 dimensions.
        y_pred: Predicted values, shape (N, M) - same shape as y_true.
                Must be numpy array with 2 dimensions.
        
    Returns:
        Array of MAE values, shape (M,) where M is number of targets.
        Each value is non-negative (>= 0).
        
    Raises:
        ValueError: If inputs have invalid shapes or are empty.
        TypeError: If inputs are not numpy arrays.
    """
    # Validate inputs
    _validate_metric_inputs(y_true, y_pred, expected_ndim=2)
    
    mae_scores = []
    
    for i in range(y_true.shape[1]):
        mae = np.mean(np.abs(y_true[:, i] - y_pred[:, i]))
        mae_scores.append(mae)
    
    return np.array(mae_scores)

