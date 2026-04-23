#!/usr/bin/env python3
"""
Package Health Threshold Checker

Enforces code quality thresholds based on package_health.py output.
Used in CI/pre-commit hooks to maintain codebase health.

Exit codes:
- 0: All checks passed
- 1: Fatal violations
- 2: Warnings only (strict mode)
"""

import argparse
import json
import sys
from pathlib import Path

# Add tools directory to path
tools_dir = Path(__file__).parent
if str(tools_dir) not in sys.path:
    sys.path.insert(0, str(tools_dir))

from thresholds import ThresholdChecker, ThresholdConfig, Severity


def main():
    """Main entry point for threshold checking."""
    # Set UTF-8 encoding for Windows compatibility
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer, encoding='utf-8', errors='replace'
        )
        sys.stderr = io.TextIOWrapper(
            sys.stderr.buffer, encoding='utf-8', errors='replace'
        )
    
    parser = argparse.ArgumentParser(
        description='Check package health thresholds',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        'report_file',
        type=Path,
        help='Path to package_health.py JSON output'
    )
    parser.add_argument(
        '--config',
        type=Path,
        help='Threshold configuration file (JSON)'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Treat warnings as failures'
    )
    
    args = parser.parse_args()
    
    # Load report
    if not args.report_file.exists():
        print(f"❌ Error: Report file not found: {args.report_file}")
        return 1
    
    try:
        with open(args.report_file) as f:
            report = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in report file: {e}")
        return 1
    
    # Load threshold config
    config = ThresholdConfig()
    if args.config and args.config.exists():
        try:
            with open(args.config) as f:
                config = ThresholdConfig.from_dict(json.load(f))
        except (json.JSONDecodeError, TypeError) as e:
            print(f"❌ Error: Invalid threshold config: {e}")
            return 1
    
    print("=" * 80)
    print("PACKAGE HEALTH THRESHOLD CHECK")
    print("=" * 80)
    print(f"Report: {args.report_file}")
    print(f"Strict mode: {args.strict}")
    print()
    
    # Run threshold checks
    checker = ThresholdChecker(config)
    passed, violations = checker.check(report)
    
    # Group violations by severity
    fails = [v for v in violations if v.severity == Severity.FAIL]
    warns = [v for v in violations if v.severity == Severity.WARN]
    infos = [v for v in violations if v.severity == Severity.INFO]
    
    # Print results
    if fails:
        print(f"❌ FAILURES ({len(fails)}):")
        for v in fails:
            print(v)
            for detail in v.details[:5]:
                print(detail)
            if len(v.details) > 5:
                print(f"  ... and {len(v.details) - 5} more")
            print()
    
    if warns:
        print(f"⚠️  WARNINGS ({len(warns)}):")
        for v in warns:
            print(v)
            for detail in v.details[:5]:
                print(detail)
            if len(v.details) > 5:
                print(f"  ... and {len(v.details) - 5} more")
            print()
    
    if infos:
        print(f"ℹ️  INFO ({len(infos)}):")
        for v in infos:
            print(v)
            for detail in v.details[:3]:
                print(detail)
            if len(v.details) > 3:
                print(f"  ... and {len(v.details) - 3} more")
            print()
    
    # Summary
    print("=" * 80)
    
    if fails:
        print("❌ HEALTH CHECK FAILED")
        print("Fix critical violations before committing.")
        return 1
    elif warns and args.strict:
        print("⚠️  HEALTH CHECK FAILED (strict mode)")
        print("Address warnings before committing.")
        return 2
    elif warns:
        print("⚠️  HEALTH CHECK PASSED WITH WARNINGS")
        print("Consider addressing warnings to improve codebase health.")
        return 0
    else:
        print("✅ HEALTH CHECK PASSED")
        print("All thresholds met!")
        return 0


if __name__ == '__main__':
    sys.exit(main())
