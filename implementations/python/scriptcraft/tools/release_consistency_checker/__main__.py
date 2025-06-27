"""Command-line interface for the release consistency checker."""

import sys
import argparse
from pathlib import Path

from ...common import shortcuts as cu
from scriptcraft.pipelines.pipeline_utils import run_qc_for_each_domain
from . import checker

def main():
    """Entry point for command-line execution."""
    parser = argparse.ArgumentParser(description="Release Consistency Checker")
    parser.add_argument(
        "--input",
        nargs=2,
        help="Two files to compare (R5 and R6)."
    )
    parser.add_argument(
        "--domain",
        help="Optional domain name (only needed for domain mode)."
    )
    parser.add_argument(
        "--mode",
        default="old_only",
        choices=["old_only", "standard"],
        help="Comparison mode: old_only or standard."
    )
    parser.add_argument(
        "--output_dir",
        default="output",
        help="Output directory to save results."
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode for dtype checks."
    )
    
    args = parser.parse_args()

    if args.input:
        # === 🛠 Manual File Mode ===
        log_dir = Path(__file__).resolve().parent.parent / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        cu.setup_logging_with_timestamp(log_dir, mode="manual_run")
        
        checker.check_manual(
            r5_filename=args.input[0],
            r6_filename=args.input[1],
            debug=args.debug,
            mode=args.mode
        )
    else:
        # === 🧪 Domain Mode via Pipeline ===
        run_qc_for_each_domain(
            log_filename="release_consistency_checker.log",
            qc_func=checker.check,
            input_key=cu.STANDARD_KEYS["raw_data"],
            check_exists=False
        )

if __name__ == "__main__":
    main()