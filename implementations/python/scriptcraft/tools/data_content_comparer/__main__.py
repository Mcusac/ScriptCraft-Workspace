"""
Data Content Comparer Tool - Command Line Interface

This module provides the command line interface for the data content comparer tool.
It allows the tool to be run as a standalone script:

    python -m scripts.tools.data_content_comparer old.csv new.csv
"""

import sys
import os
from pathlib import Path

# Check if we're in a distributable environment
IS_DISTRIBUTABLE = os.environ.get('DISTRIBUTABLE', 'false').lower() == 'true'

if IS_DISTRIBUTABLE:
    from .common import log_and_print, Config
else:
    from ...common import log_and_print, Config
    from ...common.cli import ParserFactory

from .tool import DataContentComparer


def main():
    """Main entry point for command line execution."""
    parser = ParserFactory.create_tool_parser("data_content_comparer", 
                                             "Compare the content of two datasets and generate a detailed report")
    
    # Add tool-specific arguments
    parser.add_argument("old_file", type=str, help="Path to the old/reference dataset")
    parser.add_argument("new_file", type=str, help="Path to the new/comparison dataset")
    parser.add_argument("--mode", type=str, choices=["full", "quick", "summary"], default="full",
                       help="Comparison mode (default: full)")
    
    args = parser.parse_args()
    
    try:
        # Initialize and run tool
        tool = DataContentComparer()
        tool.run(
            input_paths=[args.old_file, args.new_file],
            output_dir=args.output_dir,
            mode=args.mode,
            config=Config.from_yaml(Path(args.config))
        )
        
    except Exception as e:
        log_and_print(f"❌ Error: {str(e)}", level="error")
        sys.exit(1)


if __name__ == "__main__":
    main() 