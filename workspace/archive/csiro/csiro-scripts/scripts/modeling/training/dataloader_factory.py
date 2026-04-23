# dataloader_factory.py
# Factory functions for creating DataLoaders
# Extracted from BaseModelTrainer to improve modularity

import torch
from torch.utils.data import DataLoader
import pandas as pd
import logging
from typing import Optional, Callable, Tuple

from config.config import Config
from dataset_manipulation import StreamingBiomassDataset, StreamingBiomassSplitDataset
from dataset_manipulation.transforms.transform_factory import build_train_transform, build_val_transform

logger = logging.getLogger(__name__)


def create_dataloaders(
    train_data: pd.DataFrame,
    val_data: pd.DataFrame,
    data_root: str,
    config: Config,
    train_transform: Optional[Callable] = None,
    val_transform: Optional[Callable] = None,
    dataset_type: Optional[str] = None
) -> Tuple[DataLoader, DataLoader, Tuple[object, object]]:
    """
    Create training and validation data loaders.
    
    Uses StreamingBiomassDataset (full image) or StreamingBiomassSplitDataset (left/right split)
    for memory-efficient on-demand image loading.
    
    Args:
        train_data: Training DataFrame. Must have 'image_path' column and target columns.
        val_data: Validation DataFrame. Must have 'image_path' column and target columns.
        data_root: Root directory for images (string path).
        config: Configuration object with training and device settings.
        train_transform: Optional transform for training (if None, will be built from config).
        val_transform: Optional transform for validation (if None, will be built from config).
        dataset_type: Dataset type to use ('full' or 'split'). If None, uses config.data.dataset_type.
                     Defaults to 'split' if not specified (standard approach).
        
    Returns:
        Tuple of (train_loader, val_loader, (train_dataset, val_dataset)).
        DataLoader instances and datasets. Datasets are returned for proper cleanup after training.
        
    Raises:
        ValueError: If train_data or val_data are empty or invalid, or dataset_type is invalid.
        TypeError: If train_data or val_data are not DataFrames.
    """
    # Validate inputs
    if not isinstance(train_data, pd.DataFrame):
        raise TypeError(f"train_data must be pandas DataFrame, got {type(train_data)}")
    if not isinstance(val_data, pd.DataFrame):
        raise TypeError(f"val_data must be pandas DataFrame, got {type(val_data)}")
    
    if len(train_data) == 0:
        raise ValueError("train_data cannot be empty")
    if len(val_data) == 0:
        raise ValueError("val_data cannot be empty")
    
    if not isinstance(data_root, str):
        raise TypeError(f"data_root must be string, got {type(data_root)}")
    
    # Determine dataset type (from parameter or config, default to 'split')
    if dataset_type is None:
        dataset_type = getattr(config.data, 'dataset_type', 'split')
    
    if dataset_type not in ['full', 'split']:
        raise ValueError(f"dataset_type must be 'full' or 'split', got {dataset_type}")
    
    # Select dataset class based on type
    if dataset_type == 'split':
        DatasetClass = StreamingBiomassSplitDataset
        logger.info("Using split dataset (left/right halves)")
    else:
        DatasetClass = StreamingBiomassDataset
        logger.info("Using full image dataset")
    
    # Build transforms if not provided
    if train_transform is None:
        train_transform = build_train_transform(config)
    if val_transform is None:
        val_transform = build_val_transform(config)
    
    # Memory optimization: adjust num_workers and pin_memory
    num_workers = config.device.num_workers
    pin_memory = config.device.pin_memory
    
    if getattr(config.device, 'reduce_workers_for_memory', False):
        num_workers = 0  # Disable multiprocessing for memory efficiency
        logger.info("Reduced num_workers to 0 for memory efficiency")
    
    if getattr(config.device, 'disable_pin_memory_for_memory', False):
        pin_memory = False  # Disable pin_memory for memory efficiency
        logger.info("Disabled pin_memory for memory efficiency")
    
    # Create worker_init_fn for deterministic DataLoader behavior
    # This ensures each worker process has its own seed based on the main seed
    def worker_init_fn(worker_id: int) -> None:
        """Initialize worker with deterministic seed."""
        import random
        import numpy as np
        
        # Get seed from config or use default
        seed = getattr(config, 'seed', 42)
        # Each worker gets a unique seed based on worker_id
        worker_seed = seed + worker_id
        
        random.seed(worker_seed)
        np.random.seed(worker_seed)
        torch.manual_seed(worker_seed)
        
        # Set deterministic behavior for this worker
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    
    # Warn if num_workers > 0 and deterministic mode is enabled
    if num_workers > 0:
        if torch.backends.cudnn.deterministic:
            logger.info(
                f"Using {num_workers} DataLoader workers with deterministic worker_init_fn "
                f"(seed={getattr(config, 'seed', 42)})"
            )
        else:
            logger.warning(
                f"⚠️ Using {num_workers} DataLoader workers but deterministic mode is disabled. "
                f"Results may not be fully reproducible."
            )
    
    # Create datasets (using streaming for memory efficiency)
    train_dataset = DatasetClass(
        train_data,
        data_root=data_root,
        transform=train_transform,
        shuffle=True
    )
    val_dataset = DatasetClass(
        val_data,
        data_root=data_root,
        transform=val_transform,
        shuffle=False
    )
    logger.info("Using streaming datasets (memory-efficient)")
    
    # Get DataLoader optimization settings
    prefetch_factor = getattr(config.device, 'prefetch_factor', 2)
    persistent_workers = getattr(config.device, 'persistent_workers', False) if num_workers > 0 else False
    
    # Create data loaders
    # Note: For IterableDataset, shuffle is handled in the dataset itself
    train_loader = DataLoader(
        train_dataset,
        batch_size=config.training.batch_size,
        shuffle=False,  # Shuffle handled in dataset for IterableDataset
        num_workers=num_workers,
        pin_memory=pin_memory,
        prefetch_factor=prefetch_factor,
        persistent_workers=persistent_workers,
        worker_init_fn=worker_init_fn if num_workers > 0 else None
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=config.training.batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory,
        prefetch_factor=prefetch_factor,
        persistent_workers=persistent_workers,
        worker_init_fn=worker_init_fn if num_workers > 0 else None
    )
    
    logger.info(f"Created data loaders:")
    logger.info(f"  Train: {len(train_loader)} batches, {len(train_dataset)} samples")
    logger.info(f"  Val: {len(val_loader)} batches, {len(val_dataset)} samples")
    logger.info(f"  Batch size: {config.training.batch_size}")
    logger.info(f"  Num workers: {num_workers}")
    logger.info(f"  Pin memory: {pin_memory}")
    logger.info(f"  Prefetch factor: {prefetch_factor}")
    logger.info(f"  Persistent workers: {persistent_workers}")
    
    return train_loader, val_loader, (train_dataset, val_dataset)


