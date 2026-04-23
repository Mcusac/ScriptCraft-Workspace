# batch_processing_utils.py
# Utilities for processing batches in training and inference
# Handles both full image and split dataset formats

import torch
from typing import Tuple, Union
import logging

logger = logging.getLogger(__name__)


def process_batch_for_model(
    batch: Tuple,
    model: torch.nn.Module,
    device: torch.device,
    dataset_type: str = 'split'  # Default to 'split' (standard approach)
) -> torch.Tensor:
    """
    Process a batch for model forward pass, handling both full and split dataset types.
    
    This utility function extracts the common logic for processing batches in both
    training and inference contexts, supporting both full image and split dataset formats.
    
    Args:
        batch: Batch from DataLoader - either (images, targets) for 'full' dataset,
               or (left_img, right_img, targets) for 'split' dataset
        model: Model to run forward pass with (supports dual input for split datasets)
        device: Device to move tensors to
        dataset_type: 'full' or 'split' - determines batch format
    
    Returns:
        Model outputs tensor of shape (B, num_classes)
    
    Raises:
        ValueError: If dataset_type is not 'full' or 'split'
        TypeError: If batch format doesn't match dataset_type
    
    Note:
        For split dataset type, the model processes both left and right images
        and averages their outputs for final predictions.
    """
    if dataset_type == 'split':
        # Handle split dataset format: (left_img, right_img, targets)
        if not isinstance(batch, (tuple, list)) or len(batch) != 3:
            raise ValueError(
                f"Split dataset batch must be tuple of (left_img, right_img, targets), "
                f"got {type(batch)} with length {len(batch) if isinstance(batch, (tuple, list)) else 'N/A'}"
            )
        
        left_img, right_img, _ = batch
        left_img = left_img.to(device)
        right_img = right_img.to(device)
        
        # Forward pass with dual input (left and right images)
        # Model forward accepts tuple of (left_img, right_img) for split dataset mode
        outputs = model((left_img, right_img))
        
    elif dataset_type == 'full':
        # Handle full image dataset format: (images, targets)
        if not isinstance(batch, (tuple, list)) or len(batch) != 2:
            raise ValueError(
                f"Full dataset batch must be tuple of (images, targets), "
                f"got {type(batch)} with length {len(batch) if isinstance(batch, (tuple, list)) else 'N/A'}"
            )
        
        images, _ = batch
        images = images.to(device)
        
        # Forward pass with single input
        outputs = model(images)
        
    else:
        raise ValueError(f"dataset_type must be 'full' or 'split', got '{dataset_type}'")
    
    return outputs


def extract_batch_data(
    batch: Tuple,
    dataset_type: str = 'split',  # Default to 'split' (standard approach)
    device: torch.device = None
) -> Tuple[Union[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]], torch.Tensor]:
    """
    Extract and prepare batch data for processing.
    
    Separates the input data from targets and moves to device if provided.
    
    Args:
        batch: Batch from DataLoader - either (images, targets) for 'full' dataset,
               or (left_img, right_img, targets) for 'split' dataset
        dataset_type: 'full' or 'split' - determines batch format
        device: Optional device to move tensors to. If None, tensors are not moved.
    
    Returns:
        Tuple of (inputs, targets) where:
        - For 'full': inputs is (B, C, H, W) tensor, targets is (B, 3) tensor
        - For 'split': inputs is ((B, C, H, W), (B, C, H, W)) tuple, targets is (B, 3) tensor
    
    Raises:
        ValueError: If dataset_type is not 'full' or 'split' or batch format is invalid
    """
    if dataset_type == 'split':
        if not isinstance(batch, (tuple, list)) or len(batch) != 3:
            raise ValueError(
                f"Split dataset batch must be tuple of (left_img, right_img, targets), "
                f"got {type(batch)} with length {len(batch) if isinstance(batch, (tuple, list)) else 'N/A'}"
            )
        
        left_img, right_img, targets = batch
        
        if device is not None:
            left_img = left_img.to(device)
            right_img = right_img.to(device)
            targets = targets.to(device)
        
        inputs = (left_img, right_img)
        
    elif dataset_type == 'full':
        if not isinstance(batch, (tuple, list)) or len(batch) != 2:
            raise ValueError(
                f"Full dataset batch must be tuple of (images, targets), "
                f"got {type(batch)} with length {len(batch) if isinstance(batch, (tuple, list)) else 'N/A'}"
            )
        
        images, targets = batch
        
        if device is not None:
            images = images.to(device)
            targets = targets.to(device)
        
        inputs = images
        
    else:
        raise ValueError(f"dataset_type must be 'full' or 'split', got '{dataset_type}'")
    
    return inputs, targets

