"""
Unified model prediction interface for CAFA 6 protein function prediction.
Handles routing between sklearn and PyTorch models, eliminating version detection duplication.
"""

import numpy as np
from typing import Any, Dict, Optional


def predict_with_model(model: Any, 
                      X: np.ndarray, 
                      model_config: Dict,
                      device: Optional[str] = None,
                      batch_size: Optional[int] = None,
                      temperature_scaling: Optional[float] = None) -> np.ndarray:
    """
    Unified prediction interface that routes to appropriate model type.
    
    Handles:
    - sklearn models (LogisticRegression, XGBoost) via predict_proba()
    - PyTorch models (MLP v1, v2, v3) via centralized inference utilities
    
    NOW USES: Centralized utilities from utils/gpu_utils and local functions.
    Follows DRY/SOLID principles - single source of truth for inference.
    
    Args:
        model: Trained model object (sklearn or PyTorch)
        X: Feature matrix (n_samples, n_features)
        model_config: Model configuration dict with 'type' and 'version' keys
        device: Optional device string for PyTorch models (auto-detected if None)
        batch_size: Optional batch size for PyTorch models (uses config default if None)
        temperature_scaling: Optional temperature scaling for PyTorch models (deprecated, kept for compatibility)
        
    Returns:
        np.ndarray: Prediction probabilities (n_samples, n_labels)
        
    Raises:
        ValueError: If model type is unknown or unsupported
    """
    # Check if sklearn model (has predict_proba method)
    if hasattr(model, 'predict_proba'):
        # sklearn model (LogisticRegression, XGBoost, etc.)
        return model.predict_proba(X)
    
    # PyTorch model - use centralized inference
        if device is None:
            from utils.gpu_utils import get_device
        device = get_device()
    
    # Get batch size from config if not provided
    if batch_size is None:
        from config.features import get_batch_size
        batch_size = get_batch_size("nn_inference")
        
    # Use centralized PyTorch inference
    try:
        return predict_pytorch_full(
            model=model,
            X_test=X,
            device=device,
            batch_size=batch_size,
            use_sigmoid=True,  # Standard for multi-label classification
            prepare_model=True  # Auto-wrap DataParallel if needed
        )
    except Exception as e:
        raise ValueError(f"Error predicting with PyTorch model: {e}")


def predict_pytorch_batch(model, X_batch, device, use_sigmoid=True):
    """
    Run inference on a single batch with a PyTorch model.
    
    Handles tensor conversion and GPU transfer efficiently.
    Separated from model preparation for better composability.
    
    Args:
        model: PyTorch model (already prepared for inference)
        X_batch: Numpy array batch (batch_size, n_features)
        device: torch.device to run on
        use_sigmoid: If True, apply sigmoid to logits
    
    Returns:
        np.ndarray: Predictions (batch_size, n_outputs)
    """
    import torch
    
    # Convert to tensor with optimal memory transfer
    X_tensor = torch.FloatTensor(X_batch)
    
    if device.type == 'cuda':
        # Use pinned memory for faster CPU→GPU transfer
        X_tensor = X_tensor.pin_memory().to(device, non_blocking=True)
    else:
        X_tensor = X_tensor.to(device)
    
    with torch.no_grad():
        logits = model(X_tensor)
        if use_sigmoid:
            probs = torch.sigmoid(logits).cpu().numpy()
        else:
            probs = logits.cpu().numpy()
    
    # Cleanup
    del X_tensor, logits
    
    return probs


def predict_pytorch_full(model, X_test, device='cuda', batch_size=512, 
                        use_sigmoid=True, prepare_model=True):
    """
    Full inference pipeline for PyTorch models.
    
    Combines model preparation and batch-wise inference.
    This is the main entry point for PyTorch model inference.
    
    Args:
        model: PyTorch model
        X_test: Full test dataset (n_samples, n_features)
        device: Device to run on
        batch_size: Batch size for inference
        use_sigmoid: If True, apply sigmoid to outputs
        prepare_model: If True, prepare model (DataParallel, device placement)
    
    Returns:
        np.ndarray: Predictions (n_samples, n_outputs)
    """
    import numpy as np
    from utils.gpu_utils import prepare_model_for_inference
    
    # Prepare model for inference (if needed)
    if prepare_model:
        model, device = prepare_model_for_inference(model, device, batch_size)
    
    predictions = []
    n_samples = len(X_test)
    
    # Batch-wise inference
    for i in range(0, n_samples, batch_size):
        batch_X = X_test[i:i + batch_size]
        batch_preds = predict_pytorch_batch(model, batch_X, device, use_sigmoid)
        predictions.append(batch_preds)
    
    return np.vstack(predictions)

