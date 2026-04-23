"""
Model training execution for CAFA 6 protein function prediction.
Handles training, saving, and memory cleanup for individual ontologies.
"""

import time
import numpy as np
from typing import Dict, Optional, Any
from pathlib import Path
from utils.utils_common import cleanup_memory

from config import get_model_trainer, get_ontology_hyperparams, MODELS_DIR, DATA_INPUT_DIR
from utils.model_io import save_model, load_model, check_model_exists, save_pytorch_model
from utils.logging import get_logger

logger = get_logger(__name__)

try:
    import torch
    import torch.nn as nn
    import pickle as pkl
except ImportError:
    torch = None
    nn = None
    pkl = None


def train_single_ontology_model(X_train: np.ndarray,
                               y_train_dict: Dict[str, np.ndarray],
                               mlb_dict: Dict[str, Any],
                               ont_code: str,
                               ont_name: str,
                               model_name: str,
                               model_config: Dict,
                               mode: str = 'train_new',
                               X_val: Optional[np.ndarray] = None,
                               y_val_dict: Optional[Dict[str, np.ndarray]] = None,
                               enable_threshold_opt: bool = False) -> tuple:
    """
    Train or load a single ontology model.
    
    Args:
        X_train: Feature matrix
        y_train_dict: Dict mapping ont_code -> label matrix
        mlb_dict: Dict mapping ont_code -> MultiLabelBinarizer
        ont_code: Ontology code ('F', 'P', 'C')
        ont_name: Ontology name
        model_name: Model configuration name
        model_config: Model configuration dict
        mode: Training mode ('load_or_train', 'train_new', 'load_only')
        X_val: Optional validation features
        y_val_dict: Optional validation labels
        enable_threshold_opt: If True, optimize threshold on validation set
        
    Returns:
        tuple: (model_or_path, training_time)
    """
    ont_start = time.time()
    
    if ont_code not in y_train_dict:
        logger.warning(f"Skipping {ont_name} (no data)")
        return None, 0.0
    
    # Check if model exists for smart loading
    logger.info(f"Checking for saved {ont_name} model...")
    model_exists = check_model_exists(ont_code, model_config['type'], model_config['version'])
    
    should_train = True
    if mode == "load_or_train":
        if model_exists:
            logger.info(f"Loaded {ont_name} model from disk (v{model_config['version']}) - skipping training")
            should_train = False
        else:
            logger.info(f"Training new {ont_name} model (no saved model found)")
    elif mode == "train_new":
        logger.info(f"Training new {ont_name} model (mode: train_new)")
    elif mode == "load_only":
        if model_exists:
            logger.info(f"Loaded {ont_name} model from disk (v{model_config['version']})")
            should_train = False
        else:
            raise FileNotFoundError(f"❌ {ont_name} model not found and mode is load_only - aborting")
    
    if not should_train:
        # Load existing model
        file_ext = '.pth' if model_config['type'] == 'nn' else '.pkl'
        model_path = MODELS_DIR / model_config['type'] / model_config['version'] / f"{model_config['type']}_{model_config['version']}_{ont_code}{file_ext}"
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found at expected path: {model_path}")
        
        if model_config['type'] == 'nn':
            from utils.model_io import load_pytorch_model
            model, mlb, metadata = load_model(ont_code=ont_code, model_type=model_config['type'], version=model_config['version'])
            model_result = model_path  # Store path for PyTorch models
        else:
            model, mlb, metadata = load_model(model_path=str(model_path))
            model_result = model
        
        ont_time = time.time() - ont_start
        logger.info(f"{ont_name} load time: {ont_time:.1f}s")
        return model_result, ont_time
    
    # Train model
    logger.info(f"Training {ont_name} ({ont_code})...")
    y_ont = y_train_dict[ont_code]
    
    train_ontology_model, _ = get_model_trainer(model_name)
    model = train_ontology_model(
        X_train, y_ont, ont_code, ont_name, 
        **get_ontology_hyperparams(model_name, ont_code)
    )
    
    if model is not None:
        # Save model
        mlb = mlb_dict[ont_code]
        
        # Threshold optimization (if enabled)
        optimal_threshold = None
        if enable_threshold_opt and ont_code in y_val_dict and X_val is not None:
            optimal_threshold = _optimize_threshold(
                model, model_config, X_val, y_val_dict[ont_code], mlb, ont_name
            )
        
        # Save model based on type
        if model_config['type'] == 'nn':
            model_path = _save_pytorch_model(
                model, mlb, ont_code, ont_name, model_name, model_config, optimal_threshold
            )
            model_result = model_path
        else:
            _save_sklearn_model(
                model, mlb, ont_code, model_name, model_config, optimal_threshold
            )
            model_result = model
        
        # Cleanup memory
        _cleanup_after_training(model, model_config, ont_code, ont_name, y_train_dict)
    
    ont_time = time.time() - ont_start
    logger.info(f"{ont_name} training time: {ont_time:.1f}s")
    
    return model_result if model is not None else None, ont_time


