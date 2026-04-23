# environment package
# Environment setup utilities
#
# This package contains utilities for environment setup and configuration:
# - setup: Environment setup and GPU detection
# - device: Device detection and multi-GPU setup
# - seed: Random seed setting for reproducibility
# - weights: Weight cache management for offline Kaggle submissions

from utils.system.environment.setup import (
    suppress_kaggle_install_script_error,
    get_gpu_info,
    setup_environment,
)
from utils.system.environment.device import (
    get_device,
    setup_multi_gpu,
    get_device_info,
)
from utils.system.environment.seed import (
    set_seed,
    validate_reproducibility_settings,
)
from utils.system.environment.weights import (
    check_internet_connection,
    get_kaggle_input_weights_dir,
    find_available_weights_cache,
    configure_huggingface_cache,
    setup_weight_cache,
    prepare_weights_download_dir,
    ensure_weight_cache_ready,
)

__all__ = [
    # Setup
    'suppress_kaggle_install_script_error',
    'get_gpu_info',
    'setup_environment',
    # Device
    'get_device',
    'setup_multi_gpu',
    'get_device_info',
    # Seed
    'set_seed',
    'validate_reproducibility_settings',
    # Weights
    'check_internet_connection',
    'get_kaggle_input_weights_dir',
    'find_available_weights_cache',
    'configure_huggingface_cache',
    'setup_weight_cache',
    'prepare_weights_download_dir',
    'ensure_weight_cache_ready'
]

