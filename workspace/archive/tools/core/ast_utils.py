"""AST parsing utilities shared across analyzers."""

import ast
from pathlib import Path


def parse_file(file_path: Path) -> ast.AST | None:
    """
    Parse a Python file into an AST.
    
    Args:
        file_path: Path to Python file
        
    Returns:
        AST tree or None if parsing fails
    """
    try:
        return ast.parse(file_path.read_text(encoding='utf-8'), filename=str(file_path))
    except (SyntaxError, OSError):
        return None


def get_imports_from_ast(tree: ast.AST, current_pkg: str = "") -> dict[str, set[str]]:
    """
    Extract import statements from AST.
    
    Args:
        tree: AST tree
        current_pkg: Current package name for resolving relative imports
        
    Returns:
        Dictionary mapping module names to sets of imported attribute names.
        For 'import X' statements, the value is an empty set.
    """
    imports: dict[str, set[str]] = {}
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.setdefault(alias.name, set())
        elif isinstance(node, ast.ImportFrom):
            level = getattr(node, 'level', 0)
            resolved = _resolve_relative_import(level, current_pkg, node.module) if level >= 1 else node.module
            if not resolved:
                continue
            imports.setdefault(resolved, set())
            for alias in node.names:
                imports[resolved].add(alias.asname or alias.name)
    
    return imports


def get_imports_from_file(file_path: Path, current_pkg: str = "") -> dict[str, set[str]]:
    """
    Extract import statements from a Python file.
    
    Args:
        file_path: Path to Python file
        current_pkg: Current package name for resolving relative imports
        
    Returns:
        Dictionary mapping module names to sets of imported attribute names
    """
    tree = parse_file(file_path)
    if tree is None:
        return {}
    return get_imports_from_ast(tree, current_pkg)


def _resolve_relative_import(level: int, current_pkg: str, node_module: str | None) -> str | None:
    """
    Resolve relative import to absolute module name.
    
    Args:
        level: Import level (number of dots)
        current_pkg: Current package name
        node_module: Module name from import statement
        
    Returns:
        Resolved absolute module name or None
    """
    if level < 1:
        return node_module
    
    pkg_parts = current_pkg.split('.') if current_pkg else []
    up = max(0, len(pkg_parts) - (level - 1))
    base = '.'.join(pkg_parts[:up])
    
    if node_module:
        return f"{base}.{node_module}" if base else node_module
    return base or None


def count_function_nodes(tree: ast.AST) -> int:
    """Count function/method definitions in AST."""
    return sum(1 for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)))


def count_class_nodes(tree: ast.AST) -> int:
    """Count class definitions in AST."""
    return sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))


def get_function_complexity(node: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
    """
    Calculate cyclomatic complexity for a function.
    
    Uses simplified McCabe complexity calculation:
    - Start with 1
    - +1 for each if, elif, for, while, except, with, assert, bool op
    
    Args:
        node: Function AST node
        
    Returns:
        Complexity score
    """
    complexity = 1
    
    for child in ast.walk(node):
        if isinstance(child, (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.With, ast.Assert)):
            complexity += 1
        elif isinstance(child, ast.BoolOp):
            complexity += len(child.values) - 1
    
    return complexity


def get_all_functions(tree: ast.AST) -> list[tuple[str, ast.FunctionDef | ast.AsyncFunctionDef]]:
    """
    Get all function definitions from AST.
    
    Args:
        tree: AST tree
        
    Returns:
        List of (name, node) tuples
    """
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append((node.name, node))
    return functions


def get_all_classes(tree: ast.AST) -> list[tuple[str, ast.ClassDef]]:
    """
    Get all class definitions from AST.
    
    Args:
        tree: AST tree
        
    Returns:
        List of (name, node) tuples
    """
    classes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.append((node.name, node))
    return classes


def count_lines_in_node(node: ast.AST) -> int:
    """
    Count lines spanned by an AST node.
    
    Args:
        node: AST node
        
    Returns:
        Number of lines
    """
    if not hasattr(node, 'lineno') or not hasattr(node, 'end_lineno'):
        return 0
    return (node.end_lineno or node.lineno) - node.lineno + 1
