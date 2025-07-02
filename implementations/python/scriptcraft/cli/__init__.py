"""
Command Line Interface for ScriptCraft.

Provides command-line access to all ScriptCraft tools and utilities.
"""

# Import from common CLI module
try:
    from ..common.cli import (
        parse_tool_args,
        parse_pipeline_args,
        parse_main_args,
        ArgumentGroups,
        ParserFactory
    )
except ImportError:
    # CLI dependencies not available, provide basic functionality
    pass

__all__ = ["main", "parse_tool_args", "parse_pipeline_args", "parse_main_args"]

def main() -> None:
    """Main entry point for scriptcraft CLI."""
    print("🚀 ScriptCraft CLI")
    print("Available commands:")
    print("  scriptcraft --help    Show detailed help")
    print("  scriptcraft tools     List available tools")
    print("  scriptcraft run <tool> Run a specific tool")
    print("")
    print("Or import directly in Python:")
    print("  from scriptcraft import setup_logger, Config, BaseTool")
    
if __name__ == "__main__":
    main() 