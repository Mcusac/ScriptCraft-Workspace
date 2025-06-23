"""Command-line interface for the feature change checker."""

import argparse
from pathlib import Path
from scriptcraft.pipelines.pipeline_utils import run_qc_for_each_domain
from . import checker, run_feature_change_tracker

def main():
    """Entry point for command-line execution."""
    parser = argparse.ArgumentParser(
        description='Track and categorize feature changes between visits'
    )
    parser.add_argument(
        '--feature',
        type=str,
        default="CDX_Cog",
        help='Feature name to track changes for'
    )
    parser.add_argument(
        '--categorize',
        action='store_true',
        help='Whether to categorize changes (default: True)'
    )
    parser.add_argument(
        '--output_dir',
        type=Path,
        help='Output directory for results'
    )
    
    args = parser.parse_args()
    
    # Update checker configuration if needed
    if args.feature != "CDX_Cog" or not args.categorize:
        checker.feature_name = args.feature
        checker.categorize = args.categorize
    
    # Run the checker through the pipeline
    run_qc_for_each_domain(
        log_filename=f"Feature_Between_Visits_Checker_{args.feature}.log",
        qc_func=run_feature_change_tracker,
        filename_suffix=f"{args.feature}Changes_Visits",
        check_exists=False
    )

if __name__ == '__main__':
    main() 