def create_dataloader_with_transform(
    data: pd.DataFrame,
    data_root: str,
    config: Config,
    transform: Callable,
    dataset_type: Optional[str] = None,
    shuffle: bool = False
) -> DataLoader:
    """
    Create dataloader with specific transform (for TTA during training).
    
    Args:
        data: DataFrame with 'image_path' column and target columns.
        data_root: Root directory for images (string path).
        config: Configuration object with training and device settings.
        transform: Specific transform to use for this dataloader.
        dataset_type: Dataset type to use ('full' or 'split'). If None, uses config.data.dataset_type.
                     Defaults to 'split' if not specified (standard approach).
        shuffle: Whether to shuffle the dataset (default: False).
        
    Returns:
        DataLoader with specified transform
        
    Raises:
        ValueError: If data is empty or invalid, or dataset_type is invalid
        TypeError: If data is not a DataFrame
    """
    # Validate inputs
    if not isinstance(data, pd.DataFrame):
        raise TypeError(f"data must be pandas DataFrame, got {type(data)}")
    
    if len(data) == 0:
        raise ValueError("data cannot be empty")
    
    if not isinstance(data_root, str):
        raise TypeError(f"data_root must be string, got {type(data_root)}")
    
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
    
    # Memory optimization: adjust num_workers and pin_memory
    num_workers = config.device.num_workers
    pin_memory = config.device.pin_memory
    
    if getattr(config.device, 'reduce_workers_for_memory', False):
        num_workers = 0  # Disable multiprocessing for memory efficiency
        logger.info("Reduced num_workers to 0 for memory efficiency")
    
    if getattr(config.device, 'disable_pin_memory_for_memory', False):
        pin_memory = False  # Disable pin_memory for memory efficiency
        logger.info("Disabled pin_memory for memory efficiency")
    
    # Create worker_init_fn for deterministic DataLoader behavior
    def worker_init_fn(worker_id: int) -> None:
        """Initialize worker with deterministic seed."""
        import random
        import numpy as np
        
        # Get seed from config or use default
        seed = getattr(config, 'seed', 42)
        # Each worker gets a unique seed based on worker_id
        worker_seed = seed + worker_id
        
        random.seed(worker_seed)
        np.random.seed(worker_seed)
        torch.manual_seed(worker_seed)
        
        # Set deterministic behavior for this worker
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    
    # Create dataset
    dataset = DatasetClass(
        data,
        data_root=data_root,
        transform=transform,
        shuffle=shuffle
    )
    
    # Get DataLoader optimization settings
    prefetch_factor = getattr(config.device, 'prefetch_factor', 2)
    persistent_workers = getattr(config.device, 'persistent_workers', False) if num_workers > 0 else False
    
    # Create data loader
    loader = DataLoader(
        dataset,
        batch_size=config.training.batch_size,
        shuffle=False,  # Shuffle handled in dataset for IterableDataset
        num_workers=num_workers,
        pin_memory=pin_memory,
        prefetch_factor=prefetch_factor,
        persistent_workers=persistent_workers,
        worker_init_fn=worker_init_fn if num_workers > 0 else None
    )
    
    return loader

