# submission_utils.py
# Utilities for saving submission files
#
# Centralizes submission file saving logic to avoid duplication across
# inference.py, test_only.py, and other pipeline files.

import logging
from pathlib import Path
from typing import Optional

import pandas as pd

from config.config import Config
from utils.system import is_kaggle_environment
from utils.system import get_submission_path

logger = logging.getLogger(__name__)


def save_submission_file(
    submission_df: pd.DataFrame,
    config: Config,
    output_path: Optional[str] = None
) -> Path:
    """
    Save submission DataFrame to file(s).
    
    Saves to config output directory and optionally to Kaggle working directory
    if in Kaggle environment. This centralizes submission saving logic to avoid
    duplication across multiple pipeline files.
    
    Args:
        submission_df: Submission DataFrame with columns: sample_id, target.
                       Must not be None or empty.
        config: Configuration object with paths settings. Must not be None.
        output_path: Optional explicit output path. If None, uses config.paths.
        
    Returns:
        Path to the saved submission file (primary output path).
        
    Raises:
        ValueError: If submission_df is invalid or config is None.
        IOError: If file cannot be written.
    """
    if submission_df is None or len(submission_df) == 0:
        raise ValueError("submission_df cannot be None or empty")
    
    if config is None:
        raise ValueError("config cannot be None")
    
    # Determine primary output path
    if output_path is None:
        output_path_obj = Path(config.paths.output_dir) / config.paths.submission_file
    else:
        output_path_obj = Path(output_path)
    
    # Ensure parent directory exists
    output_path_obj.parent.mkdir(parents=True, exist_ok=True)
    
    # Save to primary location
    try:
        submission_df.to_csv(output_path_obj, index=False)
        logger.info(f"Saved submission to: {output_path_obj}")
    except Exception as e:
        raise IOError(f"Failed to save submission to {output_path_obj}: {e}")
    
    # Also save to /kaggle/working for Kaggle submission (if on Kaggle)
    if is_kaggle_environment():
        kaggle_submission_path = get_submission_path()
        submission_df.to_csv(kaggle_submission_path, index=False)
        logger.info(f"Submission also saved to: {kaggle_submission_path}")
    
    return output_path_obj

