"""
Ensemble predictions from multiple models for CAFA 6 protein function prediction.
Supports various ensemble methods and dimension compatibility handling.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from pathlib import Path
from utils.logging import setup_logging, get_logger

logger = get_logger(__name__)


def ensemble_predictions(predictions_list: List[np.ndarray], 
                        method: str = 'average',
                        weights: Optional[List[float]] = None,
                        **kwargs) -> np.ndarray:
    """
    Ensemble predictions from multiple models.
    
    Args:
        predictions_list: List of prediction arrays (n_samples, n_terms) from each model
        method: Ensemble method ('average', 'weighted_average', 'max', 'geometric_mean',
                'rank_average', 'power_average', 'percentile')
        weights: Optional weights for weighted_average (must sum to 1.0)
        **kwargs: Additional method-specific parameters:
            - power (float): Power for power_average method (default: 1.0, >1 emphasizes high probs, <1 flattens)
            - percentile (float): Percentile for percentile method (default: 75.0, range 0-100)
        
    Returns:
        np.ndarray: Ensembled predictions (n_samples, n_terms)
        
    Raises:
        ValueError: If method is invalid or predictions have incompatible shapes
    """
    if not predictions_list:
        raise ValueError("predictions_list cannot be empty")
    
    # Validate shapes
    base_shape = predictions_list[0].shape
    for i, preds in enumerate(predictions_list[1:], 1):
        if preds.shape != base_shape:
            raise ValueError(
                f"Shape mismatch: predictions_list[0] has shape {base_shape}, "
                f"but predictions_list[{i}] has shape {preds.shape}"
            )
    
    # Stack predictions for ensemble operations
    stacked = np.stack(predictions_list, axis=0)  # (n_models, n_samples, n_terms)
    
    if method == 'average':
        # Simple average across models
        ensembled = np.mean(stacked, axis=0)
        
    elif method == 'weighted_average':
        if weights is None:
            raise ValueError("weights must be provided for weighted_average method")
        if len(weights) != len(predictions_list):
            raise ValueError(f"Number of weights ({len(weights)}) must match number of predictions ({len(predictions_list)})")
        if not np.isclose(sum(weights), 1.0):
            raise ValueError(f"Weights must sum to 1.0, got {sum(weights)}")
        
        # Weighted average
        weights_array = np.array(weights).reshape(-1, 1, 1)  # (n_models, 1, 1)
        ensembled = np.sum(stacked * weights_array, axis=0)
        
    elif method == 'max':
        # Maximum probability across models
        ensembled = np.max(stacked, axis=0)
        
    elif method == 'geometric_mean':
        # Geometric mean (good for probabilities)
        # Add small epsilon to avoid log(0)
        from config.training import EPSILON_SMALL
        ensembled = np.exp(np.mean(np.log(stacked + EPSILON_SMALL), axis=0))
        
    elif method == 'rank_average':
        # Rank averaging: Convert probabilities to ranks, average ranks, convert back
        # Good for handling calibration differences between models
        n_samples, n_terms = base_shape
        n_models = len(predictions_list)
        
        # Convert each model's predictions to ranks (per sample, across terms)
        rank_stacked = np.zeros_like(stacked)
        for model_idx in range(n_models):
            # For each sample, get ranks of probabilities (high prob = high rank)
            for sample_idx in range(n_samples):
                ranks = np.argsort(np.argsort(-stacked[model_idx, sample_idx, :])) + 1  # 1-indexed ranks
                rank_stacked[model_idx, sample_idx, :] = ranks
        
        # Average ranks across models
        avg_ranks = np.mean(rank_stacked, axis=0)
        
        # Convert back to probabilities: normalize ranks to [0, 1] range
        # Ranks go from 1 to n_terms, so normalize by n_terms
        ensembled = 1.0 - (avg_ranks - 1) / (n_terms - 1) if n_terms > 1 else avg_ranks / n_terms
        
    elif method == 'power_average':
        # Power averaging: Average of probabilities raised to a power
        # power > 1: Emphasizes higher probabilities (more aggressive)
        # power < 1: Flattens probabilities (more conservative)
        power = kwargs.get('power', 1.0)
        if power <= 0:
            raise ValueError(f"power must be > 0, got {power}")
        
        # Clamp predictions to [0, 1] before applying power
        from config.training import EPSILON_SMALL
        stacked_clamped = np.clip(stacked, EPSILON_SMALL, 1.0 - EPSILON_SMALL)
        
        if power == 1.0:
            # Same as regular average
            ensembled = np.mean(stacked_clamped, axis=0)
        else:
            # Raise to power, average, then take inverse power
            powered = np.power(stacked_clamped, power)
            avg_powered = np.mean(powered, axis=0)
            ensembled = np.power(avg_powered, 1.0 / power)
        
        # Ensure output is in valid probability range
        ensembled = np.clip(ensembled, 0.0, 1.0)
        
    elif method == 'percentile':
        # Percentile ensembling: Take percentile across model predictions
        # percentile=50 is median, 75 is conservative (reduces outlier influence)
        percentile = kwargs.get('percentile', 75.0)
        if not 0 <= percentile <= 100:
            raise ValueError(f"percentile must be between 0 and 100, got {percentile}")
        
        ensembled = np.percentile(stacked, percentile, axis=0)
        
    else:
        from config.ensemble import get_available_ensemble_methods
        available_methods = get_available_ensemble_methods()
        raise ValueError(
            f"Unknown ensemble method: {method}. "
            f"Available: {', '.join(available_methods)}"
        )
    
    return ensembled


def load_multiple_models(model_specs: List[Tuple[str, str, str]]) -> Dict[str, Dict]:
    """
    Load multiple models for ensemble prediction.
    
    Args:
        model_specs: List of (ont_code, model_type, version) tuples
                    Example: [('F', 'xgb', '2.0'), ('F', 'nn', '1.0')]
        
    Returns:
        Dict mapping ont_code -> list of (model, mlb, metadata) tuples
        
    Example:
        >>> models = load_multiple_models([
        ...     ('F', 'xgb', '2.0'),
        ...     ('F', 'nn', '1.0'),
        ...     ('P', 'xgb', '2.0')
        ... ])
        >>> # Returns: {'F': [(xgb_model, xgb_mlp, meta), (nn_model, nn_mlp, meta)],
        ...              'P': [(xgb_model, xgb_mlp, meta)]}
    """
    from utils.model_io import load_model
    
    # Group models by ontology
    models_by_ont = {}
    
    setup_logging()
    for ont_code, model_type, version in model_specs:
        if ont_code not in models_by_ont:
            models_by_ont[ont_code] = []
        
        # Load model
        logger.info(f"Loading {ont_code} model: {model_type} v{version}")
        model, mlb, metadata = load_model(ont_code=ont_code, model_type=model_type, version=version)
        
        models_by_ont[ont_code].append((model, mlb, metadata))
    
    return models_by_ont


def check_ensemble_compatibility(model_configs: List[Dict]) -> Tuple[bool, List[str]]:
    """
    Check if models are compatible for ensembling.
    
    Args:
        model_configs: List of model configuration dicts
        
    Returns:
        tuple: (all_compatible: bool, issues: List[str])
    """
    issues = []
    
    if len(model_configs) < 2:
        issues.append("Need at least 2 models for ensemble")
        return False, issues
    
    # Check feature dimensions
    feature_types = set()
    dimensions = set()
    
    for i, config in enumerate(model_configs):
        feature_type = config.get('feature_type', 'hand_crafted')
        feature_types.add(feature_type)
        
        # Calculate dimensions
        if feature_type == 'fused_embeddings':
            from config.features import get_feature_dimensions
            preset = config.get('feature_preset', 'default')
            dims = get_feature_dimensions(preset)
            dimensions.add(dims)
        elif feature_type == 'hand_crafted':
            from config.features import INDIVIDUAL_FEATURES, HANDCRAFTED_FEATURE_KEY
            hc_dim = INDIVIDUAL_FEATURES[HANDCRAFTED_FEATURE_KEY]['dimensions']
            dimensions.add(hc_dim)
        else:
            issues.append(f"Model {i}: Unknown feature_type '{feature_type}'")
    
    # Check if dimensions match
    if len(dimensions) > 1:
        issues.append(
            f"Dimension mismatch detected: {dimensions}. "
            f"Models must use same input dimensions for direct ensemble. "
            f"Solutions: (1) Use padding strategy, (2) Retrain models with same features, "
            f"(3) Use submission averaging instead"
        )
        return False, issues
    
    # Check if output terms match (MLPs should have same classes)
    # This check would require loading models, so we skip for now
    # Could add later if needed
    
    if not issues:
        logger.info(f"All {len(model_configs)} models are compatible for ensemble")
        logger.info(f"Shared feature dimension: {list(dimensions)[0]}")
        return True, []
    
    return False, issues


def pad_features(X: np.ndarray, target_dim: int, method: str = 'zeros') -> np.ndarray:
    """
    Pad feature matrix to target dimension.
    
    Args:
        X: Feature matrix (n_samples, n_features)
        target_dim: Target dimension to pad to
        method: Padding method ('zeros', 'mean', 'noise')
        
    Returns:
        np.ndarray: Padded feature matrix (n_samples, target_dim)
        
    Raises:
        ValueError: If X already has more dimensions than target
    """
    current_dim = X.shape[1]
    
    if current_dim == target_dim:
        return X
    
    if current_dim > target_dim:
        raise ValueError(
            f"Cannot pad: X has {current_dim} dimensions, target is {target_dim}. "
            f"Feature reduction not supported."
        )
    
    padding_size = target_dim - current_dim
    
    if method == 'zeros':
        # Zero padding (most common)
        padding = np.zeros((X.shape[0], padding_size), dtype=X.dtype)
        
    elif method == 'mean':
        # Repeat mean value
        mean_val = np.mean(X, axis=1, keepdims=True)
        padding = np.tile(mean_val, (1, padding_size))
        
    elif method == 'noise':
        # Add Gaussian noise matching data statistics
        mean = np.mean(X)
        std = np.std(X)
        padding = np.random.normal(mean, std * 0.1, (X.shape[0], padding_size))
        
    else:
        raise ValueError(
            f"Unknown padding method: {method}. "
            f"Available: 'zeros', 'mean', 'noise'"
        )
    
    print(f"   Padded features: {current_dim} → {target_dim} (method: {method})")
    return np.hstack([X, padding])


def align_model_features(model_configs: List[Dict], 
                        X_dict: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    """
    Align feature matrices for models with different dimensions.
    Pads smaller matrices to match the largest dimension.
    
    Args:
        model_configs: List of model configuration dicts
        X_dict: Dict mapping model_idx -> feature matrix
        
    Returns:
        Dict mapping model_idx -> aligned (padded) feature matrix
    """
    # Find maximum dimension
    dimensions = []
    for idx, config in enumerate(model_configs):
        if idx in X_dict:
            dimensions.append(X_dict[idx].shape[1])
    
    if not dimensions:
        raise ValueError("X_dict is empty")
    
    max_dim = max(dimensions)
    print(f"   Aligning features to maximum dimension: {max_dim}")
    
    # Pad all matrices to max dimension
    aligned = {}
    for idx, X in X_dict.items():
        if X.shape[1] < max_dim:
            aligned[idx] = pad_features(X, max_dim, method='zeros')
        else:
            aligned[idx] = X
    
    return aligned

