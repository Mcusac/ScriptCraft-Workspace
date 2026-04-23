# streaming_biomass_dataset.py
# PyTorch IterableDataset for streaming biomass prediction (memory-efficient)
# CSIRO-SPECIFIC: Class name contains "Biomass" - should be abstracted

import torch
from typing import Tuple

from .base_streaming_dataset import BaseStreamingBiomassDataset

logger = __import__('logging').getLogger(__name__)

# CSIRO-SPECIFIC: Class name contains "Biomass" - should be abstracted to StreamingDataset
class StreamingBiomassDataset(BaseStreamingBiomassDataset):
    """
    PyTorch IterableDataset for streaming biomass prediction.
    
    Loads images on-demand instead of pre-loading, making it memory-efficient
    for large datasets and grid search scenarios. Supports multi-worker DataLoaders
    with automatic sharding.
    
    Expects aggregated train.csv format (1 row per image with all 5 targets).
    Returns 3 targets: [Dry_Green_g, Dry_Clover_g, Dry_Dead_g]
    """
    
    def _load_item(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Load a single item from the dataset.
        
        Args:
            idx: Index into data_rows list
            
        Returns:
            Tuple of (image_tensor, targets_tensor)
        """
        row = self.data_rows[idx]
        
        # Load image on-demand (not cached)
        image_path = self.data_root / row['image_path']
        image = self._load_image(image_path)
        
        # Apply transforms
        if self.transform:
            image = self.transform(image)
        
        # Get targets using base class helper
        targets = self._get_targets(row)
        
        return image, targets

