# paths.py
# Utilities for getting checkpoint and model paths

from pathlib import Path


def get_fold_checkpoint_path(model_dir: Path, fold: int) -> Path:
    """
    Get the standard checkpoint path for a fold.
    
    Args:
        model_dir: Base model directory. Can be string or Path object.
        fold: Fold number (0 to n_folds-1). Must be non-negative integer.
        
    Returns:
        Path to fold checkpoint: {model_dir}/fold_{fold}/best_model.pth
        
    Raises:
        ValueError: If fold is negative.
        TypeError: If model_dir or fold have invalid types.
    """
    # Validate inputs
    if model_dir is None:
        raise ValueError("model_dir cannot be None")
    
    model_dir_obj = Path(model_dir)
    
    if not isinstance(fold, int) or fold < 0:
        raise ValueError(f"fold must be non-negative integer, got {fold}")
    
    return model_dir_obj / f'fold_{fold}' / 'best_model.pth'


def get_fold_regression_model_path(model_dir: Path, fold: int) -> Path:
    """
    Get the regression model path for a fold (feature extraction mode).
    
    Args:
        model_dir: Base model directory. Can be string or Path object.
        fold: Fold number (0 to n_folds-1). Must be non-negative integer.
        
    Returns:
        Path to regression model: {model_dir}/fold_{fold}/regression_model.pkl
        
    Raises:
        ValueError: If fold is negative.
        TypeError: If model_dir or fold have invalid types.
    """
    # Validate inputs
    if model_dir is None:
        raise ValueError("model_dir cannot be None")
    
    model_dir_obj = Path(model_dir)
    
    if not isinstance(fold, int) or fold < 0:
        raise ValueError(f"fold must be non-negative integer, got {fold}")
    
    return model_dir_obj / f'fold_{fold}' / 'regression_model.pkl'
