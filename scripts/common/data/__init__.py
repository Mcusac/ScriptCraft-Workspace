"""
Data package for the project.

This package provides data processing and validation utilities organized into:
- cleaning: Data cleaning and preprocessing
- comparison: Data comparison utilities  
- validation: Data validation functions
- dataframe: DataFrame manipulation utilities
"""

# Import everything from all modules
from .cleaning import *
from .comparison import *
from .comparison_core import *
from .comparison_utils import *
from .dataframe import *
from .validation import *

# Build __all__ dynamically
import importlib

def _build_all():
    """Build __all__ list dynamically from all modules."""
    all_exports = []
    modules = ['cleaning', 'comparison', 'comparison_core', 'comparison_utils', 'dataframe', 'validation']
    
    for module_name in modules:
        try:
            module = importlib.import_module(f'.{module_name}', __name__)
            if hasattr(module, '__all__'):
                all_exports.extend(module.__all__)
            else:
                # Get all public attributes (functions, classes, constants)
                for name in dir(module):
                    if not name.startswith('_'):
                        attr = getattr(module, name)
                        # Include functions, classes, and constants but exclude modules
                        if not hasattr(attr, '__file__'):  # Not a module
                            all_exports.append(name)
        except ImportError:
            continue
    
    # Remove duplicates while preserving order
    seen = set()
    return [x for x in all_exports if not (x in seen or seen.add(x))]

__all__ = _build_all() 