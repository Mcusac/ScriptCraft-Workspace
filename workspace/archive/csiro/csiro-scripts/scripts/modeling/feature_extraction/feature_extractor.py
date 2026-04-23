# feature_extractor.py
# Utility class for extracting features from models without regression head
# Shared between training and inference for feature extraction mode

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import numpy as np
import pandas as pd
from typing import Optional, List, Callable
import logging

from config.config import Config
from dataset_manipulation.transforms.transform_factory import build_tta_transforms

logger = logging.getLogger(__name__)


class FeatureExtractor:
    """
    Extracts features from any model without using regression head.
    
    This utility is shared between training and inference when using
    feature extraction mode. It extracts features from the model backbone
    and handles both full image and split dataset formats.
    """
    
    def __init__(self, model: nn.Module, device: torch.device):
        """
        Initialize FeatureExtractor.
        
        Args:
            model: Model to extract features from. Should have feature extraction
                  methods (e.g., _extract_hf_features for DINOv2).
            device: Device to run feature extraction on.
        """
        self.model = model
        self.device = device
        self.model.eval()
        self.model.to(device)
    
    def extract_features(
        self,
        dataloader: DataLoader,
        dataset_type: str = 'split',  # Default to 'split' (standard approach)
        config: Optional[Config] = None,
        tta_transforms: Optional[List[Callable]] = None
    ) -> np.ndarray:
        """
        Extract features from all images in dataloader with optional TTA.
        
        If TTA is enabled, extracts features from multiple augmented versions
        of each image and averages them. TTA is always enabled by default.
        
        Args:
            dataloader: DataLoader with images to extract features from.
            dataset_type: 'full' or 'split' - determines batch format.
            config: Configuration object. Used to build TTA transforms if tta_transforms not provided.
            tta_transforms: Optional list of TTA transforms. If None and config provided,
                          builds TTA transforms from config. If both None, uses default TTA variants.
        
        Returns:
            Features array of shape (N, feat_dim) where N is number of images
            and feat_dim is the feature dimension. If TTA enabled, features are averaged
            across TTA variants.
        """
        # Determine TTA transforms to use
        if tta_transforms is not None:
            # Use provided TTA transforms
            tta_transform_list = tta_transforms
            logger.info(f"Using {len(tta_transform_list)} provided TTA transforms")
        elif config is not None:
            # Build TTA transforms from config
            tta_variants = getattr(config.data, 'tta_variants', None)
            tta_transform_list = build_tta_transforms(config, tta_variants=tta_variants)
            logger.info(f"Built {len(tta_transform_list)} TTA transforms from config")
        else:
            # Use default TTA variants (always enable TTA)
            # We need config to build transforms, so we'll extract without TTA if no config
            # But per plan, TTA should always be enabled, so we'll log a warning
            logger.warning(
                "No config or tta_transforms provided. TTA cannot be enabled. "
                "Please provide config to enable TTA."
            )
            # Fall back to single pass (no TTA)
            return self._extract_features_single_pass(dataloader, dataset_type)
        
        # Extract features with TTA
        if len(tta_transform_list) == 0:
            logger.warning("TTA transform list is empty, falling back to single pass")
            return self._extract_features_single_pass(dataloader, dataset_type)
        
        # Extract features for each TTA variant
        all_tta_features = []
        dataset = dataloader.dataset
        
        # Get dataset class and parameters
        dataset_class = type(dataset)
        data_rows = dataset.data_rows
        data_root = str(dataset.data_root)
        target_cols = getattr(dataset, 'target_cols', None)  # Preserve target_cols if present
        
        for idx, tta_transform in enumerate(tta_transform_list):
            logger.info(f"Extracting features with TTA variant {idx + 1}/{len(tta_transform_list)}")
            
            # Create new dataset with this TTA transform
            # Convert data_rows (list of dicts) back to DataFrame
            dataset_kwargs = {
                'data': pd.DataFrame(data_rows),
                'data_root': data_root,
                'transform': tta_transform,
                'shuffle': False
            }
            if target_cols is not None:
                dataset_kwargs['target_cols'] = target_cols
            
            new_dataset = dataset_class(**dataset_kwargs)
            
            # Create new dataloader with same parameters as original
            new_dataloader = DataLoader(
                new_dataset,
                batch_size=dataloader.batch_size,
                shuffle=False,
                num_workers=dataloader.num_workers,
                pin_memory=dataloader.pin_memory,
                prefetch_factor=dataloader.prefetch_factor,
                persistent_workers=dataloader.persistent_workers
            )
            
            # Extract features for this TTA variant
            features_variant = self._extract_features_single_pass(new_dataloader, dataset_type)
            all_tta_features.append(features_variant)
        
        # Average features across TTA variants
        if len(all_tta_features) == 1:
            features_array = all_tta_features[0]
        else:
            # Stack features: shape (num_tta, N, feat_dim)
            stacked_features = np.stack(all_tta_features, axis=0)
            # Average across TTA dimension: shape (N, feat_dim)
            features_array = np.mean(stacked_features, axis=0)
            logger.info(f"Averaged features across {len(all_tta_features)} TTA variants")
        
        logger.info(f"Extracted features shape: {features_array.shape}")
        return features_array
    
    def _extract_features_single_pass(
        self,
        dataloader: DataLoader,
        dataset_type: str
    ) -> np.ndarray:
        """
        Extract features from single dataloader (current logic, no TTA).
        
        Args:
            dataloader: DataLoader with images to extract features from.
            dataset_type: 'full' or 'split' - determines batch format.
        
        Returns:
            Features array of shape (N, feat_dim) where N is number of images
            and feat_dim is the feature dimension.
        """
        all_features = []
        
        with torch.no_grad():
            for batch in dataloader:
                # Extract features based on dataset type
                if dataset_type == 'split':
                    left_img, right_img, _ = batch
                    left_img = left_img.to(self.device)
                    right_img = right_img.to(self.device)
                    
                    # Extract features from each half
                    left_feat = self._extract_features_from_model(left_img)
                    right_feat = self._extract_features_from_model(right_img)
                    
                    # Concatenate features from both halves
                    features = torch.cat([left_feat, right_feat], dim=1)
                else:
                    # Full image mode
                    images, _ = batch
                    images = images.to(self.device)
                    features = self._extract_features_from_model(images)
                
                all_features.append(features.cpu().numpy())
        
        # Concatenate all features
        features_array = np.concatenate(all_features, axis=0)
        return features_array
    
    def _extract_features_from_model(self, x: torch.Tensor) -> torch.Tensor:
        """
        Extract features from model for a batch of images.
        
        Handles different model types (DINOv2, Timm, etc.) by checking
        for feature extraction methods.
        
        Args:
            x: Input tensor of shape (B, C, H, W)
        
        Returns:
            Features tensor of shape (B, feat_dim)
        """
        # Check if model has explicit feature extraction method
        if hasattr(self.model, '_extract_hf_features'):
            # DINOv2 model
            return self.model._extract_hf_features(x)
        elif hasattr(self.model, 'extract_features'):
            # Model with extract_features method
            return self.model.extract_features(x)
        elif hasattr(self.model, 'backbone'):
            # Model with backbone attribute (try to extract from backbone)
            if hasattr(self.model.backbone, '_extract_hf_features'):
                return self.model.backbone._extract_hf_features(x)
            else:
                # Fallback: use backbone forward and extract features
                output = self.model.backbone(x)
                # Try to extract features from output
                if hasattr(output, 'last_hidden_state'):
                    # HuggingFace format
                    last_hidden = output.last_hidden_state
                    cls_token = last_hidden[:, 0, :]
                    patch_tokens = last_hidden[:, 1:, :]
                    avg_pool = patch_tokens.mean(dim=1)
                    max_pool = patch_tokens.max(dim=1)[0]
                    return torch.cat([cls_token, avg_pool, max_pool], dim=1)
                else:
                    # Assume output is features directly
                    return output
        else:
            # Fallback: use model forward and assume it returns features
            # This won't work for models with regression heads, but provides
            # a fallback for models that output features directly
            output = self.model(x)
            if output.dim() == 2 and output.shape[1] > 100:
                # Likely features (not predictions)
                return output
            else:
                raise RuntimeError(
                    f"Could not extract features from model {type(self.model)}. "
                    "Model must have _extract_hf_features, extract_features, or backbone attribute."
                )

