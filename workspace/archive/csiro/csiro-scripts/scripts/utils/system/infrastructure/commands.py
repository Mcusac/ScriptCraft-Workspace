# command_utils.py
# Utilities for running commands and subprocess management

import subprocess
import sys
import os
import logging
from typing import List, Tuple, Optional

logger = logging.getLogger(__name__)


def run_command_with_streaming(
    cmd: List[str],
    description: Optional[str] = None,
    error_tail_lines: Optional[int] = None,
    keep_last_n: int = 200
) -> Tuple[int, List[str]]:
    """
    Run a command and stream output in real-time.
    
    Thin wrapper that displays output in real-time and limits memory usage.
    Scripts handle their own logging via --log-file CLI argument.
    
    Args:
        cmd: List of command arguments
        description: Optional description to print before running
        error_tail_lines: Number of lines to include in error message (default: all)
        keep_last_n: Number of lines to keep in memory for error reporting (default: 200)
    
    Returns:
        Tuple of (returncode, stdout_lines)
    """
    if description:
        logger.info(description)
    
    # Validate command list before joining (catch None values early)
    for i, arg in enumerate(cmd):
        if arg is None:
            raise ValueError(
                f"Command list contains None at index {i}. "
                f"Command list: {cmd}\n"
                f"This is a bug in command construction - all arguments must be strings."
            )
        if not isinstance(arg, str):
            raise TypeError(
                f"Command list contains non-string at index {i}: {repr(arg)} (type: {type(arg).__name__}). "
                f"Command list: {cmd}\n"
                f"All arguments must be strings."
            )
    
    # Use logger for command output (user-facing, so INFO level)
    logger.info("Running command:")
    logger.info(' '.join(cmd))
    logger.info("")
    
    # Set environment to disable Python buffering for real-time output
    env = os.environ.copy()
    env['PYTHONUNBUFFERED'] = '1'
    
    # Use Popen to stream output in real-time
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # Merge stderr into stdout
        text=True,
        bufsize=1,  # Line buffered
        env=env
    )
    
    # Stream output line-by-line in real-time
    # Keep only last N lines in memory to prevent accumulation
    stdout_lines = []
    for line in process.stdout:
        line = line.rstrip()
        print(line)
        
        # Keep only last N lines in memory (prevents memory accumulation)
        stdout_lines.append(line)
        if len(stdout_lines) > keep_last_n:
            stdout_lines.pop(0)  # Remove oldest line
        
        # Force flush to ensure immediate output
        sys.stdout.flush()
    
    # Wait for process to complete and get return code
    returncode = process.wait()
    
    return returncode, stdout_lines

