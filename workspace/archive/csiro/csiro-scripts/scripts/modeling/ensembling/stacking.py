# stacking.py
# Stacking ensemble implementation
#
# Implements stacking with out-of-fold predictions and Ridge meta-model

import pickle
import logging
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Any
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold

from modeling.models.regression_head import RegressionModel

logger = logging.getLogger(__name__)


class StackingEnsemble:
    """
    Stacking ensemble using base models and meta-model.
    
    Level 1: Base models (LGBM, XGBoost, Ridge) generate predictions
    Level 2: Meta-model (Ridge) combines base predictions
    """
    
    def __init__(
        self,
        model_paths: List[str],
        model_configs: List[Dict[str, Any]],
        feature_extraction_model_name: str,
        n_folds: int = 5,
        meta_model_alpha: float = 10.0,
        random_state: int = 42
    ):
        """
        Initialize stacking ensemble.
        
        Args:
            model_paths: List of regression model directory paths
            model_configs: List of model metadata dictionaries
            feature_extraction_model_name: Name of feature extraction model
            n_folds: Number of folds for OOF generation
            meta_model_alpha: Ridge regularization parameter
            random_state: Random seed for reproducibility
        """
        self.model_paths = model_paths
        self.model_configs = model_configs
        self.feature_extraction_model_name = feature_extraction_model_name
        self.n_folds = n_folds
        self.meta_model_alpha = meta_model_alpha
        self.random_state = random_state
        
        self.models = []
        self.meta_models = {}  # One per target
        self.model_names = []  # Names for base models (e.g., 'lgbm', 'xgboost', 'ridge')
        
        # Load all regression models
        self._load_models()
    
    def _load_models(self) -> None:
        """Load all regression models from paths."""
        logger.info(f"Loading {len(self.model_paths)} base models for stacking...")
        
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
            
            # Determine model name from config or path
            model_name = f"model_{idx + 1}"
            if idx < len(self.model_configs):
                # Try to infer from metadata
                metadata = self.model_configs[idx]
                # Could check feature_filename or other metadata
                # For now, use generic names
                pass
            
            # Try to infer from path
            if 'lgbm' in str(model_path).lower():
                model_name = 'lgbm'
            elif 'xgboost' in str(model_path).lower() or 'xgb' in str(model_path).lower():
                model_name = 'xgb'
            elif 'ridge' in str(model_path).lower():
                model_name = 'ridge'
            
            self.model_names.append(model_name)
            logger.info(f"  Loaded {model_name} model {idx + 1}/{len(self.model_paths)}: {model_file}")
        
        logger.info(f"All {len(self.models)} base models loaded")
    
    def generate_oof_predictions(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_test: np.ndarray
    ) -> Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]:
        """
        Generate out-of-fold predictions for training and test predictions.
        
        Args:
            X_train: Training features, shape (N_train, feat_dim)
            y_train: Training targets, shape (N_train, num_targets)
            X_test: Test features, shape (N_test, feat_dim)
            
        Returns:
            Tuple of (oof_preds_dict, test_preds_dict)
            - oof_preds_dict: Dict mapping model_name -> OOF predictions (N_train, num_targets)
            - test_preds_dict: Dict mapping model_name -> test predictions (N_test, num_targets)
        """
        logger.info(f"Generating OOF predictions using {self.n_folds}-fold CV...")
        
        n_train = X_train.shape[0]
        n_targets = y_train.shape[1]
        
        # Initialize OOF prediction arrays
        oof_preds = {}
        test_preds = {}
        
        for model_name in self.model_names:
            oof_preds[model_name] = np.zeros((n_train, n_targets))
            test_preds[model_name] = np.zeros((X_test.shape[0], n_targets))
        
        # Create KFold splitter
        kf = KFold(n_splits=self.n_folds, shuffle=True, random_state=self.random_state)
        
        # For each fold
        for fold, (train_idx, val_idx) in enumerate(kf.split(X_train, y_train)):
            logger.info(f"  Fold {fold + 1}/{self.n_folds}")
            
            X_tr, X_val = X_train[train_idx], X_train[val_idx]
            y_tr, y_val = y_train[train_idx], y_train[val_idx]
            
            # For each base model
            for model_name, model in zip(self.model_names, self.models):
                # Create new model instance for this fold (instead of cloning)
                model_fold = RegressionModel(
                    model_type=model.model_type,
                    model_params=model.model_params,
                    random_state=model.random_state
                )
                
                # Train on fold training data
                model_fold.fit(X_tr, y_tr)
                
                # Predict on fold validation data (OOF)
                val_pred = model_fold.predict(X_val)
                if val_pred.ndim == 1:
                    val_pred = val_pred.reshape(-1, 1)
                val_pred = np.clip(val_pred, 0, None)  # Clip negative values
                oof_preds[model_name][val_idx] = val_pred
                
                # Predict on test data
                test_pred = model_fold.predict(X_test)
                if test_pred.ndim == 1:
                    test_pred = test_pred.reshape(-1, 1)
                test_pred = np.clip(test_pred, 0, None)
                test_preds[model_name] += test_pred / self.n_folds
        
        logger.info("OOF predictions generated successfully")
        return oof_preds, test_preds
    
    def fit_meta_models(
        self,
        oof_preds: Dict[str, np.ndarray],
        y_train: np.ndarray
    ) -> None:
        """
        Train meta-models (Ridge) per target using OOF predictions.
        
        Args:
            oof_preds: Dict mapping model_name -> OOF predictions (N_train, num_targets)
            y_train: True training targets, shape (N_train, num_targets)
        """
        logger.info("Training meta-models (Ridge) per target...")
        
        n_targets = y_train.shape[1]
        
        # Train one meta-model per target
        for target_idx in range(n_targets):
            # Build meta-features: stack predictions from all base models for this target
            X_meta = np.column_stack([
                oof_preds[model_name][:, target_idx]
                for model_name in self.model_names
            ])
            
            y_meta = y_train[:, target_idx]
            
            # Train Ridge meta-model
            meta_model = Ridge(alpha=self.meta_model_alpha, random_state=self.random_state)
            meta_model.fit(X_meta, y_meta)
            
            self.meta_models[target_idx] = meta_model
            
            # Log weights (coefficients)
            coef_str = ', '.join([
                f"{name}: {coef:.3f}"
                for name, coef in zip(self.model_names, meta_model.coef_)
            ])
            logger.info(f"  Target {target_idx} weights -> {coef_str}")
        
        logger.info(f"Trained {len(self.meta_models)} meta-models")
    
    def predict(
        self,
        test_preds: Dict[str, np.ndarray]
    ) -> np.ndarray:
        """
        Generate final predictions using meta-models.
        
        Args:
            test_preds: Dict mapping model_name -> test predictions (N_test, num_targets)
            
        Returns:
            Final predictions array of shape (N_test, num_targets)
        """
        n_test = list(test_preds.values())[0].shape[0]
        n_targets = len(self.meta_models)
        
        final_preds = np.zeros((n_test, n_targets))
        
        # For each target, combine base predictions using meta-model
        for target_idx, meta_model in self.meta_models.items():
            # Build meta-features for this target
            X_meta = np.column_stack([
                test_preds[model_name][:, target_idx]
                for model_name in self.model_names
            ])
            
            # Predict using meta-model
            final_preds[:, target_idx] = meta_model.predict(X_meta)
        
        # Clip negative values
        final_preds = np.clip(final_preds, 0, None)
        
        return final_preds
