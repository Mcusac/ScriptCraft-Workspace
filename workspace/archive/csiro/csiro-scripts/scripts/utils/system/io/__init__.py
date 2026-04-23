# io package
# File and path operations utilities
#
# This package contains utilities for file and path operations:
# - files: JSON file operations and validation
# - paths: Path resolution (Kaggle vs local) and directory operations
# - validation: Generic validation functions

from utils.system.io.files import (
    validate_file_exists,
    validate_path_is_file,
    validate_path_list,
    load_json_file,
    save_json_file,
    append_to_json_list,
)
from utils.system.io.paths import (
    ensure_dir,
    ensure_config_dirs,
    is_kaggle_environment,
    get_kaggle_path,
    get_scripts_path,
    get_data_root_path,
    get_output_path,
    get_best_model_path,
    get_run_py_path,
    get_submission_path,
    apply_kaggle_paths_to_config,
)
from utils.system.io.validation import (
    validate_non_negative,
    validate_positive,
    validate_range,
    validate_optional_non_negative,
    validate_tuple_length,
    validate_min_max_tuple,
    validate_numpy_array,
    validate_matching_arrays,
    validate_array_not_empty,
)

__all__ = [
    # Files
    'validate_file_exists',
    'validate_path_is_file',
    'validate_path_list',
    'load_json_file',
    'save_json_file',
    'append_to_json_list',
    # Paths
    'ensure_dir',
    'ensure_config_dirs',
    'is_kaggle_environment',
    'get_kaggle_path',
    'get_scripts_path',
    'get_data_root_path',
    'get_output_path',
    'get_best_model_path',
    'get_run_py_path',
    'get_submission_path',
    'apply_kaggle_paths_to_config',
    # Validation
    'validate_non_negative',
    'validate_positive',
    'validate_range',
    'validate_optional_non_negative',
    'validate_tuple_length',
    'validate_min_max_tuple',
    'validate_numpy_array',
    'validate_matching_arrays',
    'validate_array_not_empty'
]

