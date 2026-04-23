# tta.py
# Test-time augmentation inference

import torch
import numpy as np
import logging
from pathlib import Path
from typing import Optional

from config.config import Config

logger = logging.getLogger(__name__)


def run_inference_with_tta(
    model: torch.nn.Module,
    test_csv_path: str,
    data_root: str,
    config: Config,
    device: torch.device,
    batch_size: Optional[int] = None,
    num_tta: int = 6
) -> np.ndarray:
    """
    Run inference with test-time augmentation (TTA).
    
    Applies multiple augmentations to test images and averages model predictions
    across augmentations for more robust predictions.
    
    Args:
        model: Trained model ready for inference. Should be in eval mode.
        test_csv_path: Path to test.csv file. Must exist and contain 'image_path' column.
        data_root: Root directory for images (string path).
        config: Configuration object with training and device settings.
        device: Device to run inference on (e.g., torch.device('cuda')).
        batch_size: Optional batch size override. If None, uses config.training.batch_size.
        num_tta: Number of TTA augmentations to apply (default: 6).
                Must be positive integer <= 6 (limited by available augmentations).
        
    Returns:
        Predictions array of shape (N, 3) where N is number of unique images.
        Columns are [Dry_Green_g, Dry_Clover_g, Dry_Dead_g].
        Values are averaged across all TTA variants.
        
    Raises:
        ValueError: If num_tta is invalid or inputs are invalid.
        ImportError: If dataset_manipulation.transforms.tta_transforms not available.
    """
    # Validate num_tta
    if not isinstance(num_tta, int) or num_tta < 1:
        raise ValueError(f"num_tta must be positive integer, got {num_tta}")
    
    logger.info(f"Running inference with TTA ({num_tta} augmentations)")
    
    # Get TTA transforms using unified system
    from dataset_manipulation.transforms.transform_factory import build_tta_transforms
    
    # Get TTA variants (from config or use defaults)
    tta_variants = None
    if hasattr(config.data, 'tta_variants') and config.data.tta_variants:
        tta_variants = config.data.tta_variants
    
    # Build TTA transforms (returns list of torchvision transforms)
    all_tta_transforms = build_tta_transforms(config, tta_variants=tta_variants)
    
    # Limit to requested number
    if num_tta > len(all_tta_transforms):
        logger.warning(
            f"Requested {num_tta} TTA variants but only {len(all_tta_transforms)} available. "
            f"Using all {len(all_tta_transforms)} variants."
        )
        num_tta = len(all_tta_transforms)
    
    tta_transforms = all_tta_transforms[:num_tta]
    
    # Load test images
    from dataset_manipulation import load_and_validate_test_data
    from PIL import Image
    
    unique_images = load_and_validate_test_data(test_csv_path)
    all_tta_predictions = []
    
    logger.info(f"Running {len(tta_transforms)} TTA variants on {len(unique_images)} images")
    
    # Run inference for each TTA variant
    for tta_idx, tta_transform in enumerate(tta_transforms):
        logger.info(f"  TTA variant {tta_idx + 1}/{len(tta_transforms)}")
        
        # Load and transform test images
        # Note: New unified system uses torchvision transforms that work with PIL Images
        transformed_images = []
        for _, row in unique_images.iterrows():
            image_path = Path(data_root) / row['image_path']
            image = Image.open(image_path).convert('RGB')
            # Apply transform (torchvision transform expects PIL Image)
            transformed = tta_transform(image)
            transformed_images.append(transformed)
        
        # Stack transformed images into batch tensor
        # Each transform returns tensor of shape (C, H, W)
        transformed_batch = torch.stack(transformed_images)  # (N, C, H, W)
        
        # Run inference on this TTA variant
        model.eval()
        with torch.no_grad():
            transformed_batch = transformed_batch.to(device)
            
            # For split dataset, we need to handle left/right splits
            # For now, just run single inference (full image)
            predictions = model(transformed_batch)  # (N, 3)
        
        all_tta_predictions.append(predictions.cpu().numpy())
    
    # Average predictions across all TTA variants
    all_tta_predictions = np.array(all_tta_predictions)  # (num_tta, N, 3)
    averaged_predictions = np.mean(all_tta_predictions, axis=0)  # (N, 3)
    
    logger.info(f"TTA complete. Averaged predictions shape: {averaged_predictions.shape}")
    
    return averaged_predictions
