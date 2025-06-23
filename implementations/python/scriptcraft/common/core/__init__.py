"""
Core package for the project.

This package provides core functionality organized into:
- base: Base classes for components
- config: Configuration management
- registry: Plugin registration and discovery
"""

from .base import (
    BaseComponent,
    BaseProcessor,
    BasePipelineStep,
    BaseEnhancement,
    BaseTool
)
from .config import Config
from .registry import PluginRegistry, registry

__all__ = [
    # Base Classes
    'BaseComponent',
    'BaseProcessor',
    'BasePipelineStep',
    'BaseEnhancement',
    'BaseTool',
    
    # Configuration
    'Config',
    
    # Plugin Registry
    'PluginRegistry',
    'registry'
] 