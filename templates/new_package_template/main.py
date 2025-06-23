"""
[Tool Name] - Main Implementation

This module provides the main implementation of the [Tool Name] tool.
It handles [main functionality description] with dual-environment support.

Usage:
    Development: python -m scripts.tools.[tool_name] [args]
    Distributable:   python main.py [args] 
    Pipeline:    Called via main_runner(**kwargs)
"""

import sys
import argparse
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# === Environment Detection & Import Setup ===
def setup_imports():
    """
    Detect environment and set up imports.
    Returns True if in distributable environment, False if in development.
    """
    current_file = Path(__file__)
    
    # Check if 'common' folder exists at same level (distributable environment)
    is_distributable = (current_file.parent / 'common').exists()
    
    if is_distributable:
        # Distributable environment: add current directory to path
        current_dir = str(current_file.parent)
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        print(f"🏗️ Distributable environment detected, added {current_dir} to path")
    else:
        print("🛠️ Development environment detected")
    
    return is_distributable

# Set up environment and get imports
IS_DISTRIBUTABLE = setup_imports()

# Alternative: Use BaseTool.is_distributable_environment() for consistency
# This can replace IS_DISTRIBUTABLE after importing BaseTool

# Import with fallbacks for dual environment support
try:
    # Development imports (try first)
    from scripts.common.logging.core import setup_logger, log_and_print
    from scripts.common.io.data_loading import load_data
    from scripts.common.core.config import Config
    from scripts.common.core.base import BaseTool
except ImportError:
    # Distributable imports (fallback)
    from common.logging.core import setup_logger, log_and_print
    from common.io.data_loading import load_data
    from common.core.config import Config
    from common.core.base import BaseTool

# Import utilities
from .utils import ToolNameUtils