def _optimize_threshold(model: Any,
                       model_config: Dict,
                       X_val: np.ndarray,
                       y_val_true: np.ndarray,
                       mlb: Any,
                       ont_name: str) -> Optional[float]:
    """Optimize threshold on validation set."""
    from prediction.threshold_optimization import load_ia_weights, optimize_threshold
    from config.prediction import PREDICTION_SETTINGS
    
    logger.info(f"   Optimizing threshold for {ont_name}...")
    
    # Load IA weights
    ia_file = DATA_INPUT_DIR / 'IA.tsv'
    ia_weights = load_ia_weights(ia_file)
    
    # Get prediction probabilities using unified prediction interface
    from utils.model_prediction import predict_with_model
    from utils.gpu_utils import get_device
    
    try:
        # Use unified prediction interface (handles both sklearn and PyTorch models)
        y_val_proba = predict_with_model(
            model=model,
            X=X_val,
            model_config=model_config,
            device=get_device()
        )
    except Exception as e:
        logger.warning(f"   Error getting predictions for threshold optimization: {e}")
        return None
    
    if y_val_proba is not None:
        pred_settings = PREDICTION_SETTINGS
        threshold_grid = pred_settings.get("threshold_grid", [i/100 for i in range(1, 51)])
        optimal_threshold, best_f1 = optimize_threshold(
            y_val_proba, y_val_true, ia_weights, mlb, threshold_grid
        )
        logger.info(f"   ✓ Optimal threshold for {ont_name}: {optimal_threshold:.3f} (F1: {best_f1:.6f})")
        return optimal_threshold
    
    return None


def _save_pytorch_model(model: Any,
                       mlb: Any,
                       ont_code: str,
                       ont_name: str,
                       model_name: str,
                       model_config: Dict,
                       optimal_threshold: Optional[float]) -> Path:
    """Save PyTorch model."""
    # Get actual model (unwrap DataParallel if present)
    actual_model = model.module if hasattr(model, 'module') else model
    
    model_path = MODELS_DIR / model_config['type'] / model_config['version'] / f"{model_config['type']}_{model_config['version']}_{ont_code}.pth"
    model_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Get ontology-specific hyperparams (handles both per_ontology_hyperparams and base hyperparams)
    hyperparams = get_ontology_hyperparams(model_name, ont_code)
    
    metadata = {
        'ont_code': ont_code,
        'ont_name': ont_name,
        'model_type': model_config['type'],
        'version': model_config['version'],
        'hyperparams': hyperparams,
        'n_features': getattr(actual_model, 'input_dim', None),
        'n_classes': getattr(actual_model, 'output_dim', None)
    }
    if optimal_threshold is not None:
        metadata['optimal_threshold'] = optimal_threshold
    
    save_pytorch_model(actual_model, model_path, metadata=metadata)
    
    # Also save MLB for prediction with consistent naming
    mlb_path = MODELS_DIR / model_config['type'] / model_config['version'] / f"{model_config['type']}_{model_config['version']}_{ont_code}_mlb.pkl"
    mlb_path.parent.mkdir(parents=True, exist_ok=True)
    with open(mlb_path, 'wb') as f:
        pkl.dump(mlb, f)
    
    logger.info(f"Saved {ont_name} model and MultiLabelBinarizer")
    return model_path


def _save_sklearn_model(model: Any,
                       mlb: Any,
                       ont_code: str,
                       model_name: str,
                       model_config: Dict,
                       optimal_threshold: Optional[float]):
    """Save sklearn model."""
    # Get ontology-specific hyperparams (handles both per_ontology_hyperparams and base hyperparams)
    hyperparams = get_ontology_hyperparams(model_name, ont_code)
    metadata = hyperparams.copy()
    if optimal_threshold is not None:
        metadata['optimal_threshold'] = optimal_threshold
    
    save_model(
        model=model,
        mlb=mlb,
        ont_code=ont_code,
        model_type=model_config['type'],
        version=model_config['version'],
        hyperparams=metadata
    )


def _cleanup_after_training(model: Any,
                           model_config: Dict,
                           ont_code: str,
                           ont_name: str,
                           y_train_dict: Dict):
    """Clean up memory after training."""
    if model_config['type'] == 'nn':
        # Cleanup GPU memory using centralized utility
        try:
            from utils.gpu_utils import cleanup_gpu_memory
            cleanup_gpu_memory()
            logger.info(f"GPU memory cleaned up for {ont_name}")
        except Exception as e:
            logger.warning(f"Could not cleanup GPU: {e}")
        
        # Clean up model object
        if hasattr(model, 'module'):
            del model.module
        del model
        cleanup_memory()
    else:
        # Clean up sklearn model
        del model
        cleanup_memory()
    
    # Delete labels for this ontology to free memory
    if ont_code in y_train_dict:
        del y_train_dict[ont_code]
        cleanup_memory()
        logger.info(f"Freed memory for {ont_name} labels")
    
    # Clean up memmap cache files if they exist (optional - can be kept for reuse)
    # Uncomment the following block if you want to delete memmap files after training:
    # try:
    #     from config.paths import DATA_OUTPUT_DIR
    #     memmap_dir = DATA_OUTPUT_DIR / 'memmap_cache'
    #     if memmap_dir.exists():
    #         import glob
    #         memmap_files = list(memmap_dir.glob('*.npy'))
    #         for memmap_file in memmap_files:
    #             try:
    #                 memmap_file.unlink()
    #                 metadata_file = memmap_file.with_suffix('.npy.meta')
    #                 if metadata_file.exists():
    #                     metadata_file.unlink()
    #             except Exception as e:
    #                 logger.warning(f"Could not delete memmap file {memmap_file}: {e}")
    #         logger.info(f"Cleaned up {len(memmap_files)} memmap cache files")
    # except Exception as e:
    #     logger.warning(f"Could not cleanup memmap cache: {e}")

