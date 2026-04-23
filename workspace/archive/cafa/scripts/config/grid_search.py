"""
Grid search configurations for hyperparameter tuning.
Includes per-ontology parameter grids for targeted optimization.
"""

# Grid Search Configurations
GRID_SEARCH_CONFIGS = {
    "lr": {
        "cv_folds": 3,
        "scoring": "f1_samples",
        "n_jobs": -1,
        "save_results": True,
        "output_dir": "kaggle/working",
        "param_grid": {
            "C": [0.01, 0.05, 0.1, 0.3, 0.5, 1.0, 2.0],
            "solver": ["lbfgs", "saga", "liblinear"],
            "max_iter": [1000, 2000],
            "class_weight": [None, "balanced"]
        },
        "quick_param_grid": {
            "C": [0.1, 0.5, 1.0],
            "solver": ["lbfgs"],
            "max_iter": [1000],
            "class_weight": [None]
        },
        # Per-ontology parameter grids for targeted optimization
        "param_grids": {
            "F": {
                "C": [0.7, 1.0, 1.5, 2.0],  # Centered around 1.0 (F ontology optimal)
                "solver": ["lbfgs", "saga"],
                "max_iter": [1000, 2000],
                "class_weight": [None, "balanced"]
            },
            "P": {
                "C": [0.3, 0.5, 0.7, 1.0],  # Centered around 0.5 (P ontology optimal)
                "solver": ["lbfgs", "saga"],
                "max_iter": [1000, 2000],
                "class_weight": [None, "balanced"]
            },
            "C": {
                "C": [0.7, 1.0, 1.5, 2.0],  # Centered around 1.0 (C ontology optimal)
                "solver": ["lbfgs", "saga"],
                "max_iter": [1000, 2000],
                "class_weight": [None, "balanced"]
            }
        }
    },
    "xgb": {
        "cv_folds": 3,
        "scoring": "f1_samples",
        "n_jobs": -1,
        "save_results": True,
        "output_dir": "kaggle/working",
        "param_grid": {
            "n_estimators": [50, 100, 200, 300],
            "max_depth": [3, 4, 5, 6, 7],
            "learning_rate": [0.01, 0.05, 0.1, 0.2, 0.3],
            "subsample": [0.8, 0.9, 1.0],
            "colsample_bytree": [0.8, 0.9, 1.0],
            "tree_method": ["gpu_hist"],
            "gpu_id": [0]
        },
        "quick_param_grid": {
            "n_estimators": [100, 200],
            "max_depth": [4, 6],
            "learning_rate": [0.1, 0.2],
            "subsample": [0.9, 1.0],
            "colsample_bytree": [0.9, 1.0],
            "tree_method": ["gpu_hist"],
            "gpu_id": [0]
        },
        # Per-ontology parameter grids for targeted optimization
        "param_grids": {
            "F": {
                "n_estimators": [100, 200, 300],
                "max_depth": [4, 6, 8],
                "learning_rate": [0.05, 0.1, 0.2],
                "subsample": [0.8, 1.0],
                "colsample_bytree": [0.8, 1.0]
            },
            "P": {
                "n_estimators": [100, 200, 300],
                "max_depth": [4, 6, 8],
                "learning_rate": [0.05, 0.1, 0.2],
                "subsample": [0.8, 1.0],
                "colsample_bytree": [0.8, 1.0]
            },
            "C": {
                "n_estimators": [100, 200, 300],
                "max_depth": [4, 6, 8],
                "learning_rate": [0.05, 0.1, 0.2],
                "subsample": [0.8, 1.0],
                "colsample_bytree": [0.8, 1.0]
            }
        }
    },
    "nn": {
        "cv_folds": 3,
        "scoring": "f1_samples",
        "n_jobs": 1,  # Neural networks don't parallelize well
        "save_results": True,
        "output_dir": "kaggle/working",
        "grid_search_epochs": 10,  # Reduced epochs for grid search speed
        "param_grid": {
            # High priority hyperparameters for MLP v3.1
            "learning_rate": [0.0003, 0.0005, 0.0007, 0.001],
            "label_smoothing": [0.0, 0.05, 0.1, 0.15],
            "batch_size": [128, 256, 512],
            "weight_decay": [0.005, 0.01, 0.02],
            "warmup_epochs": [1, 2, 3]
        },
        "quick_param_grid": {
            # Quick test grid (smaller ranges)
            "learning_rate": [0.0005, 0.0007],
            "label_smoothing": [0.05, 0.1],
            "batch_size": [256],
            "weight_decay": [0.01],
            "warmup_epochs": [2]
        },
        # Per-ontology parameter grids for MLP v3.1
        "param_grids": {
            "F": {
                # F ontology: smaller label space, can test more combinations
                "learning_rate": [0.0003, 0.0005, 0.0007, 0.001],
                "label_smoothing": [0.0, 0.05, 0.1, 0.15],
                "batch_size": [128, 256, 512],
                "weight_decay": [0.005, 0.01, 0.02],
                "warmup_epochs": [1, 2, 3]
            },
            "P": {
                # P ontology: largest label space (16,781 terms) - smaller grid to save time
                "learning_rate": [0.0003, 0.0005, 0.0007],  # Focus on lower LR for stability
                "label_smoothing": [0.05, 0.1, 0.15],  # Skip 0.0 (already tested)
                "batch_size": [128, 256],  # Smaller batch sizes for memory
                "weight_decay": [0.01, 0.02],  # Focus on regularization
                "warmup_epochs": [2, 3]  # Skip 1 (too short)
            },
            "C": {
                # C ontology: medium label space - balanced grid
                "learning_rate": [0.0003, 0.0005, 0.0007, 0.001],
                "label_smoothing": [0.0, 0.05, 0.1, 0.15],
                "batch_size": [128, 256, 512],
                "weight_decay": [0.005, 0.01, 0.02],
                "warmup_epochs": [1, 2, 3]
            }
        }
    }
}


def get_grid_search_config(model_type="lr", ontology=None):
    """
    Get grid search configuration for specified model type and ontology.
    
    Args:
        model_type: Model type (e.g., 'lr', 'xgb', 'nn')
        ontology: Ontology code ('F', 'P', 'C') for per-ontology grids
        
    Returns:
        dict: Grid search configuration
    """
    if model_type not in GRID_SEARCH_CONFIGS:
        raise ValueError(f"Unknown model type: {model_type}. Available: {list(GRID_SEARCH_CONFIGS.keys())}")
    
    config = GRID_SEARCH_CONFIGS[model_type].copy()
    
    # If ontology specified and per-ontology grids available, use targeted grid
    if ontology and "param_grids" in config and ontology in config["param_grids"]:
        config["param_grid"] = config["param_grids"][ontology]
        print(f"   🎯 Using per-ontology grid for {ontology} ontology")
    
    return config
