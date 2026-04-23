# loading_utils.py
# Batch processing utilities with progress tracking

from pathlib import Path
from typing import Union, List, Callable, TypeVar, Optional, Any
from tqdm import tqdm
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')


def batch_process_with_progress(
    items: List,
    process_func: Callable[[Union[str, Path]], T],
    desc: str = "Processing",
    show_progress: bool = True,
    progress_tracker: Optional[Any] = None,
    bar_id: Optional[str] = None
) -> List[T]:
    """
    Process a list of items with optional progress tracking.
    
    Generic batch processing utility that handles progress bars and
    error handling for batch operations. Can use either tqdm directly
    or a ProgressTracker instance for more advanced tracking.
    
    Args:
        items: List of items to process. Can be empty.
        process_func: Function that takes a single item and returns processed result.
                    Should handle its own error handling.
        desc: Description for progress bar (default: "Processing").
        show_progress: Whether to show progress bar (default: True).
        progress_tracker: Optional ProgressTracker instance for advanced tracking.
        bar_id: Optional bar ID for ProgressTracker.
        
    Returns:
        List of processed results, one for each item.
        Order matches the input items list.
        
    Raises:
        ValueError: If items is not a list.
        TypeError: If process_func is not callable.
    """
    # Validate inputs
    if not isinstance(items, list):
        raise ValueError(f"items must be a list, got {type(items)}")
    
    if not callable(process_func):
        raise TypeError(f"process_func must be callable, got {type(process_func)}")
    
    if not items:
        logger.info(f"Empty {desc.lower()} list provided, returning empty list")
        return []
    
    # Setup progress tracking
    if show_progress:
        if progress_tracker is not None and bar_id is not None:
            # Use ProgressTracker if provided
            progress_tracker.create_bar(
                bar_id=bar_id,
                total=len(items),
                desc=desc,
                level=3,  # Data loading is typically nested
                unit="item"
            )
            items_iter = items
        else:
            # Fallback to tqdm
            items_iter = tqdm(items, desc=desc)
    else:
        items_iter = items
    
    # Process all items
    results = []
    for idx, item in enumerate(items_iter):
        result = process_func(item)
        results.append(result)
        
        # Update progress tracker if using it
        if progress_tracker is not None and bar_id is not None:
            progress_tracker.update(bar_id, n=1)
    
    # Close progress tracker bar if using it
    if progress_tracker is not None and bar_id is not None:
        progress_tracker.close(bar_id)
    
    logger.info(f"Successfully processed {len(results)} items")
    return results

