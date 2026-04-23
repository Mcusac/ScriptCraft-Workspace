"""
Centralized logging utilities.

Provides idempotent setup and module-level logger factory.
"""

from __future__ import annotations

import logging
import os
import sys
from typing import Optional


_LOGGING_CONFIGURED = False


def setup_logging(level: Optional[str] = None) -> None:
    """
    Configure root logger to stream to stdout with a simple, uniform format.
    Idempotent: safe to call multiple times.
    
    Args:
        level: Optional log level name (e.g., 'INFO', 'DEBUG'). If not provided,
               uses environment variable LOG_LEVEL or defaults to INFO.
    """
    global _LOGGING_CONFIGURED
    if _LOGGING_CONFIGURED:
        return

    log_level_name = (level or os.getenv("LOG_LEVEL") or "INFO").upper()
    log_level = getattr(logging, log_level_name, logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(log_level)
    root.addHandler(handler)

    _LOGGING_CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """
    Get a module-level logger.
    """
    return logging.getLogger(name)


