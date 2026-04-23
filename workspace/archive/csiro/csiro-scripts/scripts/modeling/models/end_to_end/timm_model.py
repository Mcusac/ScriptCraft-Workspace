# timm_model.py
# Wrapper for timm models

import torch
import torch.nn as nn
from typing import Tuple, Optional
import logging

from config.path_constants import DEFAULT_IMAGE_SIZE
from config.evaluation_constants import NUM_PRIMARY_TARGETS
from .base import BaseFeatureExtractionModel
from .weight_loader import TimmWeightLoader

logger = logging.getLogger(__name__)


class TimmModel(BaseFeatureExtractionModel):
    """
    Wrapper for timm models with configurable output regression head.
    
    This class provides a unified interface for creating timm models with
    custom output dimensions, handling pretrained weight loading with fallback
    to non-pretrained models when network access is unavailable.
    """
    
    def __init__(
        self,
        model_name: str = 'efficientnet_b0',
        pretrained: bool = True,
        num_classes: int = NUM_PRIMARY_TARGETS,
        input_size: Optional[Tuple[int, int]] = None
    ):
        """
        Initialize TimmModel wrapper.
        
        Args:
            model_name: Name of timm model (e.g., 'efficientnet_b0', 'resnet50').
                       Must be a valid timm model name.
            pretrained: Whether to use pretrained weights (default: True).
                       Falls back to non-pretrained if download fails.
            num_classes: Number of output classes (default: NUM_PRIMARY_TARGETS).
                        Must be positive integer.
            input_size: Optional input size override as (height, width) tuple.
                       If None, will be inferred from pretrained config or default to DEFAULT_IMAGE_SIZE.
                       Both dimensions must be positive integers.
        
        Raises:
            ValueError: If model_name is empty, num_classes is invalid, or input_size is invalid.
            RuntimeError: If model creation fails and pretrained=False.
        """
        super().__init__()
        
        # Validate model_name
        if not model_name or not isinstance(model_name, str):
            raise ValueError(f"model_name must be non-empty string, got {model_name}")
        
        # Validate num_classes
        if not isinstance(num_classes, int) or num_classes < 1:
            raise ValueError(f"num_classes must be positive integer, got {num_classes}")
        
        # Validate input_size if provided
        if input_size is not None:
            if not isinstance(input_size, (tuple, list)) or len(input_size) != 2:
                raise ValueError(f"input_size must be tuple (height, width), got {input_size}")
            height, width = input_size
            if not isinstance(height, int) or not isinstance(width, int):
                raise ValueError(f"input_size dimensions must be integers, got {input_size}")
            if height < 1 or width < 1:
                raise ValueError(f"input_size dimensions must be positive, got {input_size}")
        
        self.num_classes = num_classes
        self.model_name = model_name
        
        # Create model using timm with weight loader
        logger.info(f"Creating timm model: {model_name} (pretrained={pretrained})")
        
        # Use weight loader to handle pretrained weight loading with fallback strategies
        # Create backbone with num_classes=0 to extract features instead of predictions
        weight_loader = TimmWeightLoader()
        self.backbone = weight_loader.load_weights(model_name, 0, pretrained)
        self._pretrained_loaded = weight_loader.is_pretrained_loaded()
        
        # Get feature dimension from backbone
        if hasattr(self.backbone, 'num_features'):
            self.feat_dim = self.backbone.num_features
        else:
            # Fallback: try to infer from model config or use a dummy forward pass
            try:
                # Try to get from model config
                if hasattr(self.backbone, 'pretrained_cfg') and self.backbone.pretrained_cfg:
                    if hasattr(self.backbone.pretrained_cfg, 'num_features'):
                        self.feat_dim = self.backbone.pretrained_cfg.num_features
                    else:
                        # Infer from a dummy forward pass
                        dummy_input = torch.randn(1, 3, 224, 224)
                        with torch.no_grad():
                            dummy_output = self.backbone(dummy_input)
                        self.feat_dim = dummy_output.shape[1]
                else:
                    # Infer from a dummy forward pass
                    dummy_input = torch.randn(1, 3, 224, 224)
                    with torch.no_grad():
                        dummy_output = self.backbone(dummy_input)
                    self.feat_dim = dummy_output.shape[1]
            except Exception as e:
                logger.warning(f"Could not determine feature dimension automatically: {e}")
                # Default fallback for common models
                if 'efficientnet' in model_name.lower():
                    self.feat_dim = 1536 if 'b3' in model_name.lower() else 1280
                else:
                    self.feat_dim = 2048  # Common default
                logger.info(f"Using default feature dimension: {self.feat_dim}")
        
        logger.info(f"Feature dimension: {self.feat_dim}")
        
        # Create regression head for single image (full mode)
        # Hidden size is 25% of feature dimension, but at least 32
        hidden_size = max(32, int(self.feat_dim * 0.25))
        self.head_single = nn.Sequential(
            nn.Linear(self.feat_dim, hidden_size),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(hidden_size, num_classes)
        )
        
        # Create regression head for split images (2x feature dimension)
        hidden_size_split = max(32, int(self.feat_dim * 2 * 0.25))
        self.head_split = nn.Sequential(
            nn.Linear(self.feat_dim * 2, hidden_size_split),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(hidden_size_split, num_classes)
        )
        
        # Cross-gating mechanism for adaptive feature fusion (optional enhancement)
        self.cross_gate_left = nn.Linear(self.feat_dim, self.feat_dim)
        self.cross_gate_right = nn.Linear(self.feat_dim, self.feat_dim)
        self.use_cross_gating = True  # Can be made configurable
        
        # Get input size from pretrained config if available
        try:
            if hasattr(self.backbone, 'pretrained_cfg') and self.backbone.pretrained_cfg:
                cfg = self.backbone.pretrained_cfg
                if input_size is None:
                    # Get from pretrained_cfg
                    if hasattr(cfg, 'input_size'):
                        # input_size is typically (3, H, W), we want (H, W)
                        if isinstance(cfg.input_size, (list, tuple)) and len(cfg.input_size) >= 2:
                            self.input_size = (cfg.input_size[-2], cfg.input_size[-1])
                        else:
                            logger.warning(f"Invalid input_size in pretrained_cfg: {cfg.input_size}, using default {DEFAULT_IMAGE_SIZE}")
                            self.input_size = DEFAULT_IMAGE_SIZE
                    else:
                        logger.debug(f"pretrained_cfg has no input_size attribute, using default {DEFAULT_IMAGE_SIZE}")
                        self.input_size = DEFAULT_IMAGE_SIZE
                else:
                    self.input_size = input_size
            else:
                self.input_size = input_size if input_size else DEFAULT_IMAGE_SIZE
        except Exception as e:
            logger.warning(f"Error extracting input_size from model config: {e}, using default {DEFAULT_IMAGE_SIZE}")
            self.input_size = input_size if input_size else DEFAULT_IMAGE_SIZE
        
        logger.info(f"Model input size: {self.input_size}")
    
    def forward(self, x: torch.Tensor | Tuple[torch.Tensor, torch.Tensor]) -> torch.Tensor:
        """
        Forward pass through the model.
        
        Supports both single image input and dual input (left/right split) modes.
        For split mode, extracts features from each half, fuses them adaptively,
        then predicts from the combined features.
        
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
            For dual input, features are extracted, fused, then predicted.
        """
        if isinstance(x, tuple):
            # Dual input mode: extract features from left and right halves, then fuse
            left_img, right_img = x
            
            # Extract features from each half (backbone outputs features, not predictions)
            left_feat = self.backbone(left_img)  # (B, feat_dim)
            right_feat = self.backbone(right_img)  # (B, feat_dim)
            
            # Apply cross-gating for adaptive feature fusion
            if self.use_cross_gating:
                # Generate gates from opposite branch features
                g_l = torch.sigmoid(self.cross_gate_left(right_feat))  # Left gate from right features
                g_r = torch.sigmoid(self.cross_gate_right(left_feat))  # Right gate from left features
                
                # Apply gates to modulate features
                left_feat = left_feat * g_l
                right_feat = right_feat * g_r
            
            # Concatenate features from both halves
            combined = torch.cat([left_feat, right_feat], dim=1)  # (B, feat_dim * 2)
            
            # Predict from combined features
            return self.head_split(combined)  # (B, num_classes)
        else:
            # Single input mode: extract features and predict
            features = self.backbone(x)  # (B, feat_dim)
            return self.head_single(features)  # (B, num_classes)
    
    def get_input_size(self) -> Tuple[int, int]:
        """
        Get expected input size for this model.
        
        Returns:
            Tuple of (height, width) representing the expected input image dimensions.
        """
        return self.input_size
    
    def freeze_backbone(self) -> None:
        """
        Freeze backbone parameters for transfer learning.
        
        Sets requires_grad=False for all backbone parameters, preventing
        gradient updates during training. Useful for fine-tuning scenarios.
        """
        for param in self.backbone.parameters():
            param.requires_grad = False
        logger.info(f"Frozen {self.model_name} backbone parameters")
    
    def unfreeze_backbone(self) -> None:
        """
        Unfreeze backbone parameters to allow training.
        
        Sets requires_grad=True for all backbone parameters, enabling
        gradient updates during training.
        """
        for param in self.backbone.parameters():
            param.requires_grad = True
        logger.info(f"Unfrozen {self.model_name} backbone parameters")
    
    def is_pretrained(self) -> bool:
        """
        Check if pretrained weights were successfully loaded.
        
        Returns:
            True if pretrained weights loaded, False otherwise.
        """
        return self._pretrained_loaded

