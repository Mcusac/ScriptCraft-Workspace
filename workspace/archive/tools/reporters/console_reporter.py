"""Console reporter for human-readable output."""

from typing import Any

from reporters.base import BaseReporter


class ConsoleReporter(BaseReporter):
    """
    Generate human-readable console reports.
    
    Uses emojis and formatting for readability.
    """
    
    @property
    def format_name(self) -> str:
        return "console"
    
    def report(self, results: dict[str, Any]) -> str:
        """Generate console report."""
        lines = []
        
        lines.append("=" * 80)
        lines.append("📊 PACKAGE HEALTH REPORT")
        lines.append("=" * 80)
        lines.append(f"Root: {results.get('root', 'N/A')}")
        lines.append("")
        
        # File metrics
        if 'file_metrics' in results:
            lines.extend(self._format_file_metrics(results['file_metrics']))
        
        # Complexity
        if 'complexity' in results:
            lines.extend(self._format_complexity(results['complexity']))
        
        # Imports
        if 'imports' in results:
            lines.extend(self._format_imports(results['imports']))
        
        # Cohesion
        if 'cohesion' in results:
            lines.extend(self._format_cohesion(results['cohesion']))
        
        # Duplication
        if 'duplication' in results:
            lines.extend(self._format_duplication(results['duplication']))
        
        # SOLID
        if 'solid' in results:
            lines.extend(self._format_solid(results['solid']))
        
        # Dead code
        if 'dead_code' in results:
            lines.extend(self._format_dead_code(results['dead_code']))
        
        lines.append("")
        lines.append("✅ Report complete")
        
        return '\n'.join(lines)
    
    def _format_file_metrics(self, metrics: dict[str, Any]) -> list[str]:
        """Format file metrics section."""
        lines = ["📄 FILE METRICS", "-" * 80]
        
        long_files = metrics.get('long_files', [])
        if long_files:
            lines.append(f"Long files ({len(long_files)} total):")
            for f in long_files[:20]:
                lines.append(f"  {f['lines']:5} lines  {f['module']}")
            if len(long_files) > 20:
                lines.append(f"  ... and {len(long_files) - 20} more")
        else:
            lines.append("✓ No excessively long files")
        
        lines.append("")
        return lines
    
    def _format_complexity(self, complexity: dict[str, Any]) -> list[str]:
        """Format complexity section."""
        lines = ["🔢 COMPLEXITY", "-" * 80]
        
        high_funcs = [f for f in complexity.get('functions', []) if f['complexity'] > 10]
        if high_funcs:
            lines.append(f"High complexity functions ({len(high_funcs)} total):")
            for f in high_funcs[:15]:
                lines.append(f"  {f['complexity']:3}  {f['module']}.{f['name']} (line {f['line']})")
            if len(high_funcs) > 15:
                lines.append(f"  ... and {len(high_funcs) - 15} more")
        else:
            lines.append("✓ All functions have reasonable complexity")
        
        lines.append("")
        return lines
    
    def _format_imports(self, imports: dict[str, Any]) -> list[str]:
        """Format imports section."""
        lines = ["📦 IMPORTS", "-" * 80]
        
        deep = imports.get('deep_cross_package', [])
        if deep:
            lines.append(f"Deep cross-package imports ({len(deep)} total):")
            for imp in deep[:15]:
                lines.append(f"  {imp['importer']} → {imp['imported']} (depth {imp['depth']})")
            if len(deep) > 15:
                lines.append(f"  ... and {len(deep) - 15} more")
        else:
            lines.append("✓ No deep cross-package imports")
        
        orphans = imports.get('orphans', [])
        if orphans:
            lines.append(f"\nOrphaned modules ({len(orphans)} total):")
            for o in orphans[:15]:
                lines.append(f"  {o}")
            if len(orphans) > 15:
                lines.append(f"  ... and {len(orphans) - 15} more")
        
        lines.append("")
        return lines
    
    def _format_cohesion(self, cohesion: dict[str, Any]) -> list[str]:
        """Format cohesion section."""
        lines = ["🎯 PACKAGE COHESION", "-" * 80]
        
        for pkg in sorted(cohesion.keys()):
            if pkg == '__pycache__':
                continue
            stats = cohesion[pkg]
            pct = stats.get('internal_pct', 0)
            emoji = "✓" if pct >= 25 else "⚠️"
            lines.append(
                f"  {emoji} {pkg}: {pct}% internal "
                f"(int:{stats['internal']}, ext:{stats['external']}, 3rd:{stats['third_party']}, files:{stats['files']})"
            )
        
        lines.append("")
        return lines
    
    def _format_duplication(self, duplication: dict[str, Any]) -> list[str]:
        """Format duplication section."""
        lines = ["🔄 CODE DUPLICATION", "-" * 80]
        
        blocks = duplication.get('duplicate_blocks', [])
        if blocks:
            lines.append(f"Duplicate blocks ({len(blocks)} total):")
            for b in blocks[:10]:
                lines.append(f"  {b['file1']} ≈ {b['file2']} ({b['lines']} lines)")
            if len(blocks) > 10:
                lines.append(f"  ... and {len(blocks) - 10} more")
        else:
            lines.append("✓ No significant code duplication detected")
        
        lines.append("")
        return lines
    
    def _format_solid(self, solid: dict[str, Any]) -> list[str]:
        """Format SOLID violations section."""
        lines = ["🏛️ SOLID PRINCIPLES", "-" * 80]
        
        srp = solid.get('srp_violations', [])
        if srp:
            lines.append(f"SRP violations ({len(srp)} total):")
            for v in srp[:10]:
                lines.append(f"  {v['module']}.{v['name']}: {v['reason']}")
            if len(srp) > 10:
                lines.append(f"  ... and {len(srp) - 10} more")
        
        dip = solid.get('dip_violations', [])
        if dip:
            lines.append(f"\nDIP violations ({len(dip)} total):")
            for v in dip[:10]:
                lines.append(f"  {v['module']} → {v['imported']}: {v['reason']}")
            if len(dip) > 10:
                lines.append(f"  ... and {len(dip) - 10} more")
        
        if not srp and not dip:
            lines.append("✓ No SOLID violations detected")
        
        lines.append("")
        return lines
    
    def _format_dead_code(self, dead_code: dict[str, Any]) -> list[str]:
        """Format dead code section."""
        lines = ["💀 DEAD CODE", "-" * 80]
        
        unused = dead_code.get('unused_imports', [])
        if unused:
            lines.append(f"Modules with unused imports ({len(unused)} total):")
            for u in unused[:10]:
                names = ', '.join(u['names'][:5])
                if len(u['names']) > 5:
                    names += f" +{len(u['names']) - 5} more"
                lines.append(f"  {u['module']}: {names}")
            if len(unused) > 10:
                lines.append(f"  ... and {len(unused) - 10} more")
        
        unreachable = dead_code.get('unreachable_code', [])
        if unreachable:
            lines.append(f"\nUnreachable code blocks ({len(unreachable)} total):")
            for u in unreachable[:10]:
                lines.append(f"  {u['module']}.{u['function']}: {u['reason']} (line {u['line']})")
            if len(unreachable) > 10:
                lines.append(f"  ... and {len(unreachable) - 10} more")
        
        if not unused and not unreachable:
            lines.append("✓ No obvious dead code detected")
        
        lines.append("")
        return lines
