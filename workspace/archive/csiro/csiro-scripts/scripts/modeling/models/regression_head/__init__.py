# regression_head package
# Regression head models for two-stage training
#
# Provides tree-based regression models that operate on extracted features.
# Used in feature extraction mode where features are extracted first, then
# a separate regression model predicts targets from those features.
#
# Components:
# - regression_model: Wrapper for tree-based regression models (LGBM, XGBoost, Ridge)
#   Provides unified interface for training and prediction on extracted features.

from modeling.models.regression_head.regression_model import RegressionModel

__all__ = [
    'RegressionModel',
]
