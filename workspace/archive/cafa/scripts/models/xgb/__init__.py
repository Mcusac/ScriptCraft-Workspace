"""
XGBoost models for CAFA 6 protein function prediction.
Contains different versions for hyperparameter tuning and experimentation.
"""

from .xgboost_trainer_v1 import (
    train_ontology_model_xgb as train_ontology_model_v1,
    train_all_ontologies_xgb as train_all_ontologies_v1
)

__all__ = [
    'train_ontology_model_v1',
    'train_all_ontologies_v1'
]