class ToolName(BaseTool):
    """Tool for [description of what the tool does]."""
    
    def __init__(self):
        """Initialize the tool."""
        super().__init__(
            name="[Tool Name]",
            description="[Tool description]"
        )
        self.utils = ToolNameUtils()
        
        # Load configuration with fallbacks
        try:
            config_path = "config.yaml" if not IS_DISTRIBUTABLE else "../config.yaml"
            self.config = Config.from_yaml(config_path)
            tool_config = self.config.get_tool_config("[tool_name]") if hasattr(self.config, 'get_tool_config') else {}
            
            # Store configurable values
            self.default_output_dir = tool_config.get("default_output_dir", "output")
            
            # ADD TOOL-SPECIFIC CONFIG VALUES HERE
            # self.custom_option = tool_config.get("custom_option", "default_value")
            
        except Exception as e:
            log_and_print(f"⚠️ Config loading failed, using defaults: {e}")
            # Fallback to defaults if config loading fails
            self.default_output_dir = "output"
            
            # ADD TOOL-SPECIFIC DEFAULTS HERE
            # self.custom_option = "default_value"
    
    def run(self,
            input_path: Optional[Union[str, Path]] = None,
            output_dir: Optional[Union[str, Path]] = None,
            mode: Optional[str] = None,
            debug: bool = False,
            **kwargs) -> None:
        """
        Run the tool's main functionality.
        
        Args:
            input_path: Path to input file/directory
            output_dir: Directory to save outputs
            mode: Operating mode (if applicable)
            debug: Enable debug logging
            **kwargs: Additional tool-specific arguments
        
        Raises:
            ValueError: If required parameters are missing or invalid
        """
        log_and_print("🚀 Starting [Tool Name]...")
        
        try:
            # Setup directories
            output_dir = Path(output_dir or self.default_output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Setup logging
            logger = setup_logger(
                name="[tool_name]",
                level="DEBUG" if debug else "INFO",
                log_file="logs/[tool_name].log"
            )
            
            # Resolve input file(s)
            input_files = self._resolve_input_files(input_path, **kwargs)
            
            # Process each input file
            for input_file in input_files:
                self._process_file(input_file, output_dir, mode, logger, **kwargs)
            
            log_and_print("✅ [Tool Name] completed successfully")
            
        except Exception as e:
            log_and_print(f"❌ Error in [Tool Name]: {str(e)}", level="error")
            raise
    
    def _resolve_input_files(self, input_path: Optional[Union[str, Path]], **kwargs) -> List[Path]:
        """Resolve input files from various sources."""
        input_files = []
        
        if input_path:
            # Direct input path provided
            input_files = [Path(input_path)]
        elif kwargs.get('auto_discover', True):
            # Auto-discover input files using DRY method from BaseTool
            # Add config to kwargs if not already present
            if 'config' not in kwargs:
                kwargs['config'] = self.config
            input_dir = self.resolve_input_directory(**kwargs)
            
            if not input_dir.exists():
                raise ValueError(f"Input directory not found: {input_dir}")
            
            # ADD FILE DISCOVERY LOGIC HERE
            # Example for Excel files:
            # excel_files = list(input_dir.glob("*.xlsx"))
            # if not excel_files:
            #     raise ValueError("No Excel files found in input directory")
            # input_files = excel_files
            
            # For template example, get all data files
            all_files = list(input_dir.iterdir())
            data_files = [f for f in all_files if f.is_file() and not f.name.startswith('.')]
            if not data_files:
                raise ValueError("No data files found in input directory")
            
            input_files = data_files[:1]  # Take first file as example
            log_and_print(f"📁 Auto-discovered input file: {input_files[0]}")
        else:
            raise ValueError("No input path provided and auto-discovery disabled")
        
        # Validate all files exist
        for input_file in input_files:
            if not input_file.exists():
                raise ValueError(f"Input file does not exist: {input_file}")
        
        return input_files
    
    def _process_file(self, input_file: Path, output_dir: Path, mode: Optional[str], logger, **kwargs) -> None:
        """Process a single input file."""
        log_and_print(f"🔄 Processing file: {input_file}")
        
        try:
            # Validate input
            if not self.utils.validate_input_file(input_file):
                raise ValueError(f"Input validation failed for: {input_file}")
            
            # Load data
            log_and_print(f"📂 Loading data from: {input_file}")
            data = load_data(input_file)
            
            # Process data using utility methods
            log_and_print("⚙️ Processing data...")
            processed_data = self.utils.process_data(data, mode, **kwargs)
            
            # Save results
            output_file = output_dir / f"processed_{input_file.name}"
            log_and_print(f"💾 Saving results to: {output_file}")
            self.utils.save_results(processed_data, output_file)
            
            log_and_print(f"✅ Completed processing: {input_file}")
            
        except Exception as e:
            log_and_print(f"❌ Error processing {input_file}: {str(e)}", level="error")
            raise
    
    def run_from_cli(self, args) -> None:
        """
        Run the tool from command line arguments.
        
        Args:
            args: Parsed command line arguments
        """
        kwargs = vars(args).copy()
        
        # Extract known arguments
        input_path = kwargs.pop('input_path', None)
        output_dir = kwargs.pop('output_dir', self.default_output_dir)
        debug = kwargs.pop('debug', False)
        mode = kwargs.pop('mode', None)
        
        # Run the tool
        self.run(
            input_path=input_path,
            output_dir=output_dir,
            mode=mode,
            debug=debug,
            **kwargs
        )


# === CLI Interface ===
def parse_cli_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="🛠️ [Tool Name] - [Tool description for CLI help]"
    )
    
    # Standard arguments
    parser.add_argument(
        "input_path",
        type=str,
        nargs='?',  # Make optional for tools that auto-discover
        help="Path to input file/directory"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Directory to save outputs (default: output)"
    )
    
    parser.add_argument(
        "--mode",
        type=str,
        choices=["basic", "advanced"],  # ADD YOUR MODES HERE
        help="Operating mode"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    
    # ADD TOOL-SPECIFIC ARGUMENTS HERE
    # parser.add_argument("--custom-option", help="Custom option description")
    # parser.add_argument("--filter", help="Filter criteria")
    # parser.add_argument("--format", choices=["json", "csv"], help="Output format")
    
    return parser.parse_args()


def run_from_args(args):
    """Run the tool with parsed arguments."""
    tool = ToolName()
    tool.run_from_cli(args)


def main_runner(**kwargs):
    """Main entry point for the tool when run from the pipeline."""
    log_and_print("🚀 Starting [Tool Name] from pipeline...")
    
    try:
        tool = ToolName()
        
        # Extract arguments from kwargs
        input_path = kwargs.get('input_path')
        output_dir = kwargs.get('output_dir', 'output')
        mode = kwargs.get('mode')
        debug = kwargs.get('debug', False)
        
        # Run the tool
        tool.run(
            input_path=input_path,
            output_dir=output_dir,
            mode=mode,
            debug=debug,
            **{k: v for k, v in kwargs.items() if k not in ['input_path', 'output_dir', 'mode', 'debug']}
        )
        
    except Exception as e:
        log_and_print(f"❌ Pipeline execution failed: {str(e)}", level="error")
        raise


def main():
    """Main CLI entry point."""
    args = parse_cli_args()
    run_from_args(args)


# === CLI Entry Point (replaces __main__.py) ===
if __name__ == "__main__":
    main() 