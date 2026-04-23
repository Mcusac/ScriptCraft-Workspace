"""
Preprocessing module for CAFA 6 protein function prediction.
Contains feature engineering and data preparation utilities.
"""

from .feature_engineering import extract_sequence_features

from .data_prep import (
    load_training_data,
    prepare_ontology_labels
)

__all__ = [
    'extract_sequence_features',
    'load_training_data',
    'prepare_ontology_labels'
]
