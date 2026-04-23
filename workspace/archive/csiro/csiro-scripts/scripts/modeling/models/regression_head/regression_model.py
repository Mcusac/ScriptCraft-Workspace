# regression_model.py
# Wrapper for tree-based regression models (LGBM, XGBoost, Ridge)
# Provides unified interface for training and prediction

import numpy as np
import logging
from typing import Optional, Dict, Any
from sklearn.multioutput import MultiOutputRegressor

logger = logging.getLogger(__name__)

# Lazy imports to avoid hard dependencies
try:
    import lightgbm as lgb
    LGBM_AVAILABLE = True
except ImportError:
    LGBM_AVAILABLE = False
    logger.warning("lightgbm not available. LGBM regression model will not work.")

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    logger.warning("xgboost not available. XGBoost regression model will not work.")

try:
    from sklearn.linear_model import Ridge
    RIDGE_AVAILABLE = True
except ImportError:
    RIDGE_AVAILABLE = False
    logger.warning("sklearn not available. Ridge regression model will not work.")


class RegressionModel:
    """
    Wrapper for tree-based regression models with unified interface.
    
    Supports LightGBM, XGBoost, and Ridge regression models.
    Handles multi-output regression (5 targets) automatically.
    """
    
    def __init__(
        self,
        model_type: str,
        model_params: Optional[Dict[str, Any]] = None,
        random_state: int = 42
    ):
        """
        Initialize RegressionModel.
        
        Args:
            model_type: Type of regression model ('lgbm', 'xgboost', 'ridge').
            model_params: Optional dictionary of model-specific hyperparameters.
                        If None, uses default parameters.
            random_state: Random seed for reproducibility.
        
        Raises:
            ValueError: If model_type is invalid or required library not available.
        """
        self.model_type = model_type.lower()
        self.model_params = model_params or {}
        self.random_state = random_state
        self.model = None
        self._create_model()
    
    def _create_model(self) -> None:
        """Create the underlying regression model based on model_type."""
        if self.model_type == 'lgbm':
            if not LGBM_AVAILABLE:
                raise ValueError(
                    "lightgbm library not available. Install with: pip install lightgbm"
                )
            
            # Default LGBM parameters
            default_params = {
                'n_estimators': 300,
                'learning_rate': 0.05,
                'num_leaves': 31,
                'random_state': self.random_state,
                'n_jobs': -1,
                'verbose': -1
            }
            default_params.update(self.model_params)
            
            base_model = lgb.LGBMRegressor(**default_params)
            self.model = MultiOutputRegressor(base_model)
            
        elif self.model_type == 'xgboost' or self.model_type == 'xgb':
            if not XGBOOST_AVAILABLE:
                raise ValueError(
                    "xgboost library not available. Install with: pip install xgboost"
                )
            
            # Default XGBoost parameters
            default_params = {
                'n_estimators': 300,
                'learning_rate': 0.05,
                'max_depth': 6,
                'subsample': 0.8,
                'colsample_bytree': 0.8,
                'objective': 'reg:squarederror',
                'n_jobs': -1,
                'random_state': self.random_state,
                'tree_method': 'hist'
            }
            default_params.update(self.model_params)
            
            base_model = xgb.XGBRegressor(**default_params)
            self.model = MultiOutputRegressor(base_model)
            
        elif self.model_type == 'ridge':
            if not RIDGE_AVAILABLE:
                raise ValueError(
                    "sklearn library not available. Install with: pip install scikit-learn"
                )
            
            # Default Ridge parameters
            default_params = {
                'alpha': 1.0,
                'random_state': self.random_state
            }
            default_params.update(self.model_params)
            
            base_model = Ridge(**default_params)
            self.model = MultiOutputRegressor(base_model)
            
        else:
            raise ValueError(
                f"Invalid model_type: {self.model_type}. "
                "Must be one of: 'lgbm', 'xgboost', 'ridge'"
            )
        
        logger.info(f"Created {self.model_type} regression model with MultiOutputRegressor")
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        """
        Train the regression model on features and targets.
        
        Args:
            X: Feature array of shape (N, feat_dim).
            y: Target array of shape (N, num_targets). Should be 5 targets.
        """
        if X.ndim != 2:
            raise ValueError(f"X must be 2D array, got shape {X.shape}")
        if y.ndim != 2:
            raise ValueError(f"y must be 2D array, got shape {y.shape}")
        if X.shape[0] != y.shape[0]:
            raise ValueError(
                f"X and y must have same number of samples. "
                f"Got X.shape[0]={X.shape[0]}, y.shape[0]={y.shape[0]}"
            )
        
        logger.info(f"Training {self.model_type} regression model on {X.shape[0]} samples")
        self.model.fit(X, y)
        logger.info(f"Training complete")
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict targets from features.
        
        Args:
            X: Feature array of shape (N, feat_dim).
        
        Returns:
            Predictions array of shape (N, num_targets).
        """
        if X.ndim != 2:
            raise ValueError(f"X must be 2D array, got shape {X.shape}")
        
        predictions = self.model.predict(X)
        
        # Ensure predictions are non-negative (biomass cannot be negative)
        predictions = np.clip(predictions, 0, None)
        
        return predictions
    
    def get_model(self):
        """Get the underlying model object (for advanced usage)."""
        return self.model

