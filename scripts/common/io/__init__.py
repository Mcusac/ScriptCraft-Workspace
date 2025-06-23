"""
I/O package for the project.

This package provides input/output operations organized into:
- data_loading: Data loading operations
- directory_ops: Directory management
- file_ops: Basic file operations
- paths: Path constants and configuration
"""

from .data_loading import (
    load_data,
    load_datasets,
    load_dataset_columns,
    load_dictionary_columns,
    load_comparison_datasets,
    load_json,
    load_yaml
)
from .directory_ops import (
    ensure_output_dir,
    get_input_dir,
    get_output_dir,
    get_qc_output_dir,
    get_output_path,
    clean_directory,
    list_files
)
from .file_ops import (
    find_first_data_file,
    find_latest_file,
    find_matching_file,
    resolve_file,
    resolve_path,
    copy_file,
    move_file
)
from .paths import (
    DOMAINS,
    FOLDER_STRUCTURE,
    DEFAULT_ENCODING,
    FALLBACK_ENCODING,
    COLUMN_ALIASES,
    STANDARD_KEYS,
    FILE_PATTERNS,
    OutlierMethod,
    MISSING_VALUE_CODES,
    MISSING_VALUE_STRINGS,
    get_project_root,
    get_domain_paths,
    get_output_path,
    get_config,
    load_config
)

__all__ = [
    # Data Loading
    'load_data',
    'load_datasets',
    'load_dataset_columns',
    'load_dictionary_columns',
    'load_comparison_datasets',
    'load_json',
    'load_yaml',
    
    # Directory Operations
    'ensure_output_dir',
    'get_input_dir',
    'get_output_dir',
    'get_qc_output_dir',
    'get_output_path',
    'clean_directory',
    'list_files',
    
    # File Operations
    'find_first_data_file',
    'find_latest_file',
    'find_matching_file',
    'resolve_file',
    'resolve_path',
    'copy_file',
    'move_file',
    
    # Paths and Constants
    'DOMAINS',
    'FOLDER_STRUCTURE',
    'DEFAULT_ENCODING',
    'FALLBACK_ENCODING',
    'COLUMN_ALIASES',
    'STANDARD_KEYS',
    'FILE_PATTERNS',
    'OutlierMethod',
    'MISSING_VALUE_CODES',
    'MISSING_VALUE_STRINGS',
    'get_project_root',
    'get_domain_paths',
    'get_output_path',
    'get_config',
    'load_config'
] 