# models package
# Model architectures organized by type
#
# This package contains all model implementations organized into sub-packages:
# - end_to_end: Complete models with built-in regression heads (TimmModel, DINOv2Model)
# - regression_head: Tree-based regression models for two-stage training (LGBM, XGBoost, Ridge)
#
# This package re-exports the main factory function and common model classes from end_to_end
# for convenience and to provide a unified package API.


__all__ = [
    # End-to-end models
    'BaseFeatureExtractionModel',
    'TimmModel',
    'DINOv2Model',
    'create_model',
    '_is_regression_model_type',
    # Regression head models
    'RegressionModel',
]
