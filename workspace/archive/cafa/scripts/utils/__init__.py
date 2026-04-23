"""
Utilities for CAFA 6 protein function prediction.
Contains model persistence and other utility functions.
"""

from .model_io import (
    save_model,
    load_model,
    list_saved_models
)

from .gpu_utils import (
    get_gpu_info,
    check_gpu_available,
    get_device,
    get_gpu_count,
    get_gpu_memory_gb,
    cleanup_gpu_memory
)

from .model_prediction import (
    predict_with_model
)

from .dataloader_utils import (
    create_training_dataloader
)

from .utils_common import (
    is_kaggle_environment,
    device_to_string,
    resolve_path,
    calculate_memory_size_mb,
    test_multiprocessing_available
)

from .cli_utils import (
    parse_model_spec,
    parse_model_specs_from_args,
    validate_pipeline_args,
    validate_submissions_arg,
    validate_ontology_codes,
    parse_comma_separated_string,
    parse_comma_separated_floats,
    parse_weights,
    normalize_weights,
    validate_and_adjust_weights,
    build_ensemble_kwargs,
    get_model_config_safe,
    parse_feature_override,
    parse_ontology_arg,
    parse_ensemble_models,
    parse_submission_files,
    create_model_specs_from_name
)

from .ontology_utils import (
    iterate_ontologies_with_check,
    get_ontology_name_safe,
    filter_ontologies_with_data,
    get_ontology_codes_and_names
)

__all__ = [
    # Model I/O
    'save_model',
    'load_model',
    'list_saved_models',
    
    # GPU utilities
    'get_gpu_info',
    'check_gpu_available',
    'get_device',
    'get_gpu_count',
    'get_gpu_memory_gb',
    'cleanup_gpu_memory',
    
    # Model prediction
    'predict_with_model',
    
    # DataLoader utilities
    'create_training_dataloader',
    
    # Common utilities
    'is_kaggle_environment',
    'device_to_string',
    'resolve_path',
    'calculate_memory_size_mb',
    'test_multiprocessing_available',
    
    # CLI utilities
    'parse_model_spec',
    'parse_model_specs_from_args',
    'validate_pipeline_args',
    'validate_submissions_arg',
    'validate_ontology_codes',
    'parse_comma_separated_string',
    'parse_comma_separated_floats',
    'parse_weights',
    'normalize_weights',
    'validate_and_adjust_weights',
    'build_ensemble_kwargs',
    'get_model_config_safe',
    'parse_feature_override',
    'parse_ontology_arg',
    'parse_ensemble_models',
    'parse_submission_files',
    'create_model_specs_from_name',
    
    # Ontology utilities
    'iterate_ontologies_with_check',
    'get_ontology_name_safe',
    'filter_ontologies_with_data',
    'get_ontology_codes_and_names'
]
