# scripts/tools/tool_dispatcher.py

"""
Tool dispatcher for managing and running tools in the scripts/tools directory.

This module provides functionality to discover and dispatch tools using a
consistent interface and error handling.
"""

from pathlib import Path
from typing import Dict, Optional, Any
from importlib import import_module
import scripts.common as cu

TOOLS_FOLDER = Path(__file__).parent

class ToolRegistry:
    """Registry for managing available tools."""
    
    def __init__(self):
        self._tools: Dict[str, str] = {}
        self._instances: Dict[str, cu.BaseTool] = {}
        self.discover_tools()
    
    def discover_tools(self) -> None:
        """Discover available tool packages in scripts/tools/."""
        for entry in TOOLS_FOLDER.iterdir():
            if entry.is_dir() and (entry / "__init__.py").exists():
                self._tools[entry.name] = f"scripts.tools.{entry.name}"
    
    def get_tool(self, tool_name: str) -> Optional[cu.BaseTool]:
        """
        Get a tool instance by name.
        
        Args:
            tool_name: Name of the tool to get
        
        Returns:
            Optional[BaseTool]: Tool instance if found, None otherwise
        """
        # Return cached instance if available
        if tool_name in self._instances:
            return self._instances[tool_name]
            
        # Try to load the tool
        import_path = self._tools.get(tool_name)
        if not import_path:
            cu.log_and_print(f"❌ Tool '{tool_name}' not found in scripts/tools/")
            return None
            
        try:
            # Load the tool's main module
            main_module = import_module(f"{import_path}.main")
            
            # Look for a tool instance
            tool_instance = None
            for attr_name in dir(main_module):
                attr = getattr(main_module, attr_name)
                if isinstance(attr, cu.BaseTool):
                    tool_instance = attr
                    break
            
            if not tool_instance:
                cu.log_and_print(f"❌ No BaseTool instance found in {tool_name}/main.py")
                return None
                
            # Cache and return the instance
            self._instances[tool_name] = tool_instance
            return tool_instance
            
        except Exception as e:
            cu.log_and_print(f"❌ Failed to load tool '{tool_name}': {e}")
            return None
    
    def list_tools(self) -> Dict[str, str]:
        """
        Get a dictionary of available tools.
        
        Returns:
            Dict[str, str]: Dictionary mapping tool names to import paths
        """
        return self._tools.copy()

# Create singleton registry
registry = ToolRegistry()

def dispatch_tool(tool_name: str, args: Any) -> None:
    """
    Dispatch a tool based on CLI args.
    
    Args:
        tool_name: Name of the tool to run
        args: Parsed command line arguments
    """
    tool = registry.get_tool(tool_name)
    if not tool:
        return
        
    try:
        # Convert input paths to list if provided
        input_paths = [args.input] if hasattr(args, 'input') and isinstance(args.input, (str, Path)) else args.input
        
        # Run the tool with standardized interface
        tool.run(
            mode=getattr(args, "mode", None),
            input_paths=input_paths,
            output_dir=getattr(args, "output", "output"),
            domain=getattr(args, "domain", None),
            output_filename=getattr(args, "output_filename", None)
        )
    except Exception as e:
        cu.log_and_print(f"❌ Error running tool '{tool_name}': {e}")
        raise
