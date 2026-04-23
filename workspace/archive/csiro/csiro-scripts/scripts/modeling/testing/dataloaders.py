# dataloaders.py
# Test dataloader creation utilities

import logging
from torch.utils.data import DataLoader
from typing import Optional, Callable
import pandas as pd

from dataset_manipulation import StreamingBiomassDataset, StreamingBiomassSplitDataset
from dataset_manipulation.transforms.transform_factory import build_val_transform
from config.evaluation_constants import PRIMARY_TARGETS
from config.config import Config

logger = logging.getLogger(__name__)


def create_test_dataloader(
    test_csv_path: str,
    data_root: str,
    config: Config,
    batch_size: Optional[int] = None,
    dataset_type: Optional[str] = None
) -> DataLoader:
    """
    Create DataLoader for test set inference.
    
    Shared utility for creating test DataLoader with consistent transforms.
    Used by both single model and ensemble inference.
    
    Args:
        test_csv_path: Path to test.csv file. Must exist and contain 'image_path' column.
        data_root: Root directory for images (string path).
        config: Configuration object with training and device settings.
        batch_size: Optional batch size override. If None, uses config.training.batch_size.
        dataset_type: Dataset type to use ('full' or 'split'). If None, uses config.data.dataset_type.
                     Defaults to 'split' if not specified (standard approach).
        
    Returns:
        DataLoader for test dataset
        
    Raises:
        ValueError: If test CSV is invalid or empty, or dataset_type is invalid
        FileNotFoundError: If test_csv_path doesn't exist
    """
    # Load test data and get unique images
    from dataset_manipulation import load_and_validate_test_data
    unique_images = load_and_validate_test_data(test_csv_path)
    
    # Determine dataset type (from parameter or config, default to 'split')
    if dataset_type is None:
        dataset_type = getattr(config.data, 'dataset_type', 'split')
    
    if dataset_type not in ['full', 'split']:
        raise ValueError(f"dataset_type must be 'full' or 'split', got {dataset_type}")
    
    # Select dataset class based on type
    if dataset_type == 'split':
        DatasetClass = StreamingBiomassSplitDataset
    else:
        DatasetClass = StreamingBiomassDataset
    
    # Create transforms using factory (no augmentation for inference)
    transform = build_val_transform(config)
    
    # Create dataset (we need to create a dummy DataFrame with image_path)
    # For inference, we don't need targets
    test_data_dict = {'image_path': unique_images['image_path']}
    for target in PRIMARY_TARGETS:
        test_data_dict[target] = [0.0] * len(unique_images)
    test_data = pd.DataFrame(test_data_dict)
    
    test_dataset = DatasetClass(
        test_data,
        data_root=data_root,
        transform=transform,
        shuffle=False
    )
    
    batch_size = batch_size or config.training.batch_size
    # Get DataLoader optimization settings
    prefetch_factor = getattr(config.device, 'prefetch_factor', 2)
    persistent_workers = getattr(config.device, 'persistent_workers', False) if config.device.num_workers > 0 else False
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=config.device.num_workers,
        pin_memory=config.device.pin_memory,
        prefetch_factor=prefetch_factor,
        persistent_workers=persistent_workers
    )
    
    return test_loader


def create_test_dataloader_with_transform(
    test_csv_path: str,
    data_root: str,
    config: Config,
    transform: Callable,
    batch_size: Optional[int] = None,
    dataset_type: Optional[str] = None
) -> DataLoader:
    """
    Create test dataloader with specific transform (for TTA).
    
    Reuses existing create_test_dataloader() logic but accepts specific transform.
    
    Args:
        test_csv_path: Path to test.csv file. Must exist and contain 'image_path' column.
        data_root: Root directory for images (string path).
        config: Configuration object with training and device settings.
        transform: Specific transform to use for this dataloader.
        batch_size: Optional batch size override. If None, uses config.training.batch_size.
        dataset_type: Dataset type to use ('full' or 'split'). If None, uses config.data.dataset_type.
                     Defaults to 'split' if not specified (standard approach).
        
    Returns:
        DataLoader for test dataset with specified transform
        
    Raises:
        ValueError: If test CSV is invalid or empty, or dataset_type is invalid
        FileNotFoundError: If test_csv_path doesn't exist
    """
    from dataset_manipulation import load_and_validate_test_data
    
    # Load test data and get unique images
    unique_images = load_and_validate_test_data(test_csv_path)
    
    # Determine dataset type (from parameter or config, default to 'split')
    if dataset_type is None:
        dataset_type = getattr(config.data, 'dataset_type', 'split')
    
    if dataset_type not in ['full', 'split']:
        raise ValueError(f"dataset_type must be 'full' or 'split', got {dataset_type}")
    
    # Select dataset class based on type
    if dataset_type == 'split':
        DatasetClass = StreamingBiomassSplitDataset
    else:
        DatasetClass = StreamingBiomassDataset
    
    # Create dataset (we need to create a dummy DataFrame with image_path)
    # For inference, we don't need targets
    test_data_dict = {'image_path': unique_images['image_path']}
    for target in PRIMARY_TARGETS:
        test_data_dict[target] = [0.0] * len(unique_images)
    test_data = pd.DataFrame(test_data_dict)
    
    test_dataset = DatasetClass(
        test_data,
        data_root=data_root,
        transform=transform,
        shuffle=False
    )
    
    batch_size = batch_size or config.training.batch_size
    # Get DataLoader optimization settings
    prefetch_factor = getattr(config.device, 'prefetch_factor', 2)
    persistent_workers = getattr(config.device, 'persistent_workers', False) if config.device.num_workers > 0 else False
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=config.device.num_workers,
        pin_memory=config.device.pin_memory,
        prefetch_factor=prefetch_factor,
        persistent_workers=persistent_workers
    )
    
    return test_loader
