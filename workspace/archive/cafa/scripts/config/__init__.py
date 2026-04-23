"""
Configuration package for CAFA 6 protein function prediction.
Hierarchical config system for centralized configuration management.
"""

# Import all configurations from submodules
from .paths import (
    PROJECT_ROOT,
    DATA_INPUT_DIR, 
    DATA_OUTPUT_DIR,
    MODELS_DIR,
    MODELS_INPUT_DIR,
    KAGGLE_ENV
)

from .models import (
    CURRENT_MODEL,
    MODEL_CONFIGS,
    get_model_config,
    get_model_trainer,
    get_model_mode,
    get_ontology_hyperparams,
    get_model_config_by_type_version
)

from .grid_search import (
    GRID_SEARCH_CONFIGS,
    get_grid_search_config
)

from .features import (
    FEATURE_EXTRACTION_METHODS,
    EMBEDDING_CONFIGS,
    INDIVIDUAL_FEATURES,
    BATCH_SIZE_CONFIG,
    HANDCRAFTED_FEATURE_KEY,
    get_feature_extraction_config,
    get_embedding_config,
    get_batch_size,
    get_optimized_batch_size,
    get_gpu_optimized_batch_size,
    parse_feature_spec,
    validate_feature_availability,
    get_feature_dimensions,
    parse_model_feature_config,
    get_embedding_feature_types,
    is_valid_embedding_type
)

from .pipelines import (
    PIPELINE_CONFIGS,
    get_pipeline_config
)

from .prediction import (
    PREDICTION_SETTINGS,
    MAX_PREDICTIONS_PER_PROTEIN,
    SUBMISSION_SORT_CHUNK_SIZE,
    VALIDATION_SAMPLE_SIZE,
    DEFAULT_THRESHOLD,
    PREDICTION_PROGRESS_INTERVALS,
    ENSEMBLE_GC_COLLECT_INTERVAL,
    BINARY_PREDICTION_THRESHOLD,
    METRICS_EPSILON,
    get_extra_output_name
)

from .ensemble import (
    ENSEMBLE_CONFIG_VERSION,
    DEFAULT_ENSEMBLE_METHOD,
    MERGE_METHOD,
    ENSEMBLE_DEFAULTS,
    ENSEMBLE_PARAM_RANGES,
    get_ensemble_default,
    validate_ensemble_param,
    get_available_ensemble_methods
)

from .ontologies import (
    ONTOLOGY_MAP,
    ONTOLOGY_CODES,
    ONTOLOGY_NAMES,
    get_ontology_name,
    get_ontology_code,
    get_all_ontologies
)

from .training import (
    PROGRESS_INDICATOR_INTERVAL,
    DEFAULT_RANDOM_SEED,
    FEATURE_EXTRACTION_MAX_WORKERS,
    EPSILON_SMALL,
    EPSILON_TINY,
    VALIDATION_SPLIT_SIZE,
    LARGE_LABEL_SPACE_THRESHOLD,
    MEDIUM_LABEL_SPACE_THRESHOLD,
    DEFAULT_N_JOBS,
    DEFAULT_VALIDATION_SPLIT,
    LARGE_ONTOLOGY_LABEL_THRESHOLD,
    REDUCED_BATCH_SIZE_LARGE_ONTOLOGY
)

# Re-export all configuration symbols
__all__ = [
    # Paths
    'PROJECT_ROOT',
    'DATA_INPUT_DIR',
    'DATA_OUTPUT_DIR', 
    'MODELS_DIR',
    'MODELS_INPUT_DIR',
    'KAGGLE_ENV',
    
    # Models
    'CURRENT_MODEL',
    'MODEL_CONFIGS',
    'get_model_config',
    'get_model_trainer',
    'get_model_mode',
    'get_ontology_hyperparams',
    'get_model_config_by_type_version',
    
    # Grid Search
    'GRID_SEARCH_CONFIGS',
    'get_grid_search_config',
    
    # Features
    'FEATURE_EXTRACTION_METHODS',
    'EMBEDDING_CONFIGS',
    'INDIVIDUAL_FEATURES',
    'BATCH_SIZE_CONFIG',
    'HANDCRAFTED_FEATURE_KEY',
    'get_feature_extraction_config',
    'get_embedding_config',
    'get_batch_size',
    'get_optimized_batch_size',
    'get_gpu_optimized_batch_size',
    'parse_feature_spec',
    'validate_feature_availability',
    'get_feature_dimensions',
    'parse_model_feature_config',
    'get_embedding_feature_types',
    'is_valid_embedding_type',
    
    # Pipelines
    'PIPELINE_CONFIGS',
    'get_pipeline_config',
    
    # Prediction
    'PREDICTION_SETTINGS',
    'MAX_PREDICTIONS_PER_PROTEIN',
    'SUBMISSION_SORT_CHUNK_SIZE',
    'VALIDATION_SAMPLE_SIZE',
    'DEFAULT_THRESHOLD',
    'PREDICTION_PROGRESS_INTERVALS',
    'ENSEMBLE_GC_COLLECT_INTERVAL',
    'BINARY_PREDICTION_THRESHOLD',
    'METRICS_EPSILON',
    'get_extra_output_name',
    
    # Ontologies
    'ONTOLOGY_MAP',
    'ONTOLOGY_CODES',
    'ONTOLOGY_NAMES',
    'get_ontology_name',
    'get_ontology_code',
    'get_all_ontologies',
    
    # Training
    'PROGRESS_INDICATOR_INTERVAL',
    'DEFAULT_RANDOM_SEED',
    'FEATURE_EXTRACTION_MAX_WORKERS',
    'EPSILON_SMALL',
    'EPSILON_TINY',
    'VALIDATION_SPLIT_SIZE',
    'LARGE_LABEL_SPACE_THRESHOLD',
    'MEDIUM_LABEL_SPACE_THRESHOLD',
    'DEFAULT_N_JOBS',
    'DEFAULT_VALIDATION_SPLIT',
    'LARGE_ONTOLOGY_LABEL_THRESHOLD',
    'REDUCED_BATCH_SIZE_LARGE_ONTOLOGY',
    'DATALOADER_PRELOAD_THRESHOLD_MB',
    'DATALOADER_PRELOAD_MAX_MB',
    'DATALOADER_GPU_MEMORY_FRACTION',
    'DATALOADER_MAX_WORKERS',
    'DATALOADER_PREFETCH_FACTOR',
    'DATALOADER_MULTIPROCESSING_TIMEOUT',
    'DATALOADER_TEST_WORKERS',
    'DATALOADER_LARGE_DATASET_THRESHOLD_MB',
    'FLOAT32_BYTES',
    'MB_TO_BYTES',
    'GB_TO_BYTES',
    'MODEL_FILE_EXTENSION_PKL',
    'MODEL_FILE_EXTENSION_PTH',
    'VALID_ONTOLOGY_CODES',
    'GPU_CHECK_TIMEOUT',
    'MEMMAP_THRESHOLD_MB',
    
    # Ensemble
    'ENSEMBLE_CONFIG_VERSION',
    'DEFAULT_ENSEMBLE_METHOD',
    'MERGE_METHOD',
    'ENSEMBLE_DEFAULTS',
    'ENSEMBLE_PARAM_RANGES',
    'get_ensemble_default',
    'validate_ensemble_param',
    'get_available_ensemble_methods'
]
