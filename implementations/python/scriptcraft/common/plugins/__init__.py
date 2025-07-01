"""
Plugin System for ScriptCraft

This package redirects to the unified registry system.
All plugin functionality is now in scriptcraft.common.registry
"""

# Redirect all imports to the new registry package
from ..registry import *

# Deprecation warning
import warnings
warnings.warn(
    "scriptcraft.common.plugins is deprecated. Use scriptcraft.common.registry instead.",
    DeprecationWarning,
    stacklevel=2
) 