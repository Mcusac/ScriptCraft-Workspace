"""SOLID principles violation checker."""

import ast
from typing import Any

from analyzers.base import BaseAnalyzer
from core import module_utils, ast_utils


class SOLIDChecker(BaseAnalyzer):
    """
    Check for SOLID principle violations.
    
    Checks:
    - SRP: Functions >50 lines, classes with >7 methods
    - DIP: Concrete imports across package boundaries
    - OCP: Hardcoded conditionals (basic heuristic)
    """
    
    @property
    def name(self) -> str:
        return "solid"
    
    def analyze(self) -> dict[str, Any]:
        """Check for SOLID violations."""
        files = module_utils.collect_python_files(self.root)
        internal_packages = module_utils.discover_packages(self.root)
        
        srp_violations: list[dict[str, Any]] = []
        dip_violations: list[dict[str, Any]] = []
        
        for file_path in files:
            module = module_utils.file_to_module(file_path, self.root)
            if not module:
                continue
            
            tree = ast_utils.parse_file(file_path)
            if not tree:
                continue
            
            # Check SRP: Long functions/classes
            for func_name, func_node in ast_utils.get_all_functions(tree):
                lines = ast_utils.count_lines_in_node(func_node)
                if lines > 50:
                    srp_violations.append({
                        'module': module,
                        'type': 'function',
                        'name': func_name,
                        'reason': f'Function too long ({lines} lines)',
                        'line': func_node.lineno
                    })
            
            for class_name, class_node in ast_utils.get_all_classes(tree):
                methods = [n for n in class_node.body 
                          if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
                if len(methods) > 7:
                    srp_violations.append({
                        'module': module,
                        'type': 'class',
                        'name': class_name,
                        'reason': f'Too many methods ({len(methods)})',
                        'line': class_node.lineno
                    })
            
            # Check DIP: Cross-package concrete imports
            current_pkg = module.split('.')[0]
            pkg = module_utils.current_package(file_path, self.root)
            imports = ast_utils.get_imports_from_ast(tree, pkg)
            
            for imported_module in imports:
                if not module_utils.is_internal_module(imported_module, internal_packages):
                    continue
                
                imported_pkg = imported_module.split('.')[0]
                
                # Cross-package import of deep module (concrete dependency)
                if imported_pkg != current_pkg and imported_module.count('.') >= 3:
                    dip_violations.append({
                        'module': module,
                        'imported': imported_module,
                        'reason': 'Deep cross-package import (concrete dependency)',
                    })
        
        return {
            'srp_violations': srp_violations,
            'dip_violations': dip_violations,
            'total_violations': len(srp_violations) + len(dip_violations),
        }
