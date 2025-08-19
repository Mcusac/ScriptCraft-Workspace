#!/usr/bin/env python3
"""
🚀 ScriptCraft Tool Runner
Simple launcher for ScriptCraft tools from embedded Python
"""

import sys
import os
import argparse
from pathlib import Path

# Ensure UTF-8 encoding for emojis
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

def detect_tool_name():
    """Detect tool name from the distributable folder name."""
    current_dir = Path(__file__).parent.name
    if current_dir.endswith('_distributable'):
        return current_dir.replace('_distributable', '')
    return 'rhq_form_autofiller'  # fallback

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
    parser = argparse.ArgumentParser(description="ScriptCraft Tool Runner", add_help=False)
    parser.add_argument('--tool', help='Tool name to run (auto-detected if not specified)')
    args, remaining_args = parser.parse_known_args()
    
    # Determine tool name
    tool_name = args.tool or detect_tool_name()
    print(f"🔧 Running tool: {tool_name}")
    
    # Auto-discover input files if no arguments provided
    if not remaining_args:
        input_dir = current_dir / "input"
        if input_dir.exists():
            input_files = list(input_dir.glob("*.xlsx")) + list(input_dir.glob("*.csv"))
            if input_files:
                print(f"📂 Auto-discovered {len(input_files)} input files in input/ directory")
                # Add input files as arguments
                remaining_args = [str(f) for f in input_files]
            else:
                print("⚠️ No .xlsx or .csv files found in input/ directory")
                print("💡 Place your data files in the input/ folder and run again")
        else:
            print("⚠️ No input/ directory found")
            print("💡 Create an input/ folder and place your data files there")
    
    # Get module path
    module_path = get_tool_module(tool_name)
    
    # Import and run the tool
    try:
        # Import the module
        module = __import__(module_path, fromlist=['main'])
        
        # Get the main function
        if hasattr(module, 'main'):
            tool_main = module.main
            print(f"🚀 Starting {tool_name}...")
            # Pass remaining arguments to the tool by updating sys.argv
            if remaining_args:
                sys.argv = [sys.argv[0]] + remaining_args
            else:
                # If still no args, provide help info
                print("💡 Usage: Place your data files in the input/ folder")
                sys.argv = [sys.argv[0], "--help"]
            tool_main()
        else:
            print(f"ERROR: No main function found in {module_path}")
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
