"""
DataLoader creation utilities for CAFA 6 protein function prediction.
Consolidates DataLoader creation logic from MLP v1 and v2 trainers.
"""

import numpy as np
import torch
from torch.utils.data import DataLoader, TensorDataset
from typing import Union, Optional
import os
from pathlib import Path
from scipy.sparse import spmatrix

from config.features import get_batch_size
from config.training import (
    DATALOADER_PRELOAD_THRESHOLD_MB,
    DATALOADER_PRELOAD_MAX_MB,
    DATALOADER_GPU_MEMORY_FRACTION,
    DATALOADER_MAX_WORKERS,
    DATALOADER_PREFETCH_FACTOR,
    DATALOADER_PREFETCH_FACTOR_LARGE_LABELS,
    DATALOADER_MULTIPROCESSING_TIMEOUT,
    DATALOADER_TEST_WORKERS,
    DATALOADER_LARGE_DATASET_THRESHOLD_MB,
    DATALOADER_MEMORY_AWARE_WORKERS,
    DATALOADER_MAX_MEMORY_PER_WORKER_MB,
    DATALOADER_LARGE_LABEL_SPACE_THRESHOLD,
    DATALOADER_MAX_WORKERS_LARGE_LABELS,
    DATALOADER_MAX_WORKERS_VERY_LARGE_LABELS,
    DATALOADER_VERY_LARGE_LABEL_SPACE_THRESHOLD,
    DATALOADER_DISABLE_PERSISTENT_FOR_LARGE_LABELS,
    FLOAT32_BYTES,
    MB_TO_BYTES
)
from utils.memory_efficient import MEMMAP_THRESHOLD_MB, estimate_memory_usage, should_use_memmap
from utils.utils_common import (
    is_kaggle_environment,
    device_to_string,
    test_multiprocessing_available,
    calculate_memory_size_mb
)


