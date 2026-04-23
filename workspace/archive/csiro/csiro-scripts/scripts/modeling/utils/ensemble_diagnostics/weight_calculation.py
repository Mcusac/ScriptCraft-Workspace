# weight_calculation.py
# Weight calculation methods for ensemble diagnostics

from typing import Dict, List, Tuple
import numpy as np


def get_method_weights(
    scores: List[float],
    method: str
) -> Tuple[List[float], Dict[str, any]]:
    """
    Calculate weights for each ensemble method given a list of scores.
    
    Args:
        scores: List of scores (CV, submission, or combined)
        method: Ensemble method name ('weighted_average', 'ranked_average', 'percentile_average')
        
    Returns:
        Tuple of (weights_list, info_dict) where info_dict contains:
        - normalized_weights: Final normalized weights
        - rank_order: Rank order for ranked/percentile methods
        - raw_weights: Raw weights before normalization
    """
    if not scores:
        return [], {}
    
    scores_array = np.array(scores, dtype=np.float32)
    info = {}
    
    if method == 'weighted_average':
        # Use scores directly as weights (after handling negatives)
        min_score = np.min(scores_array)
        if min_score <= 0:
            epsilon = 1e-6
            weights_array = scores_array - min_score + epsilon
            info['raw_weights'] = weights_array.tolist()
        else:
            weights_array = scores_array.copy()
            info['raw_weights'] = weights_array.tolist()
        
        # Normalize
        weight_sum = np.sum(weights_array)
        if weight_sum == 0:
            # Fallback to equal weights
            weights_array = np.ones_like(scores_array)
            weight_sum = len(scores_array)
        
        normalized_weights = weights_array / weight_sum
        info['normalized_weights'] = normalized_weights.tolist()
        
    elif method == 'ranked_average':
        # Rank-based weights
        rank_indices = np.argsort(-scores_array)  # Descending order
        num_models = len(scores_array)
        rank_weights = np.zeros(num_models, dtype=np.float32)
        
        for rank, original_idx in enumerate(rank_indices, start=1):
            rank_weights[original_idx] = num_models - rank + 1
        
        info['rank_order'] = [int(np.where(rank_indices == i)[0][0]) + 1 for i in range(num_models)]
        info['raw_weights'] = rank_weights.tolist()
        
        # Normalize
        weight_sum = np.sum(rank_weights)
        if weight_sum == 0:
            rank_weights = np.ones_like(scores_array)
            weight_sum = len(scores_array)
        
        normalized_weights = rank_weights / weight_sum
        info['normalized_weights'] = normalized_weights.tolist()
        
    elif method == 'percentile_average':
        # Percentile-based weights
        percentile_weights = np.zeros_like(scores_array, dtype=np.float32)
        
        for i, score in enumerate(scores_array):
            percentile = np.mean(scores_array <= score) * 100.0
            percentile_weights[i] = percentile
        
        info['percentiles'] = percentile_weights.tolist()
        info['raw_weights'] = percentile_weights.tolist()
        
        # Normalize
        weight_sum = np.sum(percentile_weights)
        if weight_sum == 0:
            percentile_weights = np.ones_like(scores_array)
            weight_sum = len(scores_array)
        
        normalized_weights = percentile_weights / weight_sum
        info['normalized_weights'] = normalized_weights.tolist()
        
    else:
        # Unknown method - return equal weights
        normalized_weights = np.ones_like(scores_array) / len(scores_array)
        info['normalized_weights'] = normalized_weights.tolist()
    
    return normalized_weights.tolist(), info

