"""
Model configurations for CAFA 6 protein function prediction pipeline.
"""

from .paths import MODELS_DIR
from .features import get_batch_size, get_optimized_batch_size

# Model Configuration
CURRENT_MODEL = "logistic_v1"

# Model Configurations for modular pipeline
MODEL_CONFIGS = {
    "logistic_v1": {
        "type": "lr",
        "version": "1.0",
        "trainer_module": "lr.logistic_regression_trainer_v1",
        "per_ontology_hyperparams": {
            "F": {"C": 0.5, "max_iter": 1000, "solver": "lbfgs", "random_state": 42},
            "P": {"C": 0.5, "max_iter": 1000, "solver": "lbfgs", "random_state": 42},
            "C": {"C": 0.5, "max_iter": 1000, "solver": "lbfgs", "random_state": 42}
        },
        "description": "Logistic Regression v1.0 - Baseline parameters"
    },
    "logistic_v1_1": {
        "type": "lr", 
        "version": "1.1",
        "trainer_module": "lr.logistic_regression_trainer_v1",  # Same trainer, optimized params
        "description": "Logistic Regression v1.1 - Grid search optimized (C ontology: C=1.0, f1=0.00878)",
        "per_ontology_hyperparams": {
            "F": {
                "C": 1.0,
                "max_iter": 1000,
                "solver": "lbfgs",
                "random_state": 42,
                "grid_search_score": 0.09754817655336974,
                "grid_search_timestamp": "2025-10-22T15:32:17"
            },
            "P": {
                "C": 0.5,
                "max_iter": 1000,
                "solver": "lbfgs",
                "random_state": 42,
                "grid_search_score": None,
                "grid_search_timestamp": None
            },
            "C": {
                "C": 1.0,
                "max_iter": 1000,
                "solver": "lbfgs",
                "random_state": 42,
                "grid_search_score": 0.00878,  # From v1.1 C model
                "grid_search_timestamp": "2025-10-21"
            }
        }
    },
    "logistic_v2": {
        "type": "lr",
        "version": "2.0",
        "trainer_module": "lr.logistic_regression_trainer_v1",  # Same trainer, uses embeddings
        "feature_type": "fused_embeddings",
        "feature_preset": "default",  # protbert + esm2 + hc (2394 dims)
        "description": "Logistic Regression v2.0 - ProtBERT + ESM2 + handcrafted features (2394 dims)",
        "per_ontology_hyperparams": {
            "F": {"C": 1.0, "max_iter": 1000, "solver": "lbfgs", "random_state": 42},
            "P": {"C": 0.5, "max_iter": 1000, "solver": "lbfgs", "random_state": 42},
            "C": {"C": 1.0, "max_iter": 1000, "solver": "lbfgs", "random_state": 42}
        }
    },
    "xgboost_v1": {
        "type": "xgb",
        "version": "1.0",
        "trainer_module": "xgb.xgboost_trainer_v1",
        "per_ontology_hyperparams": {
            "F": {"n_estimators": 100, "max_depth": 6, "learning_rate": 0.1, "random_state": 42},
            "P": {"n_estimators": 100, "max_depth": 6, "learning_rate": 0.1, "random_state": 42},
            "C": {"n_estimators": 100, "max_depth": 6, "learning_rate": 0.1, "random_state": 42}
        },
        "description": "XGBoost v1 - Gradient boosting baseline"
    },
    "xgboost_v2": {
        "type": "xgb",
        "version": "2.0",
        "trainer_module": "xgb.xgboost_trainer_v1",
        "feature_type": "fused_embeddings",
        "feature_preset": "default",  # protbert + esm2 + hc (2394 dims)
        "description": "XGBoost v2.0 - ProtBERT + ESM2 + handcrafted features",
        "per_ontology_hyperparams": {
            "F": {"n_estimators": 100, "max_depth": 6, "learning_rate": 0.1, "random_state": 42},
            "P": {"n_estimators": 100, "max_depth": 6, "learning_rate": 0.1, "random_state": 42},
            "C": {"n_estimators": 100, "max_depth": 6, "learning_rate": 0.1, "random_state": 42}
        }
    },
    "mlp_v1": {
        "type": "nn",
        "version": "1.0",
        "trainer_module": "nn.mlp_trainer_v1",
        "feature_type": "fused_embeddings",
        "feature_preset": "default",  # protbert + esm2 + hc (2394 dims)
        "per_ontology_hyperparams": {
            "F": {
                "hidden_dims": [1024, 512, 256],
                "dropout_rate": 0.25,
                "learning_rate": 0.001,
                "batch_size": get_batch_size("nn_training", "mlp_v1"),
                "epochs": 12,
                "patience": 5,
                "weight_decay": 1e-5,
                "label_smoothing": 0.1,
                "temperature_scaling": 1.5
            },
            "P": {
            "hidden_dims": [1024, 512, 256],
            "dropout_rate": 0.25,
            "learning_rate": 0.001,
                "batch_size": get_batch_size("nn_training", "mlp_v1"),
            "epochs": 12,
            "patience": 5,
            "weight_decay": 1e-5,
            "label_smoothing": 0.1,
            "temperature_scaling": 1.5
            },
            "C": {
                "hidden_dims": [1024, 512, 256],
                "dropout_rate": 0.25,
                "learning_rate": 0.001,
                "batch_size": get_batch_size("nn_training", "mlp_v1"),
                "epochs": 12,
                "patience": 5,
                "weight_decay": 1e-5,
                "label_smoothing": 0.1,
                "temperature_scaling": 1.5
            }
        },
        "description": "MLP v1 - 3-layer neural network with ProtBERT + ESM2 + handcrafted features (2394 dims). NOTE: Training code kept for MLPModel class used in model loading. Saved models available for prediction-only use."
    },
    "mlp_v3": {
        "type": "nn",
        "version": "3.0",
        "trainer_module": "nn.mlp_trainer_v3",
        "feature_type": "fused_embeddings",
        "feature_preset": "default",  # protbert + esm2 + hc (2394 dims)
        # No base hyperparams - each ontology has its own complete set
        "per_ontology_hyperparams": {
            "F": {
                "hidden_dims": [1024, 512, 256],
                "dropout_rates": [0.3, 0.25, 0.2],
                "learning_rate": 0.001,
                "batch_size": 1024,
                "epochs": 15,
                "weight_decay": 0.01,
                "early_stopping_patience": 3
            },
            "P": {
                "hidden_dims": [256, 128, 64],  # Very small model for 16,781 labels to fit in memory
                "dropout_rates": [0.3, 0.25, 0.2],
                "learning_rate": 0.001,
                "batch_size": 256,  # Increased from 128 (248 batches/epoch, still plenty for gradient updates)
                "epochs": 15,
                "weight_decay": 0.01,
                "early_stopping_patience": 3
            },
            "C": {
                "hidden_dims": [1024, 512, 256],
                "dropout_rates": [0.3, 0.25, 0.2],
                "learning_rate": 0.001,
                "batch_size": 1024,
                "epochs": 15,
                "weight_decay": 0.01,
                "early_stopping_patience": 3
            }
        },
        "description": "MLP v3 - Clean sparse-aware architecture with ProtBERT + ESM2 + handcrafted features (2394 dims). Uses sparse tensors throughout (no dense conversion). Handles large label spaces efficiently (16,781 P ontology terms)."
    },
    "mlp_v3.1": {
        "type": "nn",
        "version": "3.1",  # Incremental version - same trainer, scaled hyperparams
        "trainer_module": "nn.mlp_trainer_v3",  # Same trainer as v3.0
        "feature_type": "fused_embeddings",
        "feature_preset": "default",  # protbert + esm2 + hc (2394 dims)
        # No base hyperparams - each ontology has its own complete set
        "per_ontology_hyperparams": {
            "F": {
                "hidden_dims": [2048, 1024, 512, 256],  # 4 layers
                "dropout_rates": [0.4, 0.35, 0.3, 0.25],
                "learning_rate": 0.0005,
                "batch_size": 256,  # More batches per epoch for better gradient updates (~248 batches)
                "epochs": 20,
                "weight_decay": 0.01,
                "early_stopping_patience": 5,
                "label_smoothing": 0.1,  # Improves generalization
                "use_mixed_precision": True,  # 1.5-2x speedup on GPU
                "use_focal_loss": False,  # Optional: for future tuning
                "focal_alpha": 0.25,
                "focal_gamma": 2.0,
                "warmup_epochs": 2  # Cosine annealing warmup
            },
            "P": {
                "hidden_dims": [2048, 1536, 1024, 512],  # MUCH larger! 4 layers, wider (was [256, 128, 64])
                "dropout_rates": [0.4, 0.35, 0.3, 0.25],  # Higher dropout to prevent overfitting
                "learning_rate": 0.0005,  # Lower LR for stability
                "batch_size": 256,  # More batches per epoch (~248 batches) - better gradient estimates
                "epochs": 20,
                "weight_decay": 0.01,
                "early_stopping_patience": 5,
                "label_smoothing": 0.1,  # Improves generalization
                "use_mixed_precision": True,  # 1.5-2x speedup on GPU
                "use_focal_loss": False,  # Optional: for future tuning
                "focal_alpha": 0.25,
                "focal_gamma": 2.0,
                "warmup_epochs": 2  # Cosine annealing warmup
            },
            "C": {
                "hidden_dims": [2048, 1024, 512, 256],  # 4 layers
                "dropout_rates": [0.4, 0.35, 0.3, 0.25],
                "learning_rate": 0.001,  # Updated from grid search (best: 0.001)
                "batch_size": 128,  # Updated from grid search (best: 128)
                "epochs": 20,
                "weight_decay": 0.005,  # Updated from grid search (best: 0.005)
                "early_stopping_patience": 5,
                "label_smoothing": 0.15,  # Updated from grid search (best: 0.15)
                "use_mixed_precision": True,  # 1.5-2x speedup on GPU
                "use_focal_loss": False,  # Optional: for future tuning
                "focal_alpha": 0.25,
                "focal_gamma": 2.0,
                "warmup_epochs": 3  # Updated from grid search (best: 3)
            }
        },
        "description": "MLP v3.1 - Enhanced with label smoothing (0.1), mixed precision training, and cosine annealing LR scheduler. Scaled-up architecture for 2394-dim features. P ontology: [2048, 1536, 1024, 512]. Optimized for ProtBERT + ESM2 + handcrafted features."
    },
    "mlp_v4": {
        "type": "nn",
        "version": "4.0",
        "trainer_module": "nn.mlp_trainer_v4",
        "feature_type": "fused_embeddings",
        "feature_preset": "default",  # ProtBERT + ESM2 + HC (2394 dims) - T5 temporarily disabled
        # No base hyperparams - each ontology has its own complete set
        "per_ontology_hyperparams": {
            "F": {
                "hidden_dims": [2048, 1024, 512, 256],  # 4 layers
                "dropout_rates": [0.4, 0.35, 0.3, 0.25],
                "learning_rate": 0.0005,
                "batch_size": 256,  # More batches per epoch for better gradient updates (~248 batches)
                "epochs": 20,
                "weight_decay": 0.01,
                "early_stopping_patience": 5,
                "label_smoothing": 0.1,  # Improves generalization
                "use_mixed_precision": True,  # 1.5-2x speedup on GPU
                "use_focal_loss": True,  # Focal loss enabled
                "focal_alpha": 0.25,
                "focal_gamma": 2.0,
                "warmup_epochs": 2  # Cosine annealing warmup
            },
            "P": {
                "hidden_dims": [2048, 1536, 1024, 512],  # MUCH larger! 4 layers, wider (was [256, 128, 64])
                "dropout_rates": [0.4, 0.35, 0.3, 0.25],  # Higher dropout to prevent overfitting
                "learning_rate": 0.0005,  # Lower LR for stability
                "batch_size": 256,  # More batches per epoch (~248 batches) - better gradient estimates
                "epochs": 20,
                "weight_decay": 0.01,
                "early_stopping_patience": 5,
                "label_smoothing": 0.1,  # Improves generalization
                "use_mixed_precision": True,  # 1.5-2x speedup on GPU
                "use_focal_loss": True,  # Focal loss enabled
                "focal_alpha": 0.25,
                "focal_gamma": 2.0,
                "warmup_epochs": 2  # Cosine annealing warmup
            },
            "C": {
                "hidden_dims": [2048, 1024, 512, 256],  # 4 layers
                "dropout_rates": [0.4, 0.35, 0.3, 0.25],
                "learning_rate": 0.001,  # Updated from grid search (best: 0.001)
                "batch_size": 128,  # Updated from grid search (best: 128)
                "epochs": 20,
                "weight_decay": 0.005,  # Updated from grid search (best: 0.005)
                "early_stopping_patience": 5,
                "label_smoothing": 0.15,  # Updated from grid search (best: 0.15)
                "use_mixed_precision": True,  # 1.5-2x speedup on GPU
                "use_focal_loss": True,  # Focal loss enabled
                "focal_alpha": 0.25,
                "focal_gamma": 2.0,
                "warmup_epochs": 3  # Updated from grid search (best: 3)
            }
        },
        "description": "MLP v4 - Focal loss enabled (2394 dims). Uses ProtBERT + ESM2 + handcrafted features. Focal loss (alpha=0.25, gamma=2.0) for better handling of imbalanced labels. T5 embeddings temporarily disabled."
    },
    "mlp_v4.1": {
        "type": "nn",
        "version": "4.1",
        "trainer_module": "nn.mlp_trainer_v4",
        "feature_type": "fused_embeddings",
        "feature_preset": "default",  # ProtBERT + ESM2 + HC (2394 dims)
        "per_ontology_hyperparams": {
            "F": {
                "hidden_dims": [2048, 1024, 512, 256],
                "dropout_rates": [0.4, 0.35, 0.3, 0.25],
                "learning_rate": 0.0005,
                "batch_size": 256,
                "epochs": 20,
                "weight_decay": 0.01,
                "early_stopping_patience": 5,
                "label_smoothing": 0.1,
                "use_mixed_precision": True,
                "use_focal_loss": True,
                "focal_alpha": 0.75,  # Increased from 0.25 to favor positive class
                "focal_gamma": 2.0,
                "warmup_epochs": 2
            },
            "P": {
                "hidden_dims": [2048, 1536, 1024, 512],
                "dropout_rates": [0.4, 0.35, 0.3, 0.25],
                "learning_rate": 0.0005,
                "batch_size": 256,
                "epochs": 20,
                "weight_decay": 0.01,
                "early_stopping_patience": 5,
                "label_smoothing": 0.1,
                "use_mixed_precision": True,
                "use_focal_loss": True,
                "focal_alpha": 0.75,  # Increased from 0.25
                "focal_gamma": 2.0,
                "warmup_epochs": 2
            },
            "C": {
                "hidden_dims": [2048, 1024, 512, 256],
                "dropout_rates": [0.4, 0.35, 0.3, 0.25],
                "learning_rate": 0.001,
                "batch_size": 128,
                "epochs": 20,
                "weight_decay": 0.005,
                "early_stopping_patience": 5,
                "label_smoothing": 0.15,
                "use_mixed_precision": True,
                "use_focal_loss": True,
                "focal_alpha": 0.75,  # Increased from 0.25
                "focal_gamma": 2.0,
                "warmup_epochs": 3
            }
        },
        "description": "MLP v4.1 - Tuned focal loss with alpha=0.75 (increased from 0.25). Hypothesis: higher alpha favors rare positive class more, improving recall."
    },
    "mlp_v4.2": {
        "type": "nn",
        "version": "4.2",
        "trainer_module": "nn.mlp_trainer_v4",
        "feature_type": "fused_embeddings",
        "feature_preset": "default",
        "per_ontology_hyperparams": {
            "F": {
                "hidden_dims": [2048, 1024, 512, 256],
                "dropout_rates": [0.4, 0.35, 0.3, 0.25],
                "learning_rate": 0.0005,
                "batch_size": 256,
                "epochs": 20,
                "weight_decay": 0.01,
                "early_stopping_patience": 5,
                "label_smoothing": 0.1,
                "use_mixed_precision": True,
                "use_focal_loss": True,
                "focal_alpha": 0.25,
                "focal_gamma": 1.0,  # Reduced from 2.0 for less aggressive focusing
                "warmup_epochs": 2
            },
            "P": {
                "hidden_dims": [2048, 1536, 1024, 512],
                "dropout_rates": [0.4, 0.35, 0.3, 0.25],
                "learning_rate": 0.0005,
                "batch_size": 256,
                "epochs": 20,
                "weight_decay": 0.01,
                "early_stopping_patience": 5,
                "label_smoothing": 0.1,
                "use_mixed_precision": True,
                "use_focal_loss": True,
                "focal_alpha": 0.25,
                "focal_gamma": 1.0,  # Reduced from 2.0
                "warmup_epochs": 2
            },
            "C": {
                "hidden_dims": [2048, 1024, 512, 256],
                "dropout_rates": [0.4, 0.35, 0.3, 0.25],
                "learning_rate": 0.001,
                "batch_size": 128,
                "epochs": 20,
                "weight_decay": 0.005,
                "early_stopping_patience": 5,
                "label_smoothing": 0.15,
                "use_mixed_precision": True,
                "use_focal_loss": True,
                "focal_alpha": 0.25,
                "focal_gamma": 1.0,  # Reduced from 2.0
                "warmup_epochs": 3
            }
        },
        "description": "MLP v4.2 - Tuned focal loss with gamma=1.0 (reduced from 2.0). Hypothesis: lower gamma reduces over-focusing on hard examples."
    },
    "mlp_v4.3": {
        "type": "nn",
        "version": "4.3",
        "trainer_module": "nn.mlp_trainer_v4",
        "feature_type": "fused_embeddings",
        "feature_preset": "default",
        "per_ontology_hyperparams": {
            "F": {
                "hidden_dims": [2048, 1024, 512, 256],
                "dropout_rates": [0.4, 0.35, 0.3, 0.25],
                "learning_rate": 0.0005,
                "batch_size": 256,
                "epochs": 20,
                "weight_decay": 0.01,
                "early_stopping_patience": 5,
                "label_smoothing": 0.0,  # Removed to avoid conflict with focal loss
                "use_mixed_precision": True,
                "use_focal_loss": True,
                "focal_alpha": 0.25,
                "focal_gamma": 2.0,
                "warmup_epochs": 2
            },
            "P": {
                "hidden_dims": [2048, 1536, 1024, 512],
                "dropout_rates": [0.4, 0.35, 0.3, 0.25],
                "learning_rate": 0.0005,
                "batch_size": 256,
                "epochs": 20,
                "weight_decay": 0.01,
                "early_stopping_patience": 5,
                "label_smoothing": 0.0,  # Removed
                "use_mixed_precision": True,
                "use_focal_loss": True,
                "focal_alpha": 0.25,
                "focal_gamma": 2.0,
                "warmup_epochs": 2
            },
            "C": {
                "hidden_dims": [2048, 1024, 512, 256],
                "dropout_rates": [0.4, 0.35, 0.3, 0.25],
                "learning_rate": 0.001,
                "batch_size": 128,
                "epochs": 20,
                "weight_decay": 0.005,
                "early_stopping_patience": 5,
                "label_smoothing": 0.0,  # Removed
                "use_mixed_precision": True,
                "use_focal_loss": True,
                "focal_alpha": 0.25,
                "focal_gamma": 2.0,
                "warmup_epochs": 3
            }
        },
        "description": "MLP v4.3 - Focal loss with label_smoothing=0.0 (removed). Hypothesis: label smoothing conflicts with focal loss mechanism."
    },
    "mlp_v4.4": {
        "type": "nn",
        "version": "4.4",
        "trainer_module": "nn.mlp_trainer_v4",
        "feature_type": "fused_embeddings",
        "feature_preset": "default",
        "per_ontology_hyperparams": {
            "F": {
                "hidden_dims": [2048, 1024, 512, 256],
                "dropout_rates": [0.4, 0.35, 0.3, 0.25],
                "learning_rate": 0.0005,
                "batch_size": 256,
                "epochs": 20,
                "weight_decay": 0.01,
                "early_stopping_patience": 5,
                "label_smoothing": 0.1,
                "use_mixed_precision": True,
                "use_focal_loss": True,
                "focal_alpha": 0.75,  # Increased
                "focal_gamma": 1.5,  # Reduced (middle ground)
                "warmup_epochs": 2
            },
            "P": {
                "hidden_dims": [2048, 1536, 1024, 512],
                "dropout_rates": [0.4, 0.35, 0.3, 0.25],
                "learning_rate": 0.0005,
                "batch_size": 256,
                "epochs": 20,
                "weight_decay": 0.01,
                "early_stopping_patience": 5,
                "label_smoothing": 0.1,
                "use_mixed_precision": True,
                "use_focal_loss": True,
                "focal_alpha": 0.75,  # Increased
                "focal_gamma": 1.5,  # Reduced
                "warmup_epochs": 2
            },
            "C": {
                "hidden_dims": [2048, 1024, 512, 256],
                "dropout_rates": [0.4, 0.35, 0.3, 0.25],
                "learning_rate": 0.001,
                "batch_size": 128,
                "epochs": 20,
                "weight_decay": 0.005,
                "early_stopping_patience": 5,
                "label_smoothing": 0.15,
                "use_mixed_precision": True,
                "use_focal_loss": True,
                "focal_alpha": 0.75,  # Increased
                "focal_gamma": 1.5,  # Reduced
                "warmup_epochs": 3
            }
        },
        "description": "MLP v4.4 - Combined tuning: alpha=0.75 + gamma=1.5. Hypothesis: both parameters need adjustment for optimal performance."
    },
    "mlp_v4.5": {
        "type": "nn",
        "version": "4.5",
        "trainer_module": "nn.mlp_trainer_v4",
        "feature_type": "fused_embeddings",
        "feature_preset": "default",
        "per_ontology_hyperparams": {
            "F": {
                "hidden_dims": [2048, 1024, 512, 256],
                "dropout_rates": [0.4, 0.35, 0.3, 0.25],
                "learning_rate": 0.0005,
                "batch_size": 256,
                "epochs": 20,
                "weight_decay": 0.01,
                "early_stopping_patience": 5,
                "label_smoothing": 0.0,  # Removed
                "use_mixed_precision": True,
                "use_focal_loss": True,
                "focal_alpha": 0.75,  # Increased
                "focal_gamma": 1.5,  # Reduced
                "warmup_epochs": 2
            },
            "P": {
                "hidden_dims": [2048, 1536, 1024, 512],
                "dropout_rates": [0.4, 0.35, 0.3, 0.25],
                "learning_rate": 0.0005,
                "batch_size": 256,
                "epochs": 20,
                "weight_decay": 0.01,
                "early_stopping_patience": 5,
                "label_smoothing": 0.0,  # Removed
                "use_mixed_precision": True,
                "use_focal_loss": True,
                "focal_alpha": 0.75,  # Increased
                "focal_gamma": 1.5,  # Reduced
                "warmup_epochs": 2
            },
            "C": {
                "hidden_dims": [2048, 1024, 512, 256],
                "dropout_rates": [0.4, 0.35, 0.3, 0.25],
                "learning_rate": 0.001,
                "batch_size": 128,
                "epochs": 20,
                "weight_decay": 0.005,
                "early_stopping_patience": 5,
                "label_smoothing": 0.0,  # Removed
                "use_mixed_precision": True,
                "use_focal_loss": True,
                "focal_alpha": 0.75,  # Increased
                "focal_gamma": 1.5,  # Reduced
                "warmup_epochs": 3
            }
        },
        "description": "MLP v4.5 - Comprehensive tuning: alpha=0.75 + gamma=1.5 + label_smoothing=0.0. All three parameters tuned simultaneously."
    },
    "mlp_v4.6": {
        "type": "nn",
        "version": "4.6",
        "trainer_module": "nn.mlp_trainer_v4",
        "feature_type": "fused_embeddings",
        "feature_preset": "default",
        "per_ontology_hyperparams": {
            "F": {
                "hidden_dims": [2048, 1024, 512, 256],
                "dropout_rates": [0.4, 0.35, 0.3, 0.25],
                "learning_rate": 0.0005,
                "batch_size": 256,
                "epochs": 20,
                "weight_decay": 0.01,
                "early_stopping_patience": 5,
                "label_smoothing": 0.0,  # Removed
                "use_mixed_precision": True,
                "use_focal_loss": True,
                "focal_alpha": 0.9,  # Very high (extreme test)
                "focal_gamma": 1.5,  # Reduced
                "warmup_epochs": 2
            },
            "P": {
                "hidden_dims": [2048, 1536, 1024, 512],
                "dropout_rates": [0.4, 0.35, 0.3, 0.25],
                "learning_rate": 0.0005,
                "batch_size": 256,
                "epochs": 20,
                "weight_decay": 0.01,
                "early_stopping_patience": 5,
                "label_smoothing": 0.0,  # Removed
                "use_mixed_precision": True,
                "use_focal_loss": True,
                "focal_alpha": 0.9,  # Very high
                "focal_gamma": 1.5,  # Reduced
                "warmup_epochs": 2
            },
            "C": {
                "hidden_dims": [2048, 1024, 512, 256],
                "dropout_rates": [0.4, 0.35, 0.3, 0.25],
                "learning_rate": 0.001,
                "batch_size": 128,
                "epochs": 20,
                "weight_decay": 0.005,
                "early_stopping_patience": 5,
                "label_smoothing": 0.0,  # Removed
                "use_mixed_precision": True,
                "use_focal_loss": True,
                "focal_alpha": 0.9,  # Very high
                "focal_gamma": 1.5,  # Reduced
                "warmup_epochs": 3
            }
        },
        "description": "MLP v4.6 - Extreme focal loss tuning: alpha=0.9 (maximum positive class weight) + gamma=1.5 + label_smoothing=0.0. Test for extreme imbalance."
    },
    "mlp_v5": {
        "type": "nn",
        "version": "5.0",
        "trainer_module": "nn.mlp_trainer_v4",
        "feature_type": "fused_embeddings",
        "features": ["esm2_15b", "protbert", "hc"],  # Explicit: 6234 dims (5120 + 1024 + 90)
        "per_ontology_hyperparams": {
            "F": {
                "hidden_dims": [2048, 1024, 512, 256],  # 4 layers
                "dropout_rates": [0.4, 0.35, 0.3, 0.25],
                "learning_rate": 0.0005,
                "batch_size": 256,  # More batches per epoch for better gradient updates (~248 batches)
                "epochs": 20,
                "weight_decay": 0.01,
                "early_stopping_patience": 5,
                "label_smoothing": 0.1,  # Improves generalization
                "use_mixed_precision": True,  # 1.5-2x speedup on GPU
                "use_focal_loss": True,  # Focal loss enabled
                "focal_alpha": 0.25,
                "focal_gamma": 2.0,
                "warmup_epochs": 2  # Cosine annealing warmup
            },
            "P": {
                "hidden_dims": [2048, 1536, 1024, 512],  # MUCH larger! 4 layers, wider (was [256, 128, 64])
                "dropout_rates": [0.4, 0.35, 0.3, 0.25],  # Higher dropout to prevent overfitting
                "learning_rate": 0.0005,  # Lower LR for stability
                "batch_size": 256,  # More batches per epoch (~248 batches) - better gradient estimates
                "epochs": 20,
                "weight_decay": 0.01,
                "early_stopping_patience": 5,
                "label_smoothing": 0.1,  # Improves generalization
                "use_mixed_precision": True,  # 1.5-2x speedup on GPU
                "use_focal_loss": True,  # Focal loss enabled
                "focal_alpha": 0.25,
                "focal_gamma": 2.0,
                "warmup_epochs": 2  # Cosine annealing warmup
            },
            "C": {
                "hidden_dims": [2048, 1024, 512, 256],  # 4 layers
                "dropout_rates": [0.4, 0.35, 0.3, 0.25],
                "learning_rate": 0.001,  # Updated from grid search (best: 0.001)
                "batch_size": 128,  # Updated from grid search (best: 128)
                "epochs": 20,
                "weight_decay": 0.005,  # Updated from grid search (best: 0.005)
                "early_stopping_patience": 5,
                "label_smoothing": 0.15,  # Updated from grid search (best: 0.15)
                "use_mixed_precision": True,  # 1.5-2x speedup on GPU
                "use_focal_loss": True,  # Focal loss enabled
                "focal_alpha": 0.25,
                "focal_gamma": 2.0,
                "warmup_epochs": 3  # Updated from grid search (best: 3)
            }
        },
        "description": "MLP v5.0 - Clean config with correct feature specification. ESM2-15B + ProtBERT + HC (6234 dims). Explicit features list ensures prediction uses same embeddings as training."
    }
}