def create_training_dataloader(X: np.ndarray, 
                              y: np.ndarray, 
                              batch_size: Optional[int] = None,
                              device: Union[str, torch.device] = 'cpu',
                              shuffle: bool = True,
                              use_multi_worker: bool = False) -> DataLoader:
    """
    Create PyTorch DataLoader for training with optimized GPU utilization.
    
    Consolidates logic from MLP v1 and v2 trainers:
    - GPU pre-loading for small datasets to eliminate CPU→GPU transfer overhead
    - Optional multi-worker support (v2 feature) to utilize all CPU cores
    - Pin memory and non-blocking transfers for efficient batch loading
    
    Args:
        X: Feature matrix (n_samples, n_features)
        y: Label matrix (n_samples, n_labels)
        batch_size: Batch size for training (uses config default if None)
        device: Device to place tensors on (string or torch.device)
        shuffle: Whether to shuffle data
        use_multi_worker: If True, enable multi-worker data loading (v2 feature)
        
    Returns:
        DataLoader for training
    """
    # Use centralized config if batch_size not provided
    if batch_size is None:
        batch_size = get_batch_size("nn_training")
    
    # Handle device as string or torch.device object
    device_str = device_to_string(device)
    
    # Estimate total memory needed
    X_size_mb = calculate_memory_size_mb(X.shape, dtype_bytes=FLOAT32_BYTES)
    y_size_mb = calculate_memory_size_mb(y.shape, dtype_bytes=FLOAT32_BYTES)
    total_data_mb = X_size_mb + y_size_mb
    
    # Determine preload threshold based on GPU memory
    # v1: Fixed threshold (conservative)
    # v2: 50% of GPU memory or max threshold (more aggressive)
    from utils.gpu_utils import check_gpu_available, get_gpu_memory_gb
    if device_str == 'cuda' and check_gpu_available():
        if use_multi_worker:
            # v2 strategy: Use fraction of GPU memory or max threshold
            total_gpu_memory_gb = get_gpu_memory_gb()
            preload_threshold_mb = min(
                DATALOADER_PRELOAD_MAX_MB,
                total_gpu_memory_gb * 1024 * DATALOADER_GPU_MEMORY_FRACTION
            )
        else:
            # v1 strategy: Fixed threshold
            preload_threshold_mb = DATALOADER_PRELOAD_THRESHOLD_MB
    else:
        preload_threshold_mb = DATALOADER_PRELOAD_THRESHOLD_MB  # For CPU
    
    # Strategy 1: GPU Pre-loading for datasets that fit in GPU memory
    if device_str == 'cuda' and check_gpu_available() and total_data_mb < preload_threshold_mb:
        # Small dataset - pre-load to GPU for maximum speed
        X_tensor = torch.FloatTensor(X).to(device)
        y_tensor = torch.FloatTensor(y).to(device)
        print(f"      💡 Pre-loading dataset to GPU: X={X.shape} ({X_size_mb:.1f}MB), y={y.shape} ({y_size_mb:.1f}MB)")
        
        dataset = TensorDataset(X_tensor, y_tensor)
        pin_memory = False  # Not needed, already on GPU
        num_workers = 0  # No need for workers when data is on GPU
    else:
        # Strategy 2: Optimized DataLoader with optional multi-worker support
        # Large dataset or CPU training - use standard DataLoader with optimizations
        X_tensor = torch.FloatTensor(X)
        y_tensor = torch.FloatTensor(y)
        
        if device_str == 'cuda' and total_data_mb >= DATALOADER_LARGE_DATASET_THRESHOLD_MB:
            print(f"      💡 Large dataset ({total_data_mb:.1f}MB) - using optimized DataLoader with batch transfers")
        else:
            print(f"      Using CPU tensors (device={device_str})")
        
        dataset = TensorDataset(X_tensor, y_tensor)
        pin_memory = (device_str == 'cuda')  # Pin memory for fast CPU→GPU transfer
        
        # Multi-worker support: Enable for large datasets IF requested
        # For very large label spaces, caller may explicitly disable workers to prevent OOM
        cpu_count = os.cpu_count() or 4
        num_workers = 0
        
        # Enable multi-worker for large datasets ONLY if explicitly requested
        # This allows callers to disable workers for very large label spaces (prevents memory multiplication)
        if use_multi_worker:
            if total_data_mb >= DATALOADER_LARGE_DATASET_THRESHOLD_MB:
                # Large dataset - use multi-worker to maximize CPU utilization
                num_workers = min(DATALOADER_MAX_WORKERS, cpu_count)
            else:
                # Smaller dataset - use multi-worker if requested
                num_workers = min(DATALOADER_MAX_WORKERS, cpu_count)
        
        # Test multiprocessing on Kaggle if needed
        if num_workers > 0:
            if is_kaggle_environment():
                if test_multiprocessing_available(timeout=DATALOADER_MULTIPROCESSING_TIMEOUT):
                    print(f"      🚀 Multi-worker enabled: {num_workers} workers to utilize all CPU cores")
                else:
                    num_workers = 0
                    print(f"      ⚠️  Multi-worker test failed - using single worker")
            else:
                # Non-Kaggle environment
                print(f"      🚀 Multi-worker enabled: {num_workers} workers to utilize all CPU cores")
    
    # Create DataLoader with optimized settings
    dataloader = DataLoader(
        dataset, 
        batch_size=batch_size, 
        shuffle=shuffle, 
        pin_memory=pin_memory,
        num_workers=num_workers,
        persistent_workers=True if num_workers > 0 else False,
        prefetch_factor=DATALOADER_PREFETCH_FACTOR if num_workers > 0 else None,
        drop_last=False
    )
    
    # Log final configuration
    if num_workers > 0:
        print(f"      ✓ Multi-worker enabled: {num_workers} workers, prefetch_factor={DATALOADER_PREFETCH_FACTOR}, persistent_workers=True")
    else:
        print(f"      ✓ Single-worker mode (num_workers=0)")
    
    return dataloader


