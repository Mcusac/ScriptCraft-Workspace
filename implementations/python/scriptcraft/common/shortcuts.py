"""
Shortcuts module for common functionality.
Provides organized access to frequently used functions and classes.
"""

# Core functionality
from .core.config import Config
from .core.base import BaseTool
from .io.paths import OutlierMethod

# Convenience function for loading config
def load_config(path="config.yaml"):
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
from .io.data_loading import load_data  # load_and_validate_data not implemented yet
from .io.directory_ops import ensure_output_dir  # setup_directories not implemented yet
from .io.paths import STANDARD_KEYS, get_project_root
from .io.path_resolver import PathResolver, WorkspacePathResolver, LegacyPathResolver, create_path_resolver

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
    'load_data', 'ensure_output_dir', 'STANDARD_KEYS', 'get_project_root',  # load_and_validate_data, setup_directories not implemented yet
    'PathResolver', 'WorkspacePathResolver', 'LegacyPathResolver', 'create_path_resolver'
] 