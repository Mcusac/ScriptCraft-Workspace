"""
Shortcuts module for common functionality.
Provides organized access to frequently used functions and classes.
"""

# Core functionality
from .core.config import get_config
from .core.base import OutlierMethod

# Logging
from .logging.core import log_and_print

# Data operations
from .data.cleaning import get_clean_numeric_series, MISSING_VALUE_STRINGS
from .data.validation import FlaggedValue, ColumnValidator, get_status_emoji, PluginRegistry

# Time utilities
from .time.date_utils import standardize_date_format
from .time.timepoint import TimePoint

# IO operations  
from .io.data_loading import load_and_validate_data
from .io.directory_ops import setup_directories

__all__ = [
    # Core
    'get_config', 'OutlierMethod',
    # Logging
    'log_and_print', 
    # Data
    'get_clean_numeric_series', 'MISSING_VALUE_STRINGS', 'FlaggedValue', 
    'ColumnValidator', 'get_status_emoji', 'PluginRegistry',
    # Time
    'standardize_date_format', 'TimePoint',
    # IO
    'load_and_validate_data', 'setup_directories'
] 