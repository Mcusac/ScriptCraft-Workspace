# submission.py
# Submission format conversion and file I/O

import torch
import numpy as np
import pandas as pd
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List

from config.evaluation_constants import (
    PRIMARY_TARGETS,
    NUM_PRIMARY_TARGETS
)
from modeling.evaluation.post_processing import post_process_biomass
from config.config import Config
from .inference import run_inference
import warnings

# Import contest abstractions
try:
    from contest.registry import get_contest_config, get_contest_data_schema
    _get_contest_config = get_contest_config
    _get_contest_data_schema = get_contest_data_schema
except (ImportError, ValueError) as e:
    # Fallback to direct CSIRO import if registry not available
    warnings.warn(
        f"Could not load contest abstractions from registry: {e}. "
        f"Falling back to direct CSIRO import.",
        UserWarning
    )
    from contest.csiro.config import get_csiro_config
    from contest.csiro.data_schema import get_csiro_data_schema
    _get_contest_config = get_csiro_config
    _get_contest_data_schema = get_csiro_data_schema

logger = logging.getLogger(__name__)


def expand_predictions_to_submission_format(
    predictions: np.ndarray,
    test_csv_path: str
) -> pd.DataFrame:
    """
    Expand primary target predictions to all targets and match submission format.
    
    Args:
        predictions: Predictions array, shape (N, NUM_PRIMARY_TARGETS) - primary targets.
                     Must be numpy array with 2 dimensions, NUM_PRIMARY_TARGETS columns.
        test_csv_path: Path to test.csv for sample_id format. Must exist and contain 'image_path' column.
        
    Returns:
        DataFrame with columns: sample_id, target.
        Contains N * NUM_TOTAL_TARGETS rows (one per image per target).
        
    Raises:
        ValueError: If predictions have invalid shape or test CSV is invalid.
        TypeError: If inputs have wrong types.
        FileNotFoundError: If test_csv_path doesn't exist.
    """
    # Validate inputs
    if not isinstance(predictions, np.ndarray):
        raise TypeError(f"predictions must be numpy array, got {type(predictions)}")
    
    if predictions.ndim != 2:
        raise ValueError(f"predictions must be 2D array, got shape {predictions.shape}")
    
    if predictions.shape[1] != NUM_PRIMARY_TARGETS:
        raise ValueError(
            f"predictions must have {NUM_PRIMARY_TARGETS} columns, got {predictions.shape[1]}. "
            f"Expected {PRIMARY_TARGETS}"
        )
    
    if not isinstance(test_csv_path, str) or not test_csv_path:
        raise ValueError(f"test_csv_path must be non-empty string, got {test_csv_path}")
    
    # Get unique images
    from dataset_manipulation import load_and_validate_test_data
    unique_images = load_and_validate_test_data(test_csv_path)
    
    if len(unique_images) != predictions.shape[0]:
        raise ValueError(
            f"Number of unique images ({len(unique_images)}) doesn't match "
            f"predictions count ({predictions.shape[0]})"
        )
    
    # Get contest config and data schema
    contest_config = _get_contest_config()
    data_schema = _get_contest_data_schema()
    
    # Create DataFrame with all targets for post-processing
    # First, compute all targets from primary predictions
    # Uses contest config for target definitions
    targets_df = pd.DataFrame(index=range(len(unique_images)), columns=contest_config.all_targets)
    
    for idx, row in unique_images.iterrows():
        # Get primary targets from predictions (order defined by contest config)
        primary_targets = contest_config.primary_targets
        if len(primary_targets) != predictions.shape[1]:
            raise ValueError(
                f"Number of primary targets ({len(primary_targets)}) doesn't match "
                f"predictions shape ({predictions.shape[1]})"
            )
        
        # Extract primary target values (order matches PRIMARY_TARGETS from contest config)
        primary_values = [float(predictions[idx, i]) for i in range(len(primary_targets))]
        
        # Compute all target values (primary + derived) using contest config
        target_values = contest_config.compute_derived_target_values(*primary_values)
        
        for target_name in contest_config.all_targets:
            targets_df.loc[idx, target_name] = target_values[target_name]
    
    # Apply post-processing to enforce physical constraints
    targets_df = post_process_biomass(targets_df)
    
    # Create submission DataFrame from post-processed targets
    submission_rows: List[Dict[str, Any]] = []
    
    image_path_col = data_schema.image_path_column
    for idx, row in unique_images.iterrows():
        image_id = Path(row[image_path_col]).stem  # e.g., 'ID1001187975'
        
        # Get post-processed target values
        for target_name in contest_config.all_targets:
            value = float(targets_df.loc[idx, target_name])
            
            # Use contest schema to format sample_id
            sample_id = data_schema.format_sample_id(image_id, target_name)
            submission_rows.append({
                'sample_id': sample_id,
                'target': value
            })
    
    submission_df = pd.DataFrame(submission_rows)
    
    # Verify we have the right number of rows
    expected_rows = len(unique_images) * len(contest_config.all_targets)
    if len(submission_df) != expected_rows:
        raise ValueError(
            f"Submission format error: Expected {expected_rows} rows, got {len(submission_df)}"
        )
    
    # Verify required columns exist
    if 'sample_id' not in submission_df.columns or 'target' not in submission_df.columns:
        raise ValueError(
            f"Submission DataFrame missing required columns. "
            f"Got: {submission_df.columns.tolist()}"
        )
    
    logger.info(f"Expanded {len(unique_images)} images to {len(submission_df)} submission rows")
    
    return submission_df


