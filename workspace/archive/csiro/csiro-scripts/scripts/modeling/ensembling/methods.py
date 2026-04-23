# methods.py
# Ensembling methods for combining predictions

import numpy as np
import logging
from abc import ABC, abstractmethod
from typing import List, Optional

logger = logging.getLogger(__name__)


class EnsemblingMethod(ABC):
    """
    Abstract base class for ensembling methods.
    
    Provides interface for combining predictions from multiple models.
    """
    
    @abstractmethod
    def combine(
        self,
        predictions_list: List[np.ndarray],
        weights: Optional[List[float]] = None
    ) -> np.ndarray:
        """
        Combine predictions from multiple models.
        
        Args:
            predictions_list: List of prediction arrays, each of shape (N, 3)
                            where N is number of samples
            weights: Optional list of weights for each model (length must match predictions_list)
        
        Returns:
            Combined predictions array of shape (N, 3)
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get name of the ensembling method."""
        pass


class SimpleAverageEnsemble(EnsemblingMethod):
    """
    Simple average ensembling: equal weights for all models.
    
    prediction = mean([pred1, pred2, ..., predN])
    """
    
    def combine(
        self,
        predictions_list: List[np.ndarray],
        weights: Optional[List[float]] = None
    ) -> np.ndarray:
        """
        Combine predictions using simple average (ignores weights).
        
        Args:
            predictions_list: List of prediction arrays, each of shape (N, 3)
            weights: Ignored (all models weighted equally)
        
        Returns:
            Averaged predictions array of shape (N, 3)
        
        Raises:
            ValueError: If predictions_list is empty or shapes don't match
        """
        if not predictions_list:
            raise ValueError("predictions_list cannot be empty")
        
        # Validate all predictions have same shape
        first_shape = predictions_list[0].shape
        for idx, pred in enumerate(predictions_list[1:], 1):
            if pred.shape != first_shape:
                raise ValueError(
                    f"All predictions must have same shape. "
                    f"First: {first_shape}, prediction {idx}: {pred.shape}"
                )
        
        # Stack and average
        stacked = np.stack(predictions_list, axis=0)  # Shape: (num_models, N, 3)
        averaged = np.mean(stacked, axis=0)  # Shape: (N, 3)
        
        logger.info(f"Combined {len(predictions_list)} predictions using simple average")
        
        return averaged
    
    def get_name(self) -> str:
        return 'simple_average'


class WeightedAverageEnsemble(EnsemblingMethod):
    """
    Weighted average ensembling: weights based on CV scores.
    
    prediction = sum(weight_i * pred_i) / sum(weight_i)
    where weight_i = cv_score_i
    """
    
    def combine(
        self,
        predictions_list: List[np.ndarray],
        weights: Optional[List[float]] = None
    ) -> np.ndarray:
        """
        Combine predictions using weighted average.
        
        Args:
            predictions_list: List of prediction arrays, each of shape (N, 3)
            weights: List of weights for each model (required, length must match predictions_list)
                    Typically CV scores
        
        Returns:
            Weighted averaged predictions array of shape (N, 3)
        
        Raises:
            ValueError: If predictions_list is empty, weights missing/invalid, or shapes don't match
        """
        if not predictions_list:
            raise ValueError("predictions_list cannot be empty")
        
        if weights is None:
            raise ValueError("weights are required for weighted average ensemble")
        
        if len(weights) != len(predictions_list):
            raise ValueError(
                f"Number of weights ({len(weights)}) must match number of predictions ({len(predictions_list)})"
            )
        
        # Validate all predictions have same shape
        first_shape = predictions_list[0].shape
        for idx, pred in enumerate(predictions_list[1:], 1):
            if pred.shape != first_shape:
                raise ValueError(
                    f"All predictions must have same shape. "
                    f"First: {first_shape}, prediction {idx}: {pred.shape}"
                )
        
        # Convert weights to numpy array
        weights_array = np.array(weights, dtype=np.float32)
        
        # Handle negative scores (R² can be negative)
        # Shift scores so worst model gets weight 0, better models get proportionally higher weights
        min_weight = np.min(weights_array)
        
        if min_weight <= 0:
            # Shift all weights to be non-negative
            # Add small epsilon to ensure all weights are positive (avoids zero weights)
            epsilon = 1e-6
            weights_array = weights_array - min_weight + epsilon
            logger.info(
                f"Shifted weights to handle negative scores (min was {min_weight:.4f}). "
                f"Original scores: {[f'{w:.4f}' for w in weights]}, "
                f"Shifted weights: {[f'{w:.4f}' for w in weights_array]}"
            )
        elif np.any(weights_array <= 0):
            # Edge case: some weights are zero but min is positive
            epsilon = 1e-6
            weights_array = np.maximum(weights_array, epsilon)
            logger.warning("Some weights are zero, adding epsilon to ensure positivity")
        
        # Normalize weights
        weight_sum = np.sum(weights_array)
        if weight_sum == 0:
            logger.warning("Sum of weights is zero, falling back to simple average")
            return SimpleAverageEnsemble().combine(predictions_list)
        
        normalized_weights = weights_array / weight_sum
        
        # Weighted average
        weighted_sum = np.zeros_like(predictions_list[0], dtype=np.float32)
        for pred, weight in zip(predictions_list, normalized_weights):
            weighted_sum += pred * weight
        
        logger.info(
            f"Combined {len(predictions_list)} predictions using weighted average"
        )
        logger.info(
            f"  Original CV scores: {[f'{w:.4f}' for w in weights]}"
        )
        logger.info(
            f"  Normalized weights: {[f'{w:.4f}' for w in normalized_weights]}"
        )
        
        return weighted_sum
    
    def get_name(self) -> str:
        return 'weighted_average'


