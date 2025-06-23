"""
Plugin registry system for dynamic tool and pipeline step registration.
"""

from functools import wraps
from typing import Callable, Dict, List, Optional, Union
from pathlib import Path

class PluginRegistry:
    """Central registry for pipeline steps and tools."""
    
    def __init__(self):
        self.steps: Dict[str, Callable] = {}
        self.tools: Dict[str, Callable] = {}
        self.metadata: Dict[str, dict] = {}
    
    def register_step(self, 
                     name: str, 
                     tags: List[str] = None, 
                     input_key: str = "raw_data",
                     run_mode: str = "domain",
                     check_exists: bool = True) -> Callable:
        """Decorator to register a pipeline step."""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            
            self.steps[name] = wrapper
            self.metadata[name] = {
                "type": "step",
                "tags": tags or [],
                "input_key": input_key,
                "run_mode": run_mode,
                "check_exists": check_exists
            }
            return wrapper
        return decorator
    
    def register_tool(self, 
                     name: str,
                     description: str = "",
                     required_args: List[str] = None) -> Callable:
        """Decorator to register a tool."""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            
            self.tools[name] = wrapper
            self.metadata[name] = {
                "type": "tool",
                "description": description,
                "required_args": required_args or []
            }
            return wrapper
        return decorator
    
    def get_step(self, name: str) -> Optional[Callable]:
        """Get a registered pipeline step."""
        return self.steps.get(name)
    
    def get_tool(self, name: str) -> Optional[Callable]:
        """Get a registered tool."""
        return self.tools.get(name)
    
    def get_metadata(self, name: str) -> Optional[dict]:
        """Get metadata for a registered plugin."""
        return self.metadata.get(name)
    
    def list_plugins(self, plugin_type: str = None) -> List[str]:
        """List all registered plugins, optionally filtered by type."""
        if plugin_type:
            return [name for name, meta in self.metadata.items() 
                   if meta["type"] == plugin_type]
        return list(self.metadata.keys())

# Global registry instance
registry = PluginRegistry()

# Convenience decorators
register_step = registry.register_step
register_tool = registry.register_tool 