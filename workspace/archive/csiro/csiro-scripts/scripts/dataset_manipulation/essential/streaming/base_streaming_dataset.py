# base_streaming_dataset.py
# Base class for streaming biomass datasets
# Extracts common functionality to eliminate code duplication
# CSIRO-SPECIFIC: Class name contains "Biomass" - should be abstracted

import pandas as pd
import torch
from torch.utils.data import IterableDataset
from pathlib import Path
from typing import Optional, Callable, Iterator
import logging
import random

from dataset_manipulation.essential.loading import load_jpg
from config.evaluation_constants import PRIMARY_TARGETS

logger = logging.getLogger(__name__)


# CSIRO-SPECIFIC: Class name contains "Biomass" - should be abstracted to BaseStreamingDataset
class BaseStreamingBiomassDataset(IterableDataset):
    """
    Base class for streaming biomass datasets.
    
    Provides common functionality for memory-efficient IterableDataset implementations
    that load images on-demand. Supports multi-worker DataLoaders with automatic sharding.
    
    Subclasses should implement `_load_item` to define how individual items are loaded
    and processed.
    """
    
    def __init__(
        self,
        data: pd.DataFrame,
        data_root: str,
        transform: Optional[Callable] = None,
        target_cols: Optional[list] = None,
        shuffle: bool = False
    ):
        """
        Args:
            data: DataFrame with aggregated data (1 row per image)
            data_root: Root directory for images
            transform: Optional transform to apply to images
            target_cols: List of target column names (default: ['Dry_Green_g', 'Dry_Clover_g', 'Dry_Dead_g'])
            shuffle: Whether to shuffle data (only affects order, not memory usage)
        """
        # Store only the necessary data (not the full DataFrame in memory)
        # Convert to list of dicts to avoid keeping DataFrame in memory
        self.data_rows = data.reset_index(drop=True).to_dict('records')
        self.data_root = Path(data_root)
        self.transform = transform
        self.shuffle = shuffle
        
        if target_cols is None:
            target_cols = PRIMARY_TARGETS.copy()
        self.target_cols = target_cols
        
        # Verify required columns exist
        required_cols = ['image_path'] + target_cols
        if len(self.data_rows) > 0:
            missing_cols = [col for col in required_cols if col not in self.data_rows[0]]
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")
        
        self._length = len(self.data_rows)
    
    def __len__(self) -> int:
        """Return dataset length."""
        return self._length
    
    def __iter__(self) -> Iterator:
        """
        Iterate over dataset, loading images on-demand.
        
        Supports multi-worker DataLoaders by automatically sharding data
        based on worker info from torch.utils.data.get_worker_info().
        
        Yields:
            Items as defined by subclass's `_load_item` method.
        """
        # Get worker info for multi-worker DataLoaders
        worker_info = torch.utils.data.get_worker_info()
        
        # Prepare indices (shuffled if needed)
        indices = list(range(len(self.data_rows)))
        if self.shuffle:
            random.shuffle(indices)
        
        if worker_info is None:
            # Single worker - process all data
            for idx in indices:
                yield self._load_item(idx)
        else:
            # Multi-worker - shard data across workers
            num_workers = worker_info.num_workers
            worker_id = worker_info.id
            
            # Get this worker's portion of indices
            worker_indices = indices[worker_id::num_workers]
            
            for idx in worker_indices:
                yield self._load_item(idx)
    
    def _load_item(self, idx: int):
        """
        Load a single item from the dataset.
        
        Must be implemented by subclasses to define the specific loading behavior.
        
        Args:
            idx: Index into data_rows list
            
        Returns:
            Item(s) as defined by the subclass (e.g., (image, targets) or (left, right, targets))
        """
        raise NotImplementedError("Subclasses must implement _load_item")
    
    def _load_image(self, image_path: Path):
        """
        Load image from path.
        
        Args:
            image_path: Path to image file
            
        Returns:
            PIL Image in RGB mode
        """
        return load_jpg(image_path, convert_rgb=True)
    
    def _get_targets(self, row: dict) -> torch.Tensor:
        """
        Extract targets from a data row.
        
        Args:
            row: Dictionary containing target values
            
        Returns:
            Tensor of targets [Dry_Green_g, Dry_Clover_g, Dry_Dead_g]
        """
        return torch.tensor([
            row[col] for col in self.target_cols
        ], dtype=torch.float32)
    
    def get_targets(self) -> torch.Tensor:
        """
        Get all targets as a tensor.
        
        Note: This requires loading all target values into memory.
        Use sparingly for memory efficiency.
        
        Returns:
            Tensor of shape (N, 3) with all targets
        """
        targets = torch.tensor([
            [row[col] for col in self.target_cols]
            for row in self.data_rows
        ], dtype=torch.float32)
        return targets

