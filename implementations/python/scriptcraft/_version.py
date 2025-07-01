"""
Version information for ScriptCraft.

This is the single source of truth for version information.
All other files should import from here to maintain DRY principles.
"""

__version__ = "1.1.0"
__author__ = "ScriptCraft Team"

# Version components for programmatic access
VERSION_MAJOR = 1
VERSION_MINOR = 1
VERSION_PATCH = 0

# Version info tuple
VERSION_INFO = (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)

def get_version() -> str:
    """Get the version string."""
    return __version__

def get_version_info() -> tuple:
    """Get the version as a tuple of integers."""
    return VERSION_INFO 