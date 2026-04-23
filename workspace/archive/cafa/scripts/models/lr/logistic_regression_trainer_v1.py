"""
Logistic Regression trainer for CAFA 6 protein function prediction.
Extracted from starter_model.py for modularity.
DO NOT MODIFY THIS FILE.
Use the grid_search.py file to update the hyperparameters.
"""

import numpy as np
from typing import Dict, Any, Optional
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression

from config.training import DEFAULT_RANDOM_SEED, DEFAULT_N_JOBS
from models.training_utils import (
    check_ontology_has_terms,
    merge_hyperparams,
    train_with_error_handling,
    log_training_start,
    log_training_success
)


def train_ontology_model(X_train: np.ndarray, y_train: np.ndarray, 
                        ont_code: str, ont_name: str, **hyperparams) -> Optional[OneVsRestClassifier]:
    """
    Train logistic regression model for a specific ontology.
    
    Args:
        X_train: Feature matrix (n_samples, n_features)
        y_train: Label matrix (n_samples, n_terms)
        ont_code: Ontology code ('F', 'P', 'C')
        ont_name: Ontology name ('MFO', 'BPO', 'CCO')
        **hyperparams: Model hyperparameters
        
    Returns:
        trained model object or None if skipped
    """
    log_training_start(ont_name, "Logistic Regression")
    
    # Skip if no terms for this ontology
    if not check_ontology_has_terms(y_train, ont_name):
        return None
    
    # Default hyperparameters
    default_params = {
        'max_iter': 1000,
        'solver': 'lbfgs',
        'C': 1.0,  # Stronger regularization for 90 features
        'random_state': DEFAULT_RANDOM_SEED
    }
    
    # Merge with provided hyperparameters
    merged_params = merge_hyperparams(default_params, hyperparams)
    
    def _train_model():
        # Train logistic regression with enhanced regularization
        model = OneVsRestClassifier(
            LogisticRegression(**merged_params),
            n_jobs=DEFAULT_N_JOBS
        )
        model.fit(X_train, y_train)
        return model
    
    model = train_with_error_handling(_train_model, ont_name=ont_name)
    
    if model is not None:
        log_training_success(ont_name)
    
    return model


def train_all_ontologies(X_train: np.ndarray, y_train_dict: Dict[str, np.ndarray], 
                        ontologies: Dict[str, str], **hyperparams) -> Dict[str, OneVsRestClassifier]:
    """
    Train models for all ontologies.
    
    Args:
        X_train: Feature matrix
        y_train_dict: dict mapping ont_code -> label matrix
        ontologies: dict mapping ont_code -> ont_name
        **hyperparams: Model hyperparameters
        
    Returns:
        dict: ont_code -> trained model
    """
    print("\n[6/9] Training models...")
    
    models = {}
    
    for ont_code, ont_name in ontologies.items():
        y_ont = y_train_dict[ont_code]
        model = train_ontology_model(X_train, y_ont, ont_code, ont_name, **hyperparams)
        if model is not None:
            models[ont_code] = model
    
    print(f"   ✓ Trained {len(models)} models")
    return models