class RankedAverageEnsemble(EnsemblingMethod):
    """
    Ranked average ensembling: weights based on model rank.
    
    Assigns weights based on rank order (1st, 2nd, 3rd, etc.) rather than
    absolute score differences. Best model gets highest weight.
    
    prediction = sum(rank_weight_i * pred_i) / sum(rank_weight_i)
    where rank_weight_i is based on rank position
    """
    
    def combine(
        self,
        predictions_list: List[np.ndarray],
        weights: Optional[List[float]] = None
    ) -> np.ndarray:
        """
        Combine predictions using ranked average.
        
        Args:
            predictions_list: List of prediction arrays, each of shape (N, 3)
            weights: List of CV scores for each model (required, length must match predictions_list)
                    Used to determine rank order (higher score = better rank)
        
        Returns:
            Ranked averaged predictions array of shape (N, 3)
        
        Raises:
            ValueError: If predictions_list is empty, weights missing/invalid, or shapes don't match
        """
        if not predictions_list:
            raise ValueError("predictions_list cannot be empty")
        
        if weights is None:
            raise ValueError("weights are required for ranked average ensemble")
        
        if len(weights) != len(predictions_list):
            raise ValueError(
                f"Number of weights ({len(weights)}) must match number of predictions ({len(predictions_list)})"
            )
        
        # Validate all predictions have same shape
        first_shape = predictions_list[0].shape
        for idx, pred in enumerate(predictions_list[1:], 1):
            if pred.shape != first_shape:
                raise ValueError(
                    f"All predictions must have same shape. "
                    f"First: {first_shape}, prediction {idx}: {pred.shape}"
                )
        
        # Convert weights to numpy array
        weights_array = np.array(weights, dtype=np.float32)
        
        # Get rank order (higher score = better rank = lower rank number)
        # argsort gives indices that would sort array in ascending order
        # We want descending order (best score first), so negate
        rank_indices = np.argsort(-weights_array)  # Descending order
        
        # Assign rank-based weights: rank 1 (best) gets highest weight
        # Linear weighting: rank 1 gets weight N, rank 2 gets weight N-1, etc.
        num_models = len(predictions_list)
        rank_weights = np.zeros(num_models, dtype=np.float32)
        
        for rank, original_idx in enumerate(rank_indices, start=1):
            # Linear: best model (rank 1) gets weight num_models, worst gets weight 1
            rank_weights[original_idx] = num_models - rank + 1
        
        # Normalize weights
        weight_sum = np.sum(rank_weights)
        if weight_sum == 0:
            logger.warning("Sum of rank weights is zero, falling back to simple average")
            return SimpleAverageEnsemble().combine(predictions_list)
        
        normalized_weights = rank_weights / weight_sum
        
        # Ranked average
        weighted_sum = np.zeros_like(predictions_list[0], dtype=np.float32)
        for pred, weight in zip(predictions_list, normalized_weights):
            weighted_sum += pred * weight
        
        logger.info(
            f"Combined {len(predictions_list)} predictions using ranked average"
        )
        logger.info(
            f"  Original CV scores: {[f'{w:.4f}' for w in weights]}"
        )
        logger.info(
            f"  Rank order: {[int(np.where(rank_indices == i)[0][0]) + 1 for i in range(num_models)]}"
        )
        logger.info(
            f"  Normalized rank weights: {[f'{w:.4f}' for w in normalized_weights]}"
        )
        
        return weighted_sum
    
    def get_name(self) -> str:
        return 'ranked_average'


