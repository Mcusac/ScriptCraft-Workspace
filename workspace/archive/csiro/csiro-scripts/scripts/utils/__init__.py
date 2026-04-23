# utils package
# Utility functions for common operations
#
# Package Organization Rationale:
# This package serves as a support/infrastructure layer for the entire codebase. It is
# intentionally organized into domain-specific subpackages to maintain clear boundaries
# while providing reusable utilities across different domains.
#
# Why keep utils/ as a separate package?
# - Utilities are cross-cutting concerns used by multiple domains (config, data, modeling, pipelines)
# - Keeping them separate avoids circular dependencies that would occur if utilities were
#   embedded in domain packages (e.g., data/utils importing from modeling/)
# - Clear separation between "what" (domain logic) and "how" (utility implementations)
# - Easier to find and maintain shared functionality
#
# Organization Strategy:
# This package is organized into focused subpackages following single responsibility principle:
#
# - config: Configuration utilities (validation, updating from CLI args)
#   - config_validator: Validate config structure and CLI arguments
#   - config_updater: Apply config updates (preprocessing, augmentation, overrides)
#   - config_utils: Orchestrator for updating config from CLI arguments (convenience function)
#
# - data: Data-related utilities (preprocessing, dataset caching, image conversion, file loading)
#   - preprocessing_utils: Parse and validate preprocessing/augmentation lists
#   - dataset_cache_utils: Dataset variant caching and grid generation
#   - image_utils: PIL/numpy image conversion utilities
#   - loading_utils: Batch processing with progress tracking
#
# - modeling: Model-related utilities moved to modeling.utils
#
# - system: System-level utilities (intentionally broad - foundational utilities)
#   This subpackage contains low-level system operations that are foundational to the
#   entire codebase. It is intentionally broad because these utilities are used across
#   all domains and don't fit neatly into a single domain category.
#   - logging_utils: Logging configuration
#   - seed_utils: Random seed management
#   - device_utils: GPU/device detection and management
#   - path_utils: Path resolution (Kaggle vs local) and directory operations
#   - environment_utils: Environment setup (convenience function combining GPU check + weight download)
#   - weight_cache_utils: Pretrained weight cache management for offline Kaggle
#   - command_utils: Subprocess command execution with streaming
#   - file_utils: File operations (JSON load/save, path validation)
#   - validation_utils: Generic validation functions (numeric, array, tuple validation)
#   - notebook utilities moved to utils.notebook
#   - error_handling.py: Error handling utilities
#   - memory/: Memory management utilities (cleanup, recovery)
#
# - training: Training-related utilities moved to modeling.training.utils
#
# Import Guidelines:
# - External code should use package-level imports: `from utils.config import ...`
# - Internal utils code uses relative imports: `from ..system.io.paths import ...`
# - All public APIs are exported via __init__.py files

# Training utilities moved to modeling.training.utils
# Training utilities moved to modeling.training.utils
# Modeling utilities moved to modeling.utils

from utils.system import (
    setup_logging,
    ensure_dir,
    set_seed,
    validate_non_negative,
    validate_positive,
    validate_range,
    validate_optional_non_negative,
    validate_tuple_length,
    validate_min_max_tuple,
    validate_numpy_array,
    validate_matching_arrays,
    validate_array_not_empty,
    get_device,
    setup_multi_gpu,
    get_device_info,
    clear_gpu_memory,
    BYTES_PER_KB,
    BYTES_PER_MB,
    BYTES_PER_GB,
    run_command_with_streaming,
    is_kaggle_environment,
    get_kaggle_path,
    get_scripts_path,
    get_data_root_path,
    get_output_path,
    get_run_py_path,
    apply_kaggle_paths_to_config,
    load_json_file,
    save_json_file,
    append_to_json_list,
)

from utils.data import (
    parse_preprocessing_list,
    parse_augmentation_list,
    validate_preprocessing_names,
    validate_augmentation_names,
    DEFAULT_PREPROCESSING_LIST,
    AVAILABLE_PREPROCESSING,
    AVAILABLE_AUGMENTATION,
)

from utils.config import (
    apply_preprocessing_to_config,
    apply_augmentation_to_config,
    update_config_from_args,
    validate_pipeline_config,
)

from utils.system.environment import (
    check_internet_connection,
    find_available_weights_cache,
    configure_huggingface_cache,
    setup_weight_cache,
    prepare_weights_download_dir,
    ensure_weight_cache_ready,
    setup_environment,
)

__all__ = [
    'setup_logging',
    'ensure_dir',
    'set_seed',
    'validate_non_negative',
    'validate_positive',
    'validate_range',
    'validate_optional_non_negative',
    'validate_tuple_length',
    'validate_min_max_tuple',
    'validate_numpy_array',
    'validate_matching_arrays',
    'validate_array_not_empty',
    'get_device',
    'setup_multi_gpu',
    'get_device_info',
    'clear_gpu_memory',
    'parse_preprocessing_list',
    'parse_augmentation_list',
    'validate_preprocessing_names',
    'validate_augmentation_names',
    'DEFAULT_PREPROCESSING_LIST',
    'AVAILABLE_PREPROCESSING',
    'AVAILABLE_AUGMENTATION',
    'apply_preprocessing_to_config',
    'apply_augmentation_to_config',
    'update_config_from_args',
    'validate_pipeline_config',
    'check_internet_connection',
    'find_available_weights_cache',
    'configure_huggingface_cache',
    'setup_weight_cache',
    'prepare_weights_download_dir',
    'ensure_weight_cache_ready',
    'run_command_with_streaming',
    'is_kaggle_environment',
    'get_kaggle_path',
    'get_scripts_path',
    'get_data_root_path',
    'get_output_path',
    'get_run_py_path',
    'apply_kaggle_paths_to_config',
    'setup_environment',
    'load_json_file',
    'save_json_file',
    'append_to_json_list',
    # System constants
    'BYTES_PER_KB',
    'BYTES_PER_MB',
    'BYTES_PER_GB',
]