def get_model_config(model_name=None):
    """Get model configuration for modular pipeline."""
    if model_name is None:
        model_name = CURRENT_MODEL
    
    if model_name not in MODEL_CONFIGS:
        raise ValueError(f"Unknown model: {model_name}. Available: {list(MODEL_CONFIGS.keys())}")
    
    return MODEL_CONFIGS[model_name]


def get_model_trainer(model_name):
    """
    Get the appropriate trainer function for a model configuration.
    Supports versioned trainers through version-specific imports.
    
    Args:
        model_name: Model configuration name
        
    Returns:
        tuple: (train_ontology_model_func, train_all_ontologies_func)
    """
    config = get_model_config(model_name)
    model_type = config['type']
    version = config['version']
    
    # Determine version suffix for imports (e.g., "1.0" -> "v1", "2.0" -> "v2")
    # For non-versioned or v1, use v1; for v2+, use appropriate version
    version_major = version.split('.')[0]  # "1.0" -> "1", "2.0" -> "2"
    
    if model_type == 'lr':
        from models.lr import (
            train_ontology_model_v1,
            train_all_ontologies_v1
        )
        return train_ontology_model_v1, train_all_ontologies_v1
    
    elif model_type == 'xgb':
        from models.xgb import (
            train_ontology_model_v1,
            train_all_ontologies_v1
        )
        return train_ontology_model_v1, train_all_ontologies_v1
    
    elif model_type == 'nn':
        # Handle versioned neural network trainers
        if version_major == "1":
            from models.nn import (
                train_ontology_model_v1,
                train_all_ontologies_v1
            )
            return train_ontology_model_v1, train_all_ontologies_v1
        elif version_major == "3":
            from models.nn import (
                train_ontology_model_v3,
                train_all_ontologies_v3
            )
            return train_ontology_model_v3, train_all_ontologies_v3
        elif version_major == "4":
            from models.nn import (
                train_ontology_model_v4,
                train_all_ontologies_v4
            )
            return train_ontology_model_v4, train_all_ontologies_v4
        else:
            raise ValueError(f"Unknown neural network version: {version}")
    
    else:
        raise ValueError(f"Unknown model type: {model_type}")