class PercentileAverageEnsemble(EnsemblingMethod):
    """
    Percentile average ensembling: weights based on percentile of CV scores.
    
    Converts CV scores to percentiles, then uses percentiles as weights.
    This normalizes the score distribution and reduces sensitivity to outliers.
    
    prediction = sum(percentile_weight_i * pred_i) / sum(percentile_weight_i)
    where percentile_weight_i is based on percentile of cv_score_i
    """
    
    def combine(
        self,
        predictions_list: List[np.ndarray],
        weights: Optional[List[float]] = None
    ) -> np.ndarray:
        """
        Combine predictions using percentile average.
        
        Args:
            predictions_list: List of prediction arrays, each of shape (N, 3)
            weights: List of CV scores for each model (required, length must match predictions_list)
                    Converted to percentiles for weighting
        
        Returns:
            Percentile averaged predictions array of shape (N, 3)
        
        Raises:
            ValueError: If predictions_list is empty, weights missing/invalid, or shapes don't match
        """
        if not predictions_list:
            raise ValueError("predictions_list cannot be empty")
        
        if weights is None:
            raise ValueError("weights are required for percentile average ensemble")
        
        if len(weights) != len(predictions_list):
            raise ValueError(
                f"Number of weights ({len(weights)}) must match number of predictions ({len(predictions_list)})"
            )
        
        # Validate all predictions have same shape
        first_shape = predictions_list[0].shape
        for idx, pred in enumerate(predictions_list[1:], 1):
            if pred.shape != first_shape:
                raise ValueError(
                    f"All predictions must have same shape. "
                    f"First: {first_shape}, prediction {idx}: {pred.shape}"
                )
        
        # Convert weights to numpy array
        weights_array = np.array(weights, dtype=np.float32)
        
        # Convert scores to percentiles
        # Percentile: percentage of values that are <= this value
        # Higher percentile = better model = higher weight
        percentile_weights = np.zeros_like(weights_array, dtype=np.float32)
        
        for i, score in enumerate(weights_array):
            # Calculate percentile: (number of scores <= this score) / total
            percentile = np.mean(weights_array <= score) * 100.0
            percentile_weights[i] = percentile
        
        # Handle edge case: all scores are the same (all percentiles = 100)
        if np.all(percentile_weights == percentile_weights[0]):
            logger.info("All scores are identical, falling back to simple average")
            return SimpleAverageEnsemble().combine(predictions_list)
        
        # Normalize weights
        weight_sum = np.sum(percentile_weights)
        if weight_sum == 0:
            logger.warning("Sum of percentile weights is zero, falling back to simple average")
            return SimpleAverageEnsemble().combine(predictions_list)
        
        normalized_weights = percentile_weights / weight_sum
        
        # Percentile average
        weighted_sum = np.zeros_like(predictions_list[0], dtype=np.float32)
        for pred, weight in zip(predictions_list, normalized_weights):
            weighted_sum += pred * weight
        
        logger.info(
            f"Combined {len(predictions_list)} predictions using percentile average"
        )
        logger.info(
            f"  Original CV scores: {[f'{w:.4f}' for w in weights]}"
        )
        logger.info(
            f"  Percentiles: {[f'{p:.2f}%' for p in percentile_weights]}"
        )
        logger.info(
            f"  Normalized percentile weights: {[f'{w:.4f}' for w in normalized_weights]}"
        )
        
        return weighted_sum
    
    def get_name(self) -> str:
        return 'percentile_average'


def create_ensembling_method(method_name: str) -> EnsemblingMethod:
    """
    Factory function to create ensembling method by name.
    
    Args:
        method_name: Name of method ('simple_average', 'weighted_average', 
                    'ranked_average', or 'percentile_average')
        
    Returns:
        EnsemblingMethod instance
    
    Raises:
        ValueError: If method_name is unknown
    """
    if method_name == 'simple_average':
        return SimpleAverageEnsemble()
    elif method_name == 'weighted_average':
        return WeightedAverageEnsemble()
    elif method_name == 'ranked_average':
        return RankedAverageEnsemble()
    elif method_name == 'percentile_average':
        return PercentileAverageEnsemble()
    else:
        raise ValueError(
            f"Unknown ensembling method: {method_name}. "
            f"Valid methods: 'simple_average', 'weighted_average', 'ranked_average', 'percentile_average'"
        )


def ensemble_predictions(
    predictions_list: List[np.ndarray],
    method: str,
    weights: Optional[List[float]] = None
) -> np.ndarray:
    """
    Combine predictions using specified ensembling method.
    
    Convenience function that creates method and applies it.
    
    Args:
        predictions_list: List of prediction arrays, each of shape (N, 3)
        method: Method name ('simple_average', 'weighted_average', 'ranked_average', or 'percentile_average')
        weights: Optional weights (required for weighted_average, ranked_average, and percentile_average)
        
    Returns:
        Combined predictions array of shape (N, 3)
    """
    ensembling_method = create_ensembling_method(method)
    return ensembling_method.combine(predictions_list, weights)

