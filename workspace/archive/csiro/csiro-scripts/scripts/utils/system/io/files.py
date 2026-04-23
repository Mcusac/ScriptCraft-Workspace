# file_utils.py
# Generic file operations utilities (JSON load/save, path validation)

import json
import logging
from pathlib import Path
from typing import Union, Dict, List, Any, Optional

from .paths import ensure_dir

logger = logging.getLogger(__name__)


def validate_file_exists(path: Union[str, Path], file_type: str = "file") -> Path:
    """
    Validate that a file path exists.
    
    Args:
        path: Path to validate. Can be string or Path object.
        file_type: Type of file for error messages (e.g., "CSV", "JSON", "image").
                  Default: "file".
        
    Returns:
        Path object if validation passes.
        
    Raises:
        ValueError: If path is None or empty.
        FileNotFoundError: If file doesn't exist.
    """
    if path is None:
        raise ValueError(f"{file_type} path cannot be None")
    
    if isinstance(path, str) and not path.strip():
        raise ValueError(f"{file_type} path cannot be empty string")
    
    path_obj = Path(path)
    
    if not path_obj.exists():
        raise FileNotFoundError(f"{file_type} file not found: {path_obj}")
    
    return path_obj


def validate_path_is_file(path: Union[str, Path], file_type: str = "file") -> Path:
    """
    Validate that a path exists and is a file (not a directory).
    
    Handles None, empty strings, and other falsy values before checking file existence.
    
    Args:
        path: Path to validate. Can be string or Path object.
        file_type: Type of file for error messages (e.g., "CSV", "JSON").
                  Default: "file".
        
    Returns:
        Path object if validation passes.
        
    Raises:
        ValueError: If path is None, empty, or is not a file.
        FileNotFoundError: If file doesn't exist.
    """
    # Check for falsy values (None, empty string, empty Path, etc.)
    if not path:
        raise ValueError(f"{file_type} path cannot be empty")
    
    path_obj = validate_file_exists(path, file_type)
    
    if not path_obj.is_file():
        raise ValueError(f"Path is not a file: {path_obj}")
    
    return path_obj


