# noise_addition.py
# Artificially expanding the dataset by adding noise to the images
# Adding Gaussian noise to simulate different noise conditions.

import torch
import torch.nn as nn
import logging

from utils.system import validate_non_negative
from ..defaults import DEFAULT_NOISE_MEAN, DEFAULT_NOISE_STD

logger = logging.getLogger(__name__)


class AddGaussianNoise(nn.Module):
    """
    Add Gaussian noise to tensor images.
    
    This transform should be applied after ToTensor() since it operates on tensors.
    The noise is clipped to ensure output remains in valid range [0, 1].
    """
    
    def __init__(self, mean: float = DEFAULT_NOISE_MEAN, std: float = DEFAULT_NOISE_STD):
        """
        Initialize Gaussian noise transform.
        
        Args:
            mean: Mean of the Gaussian noise (default: 0.0).
            std: Standard deviation of the Gaussian noise (default: 0.01).
                 Must be non-negative.
        
        Raises:
            ValueError: If std is negative.
        """
        super().__init__()
        validate_non_negative(std, "std")
        self.mean = mean
        self.std = std
    
    def forward(self, tensor: torch.Tensor) -> torch.Tensor:
        """
        Add Gaussian noise to tensor.
        
        Args:
            tensor: Input tensor of shape (C, H, W) or (B, C, H, W).
                    Expected to be in range [0, 1] (after ToTensor()).
            
        Returns:
            Tensor with added noise, clipped to [0, 1] to maintain valid range.
        """
        noise = torch.randn_like(tensor) * self.std + self.mean
        noisy_tensor = tensor + noise
        # Clip to valid range [0, 1] for normalized images
        return torch.clamp(noisy_tensor, 0.0, 1.0)


def get_noise_addition_transform(
    mean: float = DEFAULT_NOISE_MEAN,
    std: float = DEFAULT_NOISE_STD
) -> AddGaussianNoise:
    """
    Get Gaussian noise addition transform.
    
    Note: This transform must be applied AFTER ToTensor() since it operates on tensors.
    
    Args:
        mean: Mean of the Gaussian noise (default: 0.0).
        std: Standard deviation of the Gaussian noise (default: 0.01).
             Must be non-negative.
        
    Returns:
        AddGaussianNoise transform instance.
        
    Raises:
        ValueError: If std is negative.
    """
    return AddGaussianNoise(mean=mean, std=std)