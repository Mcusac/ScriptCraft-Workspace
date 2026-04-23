# load_csv.py
# CSV loading utilities with error handling

import pandas as pd
from pathlib import Path
from typing import Union, List
import logging

from utils.system import validate_path_is_file
from dataset_manipulation.utils.loading_utils import batch_process_with_progress

logger = logging.getLogger(__name__)


def load_csv(path: Union[str, Path], **kwargs) -> pd.DataFrame:
    """
    Load CSV file with comprehensive error handling.
    
    Args:
        path: Path to CSV file. Can be string or Path object.
        **kwargs: Additional arguments to pass to pd.read_csv.
                  Common options: sep, header, index_col, dtype, etc.
        
    Returns:
        DataFrame containing the loaded CSV data.
        
    Raises:
        FileNotFoundError: If file doesn't exist at the specified path.
        pd.errors.EmptyDataError: If file exists but is empty.
        pd.errors.ParserError: If file cannot be parsed as CSV.
        PermissionError: If file cannot be read due to permissions.
        ValueError: If path is invalid or empty.
    """
    # Validate path
    path_obj = validate_path_is_file(path, file_type="CSV")
    
    try:
        df = pd.read_csv(path_obj, **kwargs)
        logger.info(f"Loaded CSV: {path} ({len(df)} rows, {len(df.columns)} columns)")
        return df
    except pd.errors.EmptyDataError as e:
        logger.error(f"CSV file is empty: {path}")
        raise
    except pd.errors.ParserError as e:
        logger.error(f"Error parsing CSV {path}: {e}")
        raise
    except PermissionError as e:
        logger.error(f"Permission denied reading CSV {path}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading CSV {path}: {e}", exc_info=True)
        raise


def load_and_validate_test_data(test_csv_path: Union[str, Path]) -> pd.DataFrame:
    """
    Load test CSV and extract unique images with validation.
    
    Common pattern used across multiple pipeline files for loading test data.
    Test CSV has 5 rows per image (one per target), this function extracts
    unique images and validates the CSV structure.
    
    Args:
        test_csv_path: Path to test.csv file. Must exist and contain 'image_path' column.
        
    Returns:
        DataFrame with unique images (one row per image).
        Contains 'image_path' column and other metadata columns.
        
    Raises:
        ValueError: If test CSV is empty, missing 'image_path' column, or has no unique images.
        FileNotFoundError: If test_csv_path doesn't exist.
    """
    # Load test CSV
    test_df = load_csv(test_csv_path)
    
    if len(test_df) == 0:
        raise ValueError(f"test.csv is empty: {test_csv_path}")
    
    if 'image_path' not in test_df.columns:
        raise ValueError(f"test.csv must have 'image_path' column")
    
    # CSIRO-SPECIFIC: Get unique images (test.csv has 5 rows per image - one per target)
    # Assumes test.csv structure with 5 targets per image
    unique_images = test_df[['image_path']].drop_duplicates().reset_index(drop=True)
    
    if len(unique_images) == 0:
        raise ValueError("No unique images found in test.csv")
    
    return unique_images


def load_csv_batch(
    paths: List[Union[str, Path]], 
    show_progress: bool = True, 
    **kwargs
) -> List[pd.DataFrame]:
    """
    Load multiple CSV files in batch with optional progress tracking.
    
    Args:
        paths: List of paths to CSV files. Can be strings or Path objects.
               Empty list is allowed and will return empty list.
        show_progress: Whether to show progress bar using tqdm (default: True).
        **kwargs: Additional arguments to pass to pd.read_csv for all files.
                  Common options: sep, header, index_col, dtype, etc.
        
    Returns:
        List of DataFrames, one for each successfully loaded CSV file.
        Order matches the input paths list.
        
    Raises:
        ValueError: If paths is not a list or contains invalid entries.
        FileNotFoundError: If any CSV file doesn't exist (raises on first missing file).
        pd.errors.EmptyDataError: If any CSV file is empty (raises on first empty file).
        
    Note:
        This function will stop on the first error. For more robust batch loading
        with error handling per file, consider wrapping individual calls in try-except.
    """
    # Use batch processing utility
    return batch_process_with_progress(
        items=paths,
        process_func=lambda p: load_csv(p, **kwargs),
        desc="Loading CSV files",
        show_progress=show_progress
    )