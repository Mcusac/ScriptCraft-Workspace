# inference.py
# Core inference execution for end-to-end models

import torch
import numpy as np
import logging
from typing import Optional, List

from config.evaluation_constants import NUM_PRIMARY_TARGETS
from config.config import Config
from .dataloaders import create_test_dataloader
from .validation import validate_predictions_shape

logger = logging.getLogger(__name__)


def _process_inference_batch(
    batch: tuple,
    model: torch.nn.Module,
    device: torch.device,
    dataset_type: str
) -> torch.Tensor:
    """
    Process a single batch for inference, handling both full and split dataset types.
    
    Args:
        batch: Batch from DataLoader - either (images, targets) for 'full' dataset,
               or (left_img, right_img, targets) for 'split' dataset
        model: Model to run inference with (supports dual input for split datasets)
        device: Device to run inference on
        dataset_type: 'full' or 'split' - determines batch format
    
    Returns:
        Model outputs tensor
    
    Note:
        For split dataset type, the model processes both left and right images
        and averages their outputs for final predictions.
    """
    from modeling.utils import process_batch_for_model
    
    return process_batch_for_model(batch, model, device, dataset_type)


def run_inference(
    model: torch.nn.Module,
    test_csv_path: str,
    data_root: str,
    config: Config,
    device: torch.device,
    batch_size: Optional[int] = None
) -> np.ndarray:
    """
    Run inference on test set.
    
    Args:
        model: Trained model ready for inference. Should be in eval mode.
        test_csv_path: Path to test.csv file. Must exist and contain 'image_path' column.
        data_root: Root directory for images (string path).
        config: Configuration object with training and device settings.
                Must have config.training.batch_size and config.device attributes.
        device: Device to run inference on (e.g., torch.device('cuda')).
        batch_size: Optional batch size override. If None, uses config.training.batch_size.
                   Must be positive if provided.
        
    Returns:
        Predictions array of shape (N, 3) where N is number of unique images.
        Columns are [Dry_Green_g, Dry_Clover_g, Dry_Dead_g].
        
    Raises:
        ValueError: If inputs are invalid, test CSV is empty, or predictions have wrong shape.
        TypeError: If inputs have wrong types.
        FileNotFoundError: If test_csv_path doesn't exist.
    """
    # Validate inputs
    if not isinstance(model, torch.nn.Module):
        raise TypeError(f"model must be torch.nn.Module, got {type(model)}")
    
    if not isinstance(test_csv_path, str) or not test_csv_path:
        raise ValueError(f"test_csv_path must be non-empty string, got {test_csv_path}")
    
    if not isinstance(data_root, str) or not data_root:
        raise ValueError(f"data_root must be non-empty string, got {data_root}")
    
    if config is None:
        raise ValueError("config cannot be None")
    
    if not isinstance(device, torch.device):
        raise TypeError(f"device must be torch.device, got {type(device)}")
    
    if batch_size is not None and (not isinstance(batch_size, int) or batch_size < 1):
        raise ValueError(f"batch_size must be positive integer, got {batch_size}")
    
    model.eval()
    model.to(device)
    
    # Create test DataLoader (reusing shared utility)
    test_loader = create_test_dataloader(
        test_csv_path=test_csv_path,
        data_root=data_root,
        config=config,
        batch_size=batch_size
    )
    
    # Get number of unique images for validation
    from dataset_manipulation import load_and_validate_test_data
    unique_images = load_and_validate_test_data(test_csv_path)
    
    # Determine dataset type for handling different output formats
    dataset_type = getattr(config.data, 'dataset_type', 'split')
    
    # Run inference
    all_predictions: List[np.ndarray] = []
    
    logger.info(f"Running inference on {len(unique_images)} images (dataset_type: {dataset_type})")
    with torch.no_grad():
        for batch in test_loader:
            outputs = _process_inference_batch(batch, model, device, dataset_type)
            all_predictions.append(outputs.detach().cpu().numpy())
    
    if not all_predictions:
        raise ValueError("No predictions generated - inference produced empty results")
    
    predictions = np.concatenate(all_predictions, axis=0)
    
    # Validate predictions shape
    validate_predictions_shape(predictions, len(unique_images), expected_cols=NUM_PRIMARY_TARGETS)
    
    logger.info(f"Inference complete. Predictions shape: {predictions.shape}")
    
    return predictions
