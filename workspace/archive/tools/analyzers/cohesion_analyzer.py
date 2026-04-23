"""Package cohesion analyzer."""

from typing import Any

from analyzers.base import BaseAnalyzer
from core import module_utils, ast_utils


class CohesionAnalyzer(BaseAnalyzer):
    """
    Analyze package cohesion.
    
    Measures ratio of internal vs external imports per package.
    High cohesion = package uses its own modules more than external ones.
    """
    
    @property
    def name(self) -> str:
        return "cohesion"
    
    def analyze(self) -> dict[str, Any]:
        """Analyze package cohesion."""
        files = module_utils.collect_python_files(self.root)
        internal_packages = module_utils.discover_packages(self.root)
        
        cohesion: dict[str, dict[str, Any]] = {}
        
        for file_path in files:
            module = module_utils.file_to_module(file_path, self.root)
            if not module:
                continue
            
            pkg = module.split('.')[0]
            current_pkg = module_utils.current_package(file_path, self.root)
            imports = ast_utils.get_imports_from_file(file_path, current_pkg)
            
            # Initialize package stats
            cohesion.setdefault(pkg, {
                'internal': 0,
                'external': 0,
                'third_party': 0,
                'files': 0
            })
            
            cohesion[pkg]['files'] += 1
            
            # Categorize imports
            internal_set = set()
            external_set = set()
            third_party_set = set()
            
            for dep in imports:
                if module_utils.is_third_party_module(dep, internal_packages):
                    # Third-party dependency
                    third_party_set.add(dep.split('.')[0])
                elif dep.split('.')[0] == pkg:
                    # Internal to same package
                    internal_set.add(dep)
                else:
                    # External (other internal package)
                    external_set.add(dep)
            
            cohesion[pkg]['internal'] += len(internal_set)
            cohesion[pkg]['external'] += len(external_set)
            cohesion[pkg]['third_party'] += len(third_party_set)
        
        # Calculate percentages
        for pkg_stats in cohesion.values():
            total = pkg_stats['internal'] + pkg_stats['external'] + pkg_stats['third_party']
            if total > 0:
                pkg_stats['internal_pct'] = round(100 * pkg_stats['internal'] / total, 1)
            else:
                pkg_stats['internal_pct'] = 0
        
        return cohesion
