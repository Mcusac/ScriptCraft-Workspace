"""
Centralized CLI utilities for consistent command-line interfaces.
"""

import argparse
from .argument_parsers import (
    ArgumentGroups,
    ParserFactory,
    ArgumentValidator,
    create_standard_main_function,
    parse_pipeline_args,
    parse_tool_args,
    parse_standard_tool_args,
    parse_main_args
)

# Convenience function for tools that want to use the new standardized pattern
def parse_tool_args(description: str) -> argparse.Namespace:
    """
    Parse standard tool arguments.
    
    This is a convenience function that provides the standard argument parsing
    pattern used by most tools. It includes:
    - Input file paths (required)
    - Output directory (optional, defaults to "output")
    - Domain specification (optional)
    - Output filename (optional)
    - Mode specification (optional)
    
    Args:
        description: Description of the tool for help text
        
    Returns:
        Parsed arguments namespace
    """
    return parse_standard_tool_args("tool", description)

# Export all the main functions
__all__ = [
    'ArgumentGroups',
    'ParserFactory', 
    'ArgumentValidator',
    'create_standard_main_function',
    'parse_pipeline_args',
    'parse_tool_args',
    'parse_standard_tool_args',
    'parse_main_args'
] 