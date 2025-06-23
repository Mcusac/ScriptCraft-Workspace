"""
ScriptCraft - Data processing and quality control tools for research.

This package provides a comprehensive framework for data processing, validation,
and quality control, specifically designed for research data workflows.

Most users will want to start with the common utilities:
    from scriptcraft.common import setup_logger, Config, BaseTool, load_data

For specific tools:
    from scriptcraft.tools import RHQFormAutofiller, DataContentComparer
    
For validation and checking:
    from scriptcraft.checkers import DictionaryDrivenChecker
    from scriptcraft.validators import MedVisitIntegrityValidator
"""

__version__ = "1.0.0"
__author__ = "ScriptCraft Team"

# Import the most commonly used utilities
from .common import (
    # Core functionality
    BaseTool, BaseProcessor, Config,
    setup_logger, log_and_print,
    
    # Data operations
    load_data, ensure_output_dir,
    
    # Common utilities users need most
    get_project_root, resolve_path
)

# Make tools discoverable
from . import tools
from . import checkers
from . import validators
from . import transformers
from . import enhancements

__all__ = [
    # Version info
    "__version__", "__author__",
    
    # Core classes
    "BaseTool", "BaseProcessor", "Config",
    
    # Logging
    "setup_logger", "log_and_print", 
    
    # Data operations
    "load_data", "ensure_output_dir",
    
    # Path utilities
    "get_project_root", "resolve_path",
    
    # Sub-packages
    "tools", "checkers", "validators", "transformers", "enhancements"
]
