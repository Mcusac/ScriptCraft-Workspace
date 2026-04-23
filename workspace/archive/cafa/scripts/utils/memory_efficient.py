"""
Memory-efficient utilities for CAFA 6 protein function prediction.
Handles memory-mapped arrays for large datasets to prevent OOM errors.

DEPRECATION WARNING (2025-11-17):
This module contains memory workarounds that are no longer needed with proper
sparse tensor architecture (see models/nn/mlp_trainer_v3.py).

Use sparse labels throughout instead of converting to dense + using memmap.
This module is kept for backward compatibility with older model trainers (v1/v2).
"""

import warnings

warnings.warn(
    "memory_efficient.py is deprecated. Use sparse tensors instead (see mlp_trainer_v3.py). "
    "This module will be removed in a future version.",
    DeprecationWarning,
    stacklevel=2
)

import numpy as np
from pathlib import Path
from typing import Union, Tuple, Optional
import os

from config.training import FLOAT32_BYTES, MB_TO_BYTES, MEMMAP_THRESHOLD_MB
from utils.utils_common import calculate_memory_size_mb


def estimate_memory_usage(X: np.ndarray, y: Optional[np.ndarray] = None) -> Tuple[float, float]:
    """
    Estimate memory usage for feature and label arrays.
    
    Args:
        X: Feature matrix (n_samples, n_features)
        y: Optional label matrix (n_samples, n_labels)
        
    Returns:
        tuple: (X_size_mb, y_size_mb) - Memory usage in MB
    """
    X_size_mb = calculate_memory_size_mb(X.shape, dtype_bytes=FLOAT32_BYTES)
    
    y_size_mb = 0.0
    if y is not None:
        # Sparse or dense - estimate dense size
        y_size_mb = calculate_memory_size_mb(y.shape, dtype_bytes=FLOAT32_BYTES)
    
    return X_size_mb, y_size_mb


def should_use_memmap(X: np.ndarray, y: Optional[np.ndarray] = None, 
                      threshold_mb: float = MEMMAP_THRESHOLD_MB) -> bool:
    """
    Determine if dataset should use memory-mapped arrays.
    
    Args:
        X: Feature matrix
        y: Optional label matrix
        threshold_mb: Memory threshold in MB (default: 2GB)
        
    Returns:
        bool: True if memmap should be used
    """
    X_size_mb, y_size_mb = estimate_memory_usage(X, y)
    total_mb = X_size_mb + y_size_mb
    
    return total_mb >= threshold_mb


def save_features_memmap(X: np.ndarray, path: Union[str, Path], 
                         dtype: np.dtype = np.float32) -> Path:
    """
    Save feature matrix as memory-mapped array.
    
    Args:
        X: Feature matrix to save
        path: Path to save memmap file
        dtype: Data type for memmap (default: float32)
        
    Returns:
        Path: Path to saved memmap file
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Ensure correct dtype
    if X.dtype != dtype:
        X = X.astype(dtype)
    
    # Save as memmap
    memmap = np.memmap(path, dtype=dtype, mode='w+', shape=X.shape)
    memmap[:] = X[:]
    memmap.flush()
    
    X_size_mb = calculate_memory_size_mb(X.shape, dtype_bytes=FLOAT32_BYTES)
    print(f"   💾 Saved features as memmap: {path} ({X.shape}, {X_size_mb:.1f}MB)")
    
    return path


def load_features_memmap(path: Union[str, Path], 
                        dtype: np.dtype = np.float32,
                        mode: str = 'r') -> np.memmap:
    """
    Load feature matrix as read-only memory-mapped array.
    
    Args:
        path: Path to memmap file
        dtype: Data type for memmap (default: float32)
        mode: Access mode ('r' for read-only, 'r+' for read-write)
        
    Returns:
        np.memmap: Memory-mapped array
    """
    path = Path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"Memmap file not found: {path}")
    
    # Load shape from metadata file if available
    metadata_path = path.with_suffix('.npy.meta')
    if metadata_path.exists():
        import json
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        shape = tuple(metadata['shape'])
    else:
        # Try to infer shape from file size
        file_size = path.stat().st_size
        # This is a fallback - ideally we'd have metadata
        # For now, we'll need to pass shape separately or use a different approach
        raise ValueError(f"Memmap metadata not found at {metadata_path}. Cannot determine shape.")
    
    memmap = np.memmap(path, dtype=dtype, mode=mode, shape=shape)
    
    X_size_mb = calculate_memory_size_mb(shape, dtype_bytes=FLOAT32_BYTES)
    print(f"   📂 Loaded features from memmap: {path} ({shape}, {X_size_mb:.1f}MB)")
    
    return memmap


def save_features_memmap_with_metadata(X: np.ndarray, path: Union[str, Path],
                                       dtype: np.dtype = np.float32) -> Path:
    """
    Save feature matrix as memory-mapped array with metadata.
    
    Args:
        X: Feature matrix to save
        path: Path to save memmap file
        dtype: Data type for memmap (default: float32)
        
    Returns:
        Path: Path to saved memmap file
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Ensure correct dtype
    if X.dtype != dtype:
        X = X.astype(dtype)
    
    # Save as memmap
    memmap = np.memmap(path, dtype=dtype, mode='w+', shape=X.shape)
    memmap[:] = X[:]
    memmap.flush()
    
    # Save metadata
    metadata_path = path.with_suffix('.npy.meta')
    import json
    metadata = {
        'shape': list(X.shape),
        'dtype': str(dtype),
        'size_mb': calculate_memory_size_mb(X.shape, dtype_bytes=FLOAT32_BYTES)
    }
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f)
    
    X_size_mb = calculate_memory_size_mb(X.shape, dtype_bytes=FLOAT32_BYTES)
    print(f"   💾 Saved features as memmap: {path} ({X.shape}, {X_size_mb:.1f}MB)")
    
    return path

