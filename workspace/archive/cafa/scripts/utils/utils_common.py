"""
Common utility functions shared across utils package.
Consolidates duplicate patterns to improve DRY compliance.
"""

import os
from typing import Union
from pathlib import Path

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


def is_kaggle_environment() -> bool:
    """
    Check if running in Kaggle environment.
    
    Returns:
        bool: True if running in Kaggle, False otherwise
    """
    return os.path.exists('/kaggle/input')


def device_to_string(device: Union[str, 'torch.device']) -> str:
    """
    Convert device to string representation.
    Handles both string and torch.device objects.
    
    Args:
        device: Device string or torch.device object
        
    Returns:
        str: Device string ('cuda' or 'cpu')
    """
    if hasattr(device, 'type'):
        return device.type
    return str(device)


def resolve_path(path: Union[str, Path]) -> Path:
    """
    Resolve a path to an absolute Path object.
    
    Args:
        path: Path string or Path object
        
    Returns:
        Path: Resolved absolute Path
    """
    path_obj = Path(path) if not isinstance(path, Path) else path
    return path_obj.resolve()


def calculate_memory_size_mb(shape: tuple, dtype_bytes: int = 4) -> float:
    """
    Calculate memory size in MB for an array.
    
    Args:
        shape: Array shape tuple (n_samples, n_features)
        dtype_bytes: Bytes per element (default: 4 for float32)
        
    Returns:
        float: Memory size in MB
    """
    if len(shape) < 2:
        return 0.0
    total_elements = shape[0] * shape[1]
    return (total_elements * dtype_bytes) / (1024**2)


def test_multiprocessing_available(timeout: int = 1) -> bool:
    """
    Test if multiprocessing is available (e.g., on Kaggle).
    
    Args:
        timeout: Timeout in seconds for test
        
    Returns:
        bool: True if multiprocessing works, False otherwise
    """
    if not TORCH_AVAILABLE:
        return False
    
    try:
        from torch.utils.data import DataLoader, TensorDataset
        test_dataset = TensorDataset(torch.FloatTensor([[1.0]]), torch.FloatTensor([[1.0]]))
        test_loader = DataLoader(test_dataset, batch_size=1, num_workers=2, timeout=timeout)
        next(iter(test_loader))
        return True
    except Exception:
        return False


def cleanup_memory() -> None:
    """
    Clean up memory by forcing garbage collection.
    Centralized memory cleanup function used across all packages.
    
    Consolidates the common pattern of importing gc and calling gc.collect().
    Moved from prediction.utils to utils.utils_common for cross-package use.
    """
    import gc
    gc.collect()


def open_text_file(filepath: Union[str, Path], mode: str = 'r', **kwargs):
    """
    Open a text file with automatic encoding detection.
    Detects UTF-16 from BOM, otherwise tries UTF-8, then UTF-16 variants.
    
    Args:
        filepath: Path to file
        mode: File mode ('r', 'w', etc.)
        **kwargs: Additional arguments to pass to open()
        
    Returns:
        File handle opened with correct encoding
        
    Raises:
        UnicodeDecodeError: If file cannot be decoded with any supported encoding
    """
    filepath = Path(filepath) if not isinstance(filepath, Path) else filepath
    
    # For write modes, default to UTF-8
    if 'w' in mode or 'a' in mode:
        if 'encoding' not in kwargs:
            kwargs['encoding'] = 'utf-8'
        return open(filepath, mode, **kwargs)
    
    # For read modes, detect encoding from BOM first
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    # Check BOM to detect encoding
    detected_encoding = None
    try:
        with open(filepath, 'rb') as f:
            first_bytes = f.read(3)
            if first_bytes.startswith(b'\xff\xfe'):
                # UTF-16 LE BOM detected
                detected_encoding = 'utf-16-le'
            elif first_bytes.startswith(b'\xfe\xff'):
                # UTF-16 BE BOM detected
                detected_encoding = 'utf-16-be'
    except Exception:
        pass  # If we can't read BOM, try UTF-8
    
    # Try encodings in order: detected (if BOM found), then UTF-8, then UTF-16 variants
    encodings_to_try = ['utf-8', 'utf-16-le', 'utf-16-be']
    if detected_encoding and detected_encoding not in encodings_to_try:
        encodings_to_try.insert(0, detected_encoding)
    elif detected_encoding:
        # Move detected encoding to front
        encodings_to_try.remove(detected_encoding)
        encodings_to_try.insert(0, detected_encoding)
    
    # Try each encoding
    last_error = None
    for enc in encodings_to_try:
        try:
            kwargs['encoding'] = enc
            return open(filepath, mode, **kwargs)
        except UnicodeDecodeError as e:
            last_error = e
            continue
        except Exception:
            # If it's not a decode error, re-raise
            raise
    
    # If all encodings failed, raise the last error
    if last_error:
        raise last_error
    raise UnicodeDecodeError(
        'utf-8',
        b'',
        0,
        1,
        f"Could not decode file {filepath} with any supported encoding (utf-8, utf-16-le, utf-16-be)"
    )

