"""
Logging package for the project.

This package provides logging functionality organized into:
- core: Basic logging setup and configuration
- formatters: Log message formatting
- handlers: Log output handlers
- context: Logging context management
- utils: Additional logging utilities
"""

from .core import setup_logger, log_and_print, log_message, log_fix_summary
from .formatters import create_formatter, QCFormatter, TimestampFormatter
from .handlers import (
    create_file_handler,
    create_console_handler
)
from .context import qc_log_context, with_domain_logger
from .utils import (
    setup_logging_with_timestamp,
    setup_logging_with_config,
    setup_secondary_log,
    add_file_handler,
    log_fix_summary as utils_log_fix_summary
)

# Alias for backward compatibility
setup_logging = setup_logger

__all__ = [
    'setup_logger',
    'setup_logging',
    'log_and_print',
    'log_message',
    'log_fix_summary',
    'create_formatter',
    'QCFormatter',
    'TimestampFormatter',
    'create_file_handler',
    'create_console_handler',
    'add_file_handler',
    'setup_secondary_log',
    'qc_log_context',
    'with_domain_logger',
    'setup_logging_with_timestamp',
    'setup_logging_with_config'
] 