def get_model_mode(model_name):
    """
    Get the mode for a model configuration.
    
    Args:
        model_name: Model configuration name
        
    Returns:
        str: Model mode ('train', 'predict', etc.)
    """
    config = get_model_config(model_name)
    return config.get('mode', 'train')


def get_model_config_by_type_version(model_type: str, version: str):
    """
    Get model configuration by type and version.
    
    Args:
        model_type: Model type ('lr', 'xgb', 'nn')
        version: Model version (e.g., '1.0', '2.0')
        
    Returns:
        dict: Model configuration
        
    Raises:
        ValueError: If no matching model config found
    """
    for name, config in MODEL_CONFIGS.items():
        if config['type'] == model_type and str(config['version']) == str(version):
            return config
    
    raise ValueError(f"Model config not found for {model_type} v{version}")


def get_ontology_hyperparams(model_name, ontology_code):
    """
    Get hyperparameters for specific model + ontology combination.
    
    REQUIRES: per_ontology_hyperparams must be defined for all models.
    Each ontology must have its own complete hyperparameter set.
    This ensures clarity - no confusion about which params are used.
    
    Args:
        model_name: Model configuration name
        ontology_code: Ontology code ('F', 'P', 'C')
        
    Returns:
        dict: Hyperparameters for the model-ontology combination
        
    Raises:
        ValueError: If per_ontology_hyperparams is missing or incomplete
    """
    config = get_model_config(model_name)
    
    # Require per_ontology_hyperparams (no fallback to base hyperparams)
    if 'per_ontology_hyperparams' not in config:
        raise ValueError(
            f"Model '{model_name}' must have 'per_ontology_hyperparams' defined. "
            f"Each ontology (F, P, C) should have its own complete hyperparameter set."
        )
    
    if ontology_code not in config['per_ontology_hyperparams']:
        raise ValueError(
            f"Model '{model_name}' missing hyperparameters for ontology '{ontology_code}'. "
            f"Available ontologies: {list(config['per_ontology_hyperparams'].keys())}"
        )
    
    ont_params = config['per_ontology_hyperparams'][ontology_code].copy()
    
    # Remove metadata fields that aren't hyperparameters
    metadata_fields = ['grid_search_score', 'grid_search_timestamp']
    for field in metadata_fields:
        ont_params.pop(field, None)
    
    return ont_params
