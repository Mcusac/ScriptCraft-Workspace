# training_results_utils.py
# Utilities for creating results.json from single training runs and fold operations

import logging
import math
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from .checkpoint import get_fold_checkpoint_path, get_fold_regression_model_path, find_best_fold
from utils.system.io import save_json_file

logger = logging.getLogger(__name__)


def _detect_num_folds(model_dir: Path) -> int:
    """
    Detect the number of folds by checking what fold directories exist.
    
    Args:
        model_dir: Base model directory
        
    Returns:
        Number of folds detected (at least 1, up to 10)
    """
    if not model_dir.exists():
        return 5  # Default fallback
    
    fold_dirs = [d for d in model_dir.iterdir() 
                 if d.is_dir() and d.name.startswith('fold_')]
    
    if not fold_dirs:
        return 5  # Default fallback
    
    # Extract fold numbers and find max
    fold_nums = []
    for fold_dir in fold_dirs:
        try:
            fold_num = int(fold_dir.name.split('_')[1])
            fold_nums.append(fold_num)
        except (ValueError, IndexError):
            continue
    
    if fold_nums:
        # Return max + 1 (since folds are 0-indexed)
        return max(fold_nums) + 1
    
    return 5  # Default fallback


def find_best_fold_from_scores(fold_scores: List[float]) -> Tuple[int, float]:
    """
    Find the best fold from a list of fold scores.
    
    Args:
        fold_scores: List of scores for each fold. Must not be empty.
                    Each element should be a numeric value (float or int).
                    Higher scores are considered better.
        
    Returns:
        Tuple of (best_fold_index, best_score):
        - best_fold_index: Index of the fold with highest score (int, 0-based)
        - best_score: Highest score value (float)
        
    Raises:
        ValueError: If fold_scores is empty, contains non-numeric values, or all scores are NaN.
        TypeError: If fold_scores is not a list.
    """
    # Validate input
    if not isinstance(fold_scores, list):
        raise TypeError(f"fold_scores must be list, got {type(fold_scores)}")
    
    if not fold_scores:
        raise ValueError("fold_scores cannot be empty")
    
    # Validate all elements are numeric
    for i, score in enumerate(fold_scores):
        if not isinstance(score, (int, float)):
            raise ValueError(
                f"fold_scores[{i}] must be numeric (int or float), got {type(score)}"
            )
    
    # Find best fold
    best_fold = max(range(len(fold_scores)), key=lambda i: fold_scores[i])
    best_score = fold_scores[best_fold]
    
    # Check for NaN
    if math.isnan(best_score):
        raise ValueError("All fold scores are NaN or best score is NaN")
    
    return best_fold, best_score


def create_single_training_results(
    cv_score: float,
    fold_scores: List[float],
    preprocessing_list: List[str],
    augmentation_list: List[str],
    model_name: str,
    output_path: Path
) -> Dict[str, Any]:
    """
    Create results.json format from single training run.
    
    
    Args:
        cv_score: Average cross-validation score
        fold_scores: List of scores for each fold
        preprocessing_list: List of preprocessing techniques used
        augmentation_list: List of augmentation techniques used
        model_name: Name of the model architecture
        output_path: Path to save results.json
        
    Returns:
        Dictionary containing the created variant result
    """
    # Create variant result in grid search compatible format
    variant_result = {
        'variant_index': 0,
        'variant_id': 'single_training',
        'preprocessing_list': preprocessing_list,
        'augmentation_list': augmentation_list,
        'cv_score': cv_score,
        'fold_scores': fold_scores,
        'model_name': model_name
    }
    
    # Save as array
    results = [variant_result]
    
    # Save to file
    save_json_file(results, output_path, file_type="Results JSON")
    
    logger.info(f"Created results.json at: {output_path}")
    
    return variant_result


