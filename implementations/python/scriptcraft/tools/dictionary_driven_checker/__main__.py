"""Command-line interface for the dictionary-driven checker."""

import argparse
from pathlib import Path
from . import checker

def main():
    """Entry point for command-line execution."""
    parser = argparse.ArgumentParser(
        description='Validate data against dictionary with plugin support'
    )
    parser.add_argument(
        '--data', 
        type=Path,
        required=True,
        help='Path to data file'
    )
    parser.add_argument(
        '--dict',
        type=Path,
        required=True,
        help='Path to dictionary file'
    )
    parser.add_argument(
        '--domain',
        type=str,
        required=True,
        help='Domain name (e.g., Clinical, Biomarkers)'
    )
    parser.add_argument(
        '--config',
        type=Path,
        help='Path to config file'
    )
    
    args = parser.parse_args()
    
    checker.check(
        domain=args.domain,
        input_path=str(args.data),
        output_path=str(args.data.parent / "validation_results.csv"),
        paths={"config": args.config} if args.config else {}
    )

if __name__ == '__main__':
    main()