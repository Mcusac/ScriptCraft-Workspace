# regression_ensemble.py
# Regression ensemble orchestrator for combining multiple regression models
#
# Handles loading multiple regression models, extracting features once,
# running predictions from each model, and combining predictions.

import pickle
import logging
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Any

from .methods import create_ensembling_method, EnsemblingMethod

logger = logging.getLogger(__name__)


class RegressionEnsemble:
    """
    Ensemble of multiple regression models for combined predictions.
    
    Coordinates model loading, feature extraction (shared), inference,
    and prediction combination.
    """
    
    def __init__(
        self,
        model_paths: List[str],
        model_configs: List[Dict[str, Any]],
        ensembling_method: EnsemblingMethod,
        feature_extraction_model_name: str,
        cv_scores: Optional[List[float]] = None
    ):
        """
        Initialize regression ensemble.
        
        Args:
            model_paths: List of regression model directory paths
            model_configs: List of model metadata dictionaries
            ensembling_method: Method to use for combining predictions
            feature_extraction_model_name: Name of feature extraction model (shared)
            cv_scores: Optional list of CV scores for weighting
        """
        if len(model_paths) != len(model_configs):
            raise ValueError(
                f"Number of model paths ({len(model_paths)}) must match "
                f"number of configs ({len(model_configs)})"
            )
        
        self.model_paths = model_paths
        self.model_configs = model_configs
        self.ensembling_method = ensembling_method
        self.feature_extraction_model_name = feature_extraction_model_name
        self.cv_scores = cv_scores
        self.models = []
        
        # Load all regression models
        self._load_models()
    
    def _load_models(self) -> None:
        """Load all regression models from paths."""
        logger.info(f"Loading {len(self.model_paths)} regression models...")
        
        for idx, model_path in enumerate(self.model_paths):
            model_path_obj = Path(model_path)
            
            # Find regression model file
            model_file = model_path_obj / 'regression_model.pkl'
            if not model_file.exists():
                if model_path_obj.suffix == '.pkl' and model_path_obj.exists():
                    model_file = model_path_obj
                else:
                    raise FileNotFoundError(f"Regression model not found: {model_path}")
            
            # Load model
            with open(model_file, 'rb') as f:
                model = pickle.load(f)
            
            self.models.append(model)
            logger.info(f"  Loaded model {idx + 1}/{len(self.model_paths)}: {model_file}")
        
        logger.info(f"All {len(self.models)} models loaded successfully")
    
    def predict(
        self,
        features: np.ndarray,
        return_individual: bool = False
    ) -> np.ndarray:
        """
        Run inference with all models and combine predictions.
        
        Args:
            features: Feature array of shape (N, feat_dim)
            return_individual: If True, also returns individual predictions
            
        Returns:
            Combined predictions array of shape (N, num_targets).
            If return_individual=True, returns tuple (combined, individual_list)
        """
        if features.ndim != 2:
            raise ValueError(f"Features must be 2D array, got shape {features.shape}")
        
        all_predictions = []
        
        # Run predictions from each model
        for idx, model in enumerate(self.models):
            predictions = model.predict(features)  # Shape: (N, num_targets)
            
            # Ensure 2D
            if predictions.ndim == 1:
                predictions = predictions.reshape(-1, 1)
            
            all_predictions.append(predictions)
            logger.debug(f"Model {idx + 1} predictions shape: {predictions.shape}")
        
        # Get weights for methods that require scores
        weights = None
        method_name = self.ensembling_method.get_name()
        if method_name in {'weighted_average', 'ranked_average', 'percentile_average'}:
            if self.cv_scores is not None:
                weights = self.cv_scores
            else:
                logger.warning(
                    f"Method {method_name} requires scores but cv_scores is None. "
                    f"Falling back to simple average."
                )
                from .methods import SimpleAverageEnsemble
                self.ensembling_method = SimpleAverageEnsemble()
                weights = None
        
        # Combine predictions
        combined = self.ensembling_method.combine(all_predictions, weights)
        
        # Clip negative values (biomass cannot be negative)
        combined = np.clip(combined, 0, None)
        
        if return_individual:
            return combined, all_predictions
        return combined


def create_regression_ensemble_from_paths(
    model_paths: List[str],
        model_configs: List[Dict[str, Any]],
    method: str = 'weighted_average',
    feature_extraction_model_name: Optional[str] = None,
    cv_scores: Optional[List[float]] = None
) -> RegressionEnsemble:
    """
    Create regression ensemble from model paths and configs.
    
    Args:
        model_paths: List of regression model directory paths
        model_configs: List of model metadata dictionaries
        method: Ensembling method name
        feature_extraction_model_name: Feature extraction model name (auto-detected if None)
        cv_scores: Optional CV scores for weighting
        
    Returns:
        RegressionEnsemble object ready for inference
    """
    # Auto-detect feature extraction model name from first config if not provided
    if feature_extraction_model_name is None:
        if not model_configs:
            raise ValueError("Cannot auto-detect feature extraction model: no configs provided")
        
        feature_filename = model_configs[0].get('feature_filename')
        if not feature_filename:
            raise ValueError(
                "Cannot auto-detect feature extraction model: feature_filename not in config"
            )
        
        # Parse feature filename to get model name
        # Format: variant_XXXX_features.npz where XXXX encodes model_id
        # For now, we'll extract from metadata or use a default
        # This should be improved to parse from feature_filename
        logger.warning(
            "Feature extraction model name not provided. "
            "Using default 'dinov2_base'. Ensure all models use same feature extraction."
        )
        feature_extraction_model_name = 'dinov2_base'
    
    # Create ensembling method
    ensembling_method = create_ensembling_method(method)
    
    # Create ensemble
    ensemble = RegressionEnsemble(
        model_paths=model_paths,
        model_configs=model_configs,
        ensembling_method=ensembling_method,
        feature_extraction_model_name=feature_extraction_model_name,
        cv_scores=cv_scores
    )
    
    return ensemble