def find_trained_model_path(
    model_dir: Path,
    best_fold: Optional[int] = None
) -> Tuple[Path, int]:
    """
    Find model checkpoint path from single training.
    
    Supports both regular PyTorch checkpoints and feature extraction regression models.
    
    Args:
        model_dir: Base model directory (e.g., models/)
        best_fold: Optional best fold number. If None, finds best fold from checkpoints.
        
    Returns:
        Tuple of (model_path, fold_number)
        
    Raises:
        FileNotFoundError: If no model checkpoint found
    """
    if best_fold is not None:
        # Use specified fold - try regular checkpoint first, then regression model
        model_path = get_fold_checkpoint_path(model_dir, best_fold)
        if not model_path.exists():
            # Try regression model (feature extraction mode)
            model_path = get_fold_regression_model_path(model_dir, best_fold)
        
        if model_path.exists():
            return model_path, best_fold
        else:
            raise FileNotFoundError(f"Model checkpoint not found for fold {best_fold}: {model_path}")
    
    # Use find_best_fold to find the best performing fold
    # Dynamically determine number of folds by checking what exists
    n_folds = _detect_num_folds(model_dir)
    best_fold_num, best_score, best_path = find_best_fold(model_dir, n_folds=n_folds)
    
    return best_path, best_fold_num


def analyze_cv_test_gap(
    cv_score: float,
    fold_scores: List[float],
    test_score: Optional[float] = None
) -> Dict[str, Any]:
    """
    Analyze the gap between CV scores and test performance.
    
    Helps identify potential issues like:
    - Overfitting to validation folds
    - High variance across folds (model instability)
    - Distribution shift between train/val and test
    
    Args:
        cv_score: Average cross-validation score
        fold_scores: List of scores for each fold
        test_score: Optional test score for comparison
        
    Returns:
        Dictionary with analysis results:
        - 'cv_score': Average CV score
        - 'fold_scores': List of fold scores
        - 'fold_std': Standard deviation of fold scores
        - 'fold_range': Range (max - min) of fold scores
        - 'fold_cv': Coefficient of variation (std/mean) of fold scores
        - 'test_score': Test score if provided
        - 'cv_test_gap': Difference between CV and test if both provided
        - 'warnings': List of warning messages about potential issues
    """
    import statistics
    
    if not fold_scores:
        raise ValueError("fold_scores cannot be empty")
    
    if len(fold_scores) < 2:
        raise ValueError("Need at least 2 fold scores for analysis")
    
    # Calculate statistics
    fold_mean = statistics.mean(fold_scores)
    fold_std = statistics.stdev(fold_scores) if len(fold_scores) > 1 else 0.0
    fold_min = min(fold_scores)
    fold_max = max(fold_scores)
    fold_range = fold_max - fold_min
    fold_cv = fold_std / fold_mean if fold_mean != 0 else float('inf')
    
    warnings = []
    
    # Check for high variance (model instability)
    if fold_cv > 0.15:  # More than 15% coefficient of variation
        warnings.append(
            f"⚠️ High fold variance detected (CV={fold_cv:.3f}). "
            f"Model may be unstable across folds. "
            f"Fold scores range: [{fold_min:.4f}, {fold_max:.4f}]"
        )
    
    # Check for large range
    if fold_range > 0.2:  # More than 0.2 difference between best and worst fold
        warnings.append(
            f"⚠️ Large fold score range detected ({fold_range:.4f}). "
            f"This suggests high variance in model performance across folds."
        )
    
    # Check if CV score matches fold mean (should be close)
    if abs(cv_score - fold_mean) > 1e-6:
        warnings.append(
            f"⚠️ CV score ({cv_score:.6f}) doesn't match fold mean ({fold_mean:.6f}). "
            f"This may indicate an error in score calculation."
        )
    
    # Analyze CV vs test gap if test score provided
    cv_test_gap = None
    if test_score is not None:
        cv_test_gap = cv_score - test_score
        
        if cv_test_gap > 0.15:  # More than 0.15 gap
            warnings.append(
                f"⚠️ Large CV-test gap detected ({cv_test_gap:.4f}). "
                f"CV score ({cv_score:.4f}) is much higher than test score ({test_score:.4f}). "
                f"Possible causes: overfitting to validation folds, distribution shift, or model instability."
            )
        elif cv_test_gap < -0.1:  # Test is much better (unusual)
            warnings.append(
                f"⚠️ Test score ({test_score:.4f}) is much higher than CV score ({cv_score:.4f}). "
                f"This is unusual and may indicate issues with validation set or test set leakage."
            )
    
    analysis = {
        'cv_score': cv_score,
        'fold_scores': fold_scores,
        'fold_mean': fold_mean,
        'fold_std': fold_std,
        'fold_range': fold_range,
        'fold_cv': fold_cv,
        'fold_min': fold_min,
        'fold_max': fold_max,
        'test_score': test_score,
        'cv_test_gap': cv_test_gap,
        'warnings': warnings
    }
    
    return analysis

