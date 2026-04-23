#!/usr/bin/env python3
"""
Package health checker with comprehensive analysis.

Reports:
- File metrics: line counts, long functions, large classes
- Complexity: cyclomatic complexity for functions and classes
- Imports: dependency graph, deep imports, orphans
- Cohesion: internal vs external import ratio
- Duplication: code clone detection
- SOLID: principle violation detection
- Dead code: unused imports, unreachable code

Usage:
  python tools/package_health.py [--root PATH] [--json] [--config FILE]
  python tools/package_health.py --root csiro-scripts/scripts

Defaults: --root csiro-scripts/scripts
"""

import argparse
import json
import sys
from pathlib import Path

# Add tools directory to path
tools_dir = Path(__file__).parent
if str(tools_dir) not in sys.path:
    sys.path.insert(0, str(tools_dir))

from analyzers import (
    FileMetricsAnalyzer,
    ComplexityAnalyzer,
    ImportAnalyzer,
    CohesionAnalyzer,
    DuplicationDetector,
    SOLIDChecker,
    DeadCodeFinder
)
from reporters import ConsoleReporter, JSONReporter
from thresholds import ThresholdConfig


def main() -> None:
    """Main entry point for package health analysis."""
    # Set UTF-8 encoding for Windows compatibility
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    
    default_root = Path(__file__).resolve().parent.parent / "csiro-scripts" / "scripts"
    
    parser = argparse.ArgumentParser(
        description="Package health checker with comprehensive analysis.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--root", type=Path, default=default_root, help="Scripts root directory")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--config", type=Path, help="Threshold configuration file (JSON)")
    parser.add_argument("--no-complexity", action="store_true", help="Skip complexity analysis")
    parser.add_argument("--no-duplication", action="store_true", help="Skip duplication detection")
    parser.add_argument("--no-solid", action="store_true", help="Skip SOLID checks")
    parser.add_argument("--no-dead-code", action="store_true", help="Skip dead code detection")
    
    args = parser.parse_args()
    
    if not args.root.is_dir():
        print(f"❌ Error: Root is not a directory: {args.root}")
        return 1
    
    # Load threshold config
    config = ThresholdConfig()
    if args.config and args.config.exists():
        with open(args.config) as f:
            config = ThresholdConfig.from_dict(json.load(f))
    
    # Run analyzers
    results = {'root': str(args.root)}
    
    # File metrics (always run)
    print("📄 Analyzing file metrics...")
    file_metrics = FileMetricsAnalyzer(args.root)
    results['file_metrics'] = file_metrics.analyze()
    
    # Complexity
    if not args.no_complexity:
        print("🔢 Analyzing complexity...")
        complexity = ComplexityAnalyzer(args.root)
        results['complexity'] = complexity.analyze()
    
    # Imports
    print("📦 Analyzing imports...")
    imports = ImportAnalyzer(args.root)
    results['imports'] = imports.analyze()
    
    # Cohesion
    print("🎯 Analyzing package cohesion...")
    cohesion = CohesionAnalyzer(args.root)
    results['cohesion'] = cohesion.analyze()
    
    # Duplication
    if not args.no_duplication:
        print("🔄 Detecting code duplication...")
        duplication = DuplicationDetector(args.root, min_lines=config.min_duplicate_lines)
        results['duplication'] = duplication.analyze()
    
    # SOLID
    if not args.no_solid:
        print("🏛️ Checking SOLID principles...")
        solid = SOLIDChecker(args.root)
        results['solid'] = solid.analyze()
    
    # Dead code
    if not args.no_dead_code:
        print("💀 Finding dead code...")
        dead_code = DeadCodeFinder(args.root)
        results['dead_code'] = dead_code.analyze()
    
    # Generate report
    if args.json:
        reporter = JSONReporter()
    else:
        reporter = ConsoleReporter()
    
    report = reporter.report(results)
    print()
    print(report)
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
