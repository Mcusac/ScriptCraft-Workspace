"""Import dependency analyzer."""

from typing import Any

from analyzers.base import BaseAnalyzer
from core import module_utils, ast_utils


class ImportAnalyzer(BaseAnalyzer):
    """
    Analyze import dependencies and relationships.
    
    Provides:
    - Import map (who imports what)
    - Deep imports (depth >= 4)
    - Cross-package imports
    - Incoming dependencies
    - Orphaned modules
    """
    
    @property
    def name(self) -> str:
        return "imports"
    
    def analyze(self) -> dict[str, Any]:
        """Analyze import dependencies."""
        files = module_utils.collect_python_files(self.root)
        internal_packages = module_utils.discover_packages(self.root)
        
        file_imports: dict[str, dict[str, set[str]]] = {}
        
        # Collect all imports
        for file_path in files:
            module = module_utils.file_to_module(file_path, self.root)
            if not module:
                continue
            
            pkg = module_utils.current_package(file_path, self.root)
            imports = ast_utils.get_imports_from_file(file_path, pkg)
            file_imports[module] = imports
        
        # Build internal dependencies
        internal_deps: dict[str, list[str]] = {}
        incoming: dict[str, set[str]] = {}
        
        for importer, deps in file_imports.items():
            internal_list = [
                d for d in deps
                if module_utils.is_internal_module(d, internal_packages)
            ]
            internal_deps[importer] = internal_list
            
            for dep in internal_list:
                incoming.setdefault(dep, set()).add(importer)
        
        # Find deep imports
        deep_imports = []
        deep_cross_package = []
        
        for importer, deps in internal_deps.items():
            importer_pkg = importer.split('.')[0]
            
            for dep in deps:
                parts = dep.split('.')
                depth = len(parts)
                
                if depth >= 4:
                    is_cross_package = importer_pkg != parts[0]
                    
                    import_info = {
                        'importer': importer,
                        'imported': dep,
                        'depth': depth,
                        'cross_package': is_cross_package
                    }
                    
                    deep_imports.append(import_info)
                    
                    if is_cross_package:
                        deep_cross_package.append(import_info)
        
        # Find orphans (modules with no incoming imports)
        all_internal = {
            m for m in file_imports
            if module_utils.is_internal_module(m, internal_packages)
        }
        
        # Exclude entry points and __init__ modules
        entry_points = {'run', '__init__'}
        roots_ok = {
            m for m in all_internal
            if m.split('.')[-1] in entry_points or m == 'run'
        }
        
        orphans = sorted([
            m for m in all_internal
            if m not in roots_ok and m not in incoming
        ])
        
        return {
            'import_map': {mod: sorted(deps) for mod, deps in internal_deps.items()},
            'deep_imports': deep_imports,
            'deep_cross_package': deep_cross_package,
            'incoming': {k: sorted(v) for k, v in incoming.items()},
            'orphans': orphans,
        }
