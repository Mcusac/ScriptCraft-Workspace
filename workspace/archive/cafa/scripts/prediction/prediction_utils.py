"""
Shared utility functions for prediction package.
Consolidates duplicate code patterns across prediction modules.
"""

from typing import Tuple, Optional, List
from pathlib import Path


def format_prediction_score(score: float) -> str:
    """
    Format prediction score to string with consistent precision.
    
    Args:
        score: Prediction score (0.0 to 1.0)
        
    Returns:
        str: Formatted score string (e.g., "0.123")
    """
    return f"{score:.3g}"


def is_valid_score(score: float) -> bool:
    """
    Check if score is in valid range for predictions.
    
    Args:
        score: Score to validate
        
    Returns:
        bool: True if score is in range (0, 1.0]
    """
    return 0 < score <= 1.0


def validate_go_term_format(term: str) -> Tuple[bool, Optional[str]]:
    """
    Validate GO term format.
    
    Args:
        term: GO term string to validate
        
    Returns:
        tuple: (is_valid: bool, error_message: Optional[str])
    """
    if not term.startswith('GO:'):
        return False, f"Invalid GO term format: {term} (must start with 'GO:')"
    
    if len(term) != 10:  # GO:XXXXXXX
        return False, f"Invalid GO term length: {term} (expected 10 chars, got {len(term)})"
    
    return True, None


def cleanup_temp_files(file_paths: List[Path]) -> None:
    """
    Clean up temporary files, ignoring errors.
    
    Args:
        file_paths: List of file paths to delete
    """
    for file_path in file_paths:
        try:
            Path(file_path).unlink()
        except Exception:
            pass  # Ignore errors during cleanup


def log_progress(current: int, total: int, interval: int, label: str = "") -> bool:
    """
    Check if progress should be logged based on interval.
    
    Args:
        current: Current progress count
        total: Total count
        interval: Log every N items
        label: Optional label for progress message
        
    Returns:
        bool: True if should log progress, False otherwise
    """
    return (current % interval == 0) or (current == total)

