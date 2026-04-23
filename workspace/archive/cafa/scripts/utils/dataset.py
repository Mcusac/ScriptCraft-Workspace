"""
GPU-optimized PyTorch Dataset for memory-efficient training.
Uses memory-mapped arrays and sparse label matrices to avoid loading full datasets into RAM.

DEPRECATION WARNING (2025-11-17):
This module contains complex Dataset classes that were workarounds for dense label conversion.
These are no longer needed with proper sparse tensor architecture (see models/nn/mlp_trainer_v3.py).

The SparseDataset in mlp_trainer_v3.py is simpler and more efficient.
This module is kept for backward compatibility with older model trainers (v1/v2).
"""

import warnings

warnings.warn(
    "dataset.py MemmapDataset and SparseLabelDataset are deprecated. "
    "Use SparseDataset from mlp_trainer_v3.py instead. "
    "This module will be removed in a future version.",
    DeprecationWarning,
    stacklevel=2
)

import numpy as np
import torch
from torch.utils.data import Dataset
from typing import Union, Optional, Tuple
from scipy.sparse import csr_matrix, csc_matrix, spmatrix
from pathlib import Path

from config.training import FLOAT32_BYTES


class MemmapDataset(Dataset):
    """
    PyTorch Dataset that reads features from memory-mapped arrays and labels from sparse matrices.
    Optimized for GPU training with non-blocking transfers and efficient memory usage.
    
    Features:
    - Reads features from memmap (on-disk, no RAM loading)
    - Keeps labels sparse, converts to dense only per-batch
    - Supports indexing without loading full arrays
    - Optimized for GPU: uses pin_memory, non_blocking transfers
    - Optional label smoothing applied per-sample
    """
    
    def __init__(self, 
                 X: Union[np.ndarray, np.memmap, str, Path],
                 y: Union[np.ndarray, spmatrix],
                 indices: Optional[np.ndarray] = None,
                 label_smoothing: float = 0.0):
        """
        Initialize MemmapDataset.
        
        Args:
            X: Feature matrix (numpy array, memmap, or path to memmap file)
            y: Label matrix (numpy array or sparse matrix)
            indices: Optional indices to subset the dataset (for train/val splits)
            label_smoothing: Label smoothing factor (0.0 = no smoothing)
        """
        # Keep path as-is to avoid loading into memory
        # Only load memmap when actually accessing data in __getitem__
        if isinstance(X, (str, Path)):
            self.X_path = Path(X)
            self.X = None  # Will be loaded on-demand
        else:
            self.X_path = None
            self.X = X
        
        self.y = y
        self.indices = indices if indices is not None else np.arange(len(X) if self.X is not None else self._get_length_from_path())
        self.label_smoothing = label_smoothing
        
        # Check if labels are sparse
        self.y_is_sparse = hasattr(y, 'toarray')
        
        # Store shape info
        if self.y_is_sparse:
            self.n_samples, self.n_labels = y.shape
        else:
            self.n_samples, self.n_labels = y.shape
    
    def _get_length_from_path(self) -> int:
        """Get dataset length from memmap metadata file."""
        if self.X_path is None:
            raise ValueError("Cannot get length - no path or array provided")
        metadata_path = self.X_path.with_suffix('.npy.meta')
        if metadata_path.exists():
            import json
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            return metadata['shape'][0]
        else:
            # Fallback: load memmap to get shape (one-time cost)
            from utils.memory_efficient import load_features_memmap
            X_temp = load_features_memmap(self.X_path)
            length = X_temp.shape[0]
            del X_temp
            return length
    
    def __len__(self) -> int:
        """Return dataset size."""
        return len(self.indices)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Get a single sample from the dataset.
        Optimized for memory efficiency with explicit cleanup.
        
        Args:
            idx: Index into the dataset (after applying indices mapping)
            
        Returns:
            tuple: (features, labels) as torch tensors
        """
        # Map index through indices array
        actual_idx = self.indices[idx]
        
        # Load memmap on-demand if using path (lazy loading)
        if self.X_path is not None:
            if self.X is None:
                # Load memmap once (will be reused for subsequent accesses)
                from utils.memory_efficient import load_features_memmap
                self.X = load_features_memmap(self.X_path)
        
        # Get features from memmap (creates small array in memory)
        features = np.array(self.X[actual_idx], dtype=np.float32)
        
        # Get labels - convert sparse to dense if needed
        label_row = self._extract_label_row(actual_idx)
        
        # Apply label smoothing if enabled
        if self.label_smoothing > 0.0:
            label_row = label_row * (1 - self.label_smoothing) + self.label_smoothing / self.n_labels
        
        # Convert to tensors (will be moved to GPU with non_blocking=True in DataLoader)
        features_tensor = torch.from_numpy(features)
        labels_tensor = torch.from_numpy(label_row)
        
        # Explicit cleanup of intermediate numpy arrays to free memory immediately
        # This is critical when using multiple DataLoader workers
        del features, label_row
        
        return features_tensor, labels_tensor
    
    def _extract_label_row(self, idx: int) -> np.ndarray:
        """
        Extract a single label row, handling both sparse and dense formats.
        Optimized for memory efficiency: pre-allocates arrays and uses efficient CSR slicing.
        
        Args:
            idx: Index of the row to extract
            
        Returns:
            np.ndarray: Label row as float32 array
        """
        if self.y_is_sparse:
            # Extract single row from sparse matrix efficiently
            if isinstance(self.y, csr_matrix):
                # CSR: Most efficient - pre-allocate and fill sparse values directly
                # This avoids creating intermediate dense arrays
                label_row = np.zeros(self.n_labels, dtype=np.float32)
                start = self.y.indptr[idx]
                end = self.y.indptr[idx + 1]
                if end > start:
                    # Fill only the non-zero values
                    label_row[self.y.indices[start:end]] = self.y.data[start:end].astype(np.float32)
            elif isinstance(self.y, csc_matrix):
                # CSC: Less efficient for row access, but still better than full toarray()
                # Use getrow() which is optimized for CSC row extraction
                label_row = self.y.getrow(idx).toarray()[0].astype(np.float32)
            else:
                # Generic sparse: use getrow() which is more efficient than indexing
                label_row = self.y.getrow(idx).toarray()[0].astype(np.float32)
        else:
            # Dense array - create view if possible, otherwise copy
            label_row = np.array(self.y[idx], dtype=np.float32)
        return label_row


class SparseLabelDataset(Dataset):
    """
    PyTorch Dataset optimized for sparse label matrices.
    Converts sparse labels to dense only per-batch during DataLoader iteration.
    
    This is a more memory-efficient alternative when labels are very sparse.
    """
    
    def __init__(self,
                 X: Union[np.ndarray, np.memmap],
                 y: spmatrix,
                 indices: Optional[np.ndarray] = None):
        """
        Initialize SparseLabelDataset.
        
        Args:
            X: Feature matrix (numpy array or memmap)
            y: Sparse label matrix (scipy sparse matrix)
            indices: Optional indices to subset the dataset
        """
        self.X = X
        self.y = y  # Keep sparse
        self.indices = indices if indices is not None else np.arange(len(X))
        
        if not hasattr(y, 'toarray'):
            raise ValueError("y must be a sparse matrix for SparseLabelDataset")
    
    def __len__(self) -> int:
        """Return dataset size."""
        return len(self.indices)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Get a single sample from the dataset.
        
        Args:
            idx: Index into the dataset
            
        Returns:
            tuple: (features, labels) as torch tensors
        """
        actual_idx = self.indices[idx]
        
        # Get features
        features = np.array(self.X[actual_idx], dtype=np.float32)
        
        # Extract single row from sparse matrix using optimized method
        if isinstance(self.y, csr_matrix):
            # CSR: Most efficient - pre-allocate and fill sparse values directly
            label_row = np.zeros(self.y.shape[1], dtype=np.float32)
            start = self.y.indptr[actual_idx]
            end = self.y.indptr[actual_idx + 1]
            if end > start:
                label_row[self.y.indices[start:end]] = self.y.data[start:end].astype(np.float32)
        else:
            # Other sparse formats: use getrow() which is more efficient
            label_row = self.y.getrow(actual_idx).toarray()[0].astype(np.float32)
        
        # Convert to tensors
        features_tensor = torch.from_numpy(features)
        labels_tensor = torch.from_numpy(label_row)
        
        # Explicit cleanup of intermediate numpy arrays
        del features, label_row
        
        return features_tensor, labels_tensor

