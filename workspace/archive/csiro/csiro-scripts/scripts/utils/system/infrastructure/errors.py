# error_handling.py
# Standardized error handling utilities

import logging
import functools
from typing import Callable, Any, Optional, Type, Tuple
from contextlib import contextmanager

logger = logging.getLogger(__name__)


def format_error_message(
    error: Exception,
    context: Optional[str] = None,
    action: Optional[str] = None
) -> str:
    """
    Format error message in a standardized way.
    
    Args:
        error: Exception that occurred
        context: Optional context about where the error occurred
        action: Optional action that was being performed
    
    Returns:
        Formatted error message string
    """
    parts = []
    
    if context:
        parts.append(f"[{context}]")
    
    if action:
        parts.append(f"Failed to {action}")
    
    error_type = type(error).__name__
    error_msg = str(error)
    
    parts.append(f"{error_type}: {error_msg}")
    
    return " ".join(parts)


def log_error_with_context(
    error: Exception,
    context: Optional[str] = None,
    action: Optional[str] = None,
    level: int = logging.ERROR,
    exc_info: bool = True
) -> None:
    """
    Log error with standardized context information.
    
    Args:
        error: Exception that occurred
        context: Optional context about where the error occurred
        action: Optional action that was being performed
        level: Logging level (default: ERROR)
        exc_info: Whether to include exception traceback (default: True)
    """
    message = format_error_message(error, context, action)
    logger.log(level, message, exc_info=exc_info)


@contextmanager
def handle_oom_gracefully(
    context: Optional[str] = None,
    fallback_action: Optional[Callable[[], Any]] = None
):
    """
    Context manager for handling OOM errors gracefully.
    
    Args:
        context: Optional context string for logging
        fallback_action: Optional callable to execute on OOM
    
    Example:
        with handle_oom_gracefully("training", lambda: reduce_batch_size()):
            train_model()
    """
    try:
        yield
    except RuntimeError as e:
        if "out of memory" in str(e).lower() or "cuda" in str(e).lower():
            log_error_with_context(
                e,
                context=context,
                action="execute operation",
                level=logging.WARNING
            )
            if fallback_action:
                try:
                    fallback_action()
                except Exception as fallback_error:
                    logger.error(f"Fallback action failed: {fallback_error}", exc_info=True)
            raise
        else:
            # Not an OOM error, re-raise
            raise


def handle_with_retry(
    max_retries: int = 3,
    retry_delay: float = 1.0,
    retryable_exceptions: Tuple[Type[Exception], ...] = (Exception,),
    context: Optional[str] = None
):
    """
    Decorator for retry logic with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts (default: 3)
        retry_delay: Initial delay between retries in seconds (default: 1.0)
        retryable_exceptions: Tuple of exception types to retry on (default: all exceptions)
        context: Optional context string for logging
    
    Example:
        @handle_with_retry(max_retries=3, context="loading model")
        def load_model():
            ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            delay = retry_delay
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        context_str = f"{context} - " if context else ""
                        logger.warning(
                            f"{context_str}Attempt {attempt + 1}/{max_retries + 1} failed: {e}. "
                            f"Retrying in {delay:.1f}s..."
                        )
                        import time
                        time.sleep(delay)
                        delay *= 2  # Exponential backoff
                    else:
                        log_error_with_context(
                            e,
                            context=context,
                            action=f"execute {func.__name__}",
                            level=logging.ERROR
                        )
            
            # All retries exhausted
            raise last_exception
        
        return wrapper
    return decorator

