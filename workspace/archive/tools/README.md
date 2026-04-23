# Code Health Tools

Comprehensive code health checking and analysis tools for maintaining codebase quality.

## Overview

This package provides modular, extensible tools for analyzing Python codebases with a focus on DRY, SOLID principles, and code quality metrics.

## Structure

```
tools/
├── package_health.py          # Main CLI for comprehensive analysis
├── check_health_thresholds.py # Threshold enforcement for CI/CD
├── analyzers/                 # Pluggable analyzers (SRP)
│   ├── base.py               # BaseAnalyzer abstract class
│   ├── file_metrics.py       # File length, function/class size
│   ├── complexity.py         # Cyclomatic complexity (McCabe)
│   ├── import_analyzer.py    # Import dependencies, orphans
│   ├── cohesion_analyzer.py  # Package cohesion metrics
│   ├── duplication_detector.py # Code clone detection
│   ├── solid_checker.py      # SOLID principle violations
│   └── dead_code_finder.py   # Unused code detection
├── reporters/                 # Output formatters (SRP)
│   ├── base.py               # BaseReporter abstract class
│   ├── console_reporter.py   # Human-readable output
│   └── json_reporter.py      # Machine-readable JSON
├── thresholds/                # Quality enforcement (OCP)
│   ├── config.py             # ThresholdConfig dataclass
│   └── checker.py            # ThresholdChecker with violations
└── core/                      # Shared utilities (DRY)
    ├── ast_utils.py          # AST parsing and analysis
    ├── module_utils.py       # Module discovery and resolution
    └── file_utils.py         # File operations
```

## Usage

### Package Health Analysis

Run comprehensive health analysis:

```bash
python tools/package_health.py --root csiro-scripts/scripts
```

Generate JSON output for CI:

```bash
python tools/package_health.py --root csiro-scripts/scripts --json > health_report.json
```

Skip specific analyzers:

```bash
python tools/package_health.py --no-duplication --no-dead-code
```

### Threshold Checking

Enforce quality standards:

```bash
python tools/check_health_thresholds.py health_report.json
```

Strict mode (warnings fail):

```bash
python tools/check_health_thresholds.py health_report.json --strict
```

Custom thresholds:

```bash
python tools/check_health_thresholds.py health_report.json --config thresholds.json
```

## Health Metrics

### File Metrics
- **Long files**: Files exceeding line thresholds
- **Long functions**: Functions > 50 lines
- **Large classes**: Classes with > 7 methods

### Complexity
- **Cyclomatic complexity**: McCabe complexity for functions
- **Class complexity**: Aggregate method complexity
- Flags: Functions > 10, Classes > 50

### Imports
- **Import map**: Internal dependency graph
- **Deep imports**: Imports with depth >= 4
- **Cross-package imports**: Dependencies across package boundaries
- **Orphans**: Modules with no incoming dependencies

### Cohesion
- **Internal ratio**: % of imports within same package
- **External dependencies**: Cross-package dependencies
- **Third-party usage**: External library dependencies
- Target: >= 25% internal cohesion

### Duplication
- **Token-based detection**: MD5 hash matching
- **Configurable threshold**: Minimum duplicate block size
- Flags: > 5 duplicate blocks

### SOLID Principles
- **SRP violations**: Functions > 50 lines, classes > 7 methods
- **DIP violations**: Deep cross-package concrete imports
- **OCP indicators**: Hardcoded conditionals (basic heuristic)

### Dead Code
- **Unused imports**: Imported but never referenced
- **Unreachable code**: Code after return/raise statements

## Thresholds

Default thresholds (configurable via JSON):

```json
{
  "max_file_lines": 500,
  "max_function_lines": 50,
  "max_class_methods": 7,
  "max_function_complexity": 10,
  "max_class_complexity": 50,
  "min_package_cohesion_pct": 25,
  "max_deep_imports": 30,
  "max_import_depth": 4,
  "max_duplicate_blocks": 5,
  "min_duplicate_lines": 6
}
```

## Exit Codes

`check_health_thresholds.py`:
- **0**: All checks passed
- **1**: Fatal violations (file length, etc.)
- **2**: Warnings only (strict mode)

## CI/CD Integration

See `.github/workflows/package-health.yml` for GitHub Actions integration.

Typical workflow:
1. Run `package_health.py --json` to generate report
2. Run `check_health_thresholds.py --strict` to enforce standards
3. Upload JSON report as artifact
4. Comment on PR with violations (if any)

## Design Principles

### SOLID
- **Single Responsibility**: Each analyzer does one thing
- **Open/Closed**: Add new analyzers without modifying existing code
- **Liskov Substitution**: All analyzers implement BaseAnalyzer
- **Interface Segregation**: Minimal, focused interfaces
- **Dependency Inversion**: Depend on abstractions (base classes)

### DRY
- Shared utilities in `core/` package
- No code duplication between analyzers and test suite
- Single source of truth for module discovery, AST parsing

### Extensibility
- Add new analyzers by inheriting from `BaseAnalyzer`
- Add new reporters by inheriting from `BaseReporter`
- Custom threshold configs via JSON

## Migration Notes

### Breaking Changes from Old Version
- Removed backward compatibility code
- No legacy nested path handling
- Deprecated functions removed
- Old metadata format no longer supported

### Benefits
- 50% reduction in code duplication
- Modular, testable architecture
- Comprehensive health metrics
- Easy to extend with new checks
- Better adherence to SOLID principles
