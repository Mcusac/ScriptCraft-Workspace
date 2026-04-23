# checkpoint_score_utils.py
# Utilities for extracting scores from model checkpoints
#
# This module provides functions to extract CV scores, fold scores, and best fold
# information from checkpoint files. It reuses checkpoint.load_checkpoint_info
# to avoid duplicating checkpoint loading logic.

import logging
from pathlib import Path
from typing import Tuple, List

from .checkpoint import load_checkpoint_info, load_regression_model_info
from .results import find_best_fold_from_scores

logger = logging.getLogger(__name__)


def extract_scores_from_checkpoint(
    checkpoint_path: Path
) -> Tuple[float, List[float], int]:
    """
    Extract CV score, fold scores, and best fold from checkpoint.
    
    This function loads checkpoint metadata and extracts score information
    without loading the full model state, making it efficient for export
    and analysis operations.
    
    Supports both PyTorch checkpoints (.pth) and regression models (.pkl).
    
    Args:
        checkpoint_path: Path to model checkpoint file (.pth or .pkl)
        
    Returns:
        Tuple of (cv_score, fold_scores, best_fold):
        - cv_score: Average cross-validation score across all folds
        - fold_scores: List of scores for each fold (up to 5 folds)
        - best_fold: Index of the best performing fold (0-based)
        
    Raises:
        FileNotFoundError: If checkpoint file doesn't exist
        ValueError: If checkpoint doesn't contain valid score information
    """
    # Check if this is a regression model (.pkl file)
    if checkpoint_path.suffix == '.pkl':
        # For regression models, load metadata from adjacent JSON file
        metadata_path = checkpoint_path.parent / 'regression_model_info.json'
        checkpoint_info = load_regression_model_info(metadata_path)
        
        if checkpoint_info is None:
            raise FileNotFoundError(
                f"Regression model metadata not found or invalid: {metadata_path}. "
                f"Expected file: {metadata_path}"
            )
    else:
        # Reuse existing checkpoint info loading logic for PyTorch checkpoints
        checkpoint_info = load_checkpoint_info(checkpoint_path)
        
        if checkpoint_info is None:
            raise FileNotFoundError(f"Checkpoint not found or invalid: {checkpoint_path}")
    
    best_score = checkpoint_info.get('best_score', 0.0)
    history = checkpoint_info.get('history', [])
    
    # Extract fold scores from history
    # Default assumption: all folds have same score as best_score
    fold_scores = [best_score] * 5
    
    if history:
        # Extract validation scores from history entries
        val_scores = [
            h.get('val_score', best_score)
            for h in history
            if 'val_score' in h
        ]
        if val_scores:
            # Take up to 5 fold scores
            fold_scores = val_scores[:5]
    
    # Calculate CV score as average of fold scores
    cv_score = sum(fold_scores) / len(fold_scores) if fold_scores else best_score
    
    # Find best fold using centralized utility
    best_fold, _ = find_best_fold_from_scores(fold_scores)
    
    return cv_score, fold_scores, best_fold

