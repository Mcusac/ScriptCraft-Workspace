# dinov2_model.py
# DINOv2 model wrapper for biomass prediction
# Supports left/right split with feature fusion
# Uses HuggingFace format for DINOv2 models

import torch
import torch.nn as nn
from typing import Tuple, Optional
import logging

from config.evaluation_constants import NUM_PRIMARY_TARGETS
from .base import BaseFeatureExtractionModel

logger = logging.getLogger(__name__)

# Lazy import for HuggingFace to avoid dependency if not needed
def _get_hf_dinov2():
    """Lazy import HuggingFace DINOv2 to avoid hard dependency."""
    try:
        from transformers import Dinov2Model as HFDinov2Model
        return HFDinov2Model
    except ImportError:
        logger.warning("transformers library not available. HuggingFace weight loading disabled.")
        return None


class DINOv2Model(BaseFeatureExtractionModel):
    """
    DINOv2 model wrapper with configurable output regression head.
    
    Uses HuggingFace format for loading DINOv2 models. Supports both single image
    and left/right split processing with feature fusion. DINOv2 is a self-supervised
    Vision Transformer pretrained on 142M images, providing better feature
    representations than ImageNet-pretrained models.
    
    For timm-format models, use TimmModel instead.
    """
    
    def __init__(
        self,
        model_name: str = 'facebook/dinov2-base',
        pretrained: bool = True,
        num_classes: int = NUM_PRIMARY_TARGETS,
        input_size: Optional[Tuple[int, int]] = None,
        use_tiles: bool = False,
        tile_grid_size: int = 2
    ):
        """
        Initialize DINOv2Model wrapper.
        
        Args:
            model_name: HuggingFace DINOv2 model identifier or path to local weights.
                       Examples: 'facebook/dinov2-base', 'facebook/dinov2-large',
                       or '/kaggle/input/dinov2/pytorch/base/1'
            pretrained: Whether to use pretrained weights (default: True).
                       Falls back to non-pretrained if download fails.
            num_classes: Number of output classes (default: NUM_PRIMARY_TARGETS).
                        Must be positive integer.
            input_size: Optional input size override as (height, width) tuple.
                       If None, will be inferred from model config (default: 518×518).
                       Both dimensions must be positive integers.
            use_tiles: Whether to use tile-based processing (2x2 grid per half).
                      Default: False (process halves directly).
            tile_grid_size: Grid size for tile extraction (e.g., 2 = 2x2 = 4 tiles per half).
                           Only used if use_tiles=True.
        
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
        self.use_tiles = use_tiles
        self.tile_grid_size = tile_grid_size
        
        # Always use HuggingFace format
        logger.info(f"Creating DINOv2 model: {model_name} (pretrained={pretrained}, HuggingFace format)")
        self._init_hf_backbone(model_name, pretrained)
        
        # Initialize input size and create regression heads
        self._init_input_size_and_heads(input_size)
    
    def _init_hf_backbone(self, model_name: str, pretrained: bool) -> None:
        """
        Initialize backbone using HuggingFace Dinov2Model.
        
        Args:
            model_name: HuggingFace model ID (e.g., 'facebook/dinov2-base') or path to weights
            pretrained: Whether to load pretrained weights (for HF, this means loading provided weights)
        """
        HFDinov2Model = _get_hf_dinov2()
        if HFDinov2Model is None:
            raise RuntimeError(
                "HuggingFace format model requested but 'transformers' library not available. "
                "Install with: pip install transformers"
            )
        
        try:
            logger.info(f"Loading HuggingFace DINOv2 model from: {model_name}")
            
            # Suppress MessageFactory.GetPrototype AttributeError (protobuf compatibility issue)
            # This is a known issue with HuggingFace transformers and protobuf version mismatches
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                # Load the model with add_pooling_layer=False since we'll use our own head
                try:
                    self.backbone = HFDinov2Model.from_pretrained(model_name)
                except AttributeError as e:
                    # Suppress MessageFactory.GetPrototype errors (harmless protobuf compatibility issue)
                    if 'MessageFactory' in str(e) and 'GetPrototype' in str(e):
                        logger.warning("Suppressed MessageFactory.GetPrototype error (protobuf compatibility issue)")
                        # Retry loading - the error is usually non-fatal
                        self.backbone = HFDinov2Model.from_pretrained(model_name)
                    else:
                        raise
            self._pretrained_loaded = True
            self._use_hf_output = True  # Flag to handle HF output format
            logger.info(f"✅ Successfully loaded HuggingFace DINOv2 model")
        except Exception as e:
            logger.error(f"Failed to load HuggingFace model: {e}")
            if not pretrained:
                raise RuntimeError(f"Cannot create non-pretrained HuggingFace model: {e}")
            else:
                raise
        
        # Get feature dimension from HF config
        # Note: We multiply by 3 because we concatenate CLS + AVG + MAX pooling
        if hasattr(self.backbone, 'config') and hasattr(self.backbone.config, 'hidden_size'):
            hidden_size = self.backbone.config.hidden_size
            self.feat_dim = hidden_size * 3  # CLS + AVG + MAX = 3× dimension
            logger.info(f"Feature dimension from HF config: {hidden_size} → {self.feat_dim} (3× for CLS+AVG+MAX)")
        else:
            # Fallback
            self.feat_dim = 768 * 3  # Default base model: 768 * 3 = 2304
            logger.warning(f"Could not get hidden_size from HF config, using default: {self.feat_dim}")
        
        # Set input size from HF config if available
        if hasattr(self.backbone, 'config') and hasattr(self.backbone.config, 'image_size'):
            self.input_size = (self.backbone.config.image_size, self.backbone.config.image_size)
            logger.info(f"Input size from HF config: {self.input_size}")
        else:
            # DINOv2's recommended resolution is 518×518
            self.input_size = (518, 518)
            logger.info(f"Using DINOv2 recommended input size: {self.input_size}")
        
        # Enable gradient checkpointing for memory efficiency
        if hasattr(self.backbone, 'gradient_checkpointing_enable'):
            self.backbone.gradient_checkpointing_enable()
            logger.info("✅ Gradient checkpointing enabled (trades compute for memory)")
    
    def _extract_hf_features(self, x: torch.Tensor) -> torch.Tensor:
        """
        Extract features from HuggingFace DINOv2 model.
        
        Extracts CLS token + Average pooling + Max pooling and concatenates them.
        This provides richer feature representations than CLS token alone.
        
        HF DINOv2 returns a dict with 'last_hidden_state' key.
        The output shape is (B, N, D) where N includes CLS token + patch tokens.
        We return (B, 3*D) by concatenating CLS, AVG, and MAX pooling.
        
        Args:
            x: Input tensor of shape (B, C, H, W)
            
        Returns:
            Features tensor of shape (B, 3*feat_dim) where feat_dim is the hidden size.
            Concatenated as [CLS_token, avg_pool, max_pool].
        """
        output = self.backbone(x)
        # HF DINOv2 returns BaseModelOutputWithPooling
        if hasattr(output, 'last_hidden_state'):
            last_hidden = output.last_hidden_state  # (B, N, D) where N = 1 (CLS) + N_patches
            cls_token = last_hidden[:, 0, :]  # (B, D) - CLS token
            patch_tokens = last_hidden[:, 1:, :]  # (B, N_patches, D) - Patch tokens
            
            # Average pooling across patches
            avg_pool = patch_tokens.mean(dim=1)  # (B, D)
            
            # Max pooling across patches
            max_pool = patch_tokens.max(dim=1)[0]  # (B, D)
            
            # Concatenate CLS + AVG + MAX
            features = torch.cat([cls_token, avg_pool, max_pool], dim=1)  # (B, 3*D)
        else:
            raise RuntimeError(f"Unexpected HF output format: {type(output)}")
        
        return features
    
    def _init_input_size_and_heads(self, input_size: Optional[Tuple[int, int]]) -> None:
        """
        Initialize input_size and create regression heads after feat_dim is set.
        
        Args:
            input_size: Optional input size override (HF models already set it in _init_hf_backbone)
        """
        # Input size already set in _init_hf_backbone() for HF models
        # Only override if explicitly provided
        if input_size is not None:
            self.input_size = input_size
            logger.debug(f"Input size overridden to: {self.input_size}")
        # Input size logging is handled in create_model() to avoid duplication
        
        # Create regression head for single image (full mode)
        hidden_size = max(32, int(self.feat_dim * 0.25))
        self.head_single = nn.Sequential(
            nn.Linear(self.feat_dim, hidden_size),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(hidden_size, self.num_classes)
        )
        
        # Create regression head for split images (2x feature dimension)
        hidden_size_split = max(32, int(self.feat_dim * 2 * 0.25))
        self.head_split = nn.Sequential(
            nn.Linear(self.feat_dim * 2, hidden_size_split),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(hidden_size_split, self.num_classes)
        )
        
        # Cross-gating mechanism for adaptive feature fusion
        self.cross_gate_left = nn.Linear(self.feat_dim, self.feat_dim)
        self.cross_gate_right = nn.Linear(self.feat_dim, self.feat_dim)
        self.use_cross_gating = True  # Can be made configurable
        
        # Tile processing components (if enabled)
        if self.use_tiles:
            # Mean pooling for aggregating tile features
            self.tile_pool = nn.AdaptiveAvgPool1d(1)
            logger.info(f"Tile-based processing enabled: {self.tile_grid_size}x{self.tile_grid_size} grid per half")
    
    def _extract_tiles(self, img: torch.Tensor) -> torch.Tensor:
        """
        Extract tiles from an image.
        
        Args:
            img: Input tensor of shape (B, C, H, W)
            
        Returns:
            Tensor of shape (B * num_tiles, C, tile_h, tile_w) with extracted tiles
        """
        B, C, H, W = img.shape
        tile_h = H // self.tile_grid_size
        tile_w = W // self.tile_grid_size
        
        tiles = []
        for i in range(self.tile_grid_size):
            for j in range(self.tile_grid_size):
                h_start = i * tile_h
                h_end = (i + 1) * tile_h if i < self.tile_grid_size - 1 else H
                w_start = j * tile_w
                w_end = (j + 1) * tile_w if j < self.tile_grid_size - 1 else W
                tile = img[:, :, h_start:h_end, w_start:w_end]
                # Resize tile to model input size if needed
                if tile.shape[2] != self.input_size[0] or tile.shape[3] != self.input_size[1]:
                    tile = torch.nn.functional.interpolate(
                        tile, size=self.input_size, mode='bilinear', align_corners=False
                    )
                tiles.append(tile)
        
        return torch.cat(tiles, dim=0)  # (B * num_tiles, C, H, W)
    
    def _process_tiles(self, img: torch.Tensor) -> torch.Tensor:
        """
        Process image through tile extraction and feature aggregation.
        
        Args:
            img: Input tensor of shape (B, C, H, W)
            
        Returns:
            Aggregated features of shape (B, feat_dim)
        """
        B = img.shape[0]
        tiles = self._extract_tiles(img)  # (B * num_tiles, C, H, W)
        
        # Process all tiles through backbone
        tile_features = self._extract_hf_features(tiles)  # (B * num_tiles, feat_dim)
        
        # Reshape to (B, num_tiles, feat_dim)
        num_tiles = self.tile_grid_size * self.tile_grid_size
        tile_features = tile_features.view(B, num_tiles, self.feat_dim)
        
        # Aggregate tile features (mean pooling)
        aggregated = tile_features.mean(dim=1)  # (B, feat_dim)
        
        return aggregated
    
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
            
            # Extract features from each half
            if self.use_tiles:
                left_feat = self._process_tiles(left_img)  # (B, feat_dim)
                right_feat = self._process_tiles(right_img)  # (B, feat_dim)
            else:
                left_feat = self._extract_hf_features(left_img)  # (B, feat_dim)
                right_feat = self._extract_hf_features(right_img)  # (B, feat_dim)
            
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
            if self.use_tiles:
                features = self._process_tiles(x)  # (B, feat_dim)
            else:
                features = self._extract_hf_features(x)  # (B, feat_dim)
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

