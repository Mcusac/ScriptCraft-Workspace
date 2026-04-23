# load_jpg.py
# Image loading utilities using PIL (not cv2)

from pathlib import Path
from typing import Union, List
from PIL import Image
import logging

from utils.system import validate_path_is_file
from dataset_manipulation.utils.loading_utils import batch_process_with_progress

logger = logging.getLogger(__name__)


def load_jpg(path: Union[str, Path], convert_rgb: bool = True) -> Image.Image:
    """
    Load JPEG image using PIL with comprehensive error handling.
    
    Args:
        path: Path to image file. Can be string or Path object.
              Supports JPEG, PNG, and other PIL-supported formats.
        convert_rgb: Whether to convert to RGB mode (default: True).
                     Handles RGBA, L (grayscale), P (palette), etc.
                     If False, returns image in original mode.
        
    Returns:
        PIL Image object in RGB mode (if convert_rgb=True) or original mode.
        
    Raises:
        ValueError: If path is invalid or empty.
        FileNotFoundError: If file doesn't exist at the specified path.
        IOError: If file cannot be opened as image (corrupted, wrong format, etc.).
        PermissionError: If file cannot be read due to permissions.
    """
    # Validate path
    path_obj = validate_path_is_file(path, file_type="Image")
    
    try:
        image = Image.open(path_obj)
        
        # Verify image was loaded successfully
        image.verify()  # Verify it's a valid image
        
        # Reopen after verify (verify closes the file)
        image = Image.open(path_obj)
        
        # Convert to RGB if needed (handles RGBA, L, P, etc.)
        if convert_rgb and image.mode != 'RGB':
            original_mode = image.mode
            image = image.convert('RGB')
            logger.debug(f"Converted image from {original_mode} to RGB: {path}")
        
        logger.debug(f"Loaded image: {path} (mode: {image.mode}, size: {image.size})")
        return image
        
    except IOError as e:
        logger.error(f"Error loading image {path}: {e}")
        raise
    except PermissionError as e:
        logger.error(f"Permission denied reading image {path}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading image {path}: {e}", exc_info=True)
        raise


def load_jpg_batch(
    paths: List[Union[str, Path]], 
    show_progress: bool = True,
    convert_rgb: bool = True
) -> List[Image.Image]:
    """
    Load multiple JPEG images in batch with optional progress tracking.
    
    Args:
        paths: List of paths to image files. Can be strings or Path objects.
               Empty list is allowed and will return empty list.
        show_progress: Whether to show progress bar using tqdm (default: True).
        convert_rgb: Whether to convert each image to RGB mode (default: True).
                     Handles RGBA, L (grayscale), P (palette), etc.
        
    Returns:
        List of PIL Image objects, one for each successfully loaded image.
        Order matches the input paths list.
        All images will be in RGB mode if convert_rgb=True.
        
    Raises:
        ValueError: If paths is not a list or contains invalid entries.
        FileNotFoundError: If any image file doesn't exist (raises on first missing file).
        IOError: If any image file cannot be opened (raises on first error).
        
    Note:
        This function will stop on the first error. For more robust batch loading
        with error handling per file, consider wrapping individual calls in try-except.
    """
    # Use batch processing utility
    return batch_process_with_progress(
        items=paths,
        process_func=lambda p: load_jpg(p, convert_rgb=convert_rgb),
        desc="Loading images",
        show_progress=show_progress
    )