def save_submission_file(
    submission_df: pd.DataFrame,
    config: Config,
    output_path: Optional[str] = None
) -> Path:
    """
    Save submission DataFrame to file(s).
    
    Delegates to modeling.utils.submission_utils to avoid code duplication.
    
    Args:
        submission_df: Submission DataFrame with columns: sample_id, target.
        config: Configuration object with paths settings.
        output_path: Optional explicit output path. If None, uses config.paths.
        
    Returns:
        Path to the saved submission file.
        
    Raises:
        ValueError: If submission_df is invalid or config is None.
        IOError: If file cannot be written.
    """
    from modeling.utils import save_submission_file as _save_submission_file
    return _save_submission_file(submission_df, config, output_path)


def create_submission(
    model: torch.nn.Module,
    test_csv_path: str,
    data_root: str,
    config: Config,
    device: torch.device,
    output_path: str = 'submission.csv'
) -> pd.DataFrame:
    """
    Create submission file from model predictions.
    
    Args:
        model: Trained model ready for inference. Should be in eval mode.
        test_csv_path: Path to test.csv file. Must exist and contain 'image_path' column.
        data_root: Root directory for images (string path).
        config: Configuration object with training and device settings.
                Must have config.training.batch_size and config.device attributes.
        device: Device to run inference on (e.g., torch.device('cuda')).
        output_path: Path to save submission CSV (default: 'submission.csv').
                    Parent directory will be created if it doesn't exist.
        
    Returns:
        Submission DataFrame with columns: sample_id, target.
        Contains N * 5 rows where N is number of unique images.
        
    Raises:
        ValueError: If inputs are invalid or submission format is incorrect.
        TypeError: If inputs have wrong types.
        FileNotFoundError: If test_csv_path doesn't exist.
        IOError: If submission file cannot be written.
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
    
    if not isinstance(output_path, str) or not output_path:
        raise ValueError(f"output_path must be non-empty string, got {output_path}")
    
    # Run inference
    predictions = run_inference(
        model=model,
        test_csv_path=test_csv_path,
        data_root=data_root,
        config=config,
        device=device
    )
    
    # Expand to submission format
    submission_df = expand_predictions_to_submission_format(
        predictions=predictions,
        test_csv_path=test_csv_path
    )
    
    # Save submission
    output_path_obj = save_submission_file(submission_df, config, output_path)
    
    logger.info(f"Submission shape: {submission_df.shape}")
    logger.info(f"Sample submission:\n{submission_df.head(10)}")
    
    return submission_df
