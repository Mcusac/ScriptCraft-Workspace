"""Module discovery and resolution utilities."""

import re
from pathlib import Path


# Skip patterns
SKIP_DIRS = {'__pycache__', '.git', '.venv', 'venv', 'node_modules'}
SKIP_FILES_RE = re.compile(r'^test_.*\.py$')


def file_to_module(file_path: Path, root: Path) -> str | None:
    """
    Convert file path to module name relative to root.
    
    Args:
        file_path: Path to Python file
        root: Root directory
        
    Returns:
        Module name (e.g., 'config.evaluation_constants') or None
    """
    try:
        rel = file_path.resolve().relative_to(root.resolve())
    except ValueError:
        return None
    
    parts = list(rel.parts)
    
    # Handle __init__.py
    if parts and parts[-1] == '__init__.py':
        parts = parts[:-1]
        return '.'.join(parts) if parts else None
    
    # Handle regular .py files
    if parts and parts[-1].endswith('.py'):
        parts[-1] = parts[-1][:-3]
    
    return '.'.join(parts) if parts else None


def current_package(file_path: Path, root: Path) -> str:
    """
    Get current package name for a file.
    
    Args:
        file_path: Path to Python file
        root: Root directory
        
    Returns:
        Package name
    """
    mod = file_to_module(file_path, root)
    if not mod:
        return ""
    
    if file_path.name == '__init__.py':
        return mod
    
    parts = mod.split('.')
    return '.'.join(parts[:-1]) if len(parts) > 1 else ""


def collect_python_files(root: Path, include_tests: bool = False) -> list[Path]:
    """
    Recursively collect Python files from directory.
    
    Args:
        root: Root directory
        include_tests: Whether to include test files
        
    Returns:
        Sorted list of Python file paths
    """
    files = []
    
    for path in root.rglob('*.py'):
        # Skip directories
        if SKIP_DIRS & set(path.parts):
            continue
        
        # Skip test files if requested
        if not include_tests and SKIP_FILES_RE.match(path.name):
            continue
        
        files.append(path)
    
    return sorted(files, key=str)


def discover_packages(root: Path) -> set[str]:
    """
    Discover all top-level packages in directory.
    
    Args:
        root: Root directory
        
    Returns:
        Set of package names
    """
    packages = set()
    
    for item in root.iterdir():
        if not item.is_dir():
            continue
        
        if item.name.startswith('_') or item.name.startswith('.'):
            continue
        
        if item.name in SKIP_DIRS:
            continue
        
        # Check if it's a Python package
        init_file = item / '__init__.py'
        has_py_files = any(f.is_file() and f.suffix == '.py' for f in item.iterdir())
        
        if init_file.exists() or has_py_files:
            packages.add(item.name)
    
    return packages


def discover_modules_in_package(package_name: str, package_root: Path) -> list[str]:
    """
    Recursively discover all modules in a package.
    
    Args:
        package_name: Base package name (e.g., 'config')
        package_root: Root path for the package
        
    Returns:
        List of full module paths (e.g., ['config.config', 'config.evaluation_constants'])
    """
    modules = []
    
    def walk_package(path: Path, current_module: str):
        """Recursively walk package directory."""
        for item in sorted(path.iterdir()):
            # Skip patterns
            if item.name.startswith('test_') or item.name == '__pycache__' or item.name.startswith('.'):
                continue
            
            if item.is_file() and item.suffix == '.py':
                # Skip __init__.py (already handled as package)
                if item.stem != '__init__':
                    module_name = f"{current_module}.{item.stem}"
                    modules.append(module_name)
            
            elif item.is_dir() and not item.name.startswith('_') and not item.name.startswith('.'):
                # Package directory
                init_file = item / '__init__.py'
                if init_file.exists():
                    new_module = f"{current_module}.{item.name}"
                    modules.append(new_module)
                    walk_package(item, new_module)
    
    walk_package(package_root, package_name)
    return sorted(modules)


def is_internal_module(module: str, internal_packages: set[str]) -> bool:
    """
    Check if module is internal (part of codebase).
    
    Args:
        module: Module name
        internal_packages: Set of internal package names
        
    Returns:
        True if module is internal
    """
    return module.split('.')[0] in internal_packages


def is_third_party_module(module: str, internal_packages: set[str]) -> bool:
    """
    Check if module is third-party (external dependency).
    
    Args:
        module: Module name
        internal_packages: Set of internal package names
        
    Returns:
        True if module is third-party
    """
    return not is_internal_module(module, internal_packages)
