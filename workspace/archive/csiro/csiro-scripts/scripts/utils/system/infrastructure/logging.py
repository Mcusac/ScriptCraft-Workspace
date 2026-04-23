# logging_utils.py
# Utilities for logging configuration

import logging
import sys
from pathlib import Path
from typing import Optional, Union


def setup_logging(
    log_level: int = logging.INFO,
    log_file: Optional[Union[str, Path]] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Set up logging configuration with console and optional file handlers.
    
    Args:
        log_level: Logging level (default: logging.INFO).
                   Must be a valid logging level constant (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_file: Optional path to log file. If provided, logs will also be written to file.
                 Parent directory will be created if it doesn't exist.
        format_string: Optional custom format string for log messages.
                      If None, uses default format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'.
        
    Returns:
        Configured root logger with console handler (and file handler if log_file provided).
        
    Raises:
        ValueError: If log_level is invalid or log_file path is invalid.
        PermissionError: If log_file cannot be written due to permissions.
        OSError: If log_file directory cannot be created.
    """
    # Validate log_level
    valid_levels = {logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL}
    if log_level not in valid_levels:
        raise ValueError(
            f"Invalid log_level: {log_level}. "
            f"Must be one of: {sorted(valid_levels)}"
        )
    
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    if not isinstance(format_string, str) or not format_string:
        raise ValueError(f"format_string must be non-empty string, got {format_string}")
    
    # Create formatter
    formatter = logging.Formatter(format_string)
    
    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Remove existing handlers
    logger.handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        log_path = Path(log_file)
        
        # Ensure parent directory exists
        from ..io.paths import ensure_dir
        ensure_dir(log_path.parent)
        
        try:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except PermissionError as e:
            raise PermissionError(f"Permission denied writing to log file {log_path}: {e}")
        except OSError as e:
            raise OSError(f"Failed to create log file {log_path}: {e}")
    
    return logger