def create_streaming_dataloader(X: Union[np.ndarray, np.memmap, str, Path],
                               y: Union[np.ndarray, spmatrix],
                               batch_size: Optional[int] = None,
                               device: Union[str, torch.device] = 'cpu',
                               shuffle: bool = True,
                               indices: Optional[np.ndarray] = None,
                               label_smoothing: float = 0.0) -> DataLoader:
    """
    Create streaming DataLoader using memory-mapped arrays and sparse labels.
    Optimized for large datasets that don't fit in RAM.
    
    Features:
    - Uses MemmapDataset for on-disk feature access
    - Keeps labels sparse, converts to dense per-batch
    - Memory-aware worker count and prefetch factor
    - Optimized prefetch and pin_memory for GPU training
    
    Args:
        X: Feature matrix (numpy array, memmap, or path to memmap file)
        y: Label matrix (numpy array or sparse matrix)
        batch_size: Batch size for training (uses config default if None)
        device: Device to place tensors on
        shuffle: Whether to shuffle data
        indices: Optional indices to subset the dataset (for train/val splits)
        
    Returns:
        DataLoader optimized for streaming
    """
    from utils.dataset import MemmapDataset
    
    # Use centralized config if batch_size not provided
    if batch_size is None:
        batch_size = get_batch_size("nn_training")
    
    # Handle device as string or torch.device object
    device_str = device_to_string(device)
    
    # Create streaming dataset
    dataset = MemmapDataset(X, y, indices=indices, label_smoothing=label_smoothing)
    
    # Determine label space size for memory-aware optimizations
    if hasattr(y, 'shape'):
        n_labels = y.shape[1] if len(y.shape) > 1 else 1
    else:
        n_labels = 1
    
    # Calculate optimal prefetch factor based on label space size
    # Large label spaces (>10K) use reduced prefetch to prevent memory accumulation
    if n_labels > DATALOADER_LARGE_LABEL_SPACE_THRESHOLD:
        prefetch_factor = DATALOADER_PREFETCH_FACTOR_LARGE_LABELS
        print(f"      💾 Large label space detected ({n_labels:,} labels) - using reduced prefetch_factor={prefetch_factor}")
    else:
        prefetch_factor = DATALOADER_PREFETCH_FACTOR
    
    # Calculate optimal worker count with memory awareness
    cpu_count = os.cpu_count() or 4
    
    # For very large label spaces (>15K), use 0 workers to prevent OOM
    # Each worker copies the entire dataset (sparse matrix + indices + overhead)
    # With 0 workers, only 1 copy exists (main process)
    if n_labels > DATALOADER_VERY_LARGE_LABEL_SPACE_THRESHOLD:
        # Very large label space: use 0 workers (single-threaded)
        num_workers = DATALOADER_MAX_WORKERS_VERY_LARGE_LABELS
        print(f"      ⚠️  Very large label space ({n_labels:,} labels) - using {num_workers} workers (single-threaded) to prevent OOM")
    elif n_labels > DATALOADER_LARGE_LABEL_SPACE_THRESHOLD:
        # Large label space: use reduced worker limit
        num_workers = min(DATALOADER_MAX_WORKERS_LARGE_LABELS, cpu_count)
        print(f"      💾 Large label space ({n_labels:,} labels) - limiting to {num_workers} workers to reduce memory footprint")
    else:
        # Normal label space: use standard worker limit
        num_workers = min(DATALOADER_MAX_WORKERS, cpu_count)
    
    # Memory-aware worker reduction: estimate memory per worker and reduce if needed
    if DATALOADER_MEMORY_AWARE_WORKERS and num_workers > 0:
        # Estimate memory per worker: sparse matrix size + batch accumulation
        # Sparse matrix: approximate size (indices + data)
        if hasattr(y, 'data') and hasattr(y, 'indices'):
            # Rough estimate: data + indices + indptr arrays
            sparse_memory_mb = (y.data.nbytes + y.indices.nbytes + y.indptr.nbytes) / MB_TO_BYTES
        else:
            # Dense estimate
            sparse_memory_mb = calculate_memory_size_mb(y.shape, dtype_bytes=FLOAT32_BYTES) if hasattr(y, 'shape') else 0
        
        # Batch accumulation: prefetch_factor * batch_size * label_size
        batch_memory_mb = (prefetch_factor * batch_size * n_labels * FLOAT32_BYTES) / MB_TO_BYTES
        
        # Total estimated memory per worker
        memory_per_worker_mb = sparse_memory_mb + batch_memory_mb
        
        if memory_per_worker_mb > DATALOADER_MAX_MEMORY_PER_WORKER_MB:
            # Reduce workers to stay within memory limits
            optimal_workers = max(1, int(DATALOADER_MAX_MEMORY_PER_WORKER_MB / (memory_per_worker_mb / num_workers)))
            if optimal_workers < num_workers:
                print(f"      ⚠️  Memory-aware reduction: {num_workers} → {optimal_workers} workers (estimated {memory_per_worker_mb:.1f}MB/worker)")
                num_workers = optimal_workers
    
    # Test multiprocessing on Kaggle if needed
    if num_workers > 0:
        if is_kaggle_environment():
            if not test_multiprocessing_available(timeout=DATALOADER_MULTIPROCESSING_TIMEOUT):
                # Multiprocessing failed - fall back to single worker
                num_workers = 0
                print(f"      ⚠️  Multi-worker test failed - using single worker")
        else:
            # Non-Kaggle environment - verify we're using all available cores
            if num_workers < cpu_count:
                print(f"      💡 Using {num_workers} workers (available: {cpu_count} cores)")
            else:
                print(f"      🚀 Using all {num_workers} CPU cores for data loading")
    
    # Pin memory for fast CPU→GPU transfer
    pin_memory = (device_str == 'cuda')
    
    # For large label spaces, disable persistent_workers to free memory between epochs
    # Persistent workers keep dataset in memory, which multiplies memory usage
    use_persistent_workers = True if num_workers > 0 else False
    if DATALOADER_DISABLE_PERSISTENT_FOR_LARGE_LABELS and n_labels > DATALOADER_LARGE_LABEL_SPACE_THRESHOLD:
        use_persistent_workers = False
        print(f"      💾 Disabling persistent_workers for large label space to free memory between epochs")
    
    # Estimate total memory before creating DataLoader
    # Each worker copies the entire dataset object (sparse matrix + indices + overhead)
    # The actual memory is higher than just sparse arrays due to Python object overhead
    if hasattr(y, 'data') and hasattr(y, 'indices'):
        # Sparse matrix arrays
        sparse_arrays_mb = (y.data.nbytes + y.indices.nbytes + y.indptr.nbytes) / MB_TO_BYTES
        
        # Indices array (train_indices or val_indices) - can be large
        indices_mb = 0
        if indices is not None:
            indices_mb = (indices.nbytes) / MB_TO_BYTES
        
        # Python object overhead estimate (sparse matrix object + dataset object)
        # Rough estimate: 10-20% overhead for Python objects
        object_overhead_mb = sparse_arrays_mb * 0.15
        
        # Total per process
        memory_per_process_mb = sparse_arrays_mb + indices_mb + object_overhead_mb
        
        # Total with workers (each worker gets a copy)
        total_estimated_mb = memory_per_process_mb * (num_workers + 1)  # +1 for main process
        
        print(f"      💾 Estimated memory: {total_estimated_mb:.1f}MB ({memory_per_process_mb:.1f}MB/process × {num_workers + 1} processes)")
        print(f"         - Sparse arrays: {sparse_arrays_mb:.1f}MB, Indices: {indices_mb:.1f}MB, Overhead: {object_overhead_mb:.1f}MB")
        
        # If estimated memory exceeds 20GB, force 0 workers
        if total_estimated_mb > 20000 and num_workers > 0:
            num_workers = 0
            print(f"      ⚠️  High memory estimate ({total_estimated_mb:.1f}MB) - forcing {num_workers} workers (single-threaded) to prevent OOM")
    
    # Create DataLoader with optimized settings for GPU training
    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        pin_memory=pin_memory,
        num_workers=num_workers,
        persistent_workers=use_persistent_workers,
        prefetch_factor=prefetch_factor if num_workers > 0 else None,
        drop_last=False
    )
    
    # Log configuration
    if num_workers > 0:
        persistent_str = "True" if use_persistent_workers else "False"
        print(f"      🚀 Streaming DataLoader: {num_workers} workers, prefetch_factor={prefetch_factor}, persistent_workers={persistent_str}")
    else:
        print(f"      ✓ Streaming DataLoader: single-worker mode")
    
    return dataloader

