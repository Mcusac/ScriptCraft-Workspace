"""
Command Line Interface for ScriptCraft.

Provides command-line access to all ScriptCraft tools and utilities.
"""

# Import argument parsers if available
try:
    from .argument_parsers import *
except ImportError:
    # CLI dependencies not available, provide basic functionality
    pass

__all__ = ["main"]

def main():
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