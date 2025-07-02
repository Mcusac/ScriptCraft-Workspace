# dictionary_driven_checker/plugins/__init__.py

"""Plugin system for dictionary-driven validation."""

from scriptcraft.common.plugins import registry

# Import plugins after registry is created to avoid circular dependency
def _load_plugins() -> None:
    """Load all plugins after registry is initialized."""
    try:
        from . import validators  # Load the main validators file
        # Individual plugin files are kept for reference but not loaded
        # from . import numeric_plugin
        # from . import text_plugin  
        # from . import date_plugin
    except ImportError as e:
        # Plugins are optional - if they fail to import, continue
        print(f"Warning: Failed to load plugins: {e}")
        pass

# Load plugins immediately
_load_plugins()
