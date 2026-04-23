"""Threshold checker for enforcing code health standards."""

from dataclasses import dataclass
from enum import Enum
from typing import Any

from .config import ThresholdConfig


class Severity(Enum):
    """Severity level for threshold violations."""
    FAIL = "fail"
    WARN = "warn"
    INFO = "info"


@dataclass
class Violation:
    """Represents a threshold violation."""
    category: str
    severity: Severity
    message: str
    details: list[str]
    
    def __str__(self) -> str:
        """String representation."""
        emoji = {"fail": "❌", "warn": "⚠️", "info": "ℹ️"}
        return f"{emoji[self.severity.value]} {self.message}"


class ThresholdChecker:
    """
    Checks analysis results against configured thresholds.
    
    Enforces code quality standards and reports violations.
    """
    
    def __init__(self, config: ThresholdConfig | None = None):
        """
        Initialize checker.
        
        Args:
            config: Threshold configuration (uses defaults if None)
        """
        self.config = config or ThresholdConfig()
        self.violations: list[Violation] = []
    
    def check(self, results: dict[str, Any]) -> tuple[bool, list[Violation]]:
        """
        Check results against thresholds.
        
        Args:
            results: Analysis results from analyzers
            
        Returns:
            Tuple of (passed, violations_list)
            passed is True if no FAIL violations
        """
        self.violations = []
        
        # Check file metrics
        if 'file_metrics' in results:
            self._check_file_metrics(results['file_metrics'])
        
        # Check complexity
        if 'complexity' in results:
            self._check_complexity(results['complexity'])
        
        # Check cohesion
        if 'cohesion' in results:
            self._check_cohesion(results['cohesion'])
        
        # Check imports
        if 'imports' in results:
            self._check_imports(results['imports'])
        
        # Check duplication
        if 'duplication' in results:
            self._check_duplication(results['duplication'])
        
        # Check dead code
        if 'dead_code' in results:
            self._check_dead_code(results['dead_code'])
        
        # Determine if passed
        has_failures = any(v.severity == Severity.FAIL for v in self.violations)
        return not has_failures, self.violations
    
    def _check_file_metrics(self, metrics: dict[str, Any]) -> None:
        """Check file length metrics."""
        long_files = [
            f for f in metrics.get('long_files', [])
            if f['lines'] > self.config.max_file_lines
        ]
        
        if long_files:
            details = [f"  {f['module']}: {f['lines']} lines" for f in long_files[:10]]
            if len(long_files) > 10:
                details.append(f"  ... and {len(long_files) - 10} more")
            
            self.violations.append(Violation(
                category='file_metrics',
                severity=Severity.FAIL,
                message=f"{len(long_files)} file(s) exceed {self.config.max_file_lines} lines",
                details=details
            ))
    
    def _check_complexity(self, complexity: dict[str, Any]) -> None:
        """Check complexity metrics."""
        high_complexity_funcs = [
            f for f in complexity.get('functions', [])
            if f['complexity'] > self.config.max_function_complexity
        ]
        
        if high_complexity_funcs:
            details = [
                f"  {f['module']}.{f['name']}: complexity {f['complexity']}"
                for f in high_complexity_funcs[:10]
            ]
            if len(high_complexity_funcs) > 10:
                details.append(f"  ... and {len(high_complexity_funcs) - 10} more")
            
            self.violations.append(Violation(
                category='complexity',
                severity=Severity.WARN,
                message=f"{len(high_complexity_funcs)} function(s) exceed complexity {self.config.max_function_complexity}",
                details=details
            ))
    
    def _check_cohesion(self, cohesion: dict[str, Any]) -> None:
        """Check package cohesion."""
        low_cohesion = []
        for pkg, stats in cohesion.items():
            if pkg == '__pycache__':
                continue
            pct = stats.get('internal_pct', 0)
            if pct < self.config.min_package_cohesion_pct:
                low_cohesion.append((pkg, pct))
        
        if low_cohesion:
            details = [
                f"  {pkg}: {pct}% cohesion (target {self.config.min_package_cohesion_pct}%)"
                for pkg, pct in low_cohesion
            ]
            
            self.violations.append(Violation(
                category='cohesion',
                severity=Severity.WARN,
                message=f"{len(low_cohesion)} package(s) below {self.config.min_package_cohesion_pct}% cohesion",
                details=details
            ))
    
    def _check_imports(self, imports: dict[str, Any]) -> None:
        """Check import depth."""
        deep = imports.get('deep_cross_package', [])
        if len(deep) > self.config.max_deep_imports:
            details = [
                f"  {imp['importer']} → {imp['imported']}"
                for imp in deep[:5]
            ]
            
            self.violations.append(Violation(
                category='imports',
                severity=Severity.WARN,
                message=f"{len(deep)} depth-{self.config.max_import_depth}+ cross-package imports (target <{self.config.max_deep_imports})",
                details=details
            ))
    
    def _check_duplication(self, duplication: dict[str, Any]) -> None:
        """Check code duplication."""
        blocks = duplication.get('duplicate_blocks', [])
        if len(blocks) > self.config.max_duplicate_blocks:
            details = [
                f"  {block['file1']} ≈ {block['file2']}: {block['lines']} lines"
                for block in blocks[:5]
            ]
            
            self.violations.append(Violation(
                category='duplication',
                severity=Severity.WARN,
                message=f"{len(blocks)} duplicate code blocks found (target ≤{self.config.max_duplicate_blocks})",
                details=details
            ))
    
    def _check_dead_code(self, dead_code: dict[str, Any]) -> None:
        """Check for dead code."""
        unused = dead_code.get('unused_imports', [])
        if len(unused) > self.config.max_unused_imports:
            details = [f"  {imp['module']}: {', '.join(imp['names'][:3])}" for imp in unused[:5]]
            
            self.violations.append(Violation(
                category='dead_code',
                severity=Severity.INFO,
                message=f"{len(unused)} module(s) with unused imports",
                details=details
            ))
