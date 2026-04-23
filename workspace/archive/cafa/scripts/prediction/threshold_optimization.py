"""
Threshold optimization for CAFA 6 protein function prediction.
Uses IA-weighted F1 score to find optimal prediction threshold on validation set.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from sklearn.preprocessing import MultiLabelBinarizer


def load_ia_weights(ia_file_path: Path) -> Dict[str, float]:
    """
    Load IA (Information Accretion) weights from IA.tsv file.
    
    Args:
        ia_file_path: Path to IA.tsv file
        
    Returns:
        dict: Mapping from GO term ID to IA weight (float)
    """
    if not ia_file_path.exists():
        print(f"   ⚠️  Warning: IA file not found at {ia_file_path}, returning empty dict")
        return {}
    
    ia_weights = {}
    try:
        df = pd.read_csv(ia_file_path, sep='\t', header=None, names=['go', 'ia'], dtype=str)
        
        for _, row in df.iterrows():
            go_id = row['go']
            ia_str = row['ia']
            
            # Try to parse as float, handle comma decimal separator
            try:
                ia_weights[go_id] = float(ia_str)
            except ValueError:
                try:
                    # Try replacing comma with dot
                    ia_weights[go_id] = float(ia_str.replace(',', '.'))
                except ValueError:
                    # Default to 0.0 if parsing fails
                    ia_weights[go_id] = 0.0
        
        print(f"   ✓ Loaded {len(ia_weights):,} IA weights")
    except Exception as e:
        print(f"   ⚠️  Warning: Error loading IA file: {e}, returning empty dict")
        return {}
    
    return ia_weights


def compute_ia_weighted_f1(y_true: np.ndarray,
                          y_pred_binary: np.ndarray,
                          ia_weights: Dict[str, float],
                          mlb: MultiLabelBinarizer) -> Tuple[float, float, float]:
    """
    Compute IA-weighted precision, recall, and F1 score.
    
    Args:
        y_true: True binary labels, shape (n_samples, n_classes)
        y_pred_binary: Predicted binary labels, shape (n_samples, n_classes)
        ia_weights: Dictionary mapping GO term ID to IA weight
        mlb: MultiLabelBinarizer with classes_ attribute
        
    Returns:
        tuple: (weighted_precision, weighted_recall, weighted_f1)
    """
    from config.training import EPSILON_TINY
    eps = EPSILON_TINY
    
    # Compute per-class TP, FP, FN
    tp = ((y_true == 1) & (y_pred_binary == 1)).sum(axis=0).astype(float)
    fp = ((y_true == 0) & (y_pred_binary == 1)).sum(axis=0).astype(float)
    fn = ((y_true == 1) & (y_pred_binary == 0)).sum(axis=0).astype(float)
    
    # Compute per-class precision, recall, F1
    prec = tp / (tp + fp + eps)
    rec = tp / (tp + fn + eps)
    f1 = 2 * prec * rec / (prec + rec + eps)
    
    # Get weights for each class (term)
    classes = mlb.classes_
    weights = np.array([ia_weights.get(c, 1.0) for c in classes], dtype=float)
    
    # Compute weighted averages
    weighted_f1 = (f1 * weights).sum() / (weights.sum() + eps)
    weighted_prec = (prec * weights).sum() / (weights.sum() + eps)
    weighted_rec = (rec * weights).sum() / (weights.sum() + eps)
    
    return weighted_prec, weighted_rec, weighted_f1


def optimize_threshold(y_val_proba: np.ndarray,
                      y_val_true: np.ndarray,
                      ia_weights: Dict[str, float],
                      mlb: MultiLabelBinarizer,
                      threshold_grid: List[float]) -> Tuple[float, float]:
    """
    Find optimal threshold by searching threshold grid and maximizing IA-weighted F1.
    
    Args:
        y_val_proba: Validation prediction probabilities, shape (n_samples, n_classes)
        y_val_true: True binary labels, shape (n_samples, n_classes)
        ia_weights: Dictionary mapping GO term ID to IA weight
        mlb: MultiLabelBinarizer with classes_ attribute
        threshold_grid: List of threshold values to search (e.g., [0.01, 0.02, ..., 0.50])
        
    Returns:
        tuple: (best_threshold, best_f1_score)
    """
    from config.prediction import DEFAULT_THRESHOLD
    best_threshold = DEFAULT_THRESHOLD
    best_f1 = -1.0
    
    print(f"   Searching {len(threshold_grid)} threshold values...")
    
    for threshold in threshold_grid:
        # Binarize predictions at this threshold
        y_pred_binary = (y_val_proba >= threshold).astype(int)
        
        # Compute IA-weighted F1
        _, _, f1 = compute_ia_weighted_f1(y_val_true, y_pred_binary, ia_weights, mlb)
        
        if f1 > best_f1:
            best_f1 = f1
            best_threshold = threshold
    
    print(f"   ✓ Best threshold: {best_threshold:.3f}, Best IA-weighted F1: {best_f1:.6f}")
    
    return best_threshold, best_f1

