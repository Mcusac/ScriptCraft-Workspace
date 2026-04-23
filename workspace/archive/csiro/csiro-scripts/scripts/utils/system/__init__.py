# System utilities package
# Re-export commonly used functions and constants for convenience

from utils.system.constants import BYTES_PER_KB, BYTES_PER_MB, BYTES_PER_GB

# Re-export from io module
from utils.system.io import (
    validate_file_exists,
    validate_path_is_file,
    validate_path_list,
    load_json_file,
    save_json_file,
    append_to_json_list,
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

# Re-export from environment module
from utils.system.environment import (
    setup_environment,
    get_device,
    setup_multi_gpu,
    get_device_info,
    set_seed,
    validate_reproducibility_settings,
    get_kaggle_input_weights_dir,
    configure_huggingface_cache,
    setup_weight_cache,
)

# Re-export from infrastructure module
from utils.system.infrastructure import (
    setup_logging,
    run_command_with_streaming,
    ProgressTracker,
)

# Re-export from memory module
from utils.system.memory import (
    clear_gpu_memory,
    cleanup_dataframe_and_memory,
    recover_from_oom,
)

__all__ = [
    # Constants
    'BYTES_PER_KB',
    'BYTES_PER_MB',
    'BYTES_PER_GB',
    # IO - File operations
    'validate_file_exists',
    'validate_path_is_file',
    'validate_path_list',
    'load_json_file',
    'save_json_file',
    'append_to_json_list',
    # IO - Path operations
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
    # IO - Validation functions
    'validate_non_negative',
    'validate_positive',
    'validate_range',
    'validate_optional_non_negative',
    'validate_tuple_length',
    'validate_min_max_tuple',
    'validate_numpy_array',
    'validate_matching_arrays',
    'validate_array_not_empty',
    # Environment
    'setup_environment',
    'get_device',
    'setup_multi_gpu',
    'get_device_info',
    'set_seed',
    'validate_reproducibility_settings',
    'get_kaggle_input_weights_dir',
    'configure_huggingface_cache',
    'setup_weight_cache',
    # Infrastructure
    'setup_logging',
    'run_command_with_streaming',
    'ProgressTracker',
    # Memory
    'clear_gpu_memory',
    'cleanup_dataframe_and_memory',
    'recover_from_oom'
]
