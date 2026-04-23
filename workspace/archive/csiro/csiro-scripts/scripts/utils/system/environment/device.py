# device_utils.py
# Utilities for device detection and setup
# Memory management utilities are in memory_utils.py

import torch
import logging
import os
from typing import Optional

# Set PyTorch CUDA allocator config to reduce memory fragmentation
# This helps prevent OOM errors from fragmentation, especially during grid search
os.environ.setdefault('PYTORCH_CUDA_ALLOC_CONF', 'expandable_segments:True')

logger = logging.getLogger(__name__)


def get_device(prefer_device: Optional[str] = None) -> torch.device:
    """
    Get the best available device for training/inference.
    
    Args:
        prefer_device: Preferred device ('cuda', 'cpu', 'mps', 'tpu')
        
    Returns:
        torch.device object
    """
    # Check for CUDA (NVIDIA GPU)
    if torch.cuda.is_available():
        device = torch.device('cuda')
        gpu_name = torch.cuda.get_device_name(0)
        gpu_count = torch.cuda.device_count()
        logger.info(f"✅ CUDA available: {gpu_name} (x{gpu_count})")
        if gpu_count > 1:
            logger.info(f"   Multiple GPUs detected - consider using DataParallel")
        return device
    
    # Check for MPS (Apple Silicon)
    if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
        device = torch.device('mps')
        logger.info("✅ MPS (Apple Silicon) available")
        return device
    
    # Check for TPU (requires torch_xla)
    if os.environ.get('XRT_TPU_CONFIG') or os.environ.get('TPU_NAME'):
        try:
            import torch_xla.core.xla_model as xm
            device = xm.xla_device()
            logger.info("✅ TPU available")
            return device
        except ImportError:
            logger.warning("TPU environment detected but torch_xla not installed")
    
    # Fallback to CPU
    device = torch.device('cpu')
    logger.warning("⚠️ No GPU/TPU available, using CPU")
    return device


def setup_multi_gpu(model: torch.nn.Module, device_ids: Optional[list] = None) -> torch.nn.Module:
    """
    Set up model for multi-GPU training using DataParallel.
    
    Note: Model should already be on a CUDA device before wrapping.
    
    Args:
        model: PyTorch model (should already be on CUDA device)
        device_ids: List of GPU IDs to use (None = use all available)
        
    Returns:
        Model wrapped in DataParallel (or original model if single GPU)
    """
    if not torch.cuda.is_available():
        return model
    
    gpu_count = torch.cuda.device_count()
    
    if gpu_count <= 1:
        return model
    
    # Check if already wrapped
    if isinstance(model, torch.nn.DataParallel):
        logger.warning("Model is already wrapped in DataParallel")
        return model
    
    if device_ids is None:
        device_ids = list(range(gpu_count))
    
    logger.info(f"Setting up DataParallel for {len(device_ids)} GPUs: {device_ids}")
    model = torch.nn.DataParallel(model, device_ids=device_ids)
    
    return model


def get_device_info() -> dict:
    """
    Get information about available devices.
    
    Returns:
        Dictionary with device information
    """
    info = {
        'cuda_available': torch.cuda.is_available(),
        'device_count': 0,
        'device_names': [],
        'current_device': None
    }
    
    if torch.cuda.is_available():
        info['device_count'] = torch.cuda.device_count()
        info['device_names'] = [torch.cuda.get_device_name(i) for i in range(info['device_count'])]
        info['current_device'] = torch.cuda.current_device()
        info['cuda_version'] = torch.version.cuda
    
    return info

