"""
Unified Registry System for ScriptCraft

This package provides a single, comprehensive registry system that handles:
- Tool discovery and management
- Plugin registration and discovery
- Validation plugin management
- Metadata management

This is the ONLY registry system in ScriptCraft - all other registry code should be removed.
"""

from .registry import *
from .plugin_registry import *

# Main registry instance (the ONE registry to rule them all)
registry = unified_registry 