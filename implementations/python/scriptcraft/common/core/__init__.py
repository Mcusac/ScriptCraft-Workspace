"""
Core package for ScriptCraft common utilities.

This package contains base classes and configuration management.
Registry functionality has been moved to the registry package.
"""

from .base import BaseTool, BaseMainRunner
from .config import Config, get_config, load_config

__all__ = [
    # Base classes
    'BaseTool', 'BaseMainRunner',
    
    # Configuration
    'Config', 'get_config', 'load_config'
]