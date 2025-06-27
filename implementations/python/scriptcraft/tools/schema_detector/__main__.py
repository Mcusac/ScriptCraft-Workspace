#!/usr/bin/env python3
"""
🔍 Schema Detector Tool - Main Entry Point

Command-line interface for the schema detection tool.
Analyzes datasets and generates database schemas with privacy protection.

Usage:
    python -m scriptcraft.tools.schema_detector input/data.csv
    python -m scriptcraft.tools.schema_detector input/*.xlsx --database sqlserver
    python -m scriptcraft.tools.schema_detector input/data1.csv input/data2.json

Author: ScriptCraft Team
"""

import sys
import argparse
from pathlib import Path
from typing import List

from scriptcraft.common.cli import parse_tool_args
from scriptcraft.common.logging import setup_logger
from scriptcraft.common.io import get_project_root
from .tool import SchemaDetector


def main():
    """🚀 Main entry point for schema detection"""
    parser = argparse.ArgumentParser(
        description="🔍 Automatically detect and generate database schemas from datasets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m scriptcraft.tools.schema_detector input/patient_data.csv
  python -m scriptcraft.tools.schema_detector input/*.xlsx --database sqlserver
  python -m scriptcraft.tools.schema_detector input/data1.csv input/data2.json --privacy-mode
        """
    )
    
    parser.add_argument('files', nargs='+', help='Dataset files to analyze')
    parser.add_argument('--output', default='output', help='Output directory (default: output)')
    parser.add_argument('--database', choices=['sqlite', 'sqlserver', 'postgresql'], 
                       default='sqlite', help='Target database type (default: sqlite)')
    parser.add_argument('--privacy-mode', action='store_true', default=True,
                       help='Enable privacy-safe analysis (default: True)')
    parser.add_argument('--no-privacy', action='store_true',
                       help='Disable privacy mode (show actual sample values)')
    parser.add_argument('--sample-size', type=int, default=1000,
                       help='Maximum rows to analyze (default: 1000)')
    parser.add_argument('--naming', choices=['snake_case', 'pascal_case', 'camel_case'],
                       default='pascal_case', help='Column naming convention (default: pascal_case)')
    parser.add_argument('--formats', nargs='+', choices=['sql', 'json', 'yaml'],
                       default=['sql', 'json', 'yaml'], help='Output formats (default: all)')
    
    args = parser.parse_args()
    
    # Set up logging
    logger = setup_logger("schema_detector")
    
    try:
        # Create schema detector
        detector = SchemaDetector()
        
        # Configure privacy mode
        privacy_mode = args.privacy_mode and not args.no_privacy
        
        # Run schema detection
        success = detector.run(
            input_paths=args.files,
            output_dir=args.output,
            target_database=args.database,
            privacy_mode=privacy_mode,
            sample_size=args.sample_size,
            naming_convention=args.naming,
            output_formats=args.formats
        )
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        logger.info("🛑 Schema detection interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"❌ Fatal error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 