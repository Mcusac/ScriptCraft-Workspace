"""
Common utilities package for the project.

This package provides shared functionality organized into:
- core: Base classes and core functionality
- logging: Logging utilities and configuration
- io: Input/output operations and path management
- data: Data processing and validation utilities
- time: Time and date handling utilities
- tools: Tool utilities and runners
"""

# Import everything from all sub-packages
from .core import *
from .logging import *
from .io import *
from .data import *
from .time import *
from .tools import *

# Build __all__ dynamically by collecting from all sub-modules
import importlib
import pkgutil

def _build_all():
    """Build __all__ list dynamically from all sub-packages."""
    all_exports = []
    
    # Get all sub-package names
    sub_packages = ['core', 'logging', 'io', 'data', 'time', 'tools']
    
    for package_name in sub_packages:
        try:
            # Import the sub-package
            package = importlib.import_module(f'.{package_name}', __name__)
            
            # Get its __all__ if it exists, otherwise get all public names
            if hasattr(package, '__all__'):
                all_exports.extend(package.__all__)
            else:
                # Get all public attributes (not starting with _)
                all_exports.extend([name for name in dir(package) if not name.startswith('_')])
        except ImportError:
            # Skip if package doesn't exist
            continue
    
    # Remove duplicates while preserving order
    seen = set()
    return [x for x in all_exports if not (x in seen or seen.add(x))]

__all__ = _build_all()
