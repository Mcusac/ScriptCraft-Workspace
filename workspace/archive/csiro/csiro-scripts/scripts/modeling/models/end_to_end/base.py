# base.py
# Base class for feature extraction models
#
# Provides a common interface for all feature extraction models (TimmModel, DINOv2Model, etc.)
# Enforces SOLID principles by defining a consistent contract that all models must implement.

import torch
import torch.nn as nn
from abc import ABC, abstractmethod
from typing import Tuple, Union

logger = None  # Will be initialized when needed


class BaseFeatureExtractionModel(nn.Module, ABC):
    """
    Abstract base class for feature extraction models.
    
    This class defines the common interface that all feature extraction models must implement.
    It enforces consistency across different model architectures (TimmModel, DINOv2Model, etc.)
    and ensures that all models can be used interchangeably in the feature extraction pipeline.
    
    All feature extraction models must:
    - Support forward pass with single or dual (split) image inputs
    - Provide input size information
    - Support freezing/unfreezing backbone for transfer learning
    - Report whether pretrained weights were loaded
    """
    
    def __init__(self):
        """
        Initialize base model.
        
        Subclasses should call super().__init__() in their __init__ methods.
        """
        super().__init__()
    
    @abstractmethod
    def forward(
        self, 
        x: Union[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]
    ) -> torch.Tensor:
        """
        Forward pass through the model.
        
        Args:
            x: Input tensor(s) of shape (B, C, H, W) where:
               - B is batch size
               - C is number of channels (typically 3 for RGB)
               - H, W are height and width (should match input_size)
               Can be:
               - Single tensor: (B, C, H, W) for full image or single view
               - Tuple of two tensors: ((B, C, H, W), (B, C, H, W)) for left/right split
        
        Returns:
            Output tensor of shape (B, num_classes) with model predictions.
        """
        pass
    
    @abstractmethod
    def get_input_size(self) -> Tuple[int, int]:
        """
        Get expected input size for this model.
        
        Returns:
            Tuple of (height, width) representing the expected input image dimensions.
        """
        pass
    
    @abstractmethod
    def freeze_backbone(self) -> None:
        """
        Freeze backbone parameters for transfer learning.
        
        Sets requires_grad=False for all backbone parameters, preventing
        gradient updates during training. Useful for fine-tuning scenarios.
        """
        pass
    
    @abstractmethod
    def unfreeze_backbone(self) -> None:
        """
        Unfreeze backbone parameters to allow training.
        
        Sets requires_grad=True for all backbone parameters, enabling
        gradient updates during training.
        """
        pass
    
    @abstractmethod
    def is_pretrained(self) -> bool:
        """
        Check if pretrained weights were successfully loaded.
        
        Returns:
            True if pretrained weights loaded, False otherwise.
        """
        pass

