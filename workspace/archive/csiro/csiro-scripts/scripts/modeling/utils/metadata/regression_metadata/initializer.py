# initializer.py
# Initialization utilities for regression metadata

import logging
import shutil
from pathlib import Path
from typing import Tuple

from utils.system.io import save_json_file
from ..data_manipulation_loader import find_metadata_dir, get_writable_metadata_dir

logger = logging.getLogger(__name__)


def initialize_working_metadata_files(
    regression_model_type: str
) -> Tuple[Path, Path]:
    """
    Initialize working metadata directory by copying from input (always fresh copy).
    
    ALWAYS copies from input directory to working directory (overwrites existing).
    This ensures we start with the latest uploaded metadata files every run.
    
    Args:
        regression_model_type: Type of regression model ('lgbm', 'xgboost', 'ridge')
        
    Returns:
        Tuple of (metadata_file_path, gridsearch_file_path) in working directory.
    """
    # Validate regression model type
    valid_types = {'lgbm', 'xgboost', 'ridge'}
    if regression_model_type not in valid_types:
        raise ValueError(
            f"Invalid regression_model_type: {regression_model_type}. "
            f"Must be one of: {valid_types}"
        )
    
    # Get writable working directory
    working_dir = get_writable_metadata_dir() / regression_model_type
    working_dir.mkdir(parents=True, exist_ok=True)
    
    # Get input directory (if it exists)
    input_dir = find_metadata_dir()
    input_metadata_file = None
    input_gridsearch_file = None
    
    if input_dir and str(input_dir).startswith('/kaggle/input'):
        input_metadata_file = input_dir / regression_model_type / 'metadata.json'
        input_gridsearch_file = input_dir / regression_model_type / 'gridsearch_metadata.json'
    
    # Working directory file paths
    working_metadata_file = working_dir / 'metadata.json'
    working_gridsearch_file = working_dir / 'gridsearch_metadata.json'
    
    # ALWAYS copy metadata.json from input if it exists (fresh copy every run)
    if input_metadata_file and input_metadata_file.exists():
        shutil.copy2(input_metadata_file, working_metadata_file)
        logger.info(f"Copied fresh metadata.json from input to working: {working_metadata_file}")
    elif not working_metadata_file.exists():
        # Create empty file if input doesn't exist and working doesn't exist
        working_metadata_file.parent.mkdir(parents=True, exist_ok=True)
        save_json_file([], working_metadata_file, file_type="Regression metadata JSON")
        logger.info(f"Created new metadata.json in working directory: {working_metadata_file}")
    
    # ALWAYS copy gridsearch_metadata.json from input if it exists (fresh copy every run)
    if input_gridsearch_file and input_gridsearch_file.exists():
        shutil.copy2(input_gridsearch_file, working_gridsearch_file)
        logger.info(f"Copied fresh gridsearch_metadata.json from input to working: {working_gridsearch_file}")
    elif not working_gridsearch_file.exists():
        # Create empty file if input doesn't exist and working doesn't exist
        save_json_file([], working_gridsearch_file, file_type="Regression gridsearch metadata JSON")
        logger.info(f"Created new gridsearch_metadata.json in working directory: {working_gridsearch_file}")
    
    return working_metadata_file, working_gridsearch_file