def load_json_file(
    json_path: Union[str, Path],
    expected_type: Optional[type] = None,
    file_type: str = "JSON"
) -> Union[Dict[str, Any], List[Any]]:
    """
    Load data from a JSON file with validation and error handling.
    
    Args:
        json_path: Path to JSON file. Can be string or Path object.
        expected_type: Optional expected type (dict or list). If provided, validates the loaded data.
        file_type: Type of file for error messages (default: "JSON").
        
    Returns:
        Loaded JSON data (dict or list).
        
    Raises:
        ValueError: If json_path is invalid or data doesn't match expected_type.
        FileNotFoundError: If JSON file doesn't exist.
        json.JSONDecodeError: If JSON is invalid or malformed.
        PermissionError: If file cannot be read due to permissions.
    """
    # Validate path
    json_path_obj = validate_path_is_file(json_path, file_type)
    
    # Load JSON
    try:
        with open(json_path_obj, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {file_type} file {json_path_obj}: {e}")
        raise
    except PermissionError as e:
        logger.error(f"Permission denied reading {file_type} file {json_path_obj}: {e}")
        raise
    except OSError as e:
        # Catch file system errors (FileNotFoundError, IOError, etc.)
        logger.error(f"File system error loading {file_type} from {json_path_obj}: {e}")
        raise
    except Exception as e:
        # Catch any other unexpected errors (should rarely happen)
        logger.error(f"Unexpected error loading {file_type} from {json_path_obj}: {e}", exc_info=True)
        raise
    
    # Validate type if expected
    if expected_type is not None:
        if not isinstance(data, expected_type):
            raise ValueError(
                f"{file_type} file must contain {expected_type.__name__}, got {type(data)}"
            )
    
    logger.debug(f"Loaded {file_type} from {json_path_obj}")
    return data


def save_json_file(
    data: Any,
    json_path: Union[str, Path],
    indent: int = 2,
    file_type: str = "JSON"
) -> None:
    """
    Save data to a JSON file with error handling.
    
    Creates parent directories if they don't exist.
    
    Args:
        data: Data to save (must be JSON-serializable).
        json_path: Path to JSON file. Can be string or Path object.
        indent: JSON indentation level (default: 2).
        file_type: Type of file for error messages (default: "JSON").
        
    Raises:
        ValueError: If json_path is invalid.
        PermissionError: If file cannot be written due to permissions.
        TypeError: If data is not JSON-serializable.
    """
    if json_path is None:
        raise ValueError(f"{file_type} path cannot be None")
    
    json_path_obj = Path(json_path)
    
    # Ensure parent directory exists
    ensure_dir(json_path_obj.parent)
    
    # Save JSON
    try:
        with open(json_path_obj, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent)
    except PermissionError as e:
        logger.error(f"Permission denied writing {file_type} file {json_path_obj}: {e}")
        raise
    except TypeError as e:
        logger.error(f"Data is not JSON-serializable: {e}")
        raise
    except OSError as e:
        # Catch file system errors (IOError, disk full, etc.)
        logger.error(f"File system error saving {file_type} to {json_path_obj}: {e}")
        raise
    except Exception as e:
        # Catch any other unexpected errors (should rarely happen)
        logger.error(f"Unexpected error saving {file_type} to {json_path_obj}: {e}", exc_info=True)
        raise
    
    logger.debug(f"Saved {file_type} to {json_path_obj}")


def append_to_json_list(
    item: Any,
    json_path: Union[str, Path],
    indent: int = 2,
    file_type: str = "JSON"
) -> None:
    """
    Append an item to a JSON list file (incremental save).
    
    Loads existing list from file (or creates empty list), appends item,
    and saves back. This is useful for grid search results where we want
    to save incrementally to avoid losing progress on timeout.
    
    Args:
        item: Item to append to the list (must be JSON-serializable).
        json_path: Path to JSON file. Can be string or Path object.
        indent: JSON indentation level (default: 2).
        file_type: Type of file for error messages (default: "JSON").
        
    Raises:
        ValueError: If json_path is invalid or existing file doesn't contain a list.
        PermissionError: If file cannot be read/written due to permissions.
        TypeError: If item is not JSON-serializable.
    """
    if json_path is None:
        raise ValueError(f"{file_type} path cannot be None")
    
    json_path_obj = Path(json_path)
    
    # Ensure parent directory exists
    ensure_dir(json_path_obj.parent)
    
    # Load existing list or create new one
    if json_path_obj.exists():
        try:
            with open(json_path_obj, 'r', encoding='utf-8') as f:
                existing_list = json.load(f)
            if not isinstance(existing_list, list):
                raise ValueError(
                    f"{file_type} file {json_path_obj} exists but doesn't contain a list, got {type(existing_list)}"
                )
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {file_type} file {json_path_obj}: {e}")
            raise
        except PermissionError as e:
            logger.error(f"Permission denied reading {file_type} file {json_path_obj}: {e}")
            raise
        except OSError as e:
            logger.error(f"File system error reading {file_type} file {json_path_obj}: {e}")
            raise
    else:
        existing_list = []
    
    # Append item
    existing_list.append(item)
    
    # Save back
    try:
        with open(json_path_obj, 'w', encoding='utf-8') as f:
            json.dump(existing_list, f, indent=indent)
    except PermissionError as e:
        logger.error(f"Permission denied writing {file_type} file {json_path_obj}: {e}")
        raise
    except TypeError as e:
        logger.error(f"Item is not JSON-serializable: {e}")
        raise
    except OSError as e:
        logger.error(f"File system error saving {file_type} to {json_path_obj}: {e}")
        raise
    except Exception as e:
        # Catch any other unexpected errors (should rarely happen)
        logger.error(f"Unexpected error saving {file_type} to {json_path_obj}: {e}", exc_info=True)
        raise
    
    logger.debug(f"Appended item to {file_type} list at {json_path_obj}")


def validate_path_list(paths: List[Union[str, Path]], name: str = "paths") -> None:
    """
    Validate that a list of paths is valid.
    
    Args:
        paths: List of paths to validate.
        name: Name of the parameter for error messages (default: "paths").
        
    Raises:
        ValueError: If paths is not a list.
        TypeError: If any path in the list is not a string or Path.
    """
    if not isinstance(paths, list):
        raise ValueError(f"{name} must be a list, got {type(paths)}")
    
    for i, path in enumerate(paths):
        if not isinstance(path, (str, Path)):
            raise TypeError(
                f"{name}[{i}] must be string or Path, got {type(path)}"
            )

