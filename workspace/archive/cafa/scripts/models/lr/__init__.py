"""
Logistic Regression models for CAFA 6 protein function prediction.
Contains different versions for hyperparameter tuning and experimentation.
"""

from .logistic_regression_trainer_v1 import (
    train_ontology_model as train_ontology_model_v1,
    train_all_ontologies as train_all_ontologies_v1
)


__all__ = [
    'train_ontology_model_v1',
    'train_all_ontologies_v1'
]
