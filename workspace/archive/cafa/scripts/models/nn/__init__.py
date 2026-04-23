"""
Neural Network models for CAFA 6 protein function prediction.
Contains MLP and other deep learning implementations.
"""

# MLP v1 imports (prediction-only - MLPModel class needed for loading saved v1.0 models)
# NOTE: Training functions kept but not actively used. MLPModel class is required for model loading.
from models.nn.mlp_trainer_v1 import (
    train_ontology_model_mlp as train_ontology_model_v1,
    train_all_ontologies_mlp as train_all_ontologies_v1,
    MLPModel
)

# GPU cleanup utility (centralized in utils.gpu_utils)
from utils.gpu_utils import cleanup_gpu_memory

# MLP v3 imports (training only - prediction moved to utils/model_prediction.py)
from models.nn.mlp_trainer_v3 import (
    train_ontology_model as train_ontology_model_v3,
    train_all_ontologies as train_all_ontologies_v3,
    MLPModelV3
)

# MLP v4 imports (training only - prediction moved to utils/model_prediction.py)
from models.nn.mlp_trainer_v4 import (
    train_ontology_model as train_ontology_model_v4,
    train_all_ontologies as train_all_ontologies_v4,
    MLPModelV3 as MLPModelV4  # Same model class, just versioned name
)

# Prediction logic has been moved to utils/model_prediction.py for DRY/SOLID compliance
# Use predict_with_model() from utils.model_prediction instead

__all__ = [
    # V1 exports (prediction-only - MLPModel class needed for loading saved models)
    'train_ontology_model_v1',
    'train_all_ontologies_v1',
    'MLPModel',
    
    # V3 exports (training only)
    'train_ontology_model_v3',
    'train_all_ontologies_v3',
    'MLPModelV3',
    
    # V4 exports (training only)
    'train_ontology_model_v4',
    'train_all_ontologies_v4',
    'MLPModelV4',
    
    # Shared utilities
    'cleanup_gpu_memory'
]
