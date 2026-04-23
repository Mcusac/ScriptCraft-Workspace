# info.py
# Checkpoint metadata and info loading utilities

import torch
import logging
import json
from pathlib import Path
from typing import Optional, Dict, Tuple, Any

logger = logging.getLogger(__name__)


def load_checkpoint_info(checkpoint_path: Path) -> Optional[Dict[str, Any]]:
    """
    Load checkpoint metadata without loading the full model.
    
    Useful for checking if training is complete without loading the entire model state.
    Only loads metadata (epoch, best_score, history) for efficiency.
    
    Args:
        checkpoint_path: Path to checkpoint file. Can be string or Path object.
        
    Returns:
        Dictionary with checkpoint info if file exists and is valid:
        - 'best_score': Best validation score (float)
        - 'history': Training history (List[Dict])
        - 'epoch': Epoch number when checkpoint was saved (int)
        - 'exists': Always True if returned
        Returns None if file doesn't exist or cannot be loaded.
        
    Raises:
        TypeError: If checkpoint_path is not Path or string.
    """
    # Validate input
    if checkpoint_path is None:
        return None
    
    checkpoint_path_obj = Path(checkpoint_path)
    
    if not checkpoint_path_obj.exists():
        return None
    
    if not checkpoint_path_obj.is_file():
        logger.warning(f"Checkpoint path is not a file: {checkpoint_path_obj}")
        return None
    
    try:
        checkpoint = torch.load(checkpoint_path_obj, map_location='cpu', weights_only=False)
        
        # Validate checkpoint structure
        if not isinstance(checkpoint, dict):
            logger.warning(f"Checkpoint is not a dictionary: {checkpoint_path_obj}")
            return None
        
        return {
            'best_score': checkpoint.get('best_score', -float('inf')),
            'history': checkpoint.get('history', []),
            'epoch': checkpoint.get('epoch', 0),
            'exists': True
        }
    except (KeyError, TypeError, ValueError) as e:
        # Handle malformed checkpoint data
        logger.warning(f"Failed to load checkpoint info from {checkpoint_path_obj}: Invalid checkpoint format: {e}")
        return None
    except (OSError, PermissionError) as e:
        # Handle file system errors
        logger.warning(f"Failed to load checkpoint info from {checkpoint_path_obj}: File system error: {e}")
        return None
    except Exception as e:
        # Catch any other unexpected errors
        logger.warning(f"Failed to load checkpoint info from {checkpoint_path_obj}: Unexpected error: {e}", exc_info=True)
        return None


def is_checkpoint_complete(checkpoint_path: Path, min_epochs: int = 1) -> Tuple[bool, Optional[Dict]]:
    """
    Check if a checkpoint exists and appears to be from a complete training run.
    
    Args:
        checkpoint_path: Path to checkpoint file
        min_epochs: Minimum number of epochs to consider training complete
        
    Returns:
        Tuple of (is_complete, checkpoint_info)
        - is_complete: True if checkpoint exists and appears complete
        - checkpoint_info: Dictionary with checkpoint info, or None if not found
    """
    info = load_checkpoint_info(checkpoint_path)
    
    if info is None:
        return False, None
    
    # Check if training appears complete
    existing_epochs = len(info.get('history', []))
    existing_score = info.get('best_score', -float('inf'))
    
    is_complete = (
        existing_epochs >= min_epochs and 
        existing_score > -float('inf')
    )
    
    return is_complete, info


def load_regression_model_info(metadata_path: Path) -> Optional[Dict[str, Any]]:
    """
    Load regression model metadata from JSON file.
    
    Args:
        metadata_path: Path to regression_model_info.json file
        
    Returns:
        Dictionary with metadata:
        - 'best_score': Best validation score (float)
        - 'val_score': Validation score (float)
        - 'history': Training history (List[Dict])
        - 'epoch': Always 0 for regression models
        - 'exists': Always True if returned
        - 'model_type': 'regression'
        - 'regression_model_type': Type of regression model (str)
        Returns None if file doesn't exist or cannot be loaded.
        
    Raises:
        TypeError: If metadata_path is not Path or string.
    """
    # Validate input
    if metadata_path is None:
        return None
    
    metadata_path_obj = Path(metadata_path)
    
    if not metadata_path_obj.exists():
        return None
    
    if not metadata_path_obj.is_file():
        logger.warning(f"Metadata path is not a file: {metadata_path_obj}")
        return None
    
    try:
        with open(metadata_path_obj, 'r') as f:
            metadata = json.load(f)
        
        # Validate metadata structure
        if not isinstance(metadata, dict):
            logger.warning(f"Metadata is not a dictionary: {metadata_path_obj}")
            return None
        
        # Validate required fields
        if 'best_score' not in metadata:
            logger.warning(f"Metadata missing 'best_score' field: {metadata_path_obj}")
            logger.warning(f"  Available keys: {list(metadata.keys())}")
            logger.warning(f"  Metadata content: {metadata}")
            return None
        
        # Ensure best_score is a valid number
        best_score = metadata.get('best_score')
        try:
            float(best_score)  # Validate it's a number
        except (TypeError, ValueError):
            logger.warning(f"Metadata 'best_score' is not a valid number: {best_score} (type: {type(best_score)})")
            return None
        
        return metadata
    except json.JSONDecodeError as e:
        logger.warning(f"Invalid JSON in regression model info: {metadata_path_obj}: {e}")
        return None
    except (OSError, PermissionError) as e:
        logger.warning(f"Failed to load regression model info from {metadata_path_obj}: File system error: {e}")
        return None
    except Exception as e:
        # Catch any other unexpected errors
        logger.warning(f"Failed to load regression model info from {metadata_path_obj}: Unexpected error: {e}", exc_info=True)
        return None
