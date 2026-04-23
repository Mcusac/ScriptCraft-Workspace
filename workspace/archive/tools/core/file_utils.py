"""File operation utilities."""

from pathlib import Path


def count_lines(path: Path) -> int:
    """
    Count lines in a file.
    
    Args:
        path: Path to file
        
    Returns:
        Number of lines
    """
    try:
        return sum(1 for _ in path.read_text(encoding='utf-8').splitlines())
    except OSError:
        return 0


def read_file_safe(path: Path) -> str | None:
    """
    Safely read file contents.
    
    Args:
        path: Path to file
        
    Returns:
        File contents or None if read fails
    """
    try:
        return path.read_text(encoding='utf-8')
    except OSError:
        return None
