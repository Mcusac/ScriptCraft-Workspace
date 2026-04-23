"""
Workflow path utilities for CAFA 6 protein function prediction.
Handles standard path setup for workflows.
"""

from pathlib import Path
from typing import Tuple

from config import DATA_INPUT_DIR, DATA_OUTPUT_DIR


def setup_workflow_paths(test: bool = False) -> Tuple[Path, Path]:
    """
    Set up standard workflow paths.
    
    Args:
        test: If True, setup test data directory, else training data directory
        
    Returns:
        tuple: (data_dir, output_dir) with output_dir already created
    """
    if test:
        data_dir = DATA_INPUT_DIR / 'Test'
    else:
        data_dir = DATA_INPUT_DIR / 'Train'
    
    output_dir = DATA_OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    
    return data_dir, output_dir

