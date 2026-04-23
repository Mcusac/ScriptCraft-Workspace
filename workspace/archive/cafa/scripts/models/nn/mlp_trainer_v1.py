"""
Multi-Layer Perceptron trainer for CAFA 6 protein function prediction.
PyTorch-based neural network implementation with GPU support.
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from typing import Dict, Any, Optional, Tuple
import time
from pathlib import Path
import os

# Import batch size config
from config.features import get_batch_size, get_optimized_batch_size
from config.training import DEFAULT_VALIDATION_SPLIT, LARGE_ONTOLOGY_LABEL_THRESHOLD
from models.training_utils import (
    check_ontology_has_terms,
    merge_hyperparams,
    log_training_start,
    log_epoch_progress,
    calculate_metrics,
    compute_final_metrics_from_accumulator
)
from utils.utils_common import cleanup_memory

# Detect if running on Kaggle (multiprocessing issues with num_workers > 0)
KAGGLE_ENV = os.path.exists('/kaggle/input')


class MLPModel(nn.Module):
    """
    Simple Multi-Layer Perceptron for multi-label protein function prediction.
    
    Architecture:
    Input → Dense(512) → BatchNorm → ReLU → Dropout(0.3)
         → Dense(256) → BatchNorm → ReLU → Dropout(0.3) 
         → Dense(n_terms) → Sigmoid
    """
    
    def __init__(self, input_dim: int, output_dim: int, hidden_dims: list = [512, 256], 
                 dropout_rate: float = 0.3):
        """
        Initialize MLP model.
        
        Args:
            input_dim: Input feature dimension (e.g., 1024 for ProtBERT)
            output_dim: Output dimension (number of GO terms)
            hidden_dims: List of hidden layer dimensions
            dropout_rate: Dropout rate for regularization
        """
        super(MLPModel, self).__init__()
        
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.hidden_dims = hidden_dims
        
        # Build layers dynamically
        layers = []
        prev_dim = input_dim
        
        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.BatchNorm1d(hidden_dim),
                nn.ReLU(),
                nn.Dropout(dropout_rate)
            ])
            prev_dim = hidden_dim
        
        # Output layer
        layers.append(nn.Linear(prev_dim, output_dim))
        
        self.network = nn.Sequential(*layers)
        
    def forward(self, x):
        """Forward pass through the network.
        Returns logits (no sigmoid) for use with BCEWithLogitsLoss.
        Apply sigmoid during inference/prediction.
        """
        logits = self.network(x)
        return logits


# calculate_metrics() moved to models.utils for reuse


def calculate_metrics_streaming(y_true_batch: np.ndarray, y_pred_batch: np.ndarray, 
                                accumulator: Dict[str, list] = None) -> Dict[str, list]:
    """
    Calculate metrics incrementally (streaming) to avoid storing all predictions.
    Accumulates true positives, false positives, false negatives per sample.
    Uses lists to avoid memory copying overhead from concatenation.
    
    Args:
        y_true_batch: True labels for current batch (n_samples, n_labels)
        y_pred_batch: Predicted probabilities for current batch (n_samples, n_labels)
        accumulator: Previous accumulator state (dict with 'tp', 'fp', 'fn' lists)
        
    Returns:
        Updated accumulator dict (lists are appended to, not copied)
    """
    from config.prediction import BINARY_PREDICTION_THRESHOLD
    
    # Convert probabilities to binary predictions
    y_pred_binary = (y_pred_batch > BINARY_PREDICTION_THRESHOLD).astype(int)
    y_true_binary = (y_true_batch > BINARY_PREDICTION_THRESHOLD).astype(int)
    
    # Calculate per-sample metrics (sum across labels for each sample)
    tp = np.sum(y_pred_binary * y_true_binary, axis=1)  # True positives per sample
    fp = np.sum(y_pred_binary * (1 - y_true_binary), axis=1)  # False positives per sample
    fn = np.sum((1 - y_pred_binary) * y_true_binary, axis=1)  # False negatives per sample
    
    if accumulator is None:
        accumulator = {
            'tp': tp.tolist(),  # Convert to list for efficient appending
            'fp': fp.tolist(),
            'fn': fn.tolist()
        }
    else:
        # Append to lists (no copying, just reference updates)
        accumulator['tp'].extend(tp.tolist())
        accumulator['fp'].extend(fp.tolist())
        accumulator['fn'].extend(fn.tolist())
    
    return accumulator

# compute_final_metrics_from_accumulator() moved to models.utils for reuse


def train_epoch(model: MLPModel, dataloader: DataLoader, optimizer: optim.Optimizer, 
                criterion: nn.Module, device: str, scaler=None, 
                use_streaming_metrics: bool = True) -> Dict[str, float]:
    """
    Train model for one epoch.
    
    Args:
        model: PyTorch model
        dataloader: Training data loader
        optimizer: Optimizer
        criterion: Loss function
        device: Device to train on
        scaler: Gradient scaler for mixed precision (optional)
        use_streaming_metrics: If True, use memory-efficient streaming metrics (default: True)
        
    Returns:
        Dictionary of training metrics
    """
    model.train()
    total_loss = 0.0
    
    # Use streaming metrics for large ontologies to avoid OOM
    if use_streaming_metrics:
        metrics_accumulator = None
    else:
        all_predictions = []
        all_targets = []
    
    for batch_X, batch_y in dataloader:
        # Transfer batches to GPU (data may be on CPU for large datasets)
        # non_blocking=True allows GPU to start working while CPU prepares next batch
        batch_X = batch_X.to(device, non_blocking=True)
        batch_y = batch_y.to(device, non_blocking=True)
        
        optimizer.zero_grad()
        
        # Forward pass with mixed precision if enabled
        if scaler is not None:
            from torch.cuda.amp import autocast
            with autocast():
                outputs = model(batch_X)
                loss = criterion(outputs, batch_y)
            
            # Backward pass with gradient scaling
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            scaler.step(optimizer)
            scaler.update()
        else:
            # Standard precision training
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            
            # Backward pass
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
        
        total_loss += loss.item()
        
        # Calculate metrics (memory-efficient for large ontologies)
        with torch.no_grad():
            # Apply sigmoid to logits for metrics (model now returns logits, not probabilities)
            predictions = torch.sigmoid(outputs).detach().cpu().numpy()
            targets = batch_y.cpu().numpy()
            
            if use_streaming_metrics:
                # Memory-efficient: accumulate TP/FP/FN instead of storing all predictions
                metrics_accumulator = calculate_metrics_streaming(targets, predictions, metrics_accumulator)
            else:
                # Standard approach: store all predictions (uses more memory)
                all_predictions.append(predictions)
                all_targets.append(targets)
    
    # Calculate final metrics
    if use_streaming_metrics and metrics_accumulator is not None:
        metrics = compute_final_metrics_from_accumulator(metrics_accumulator)
    elif not use_streaming_metrics and all_predictions:
        all_predictions = np.vstack(all_predictions)
        all_targets = np.vstack(all_targets)
        metrics = calculate_metrics(all_targets, all_predictions)
    else:
        # Fallback if no predictions collected
        metrics = {'f1_score': 0.0, 'precision': 0.0, 'recall': 0.0}
    
    metrics['loss'] = total_loss / len(dataloader)
    
    return metrics


def validate_epoch(model: MLPModel, dataloader: DataLoader, criterion: nn.Module, 
                  device: str, use_streaming_metrics: bool = True) -> Dict[str, float]:
    """
    Validate model for one epoch.
    
    Args:
        model: PyTorch model
        dataloader: Validation data loader
        criterion: Loss function
        device: Device to validate on
        use_streaming_metrics: If True, use memory-efficient streaming metrics (default: True)
        
    Returns:
        Dictionary of validation metrics
    """
    model.eval()
    total_loss = 0.0
    
    # Use streaming metrics for large ontologies to avoid OOM
    if use_streaming_metrics:
        metrics_accumulator = None
    else:
        all_predictions = []
        all_targets = []
    
    with torch.no_grad():
        for batch_X, batch_y in dataloader:
            # Transfer batches to GPU (data may be on CPU for large datasets)
            batch_X = batch_X.to(device, non_blocking=True)
            batch_y = batch_y.to(device, non_blocking=True)
            
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            
            total_loss += loss.item()
            
            # Calculate metrics (memory-efficient for large ontologies)
            # Apply sigmoid to logits for metrics (model now returns logits, not probabilities)
            predictions = torch.sigmoid(outputs).detach().cpu().numpy()
            targets = batch_y.cpu().numpy()
            
            if use_streaming_metrics:
                # Memory-efficient: accumulate TP/FP/FN instead of storing all predictions
                metrics_accumulator = calculate_metrics_streaming(targets, predictions, metrics_accumulator)
            else:
                # Standard approach: store all predictions (uses more memory)
                all_predictions.append(predictions)
                all_targets.append(targets)
    
    # Calculate final metrics
    if use_streaming_metrics and metrics_accumulator is not None:
        metrics = compute_final_metrics_from_accumulator(metrics_accumulator)
    elif not use_streaming_metrics and all_predictions:
        all_predictions = np.vstack(all_predictions)
        all_targets = np.vstack(all_targets)
        metrics = calculate_metrics(all_targets, all_predictions)
    else:
        # Fallback if no predictions collected
        metrics = {'f1_score': 0.0, 'precision': 0.0, 'recall': 0.0}
    
    metrics['loss'] = total_loss / len(dataloader)
    
    return metrics


def train_ontology_model_mlp(X_train: np.ndarray, y_train: np.ndarray, 
                            ont_code: str, ont_name: str, 
                            validation_split: float = None,
                            **hyperparams) -> Optional[MLPModel]:
    """
    Train MLP model for a specific ontology.
    
    Args:
        X_train: Feature matrix (n_samples, n_features)
        y_train: Label matrix (n_samples, n_terms)
        ont_code: Ontology code ('F', 'P', 'C')
        ont_name: Ontology name ('MFO', 'BPO', 'CCO')
        validation_split: Fraction of data to use for validation
        **hyperparams: Model hyperparameters
        
    Returns:
        trained model object or None if skipped
    """
    log_training_start(ont_name, "MLP")
    
    # Use default validation split if not provided
    if validation_split is None:
        validation_split = DEFAULT_VALIDATION_SPLIT
    
    # Check if we have data for this ontology
    if not check_ontology_has_terms(y_train, ont_name):
        return None
    
    # Set device using centralized utility
    from utils.gpu_utils import get_device
    device = get_device()
    print(f"      Using device: {device}")
    
    # Default hyperparameters (batch_size comes from hyperparams, which comes from config)
    default_params = {
        'input_dim': X_train.shape[1],
        'output_dim': y_train.shape[1],
        'hidden_dims': [1024, 512, 256],
        'dropout_rate': 0.25,
        'learning_rate': 0.001,
        'epochs': 12,
        'patience': 5,
        'weight_decay': 1e-5
    }
    
    # Merge with provided hyperparameters (includes batch_size from config)
    default_params = merge_hyperparams(default_params, hyperparams)
    
    # Ensure batch_size is set (fallback to config default if missing)
    if 'batch_size' not in default_params:
        default_params['batch_size'] = get_batch_size("nn_training")
    
    # Also ensure features are float32 (PyTorch expects float32 anyway)
    if X_train.dtype != np.float32:
        X_train = X_train.astype(np.float32)
    
    # Create train/validation split FIRST (before converting to dense)
    # This allows us to convert only the needed indices, saving memory
    n_samples = X_train.shape[0]
    n_val = int(n_samples * validation_split)
    indices = np.random.permutation(n_samples)
    
    train_indices = indices[n_val:]
    val_indices = indices[:n_val]
    
    # Convert sparse labels to dense ONLY for the indices we need (memory optimization)
    # This avoids loading the entire dense matrix into RAM (~5.3 GB for P ontology)
    if hasattr(y_train, 'toarray'):
        print(f"      Converting sparse labels to dense for splits only: {y_train.shape}")
        # Convert only train indices first
        y_train_dense = y_train[train_indices].toarray().astype(np.float32)
        # Convert validation indices
        y_val_dense = y_train[val_indices].toarray().astype(np.float32)
        # Free the sparse matrix immediately
        del y_train
        cleanup_memory()
        print(f"      Converted to dense: train={y_train_dense.shape}, val={y_val_dense.shape} (dtype: float32)")
    else:
        # Already dense, ensure float32 and extract splits
        if y_train.dtype != np.float32:
            y_train = y_train.astype(np.float32)
        y_train_dense = y_train[train_indices]
        y_val_dense = y_train[val_indices]
        del y_train  # Free original if we created a copy
        cleanup_memory()
    
    # Apply label smoothing to training data
    label_smoothing = 0.1
    y_train_smooth = y_train_dense * (1 - label_smoothing) + label_smoothing / y_train_dense.shape[1]
    y_val_smooth = y_val_dense * (1 - label_smoothing) + label_smoothing / y_val_dense.shape[1]
    print(f"      Applied label smoothing (value={label_smoothing})")
    
    # Extract feature splits
    X_train_split = X_train[train_indices]
    X_val_split = X_train[val_indices]
    
    # Free intermediate dense arrays
    del y_train_dense, y_val_dense
    
    print(f"      Train samples: {len(train_indices):,}")
    print(f"      Validation samples: {len(val_indices):,}")
    print(f"      Features: {default_params['input_dim']}")
    print(f"      Terms: {default_params['output_dim']}")
    
    # GPU setup strategy: Aggressively maximize GPU utilization
    # For large embedding models, push batch sizes and use mixed precision
    from utils.gpu_utils import get_gpu_count, get_gpu_memory_gb, check_gpu_available
    num_gpus = get_gpu_count()
    print(f"      Detected {num_gpus} GPU(s)")
    
    use_dataparallel = default_params.get('use_dataparallel', False)
    use_mixed_precision = default_params.get('use_mixed_precision', True)  # Enable by default for speed
    
    # Get optimized batch size from centralized config
    if check_gpu_available():
        gpu_memory_gb = get_gpu_memory_gb()
        print(f"      GPU memory: {gpu_memory_gb:.1f}GB")
        
        # Use centralized config function (returns direct batch size for GPU tier)
        base_batch_size = get_optimized_batch_size(gpu_memory_gb)
        
        # For large ontologies, reduce batch size to avoid OOM
        # P ontology: 16,781 labels * 16,384 batch = ~1.1GB labels alone
        # Need to be very conservative for large label spaces
        n_labels = default_params['output_dim']
        n_features = default_params['input_dim']
        
        # Memory per sample: (features + labels) * 4 bytes (float32)
        # Model overhead: activations, gradients, optimizer states (roughly 2-3x data)
        data_bytes_per_sample = (n_features + n_labels) * 4  # Just data
        overhead_multiplier = 3  # Conservative: 3x for model/gradients/optimizer
        total_bytes_per_sample = data_bytes_per_sample * overhead_multiplier
        
        # Very conservative: max 300MB per batch to leave plenty of room
        # For P: (2390 + 16781) * 4 * 3 = ~230KB per sample
        # 300MB / 230KB = ~1,300 samples max
        max_batch_mb = 300  # MB per batch
        max_samples_per_batch = int((max_batch_mb * 1024**2) / total_bytes_per_sample)
        
        # Round down to nearest power of 2 for efficiency (1024, 2048, 4096, etc.)
        if max_samples_per_batch > 0:
            # Find largest power of 2 <= max_samples_per_batch
            power_of_2 = 1 << (max_samples_per_batch.bit_length() - 1)
            if power_of_2 > max_samples_per_batch:
                power_of_2 = power_of_2 // 2
            safe_batch_size = max(512, power_of_2)  # Floor at 512
        else:
            safe_batch_size = 512  # Minimum safe batch size
        
        if safe_batch_size < base_batch_size:
            final_batch_size = safe_batch_size
            print(f"      ⚠️  Large ontology ({n_labels:,} labels) - reducing batch size: {base_batch_size:,} → {final_batch_size:,}")
            print(f"      💾 Estimated memory per batch: ~{final_batch_size * total_bytes_per_sample / (1024**2):.1f}MB")
        else:
            final_batch_size = base_batch_size
        
        print(f"      💡 Using batch size: {final_batch_size:,}")
    else:
        # No GPU - use base batch size from model config
        final_batch_size = default_params['batch_size']
    
    # Consider DataParallel for very large batches (>8192)
    if num_gpus > 1 and final_batch_size > 8192 and not use_dataparallel:
        print(f"      💡 Very large batch size ({final_batch_size}) - enabling DataParallel")
        use_dataparallel = True
    
    # Create data loaders with final batch size
    from utils.dataloader_utils import create_training_dataloader
    train_loader = create_training_dataloader(
        X=X_train_split,
        y=y_train_split,
        batch_size=final_batch_size,
        device=device,
        shuffle=True,
        use_multi_worker=False  # v1: simple mode
    )
    val_loader = create_training_dataloader(
        X=X_val_split,
        y=y_val_split,
        batch_size=final_batch_size,
        device=device,
        shuffle=False,
        use_multi_worker=False  # v1: simple mode
    )
    
    # Create model
    model = MLPModel(
        input_dim=default_params['input_dim'],
        output_dim=default_params['output_dim'],
        hidden_dims=default_params['hidden_dims'],
        dropout_rate=default_params['dropout_rate']
    ).to(device)
    
    if num_gpus > 1 and use_dataparallel:
        print(f"      🚀 Multiple GPUs detected ({num_gpus}) - enabling DataParallel")
        model = nn.DataParallel(model)
        print(f"      Model wrapped with DataParallel across {num_gpus} GPUs")
        print(f"      Effective batch size per GPU: {final_batch_size // num_gpus}")
        print(f"      Total effective batch size: {final_batch_size} (split across GPUs)")
    else:
        print(f"      Model placed on: {device}")
    
    # Always print final batch size (after all adjustments)
    print(f"      Final batch size: {final_batch_size:,}")
    
    # Loss function and optimizer
    # Use BCEWithLogitsLoss (combines sigmoid + BCE) for mixed precision compatibility
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), 
                          lr=default_params['learning_rate'],
                          weight_decay=default_params['weight_decay'])
    
    # Mixed precision training for 2x speedup on modern GPUs
    scaler = None
    if use_mixed_precision and check_gpu_available():
        try:
            from torch.cuda.amp import autocast, GradScaler
            scaler = GradScaler()
            print(f"      🚀 Mixed precision (FP16) enabled - expect 1.5-2x speedup")
        except ImportError:
            print(f"      ⚠️  Mixed precision not available (requires PyTorch 1.6+)")
            scaler = None
    
    # Learning rate scheduler
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='max', factor=0.5, patience=3, verbose=True
    )
    
    # Temperature scaling for inference
    temperature = 1.5

    # Initialize best model state (defensive: safe fallback if training fails)
    best_model_state = model.state_dict().copy()

    # Training loop
    best_f1 = 0.0
    patience_counter = 0
    train_metrics_history = []
    val_metrics_history = []
    
    print(f"      Starting training for {default_params['epochs']} epochs...")
    start_time = time.time()
    
    # Use streaming metrics for large ontologies (>10k labels) to avoid OOM
    # Streaming metrics use ~1000x less memory (only store TP/FP/FN per sample, not all predictions)
    use_streaming = default_params['output_dim'] > LARGE_ONTOLOGY_LABEL_THRESHOLD
    if use_streaming:
        print(f"      💾 Large ontology detected ({default_params['output_dim']:,} labels) - using memory-efficient metrics")
    
    for epoch in range(default_params['epochs']):
        # Train
        train_metrics = train_epoch(model, train_loader, optimizer, criterion, device, 
                                  scaler=scaler, use_streaming_metrics=use_streaming)
        train_metrics_history.append(train_metrics)
        
        # Validate
        val_metrics = validate_epoch(model, val_loader, criterion, device, 
                                   use_streaming_metrics=use_streaming)
        val_metrics_history.append(val_metrics)
        
        # Learning rate scheduling
        scheduler.step(val_metrics['f1_score'])
        
        # Early stopping
        if val_metrics['f1_score'] > best_f1:
            best_f1 = val_metrics['f1_score']
            patience_counter = 0
            # Save best model state
            best_model_state = model.state_dict().copy()
        else:
            patience_counter += 1
        
        # Print progress
        log_epoch_progress(epoch, default_params['epochs'], train_metrics, val_metrics)
        
        # Early stopping
        if patience_counter >= default_params['patience']:
            print(f"         Early stopping at epoch {epoch+1}")
            break
    
    # Load best model
    model.load_state_dict(best_model_state)
    
    training_time = time.time() - start_time
    print(f"      ✓ {ont_name} MLP training completed in {training_time:.1f}s")
    print(f"      ✓ Best validation F1: {best_f1:.4f}")
    
    # Clean up GPU memory using centralized utility
    del train_loader, val_loader
    from utils.gpu_utils import cleanup_gpu_memory
    cleanup_gpu_memory()
    
    return model


def train_all_ontologies_mlp(X_train: np.ndarray, y_train_dict: Dict[str, np.ndarray], 
                           ontologies: Dict[str, str], **hyperparams) -> Dict[str, MLPModel]:
    """
    Train MLP models for all ontologies.
    
    Args:
        X_train: Feature matrix
        y_train_dict: dict mapping ont_code -> label matrix
        ontologies: dict mapping ont_code -> ont_name
        **hyperparams: Model hyperparameters
        
    Returns:
        dict: ont_code -> trained model
    """
    print("\n[6/9] Training MLP models...")
    
    models = {}
    
    for ont_code, ont_name in ontologies.items():
        if ont_code not in y_train_dict:
            print(f"   ⚠️  Skipping {ont_name} (no data)")
            continue
            
        y_ont = y_train_dict[ont_code]
        model = train_ontology_model_mlp(X_train, y_ont, ont_code, ont_name, **hyperparams)
        
        if model is not None:
            models[ont_code] = model
    
    print(f"   ✓ Trained {len(models)} MLP models")
    return models


# Prediction logic has been moved to utils/model_prediction.py for DRY/SOLID compliance
# Use predict_with_model() from utils.model_prediction instead
