# path_utils.py
# Utilities for path handling and resolution
#
# Note: Imports from config.path_constants are done lazily (inside functions)
# to avoid circular import issues. This allows path_utils to be imported
# without triggering the config → modeling → utils circular dependency.

import os
from pathlib import Path
from typing import Union


# ============================================================================
# Directory Operations
# ============================================================================

def ensure_dir(path: Union[str, Path], parents: bool = True) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Directory path. Can be string or Path object.
              Must be a valid path (not None or empty).
        parents: If True, create parent directories as needed (default: True).
        
    Returns:
        Path object of the directory (guaranteed to exist after call).
        
    Raises:
        ValueError: If path is None or empty.
        PermissionError: If directory cannot be created due to permissions.
        OSError: If directory creation fails for other reasons.
    """
    if path is None:
        raise ValueError("path cannot be None")
    
    if isinstance(path, str) and not path.strip():
        raise ValueError("path cannot be empty string")
    
    path_obj = Path(path)
    
    try:
        path_obj.mkdir(parents=parents, exist_ok=True)
    except PermissionError as e:
        raise PermissionError(f"Permission denied creating directory {path_obj}: {e}")
    except OSError as e:
        raise OSError(f"Failed to create directory {path_obj}: {e}")
    
    return path_obj


def ensure_config_dirs(paths_config) -> None:
    """
    Ensure all output directories from a paths config exist.
    
    Creates output_dir, model_dir, and log_dir if they don't exist.
    Parent directories are created as needed.
    
    Args:
        paths_config: Configuration object with output_dir, model_dir, and log_dir attributes.
                     Can be any object with these attributes (e.g., Config.paths).
        
    Raises:
        AttributeError: If paths_config is None or missing required attributes.
        PermissionError: If directories cannot be created due to permissions.
        OSError: If directory creation fails.
    """
    if paths_config is None:
        raise AttributeError("paths_config is None - cannot ensure directories")
    
    if not hasattr(paths_config, 'output_dir'):
        raise AttributeError("paths_config missing 'output_dir' attribute")
    
    if not hasattr(paths_config, 'model_dir'):
        raise AttributeError("paths_config missing 'model_dir' attribute")
    
    if not hasattr(paths_config, 'log_dir'):
        raise AttributeError("paths_config missing 'log_dir' attribute")
    
    ensure_dir(paths_config.output_dir)
    ensure_dir(paths_config.model_dir)
    ensure_dir(paths_config.log_dir)


# ============================================================================
# Path Resolution (Kaggle vs Local)
# ============================================================================

def is_kaggle_environment() -> bool:
    """
    Check if running in Kaggle environment.
    
    Returns:
        True if running on Kaggle, False otherwise
    """
    return os.environ.get('KAGGLE_KERNEL_RUN_TYPE', '') != ''


def get_kaggle_path(kaggle_path: str, local_path: str) -> str:
    """
    Get the appropriate path based on environment.
    
    Args:
        kaggle_path: Path to use when running on Kaggle
        local_path: Path to use when running locally
        
    Returns:
        Appropriate path string based on environment
    """
    if is_kaggle_environment():
        return kaggle_path
    return local_path


def get_scripts_path() -> str:
    """
    Get the path to the scripts directory.
    
    Returns:
        Path to scripts directory (Kaggle or local)
    """
    from config.path_constants import KAGGLE_INPUT_SCRIPTS, LOCAL_SCRIPTS
    return get_kaggle_path(
        str(KAGGLE_INPUT_SCRIPTS),
        str(LOCAL_SCRIPTS)
    )


def get_data_root_path() -> str:
    """
    Get the path to the data root directory.
    
    Returns:
        Path to data root (Kaggle or local)
    """
    from config.path_constants import KAGGLE_INPUT_BIOMASS, LOCAL_BIOMASS
    return get_kaggle_path(
        str(KAGGLE_INPUT_BIOMASS),
        str(LOCAL_BIOMASS)
    )


def get_output_path(relative_path: str) -> str:
    """
    Get the path to an output file/directory.
    
    Args:
        relative_path: Relative path from output root (e.g., 'grid_search_output.log')
        
    Returns:
        Full path to output location (Kaggle or local)
    """
    from config.path_constants import KAGGLE_WORKING_OUTPUTS, LOCAL_OUTPUTS
    if is_kaggle_environment():
        return str(KAGGLE_WORKING_OUTPUTS / relative_path)
    return str(LOCAL_OUTPUTS / relative_path)


def get_best_model_path() -> str:
    """
    Get the path to the best_model export directory.
    
    Returns:
        Full path to best_model directory (Kaggle or local)
        - Kaggle: /kaggle/working/best_model
        - Local: ../output/best_model
    """
    from config.path_constants import KAGGLE_WORKING_BEST_MODEL, LOCAL_OUTPUTS
    if is_kaggle_environment():
        return str(KAGGLE_WORKING_BEST_MODEL)
    return str(LOCAL_OUTPUTS / 'best_model')


def get_run_py_path() -> str:
    """
    Get the path to run.py script.
    
    Returns:
        Path to run.py (Kaggle or local)
    """
    from config.path_constants import KAGGLE_INPUT_SCRIPTS, LOCAL_SCRIPTS
    return get_kaggle_path(
        str(KAGGLE_INPUT_SCRIPTS / 'run.py'),
        str(LOCAL_SCRIPTS / 'run.py')
    )


def get_submission_path() -> Path:
    """
    Get the path to the submission file in Kaggle working directory.
    
    Returns:
        Path to submission.csv in Kaggle working directory
    """
    from config.path_constants import KAGGLE_WORKING_SUBMISSION
    return KAGGLE_WORKING_SUBMISSION


def apply_kaggle_paths_to_config(config) -> None:
    """
    Apply Kaggle-specific paths to config if running on Kaggle.
    
    Args:
        config: Config object to update. Must not be None and must have paths attribute.
        
    Raises:
        ValueError: If config is None or missing paths attribute.
    """
    if config is None:
        raise ValueError("config cannot be None")
    
    if not hasattr(config, 'paths') or config.paths is None:
        raise ValueError("config.paths cannot be None")
    
    if is_kaggle_environment():
        from config.path_constants import KAGGLE_WORKING_OUTPUTS, KAGGLE_WORKING_MODELS, KAGGLE_WORKING_LOGS
        config.paths.output_dir = str(KAGGLE_WORKING_OUTPUTS)
        config.paths.model_dir = str(KAGGLE_WORKING_MODELS)
        config.paths.log_dir = str(KAGGLE_WORKING_LOGS)

