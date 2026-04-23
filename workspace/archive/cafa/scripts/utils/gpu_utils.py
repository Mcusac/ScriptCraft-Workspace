"""
GPU detection and device management utilities for CAFA 6 protein function prediction.
Centralized GPU detection logic to eliminate duplication across the codebase.
"""

from typing import Tuple, Optional
import os

from config.training import GB_TO_BYTES, GPU_CHECK_TIMEOUT


def get_gpu_info() -> Tuple[bool, int, float]:
    """
    Get comprehensive GPU information.
    
    Returns:
        tuple: (available: bool, count: int, memory_gb: float)
            - available: Whether GPU is available
            - count: Number of GPUs available
            - memory_gb: Total memory of first GPU in GB (0.0 if no GPU)
    """
    gpu_available = False
    num_gpus = 0
    memory_gb = 0.0
    
    # Try PyTorch first (most reliable)
    try:
        import torch
        gpu_available = torch.cuda.is_available()
        if gpu_available:
            num_gpus = torch.cuda.device_count()
            if num_gpus > 0:
                memory_gb = torch.cuda.get_device_properties(0).total_memory / GB_TO_BYTES
    except ImportError:
        # PyTorch not available, try nvidia-smi fallback
        pass
    except Exception:
        # PyTorch available but CUDA check failed
        pass
    
    # Fallback: nvidia-smi check if PyTorch didn't work
    if not gpu_available:
        try:
            import subprocess
            result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=GPU_CHECK_TIMEOUT)
            gpu_available = result.returncode == 0
            num_gpus = 1 if gpu_available else 0
            # Can't get memory from nvidia-smi easily, leave as 0.0
        except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
            pass
    
    return gpu_available, num_gpus, memory_gb


def check_gpu_available() -> bool:
    """
    Simple check for GPU availability.
    
    Returns:
        bool: True if GPU is available, False otherwise
    """
    available, _, _ = get_gpu_info()
    return available


def get_device(device: Optional[str] = None) -> 'torch.device':
    """
    Get PyTorch device object, defaulting to CUDA if available.
    
    Args:
        device: Optional device string ('cuda', 'cpu', or None for auto-detect)
        
    Returns:
        torch.device: PyTorch device object
    """
    try:
        import torch
    except ImportError:
        raise ImportError("PyTorch is required for get_device()")
    
    if device is None:
        # Auto-detect: use CUDA if available, otherwise CPU
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    return torch.device(device)


def get_gpu_count() -> int:
    """
    Get number of available GPUs.
    
    Returns:
        int: Number of GPUs (0 if none available)
    """
    _, count, _ = get_gpu_info()
    return count


def get_gpu_memory_gb() -> float:
    """
    Get GPU memory in GB for first GPU.
    
    Returns:
        float: Memory in GB (0.0 if no GPU or can't determine)
    """
    _, _, memory_gb = get_gpu_info()
    return memory_gb


def cleanup_gpu_memory():
    """
    Clean up GPU memory after training or inference.
    Essential for sequential training of multiple models on limited GPU memory.
    Also cleans up any pre-loaded data tensors.
    
    This function centralizes GPU cleanup logic that was previously duplicated
    across mlp_trainer_v1.py, mlp_trainer_v3.py, and mlp_trainer_v4.py.
    """
    from utils.utils_common import cleanup_memory
    
    try:
        import torch
        
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
            # Use centralized memory cleanup
            cleanup_memory()
            torch.cuda.empty_cache()  # Clear again after GC
        else:
            # No GPU, just do CPU cleanup
            cleanup_memory()
    except ImportError:
        # PyTorch not available, just do regular GC
        cleanup_memory()
    except Exception:
        # GPU cleanup failed, still try regular GC
        cleanup_memory()


def prepare_model_for_inference(model, device='cuda', batch_size=None, force_cpu=False):
    """
    Prepare PyTorch model for inference with optimal GPU configuration.
    
    Handles:
    - DataParallel wrapping for multi-GPU inference
    - Device placement
    - Model evaluation mode
    - Logging
    
    Single source of truth for GPU inference setup across all model versions.
    
    Args:
        model: PyTorch model (may already be wrapped in DataParallel)
        device: Target device ('cuda', 'cpu', or torch.device)
        batch_size: Optional batch size for logging
        force_cpu: If True, force CPU execution (ignore GPU availability)
    
    Returns:
        tuple: (prepared_model, device)
            - prepared_model: Model ready for inference (potentially DataParallel-wrapped)
            - device: Final device (torch.device object)
    
    Example:
        >>> model, device = prepare_model_for_inference(model, device='cuda', batch_size=1024)
        >>> predictions = predict_with_prepared_model(model, X_test, device)
    """
    import torch
    import torch.nn as nn
    
    # Set to eval mode
    model.eval()
    
    # Force CPU if requested
    if force_cpu:
        return model.to('cpu'), torch.device('cpu')
    
    # Normalize device to torch.device object
    if isinstance(device, str):
        device = torch.device(device)
    
    # Check if already wrapped in DataParallel
    if hasattr(model, 'module'):
        # Already wrapped - just move to device
        return model.to(device), device
    
    # Multi-GPU inference support
    if device.type == 'cuda' and torch.cuda.is_available():
        num_gpus = get_gpu_count()
        if num_gpus > 1:
            # Wrap in DataParallel for multi-GPU inference
            model = nn.DataParallel(model)
            if batch_size:
                print(f"   🚀 Multi-GPU inference: {num_gpus} GPUs, batch_size={batch_size}")
    
    # Move to device
    model = model.to(device)
    
    return model, device

