"""
Models package for CAFA 6 protein function prediction.
Contains different model implementations with versioning support.
"""

# Import from subdirectories
from .lr import (
    train_ontology_model_v1,
    train_all_ontologies_v1
)

from .xgb import (
    train_ontology_model_v1 as train_ontology_model_xgb_v1,
    train_all_ontologies_v1 as train_all_ontologies_xgb_v1
)

__all__ = [
    # Versioned imports
    'train_ontology_model_v1',
    'train_all_ontologies_v1',
    'train_ontology_model_xgb_v1',
    'train_all_ontologies_xgb_v1'
]
