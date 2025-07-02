"""
Shortcuts module for common functionality.
Provides organized access to frequently used functions and classes.
"""

from pathlib import Path
from typing import Union, Tuple
import pandas as pd

# Core functionality
from .core.config import Config
from .core.base import BaseTool
from .io.paths import OutlierMethod

# Convenience function for loading config
def load_config(path: Union[str, Path] = "config.yaml") -> Config:
    """Load configuration from YAML file."""
    return Config.from_yaml(path)

# Logging
from .logging.core import log_and_print
from .logging.context import qc_log_context, with_domain_logger

# Data operations
from .data.cleaning import get_clean_numeric_series, MISSING_VALUE_STRINGS
from .data.validation import FlaggedValue, ColumnValidator, get_status_emoji, PluginRegistry

# Time utilities
from .time.date_utils import standardize_date_column
# from .time.timepoint import TimePoint  # TODO: TimePoint class not implemented yet

# IO operations  
from .io.data_loading import load_data, load_datasets_as_dict  # load_and_validate_data not implemented yet
from .io.directory_ops import ensure_output_dir  # setup_directories not implemented yet
from .io.paths import STANDARD_KEYS, get_project_root
from .io.path_resolver import PathResolver, WorkspacePathResolver, LegacyPathResolver, create_path_resolver

def load_datasets(*filenames: str, data_dir: str = ".", **kwargs) -> Tuple[pd.DataFrame, ...]:
    """
    Load multiple datasets from individual filenames.
    
    Args:
        *filenames: Individual filenames to load
        data_dir: Directory containing the files
        **kwargs: Additional arguments for load_data
        
    Returns:
        Tuple of loaded DataFrames in the same order as filenames
    """
    data_path = Path(data_dir)
    
    datasets = []
    for filename in filenames:
        file_path = data_path / filename
        try:
            df = load_data(file_path, **kwargs)
            datasets.append(df)
        except Exception as e:
            log_and_print(f"❌ Error loading {filename}: {e}")
            datasets.append(None)
    
    return tuple(datasets)


__all__ = [
    # Core
    'Config', 'load_config', 'BaseTool', 'OutlierMethod',
    # Logging
    'log_and_print', 'qc_log_context', 'with_domain_logger',
    # Data
    'get_clean_numeric_series', 'MISSING_VALUE_STRINGS', 'FlaggedValue', 
    'ColumnValidator', 'get_status_emoji', 'PluginRegistry',
    # Time
    'standardize_date_column',  # 'TimePoint', - not implemented yet
    # IO
    'load_data', 'load_datasets', 'load_datasets_as_dict', 'ensure_output_dir', 'STANDARD_KEYS', 'get_project_root', # load_and_validate_data, setup_directories not implemented yet
    'PathResolver', 'WorkspacePathResolver', 'LegacyPathResolver', 'create_path_resolver'
] 