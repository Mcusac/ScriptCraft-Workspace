"""
Tools Package

This package contains various tools for data processing and automation.
Each tool is implemented as a module with its own functionality.
"""

import importlib
import pkgutil
from pathlib import Path
from typing import Dict, List, Optional, Type

from scriptcraft.common.core import BaseTool
from scriptcraft.common.core import registry

# Cache for loaded tools to avoid re-loading
_cached_tools: Optional[Dict[str, BaseTool]] = None


def get_available_tools() -> Dict[str, BaseTool]:
    """
    Get all available tools from the tools directory.
    
    Returns:
        Dict mapping tool names to their instances
    """
    global _cached_tools
    
    # Return cached tools if already loaded
    if _cached_tools is not None:
        return _cached_tools
    
    tools = {}
    
    # Get the tools directory path
    tools_dir = Path(__file__).parent
    
    # Import all tool modules
    for _, name, is_pkg in pkgutil.iter_modules([str(tools_dir)]):
        if is_pkg and not name.startswith('_'):
            try:
                # Import the tool module
                module = importlib.import_module(f".{name}", package="scripts.tools")
                
                # Look for the tool instance
                if hasattr(module, 'tool'):
                    tool_instance = getattr(module, 'tool')
                    if isinstance(tool_instance, BaseTool):
                        tools[tool_instance.name] = tool_instance
                        # Register the tool with the registry
                        registry.register_tool(tool_instance)
            except Exception as e:
                print(f"Warning: Failed to load tool {name}: {e}")
    
    # Cache the tools
    _cached_tools = tools
    return tools


def run_tool(tool_name: str, **kwargs) -> None:
    """
    Run a specific tool by name.
    
    Args:
        tool_name: Name of the tool to run
        **kwargs: Arguments to pass to the tool's run method
    """
    tools = get_available_tools()
    
    if tool_name not in tools:
        raise ValueError(f"Tool '{tool_name}' not found. Available tools: {list(tools.keys())}")
    
    tool = tools[tool_name]
    tool.run(**kwargs)


# Make tools available at package level
__all__ = ['run_tool', 'get_available_tools']
