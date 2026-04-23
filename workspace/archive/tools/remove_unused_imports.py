#!/usr/bin/env python3
"""
Remove unused imports from Python files based on package health report.

Usage:
  python tools/remove_unused_imports.py --report unused_imports_report.json --dry-run
  python tools/remove_unused_imports.py --report unused_imports_report.json
"""

import argparse
import json
import re
from pathlib import Path
from typing import Any


class UnusedImportRemover:
    """Remove unused imports from Python files."""
    
    def __init__(self, root: Path, dry_run: bool = False):
        self.root = root
        self.dry_run = dry_run
        self.stats = {
            'files_modified': 0,
            'imports_removed': 0,
            'lines_removed': 0
        }
    
    def process_report(self, report_data: dict[str, Any]) -> None:
        """Process the health report and remove unused imports."""
        unused_imports = report_data['dead_code']['unused_imports']
        
        print(f"📋 Processing {len(unused_imports)} modules with unused imports...")
        print(f"   Mode: {'DRY RUN' if self.dry_run else 'EXECUTE'}")
        print()
        
        for module_info in unused_imports:
            self._process_module(module_info)
        
        self._print_summary()
    
    def _process_module(self, module_info: dict[str, Any]) -> None:
        """Process a single module to remove unused imports."""
        module = module_info['module']
        unused_names = set(module_info['names'])
        
        # Convert module name to file path
        file_path = self.root / module.replace('.', '\\')
        
        # Check if it's a directory (package) -> use __init__.py
        if file_path.is_dir():
            file_path = file_path / '__init__.py'
        elif not file_path.exists():
            # Try adding .py extension
            file_path = file_path.with_suffix('.py')
        
        if not file_path.exists() or not file_path.is_file():
            print(f"⚠️  {module}: File not found at {file_path}")
            return
        
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
            lines = original_content.splitlines(keepends=True)
        
        # Process imports
        modified_lines, removed_count = self._remove_unused_imports(
            lines, unused_names, module
        )
        
        if removed_count == 0:
            return
        
        # Check if anything changed
        modified_content = ''.join(modified_lines)
        if modified_content == original_content:
            return
        
        # Show changes
        print(f"{'🔍' if self.dry_run else '✅'} {module}")
        print(f"   Removed: {', '.join(sorted(unused_names)[:5])}")
        if len(unused_names) > 5:
            print(f"   ... and {len(unused_names) - 5} more")
        
        # Write if not dry run
        if not self.dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
        
        self.stats['files_modified'] += 1
        self.stats['imports_removed'] += removed_count
    
    def _remove_unused_imports(
        self, 
        lines: list[str], 
        unused_names: set[str],
        module: str
    ) -> tuple[list[str], int]:
        """
        Remove unused imports from lines.
        
        Returns:
            (modified_lines, count_removed)
        """
        modified_lines = []
        removed_count = 0
        lines_removed = 0
        i = 0
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            # Handle multi-line imports
            if stripped.startswith('from ') or stripped.startswith('import '):
                full_import = line
                j = i
                
                # Collect multi-line import
                while j < len(lines) and (
                    '(' in full_import or 
                    (stripped and stripped.endswith('\\'))
                ):
                    j += 1
                    if j < len(lines):
                        full_import += lines[j]
                        if ')' in lines[j]:
                            break
                
                # Parse and modify the import
                modified, removed = self._modify_import_statement(
                    lines[i:j+1], unused_names
                )
                
                if removed > 0:
                    removed_count += removed
                    if not modified:  # Entire import removed
                        lines_removed += (j - i + 1)
                        i = j + 1
                        continue
                    else:
                        modified_lines.extend(modified)
                        i = j + 1
                        continue
                else:
                    modified_lines.append(line)
                    i += 1
            else:
                modified_lines.append(line)
                i += 1
        
        self.stats['lines_removed'] += lines_removed
        return modified_lines, removed_count
    
    def _modify_import_statement(
        self, 
        import_lines: list[str],
        unused_names: set[str]
    ) -> tuple[list[str] | None, int]:
        """
        Modify an import statement to remove unused names.
        
        Returns:
            (modified_lines or None if entire import removed, count_removed)
        """
        full_import = ''.join(import_lines)
        original_import = full_import
        removed_count = 0
        
        # Handle "import X, Y, Z" or "import X as Y"
        if full_import.strip().startswith('import '):
            import_match = re.match(r'(\s*)import\s+(.+)', full_import, re.DOTALL)
            if import_match:
                indent, import_part = import_match.groups()
                
                # Split by commas, handling "as" aliases
                imports = [item.strip() for item in import_part.split(',')]
                kept_imports = []
                
                for imp in imports:
                    # Extract base name (before "as" if present)
                    base_name = imp.split()[0].split('.')[0]
                    if base_name not in unused_names:
                        kept_imports.append(imp)
                    else:
                        removed_count += 1
                
                if not kept_imports:
                    return None, removed_count
                
                if removed_count > 0:
                    new_import = f"{indent}import {', '.join(kept_imports)}\n"
                    return [new_import], removed_count
        
        # Handle "from X import Y, Z" or "from X import (Y, Z)"
        elif full_import.strip().startswith('from '):
            from_match = re.match(
                r'(\s*)from\s+(\S+)\s+import\s+(.+)',
                full_import,
                re.DOTALL
            )
            if from_match:
                indent, module, import_part = from_match.groups()
                
                # Check for parentheses
                has_parens = '(' in import_part
                import_part = import_part.strip()
                if has_parens:
                    import_part = re.sub(r'[()]', '', import_part)
                
                # Split imports, handling "as" aliases and comments
                import_items = []
                for item in import_part.split(','):
                    item = item.strip()
                    if item and not item.startswith('#'):
                        import_items.append(item)
                
                kept_imports = []
                for item in import_items:
                    # Extract name (before "as" if present)
                    parts = item.split()
                    name = parts[0] if parts else ''
                    
                    if name and name not in unused_names:
                        kept_imports.append(item)
                    elif name in unused_names:
                        removed_count += 1
                
                if not kept_imports:
                    return None, removed_count
                
                if removed_count > 0:
                    # Reconstruct import
                    if len(kept_imports) == 1 or not has_parens:
                        new_import = f"{indent}from {module} import {', '.join(kept_imports)}\n"
                    else:
                        # Multi-line format
                        new_import = f"{indent}from {module} import (\n"
                        for imp in kept_imports[:-1]:
                            new_import += f"{indent}    {imp},\n"
                        new_import += f"{indent}    {kept_imports[-1]}\n"
                        new_import += f"{indent})\n"
                    
                    return [new_import], removed_count
        
        return import_lines, 0
    
    def _print_summary(self) -> None:
        """Print summary of changes."""
        print()
        print("=" * 80)
        print("📊 SUMMARY")
        print("=" * 80)
        print(f"Files {'would be ' if self.dry_run else ''}modified: {self.stats['files_modified']}")
        print(f"Imports {'would be ' if self.dry_run else ''}removed: {self.stats['imports_removed']}")
        print(f"Lines {'would be ' if self.dry_run else ''}removed: {self.stats['lines_removed']}")
        
        if self.dry_run:
            print()
            print("ℹ️  This was a DRY RUN. No files were modified.")
            print("   Run without --dry-run to apply changes.")
        else:
            print()
            print("✅ Changes applied successfully!")


def main() -> int:
    """Main entry point."""
    # Set UTF-8 encoding for Windows compatibility
    import sys
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer, encoding='utf-8', errors='replace'
        )
        sys.stderr = io.TextIOWrapper(
            sys.stderr.buffer, encoding='utf-8', errors='replace'
        )
    
    parser = argparse.ArgumentParser(
        description="Remove unused imports based on package health report"
    )
    parser.add_argument(
        '--report',
        type=Path,
        required=True,
        help='Path to JSON report from package_health.py'
    )
    parser.add_argument(
        '--root',
        type=Path,
        help='Root directory of scripts (default: csiro-scripts/scripts)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without modifying files'
    )
    
    args = parser.parse_args()
    
    # Load report
    if not args.report.exists():
        print(f"❌ Report file not found: {args.report}")
        return 1
    
    with open(args.report, 'r', encoding='utf-8') as f:
        report_data = json.load(f)
    
    # Determine root
    if args.root:
        root = args.root
    else:
        root = Path(__file__).resolve().parent.parent / "csiro-scripts" / "scripts"
    
    if not root.exists():
        print(f"❌ Root directory not found: {root}")
        return 1
    
    # Process
    remover = UnusedImportRemover(root, args.dry_run)
    remover.process_report(report_data)
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
