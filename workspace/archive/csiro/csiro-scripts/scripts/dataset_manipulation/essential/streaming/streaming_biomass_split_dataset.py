# streaming_biomass_split_dataset.py
# PyTorch IterableDataset for streaming biomass prediction with left/right image split
# Memory-efficient dataset that splits images into left and right halves
# CSIRO-SPECIFIC: Class name contains "Biomass" - should be abstracted

import torch
from typing import Tuple

from .base_streaming_dataset import BaseStreamingBiomassDataset

logger = __import__('logging').getLogger(__name__)

# CSIRO-SPECIFIC: Class name contains "Biomass" - should be abstracted to StreamingSplitDataset
class StreamingBiomassSplitDataset(BaseStreamingBiomassDataset):
    """
    PyTorch IterableDataset for streaming biomass prediction with left/right image split.
    
    Loads images on-demand and splits them into left and right halves at the midpoint.
    This addresses the stereo/dual-view nature of competition images by processing
    each half separately, enabling view-specific feature extraction.
    
    Loads images on-demand instead of pre-loading, making it memory-efficient
    for large datasets and grid search scenarios. Supports multi-worker DataLoaders
    with automatic sharding.
    
    Expects aggregated train.csv format (1 row per image with all 5 targets).
    Returns 3 targets: [Dry_Green_g, Dry_Clover_g, Dry_Dead_g]
    
    Returns:
        Tuple of (left_tensor, right_tensor, targets_tensor)
        - left_tensor: Transformed left half image tensor
        - right_tensor: Transformed right half image tensor
        - targets_tensor: Tensor of 3 targets [Dry_Green_g, Dry_Clover_g, Dry_Dead_g]
    """
    
    def _load_item(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Load a single item from the dataset and split into left/right halves.
        
        Args:
            idx: Index into data_rows list
            
        Returns:
            Tuple of (left_tensor, right_tensor, targets_tensor)
        """
        row = self.data_rows[idx]
        
        # Load image on-demand (not cached)
        image_path = self.data_root / row['image_path']
        image = self._load_image(image_path)
        
        # Split image into left and right halves at midpoint
        # image is PIL Image, so use .size property and crop method
        w, h = image.size  # PIL Image size is (width, height)
        mid = w // 2
        left_img = image.crop((0, 0, mid, h))    # Left half: (left, top, right, bottom)
        right_img = image.crop((mid, 0, w, h))  # Right half: (left, top, right, bottom)
        
        # Apply transforms to each half separately
        if self.transform:
            left_tensor = self.transform(left_img)
            right_tensor = self.transform(right_img)
        else:
            # If no transform, convert to tensor manually
            from torchvision.transforms import ToTensor
            to_tensor = ToTensor()
            left_tensor = to_tensor(left_img)
            right_tensor = to_tensor(right_img)
        
        # Get targets using base class helper
        targets = self._get_targets(row)
        
        return left_tensor, right_tensor, targets

