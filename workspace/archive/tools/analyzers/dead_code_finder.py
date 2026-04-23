"""Dead code finder."""

import ast
from typing import Any

from analyzers.base import BaseAnalyzer
from core import module_utils, ast_utils


class DeadCodeFinder(BaseAnalyzer):
    """
    Find potentially dead code.
    
    Detects:
    - Unused imports
    - Unreachable code after return/raise
    """
    
    @property
    def name(self) -> str:
        return "dead_code"
    
    def analyze(self) -> dict[str, Any]:
        """Find dead code."""
        files = module_utils.collect_python_files(self.root)
        
        unused_imports: list[dict[str, Any]] = []
        unreachable_code: list[dict[str, Any]] = []
        
        for file_path in files:
            module = module_utils.file_to_module(file_path, self.root)
            if not module:
                continue
            
            tree = ast_utils.parse_file(file_path)
            if not tree:
                continue
            
            # Find unused imports
            unused = self._find_unused_imports(tree, module)
            if unused:
                unused_imports.append({
                    'module': module,
                    'names': unused
                })
            
            # Find unreachable code
            unreachable = self._find_unreachable_code(tree, module)
            unreachable_code.extend(unreachable)
        
        return {
            'unused_imports': unused_imports,
            'unreachable_code': unreachable_code,
            'total_unused_imports': sum(len(u['names']) for u in unused_imports),
            'total_unreachable_blocks': len(unreachable_code),
        }
    
    def _find_unused_imports(self, tree: ast.AST, module: str) -> list[str]:
        """Find imports that are never used."""
        imports: set[str] = set()
        used_names: set[str] = set()
        
        # Collect imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.asname or alias.name.split('.')[0]
                    imports.add(name)
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    if alias.name != '*':
                        name = alias.asname or alias.name
                        imports.add(name)
        
        # Collect name usage
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                used_names.add(node.id)
            elif isinstance(node, ast.Attribute):
                # Get the root name
                curr = node
                while isinstance(curr, ast.Attribute):
                    curr = curr.value
                if isinstance(curr, ast.Name):
                    used_names.add(curr.id)
        
        # Find unused
        unused = imports - used_names
        return sorted(unused)
    
    def _find_unreachable_code(self, tree: ast.AST, module: str) -> list[dict[str, Any]]:
        """Find code after return/raise statements."""
        unreachable = []
        
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            
            # Check each function body
            for i, stmt in enumerate(node.body):
                if isinstance(stmt, (ast.Return, ast.Raise)):
                    # Check if there's code after this
                    if i < len(node.body) - 1:
                        next_stmt = node.body[i + 1]
                        unreachable.append({
                            'module': module,
                            'function': node.name,
                            'line': next_stmt.lineno,
                            'reason': f'Code after {stmt.__class__.__name__.lower()}'
                        })
        
        return unreachable
