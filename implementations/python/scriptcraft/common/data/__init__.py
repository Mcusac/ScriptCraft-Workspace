"""
Data package for the project.

This package provides data processing and validation utilities organized into:
- cleaning: Data cleaning and preprocessing
- comparison: Data comparison utilities  
- validation: Data validation functions
- dataframe: DataFrame manipulation utilities
- processing: Data processing patterns and utilities
- processor: Universal data processor for common operations

Usage:
    # Import everything (recommended for internal use)
    from scriptcraft.common.data import *
    
    # Import specific items (recommended for external use)
    from scriptcraft.common.data import compare_dataframes, FlaggedValue
"""

# Import everything from all modules for scalability
from .cleaning import *
from .comparison import *
from .comparison_core import *
from .dataframe import *
from .validation import *
from .processing import *
from .processor import * 