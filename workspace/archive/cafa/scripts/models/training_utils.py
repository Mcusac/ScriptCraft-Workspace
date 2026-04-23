"""
Shared utility functions for model trainers.
Consolidates duplicate code patterns across different model implementations.
"""

import numpy as np
from typing import Dict, Any, Optional, Callable, Tuple
from sklearn.metrics import f1_score, precision_score, recall_score

from config.training import DEFAULT_RANDOM_SEED, DEFAULT_VALIDATION_SPLIT, LARGE_ONTOLOGY_LABEL_THRESHOLD
from config.prediction import BINARY_PREDICTION_THRESHOLD, METRICS_EPSILON


def check_ontology_has_terms(y_train: np.ndarray, ont_name: str) -> bool:
    """
    Check if ontology has any terms (labels).
    
    Args:
        y_train: Label matrix (n_samples, n_terms)
        ont_name: Ontology name for logging
        
    Returns:
        bool: True if ontology has terms, False otherwise (prints skip message)
    """
    if y_train.shape[1] == 0:
        print(f"      Skipping {ont_name} (no terms)")
        return False
    return True


def merge_hyperparams(defaults: Dict[str, Any], provided: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge provided hyperparameters into defaults.
    
    Args:
        defaults: Default hyperparameters dict
        provided: Provided hyperparameters dict (will override defaults)
        
    Returns:
        dict: Merged hyperparameters
    """
    merged = defaults.copy()
    merged.update(provided)
    return merged


def train_with_error_handling(train_fn: Callable, *args, ont_name: str, **kwargs) -> Optional[Any]:
    """
    Wrap training function with consistent error handling.
    
    Args:
        train_fn: Training function to call
        *args: Positional arguments for training function
        ont_name: Ontology name for error messages
        **kwargs: Keyword arguments for training function
        
    Returns:
        Trained model or None on error
    """
    try:
        return train_fn(*args, **kwargs)
    except Exception as e:
        print(f"      ❌ Error training {ont_name} model: {e}")
        return None


def log_training_start(ont_name: str, model_type: str) -> None:
    """
    Log training start message.
    
    Args:
        ont_name: Ontology name
        model_type: Model type (e.g., 'MLP', 'XGBoost', 'Logistic Regression')
    """
    print(f"   Training {ont_name} {model_type} model...")


def log_skip_ontology(ont_name: str, reason: str = "no terms") -> None:
    """
    Log ontology skip message.
    
    Args:
        ont_name: Ontology name
        reason: Reason for skipping
    """
    print(f"      Skipping {ont_name} ({reason})")


def log_training_success(ont_name: str) -> None:
    """
    Log training success message.
    
    Args:
        ont_name: Ontology name
    """
    print(f"      ✓ {ont_name} model trained")


def log_training_error(ont_name: str, error: Exception) -> None:
    """
    Log training error message.
    
    Args:
        ont_name: Ontology name
        error: Exception that occurred
    """
    print(f"      ❌ Error training {ont_name} model: {error}")


def log_epoch_progress(epoch: int, total_epochs: int, train_metrics: Dict[str, float], 
                      val_metrics: Dict[str, float]) -> None:
    """
    Log epoch training progress.
    
    Args:
        epoch: Current epoch (0-indexed)
        total_epochs: Total number of epochs
        train_metrics: Training metrics dict
        val_metrics: Validation metrics dict
    """
    if (epoch + 1) % 5 == 0 or epoch == 0:
        print(f"         Epoch {epoch+1:2d}: "
              f"Train F1={train_metrics['f1_score']:.4f}, "
              f"Val F1={val_metrics['f1_score']:.4f}, "
              f"Val Loss={val_metrics['loss']:.4f}")


def get_ontology_gpu_mapping() -> Dict[str, int]:
    """
    Get mapping of ontology codes to GPU IDs.
    
    Returns:
        dict: Mapping of ont_code -> gpu_id (F->0, P->1, C->2)
    """
    return {'F': 0, 'P': 1, 'C': 2}


def train_all_ontologies_base(X_train: np.ndarray,
                             y_train_dict: Dict[str, np.ndarray],
                             ontologies: Dict[str, str],
                             train_fn: Callable,
                             model_type_name: str,
                             **hyperparams) -> Dict[str, Any]:
    """
    Generic function to train models for all ontologies.
    
    Args:
        X_train: Feature matrix
        y_train_dict: dict mapping ont_code -> label matrix
        ontologies: dict mapping ont_code -> ont_name
        train_fn: Function to train single ontology model
                  Signature: train_fn(X_train, y_train, ont_code, ont_name, **hyperparams) -> model
        model_type_name: Name of model type for logging (e.g., "MLP", "XGBoost")
        **hyperparams: Model hyperparameters
        
    Returns:
        dict: ont_code -> trained model
    """
    print(f"\n[6/9] Training {model_type_name} models...")
    
    models = {}
    
    for ont_code, ont_name in ontologies.items():
        if ont_code not in y_train_dict:
            print(f"   ⚠️  Skipping {ont_name} (no data)")
            continue
        
        y_ont = y_train_dict[ont_code]
        model = train_fn(X_train, y_ont, ont_code, ont_name, **hyperparams)
        
        if model is not None:
            models[ont_code] = model
    
    print(f"   ✓ Trained {len(models)} {model_type_name} models")
    return models


def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    Calculate evaluation metrics for multi-label classification.
    
    Args:
        y_true: True labels (n_samples, n_labels)
        y_pred: Predicted probabilities (n_samples, n_labels)
        
    Returns:
        Dictionary of metrics
    """
    # Convert probabilities to binary predictions
    y_pred_binary = (y_pred > BINARY_PREDICTION_THRESHOLD).astype(int)
    y_true_binary = (y_true > BINARY_PREDICTION_THRESHOLD).astype(int)
    
    # Calculate metrics
    f1 = f1_score(y_true_binary, y_pred_binary, average='samples', zero_division=0)
    precision = precision_score(y_true_binary, y_pred_binary, average='samples', zero_division=0)
    recall = recall_score(y_true_binary, y_pred_binary, average='samples', zero_division=0)
    
    return {
        'f1_score': f1,
        'precision': precision,
        'recall': recall
    }


def compute_final_metrics_from_accumulator(accumulator: Dict[str, list]) -> Dict[str, float]:
    """
    Compute final F1, precision, recall from streaming accumulator.
    
    Args:
        accumulator: Dict with 'tp', 'fp', 'fn' lists (one value per sample)
        
    Returns:
        Dictionary of metrics
    """
    # Convert lists to numpy arrays for efficient computation
    tp = np.array(accumulator['tp'], dtype=np.float32)
    fp = np.array(accumulator['fp'], dtype=np.float32)
    fn = np.array(accumulator['fn'], dtype=np.float32)
    
    # Per-sample precision and recall
    precision_per_sample = tp / (tp + fp + METRICS_EPSILON)
    recall_per_sample = tp / (tp + fn + METRICS_EPSILON)
    f1_per_sample = 2 * (precision_per_sample * recall_per_sample) / (precision_per_sample + recall_per_sample + METRICS_EPSILON)
    
    # Average across samples (micro-averaged)
    precision = np.mean(precision_per_sample)
    recall = np.mean(recall_per_sample)
    f1 = np.mean(f1_per_sample)
    
    return {
        'f1_score': float(f1),
        'precision': float(precision),
        'recall': float(recall)
    }

