#!/usr/bin/env python3
"""
🚀 ScriptCraft Tool Runner
Simple launcher for ScriptCraft tools from PyPI package
"""

import sys
import os
import argparse
from pathlib import Path

def load_config():
    """Load tool configuration from config.bat or environment."""
    config_file = Path(__file__).parent / "config.bat"
    tool_name = None
    
    if config_file.exists():
        # Read tool name from config.bat
        with open(config_file, 'r') as f:
            for line in f:
                if line.strip().startswith('set "TOOL_NAME='):
                    tool_name = line.split('=')[1].strip().strip('"')
                    break
    
    # Fallback to environment variable
    if not tool_name:
        tool_name = os.environ.get('TOOL_NAME', 'rhq_form_autofiller')
    
    return tool_name

def get_tool_module(tool_name):
    """Get the module path for a given tool."""
    tool_modules = {
        'rhq_form_autofiller': 'scriptcraft.tools.rhq_form_autofiller.main',
        'data_content_comparer': 'scriptcraft.tools.data_content_comparer.main',
        'automated_labeler': 'scriptcraft.tools.automated_labeler.main',
        'dictionary_cleaner': 'scriptcraft.tools.dictionary_cleaner.main',
        'dictionary_validator': 'scriptcraft.tools.dictionary_validator.main',
        'dictionary_driven_checker': 'scriptcraft.tools.dictionary_driven_checker.main',
        'date_format_standardizer': 'scriptcraft.tools.date_format_standardizer.main',
        'medvisit_integrity_validator': 'scriptcraft.tools.medvisit_integrity_validator.main',
        'score_totals_checker': 'scriptcraft.tools.score_totals_checker.main',
        'feature_change_checker': 'scriptcraft.tools.feature_change_checker.main',
        'schema_detector': 'scriptcraft.tools.schema_detector.main',
    }
    
    return tool_modules.get(tool_name, f'scriptcraft.tools.{tool_name}.main')

def main():
    """Main entry point for the tool."""
    # Add the current directory to Python path for local imports
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="ScriptCraft Tool Runner")
    parser.add_argument('--tool', help='Tool name to run')
    args, remaining_args = parser.parse_known_args()
    
    # Determine tool name
    tool_name = args.tool or load_config()
    print(f"🔧 Running tool: {tool_name}")
    
    # Get module path
    module_path = get_tool_module(tool_name)
    
    # Import and run the tool
    try:
        # Import the module
        module_parts = module_path.split('.')
        module = __import__(module_path, fromlist=['main'])
        
        # Get the main function
        if hasattr(module, 'main'):
            tool_main = module.main
            print(f"🚀 Starting {tool_name}...")
            tool_main()
        else:
            print(f"❌ No main function found in {module_path}")
            sys.exit(1)
            
    except ImportError as e:
        print(f"❌ Error importing tool {tool_name}: {e}")
        print("💡 Make sure scriptcraft package is installed in the embedded Python")
        print(f"💡 Tried to import: {module_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running tool {tool_name}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
