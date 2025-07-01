"""
Plugin Registry System

This module provides plugin registration and management functionality.
It consolidates all plugin-related code from the old plugins system.
"""

from typing import Dict, List, Optional, Callable, Any, Type
from abc import ABC, abstractmethod
from functools import wraps

from ..logging import log_and_print


class PluginBase(ABC):
    """Base class for all plugins."""
    
    def __init__(self):
        self.name = self.__class__.__name__
        self.description = getattr(self, '__doc__', 'No description available')
    
    @abstractmethod
    def get_plugin_type(self) -> str:
        """Return the type of this plugin."""
        pass


class PluginRegistry:
    """
    Plugin registry for managing validator, tool, and pipeline plugins.
    
    This is a simplified, focused plugin registry that works with the unified registry.
    """
    
    def __init__(self):
        self._plugins: Dict[str, Dict[str, Type[PluginBase]]] = {}
        self._metadata: Dict[str, Dict[str, Dict[str, Any]]] = {}
    
    def register_plugin(self, 
                       plugin_type: str,
                       name: str,
                       plugin_class: Type[PluginBase],
                       metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Register a plugin class.
        
        Args:
            plugin_type: Type of plugin (e.g., 'validator', 'tool', 'pipeline_step')
            name: Unique name for the plugin
            plugin_class: Plugin class to register
            metadata: Optional metadata for the plugin
        """
        if plugin_type not in self._plugins:
            self._plugins[plugin_type] = {}
            self._metadata[plugin_type] = {}
        
        self._plugins[plugin_type][name] = plugin_class
        self._metadata[plugin_type][name] = metadata or {}
        
        log_and_print(f"🔌 Registered {plugin_type} plugin: {name}")
    
    def get_plugin(self, plugin_type: str, name: str) -> Optional[Type[PluginBase]]:
        """Get a registered plugin class."""
        return self._plugins.get(plugin_type, {}).get(name)
    
    def get_plugin_instance(self, plugin_type: str, name: str, **kwargs) -> Optional[PluginBase]:
        """Get an instance of a registered plugin."""
        plugin_class = self.get_plugin(plugin_type, name)
        if plugin_class:
            return plugin_class(**kwargs)
        return None
    
    def get_all_plugins(self, plugin_type: Optional[str] = None) -> Dict[str, Dict[str, Type[PluginBase]]]:
        """Get all registered plugins, optionally filtered by type."""
        if plugin_type:
            return {plugin_type: self._plugins.get(plugin_type, {})}
        return self._plugins
    
    def list_plugins(self, plugin_type: Optional[str] = None) -> List[str]:
        """List all plugin names, optionally filtered by type."""
        if plugin_type:
            return list(self._plugins.get(plugin_type, {}).keys())
        return [name for plugins in self._plugins.values() for name in plugins.keys()]
    
    def get_metadata(self, plugin_type: str, name: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a specific plugin."""
        return self._metadata.get(plugin_type, {}).get(name)


# Global plugin registry instance
plugin_registry = PluginRegistry()


# ===== CONVENIENCE DECORATORS =====

def register_validator(name: str, **metadata):
    """Decorator for registering validator plugins."""
    def decorator(plugin_class: Type[PluginBase]) -> Type[PluginBase]:
        plugin_registry.register_plugin('validator', name, plugin_class, metadata)
        return plugin_class
    return decorator

def register_tool_plugin(name: str, **metadata):
    """Decorator for registering tool plugins."""
    def decorator(plugin_class: Type[PluginBase]) -> Type[PluginBase]:
        plugin_registry.register_plugin('tool', name, plugin_class, metadata)
        return plugin_class
    return decorator

def register_pipeline_step(name: str, **metadata):
    """Decorator for registering pipeline step plugins."""
    def decorator(plugin_class: Type[PluginBase]) -> Type[PluginBase]:
        plugin_registry.register_plugin('pipeline_step', name, plugin_class, metadata)
        return plugin_class
    return decorator


# ===== BACKWARD COMPATIBILITY =====

class LegacyPluginRegistry:
    """Backward compatibility wrapper for the old validation PluginRegistry."""
    
    def __init__(self):
        self._validators: Dict[str, Type] = {}
    
    def register(self, type_name: str) -> callable:
        def decorator(validator_class) -> type:
            self._validators[type_name] = validator_class
            # Also register with the new plugin registry
            plugin_registry.register_plugin('validator', type_name, validator_class)
            return validator_class
        return decorator
    
    def get_all_validators(self):
        return self._validators


# Export for backward compatibility
PluginRegistry = LegacyPluginRegistry 