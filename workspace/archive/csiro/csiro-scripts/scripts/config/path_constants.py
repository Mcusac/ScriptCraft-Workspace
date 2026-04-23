# path_constants.py
# Centralized path constants for Kaggle and local environments
#
# All hardcoded paths should reference these constants instead of being
# directly embedded in code. This ensures consistency and makes it easier
# to update paths across the codebase.
#
# Contest-specific paths now use the contest abstraction for flexibility.

from pathlib import Path
import warnings

# ============================================================================
# Kaggle Path Constants (Non-Contest-Specific)
# ============================================================================

# Kaggle base directories
KAGGLE_WORKING = Path('/kaggle/working')
KAGGLE_INPUT = Path('/kaggle/input')

# Kaggle working subdirectories
KAGGLE_WORKING_OUTPUTS = KAGGLE_WORKING / 'output'
KAGGLE_WORKING_MODELS = KAGGLE_WORKING / 'models'
KAGGLE_WORKING_LOGS = KAGGLE_WORKING / 'logs'
KAGGLE_WORKING_DATASETS = KAGGLE_WORKING / 'datasets'
KAGGLE_WORKING_BEST_MODEL = KAGGLE_WORKING / 'best_model'
KAGGLE_WORKING_SUBMISSION = KAGGLE_WORKING / 'submission.csv'
KAGGLE_WORKING_WEIGHTS = KAGGLE_WORKING / 'timm_weights'

# Kaggle input paths (non-contest-specific)
KAGGLE_INPUT_WEIGHTS = KAGGLE_INPUT / 'timm-weights'

# ============================================================================
# Contest-Specific Path Constants (Using Contest Abstraction)
# ============================================================================

# Import contest paths abstraction
try:
    from contest.registry import get_contest_paths
    _contest_paths = get_contest_paths()
except (ImportError, ValueError) as e:
    # Fallback to direct CSIRO import if registry not available
    warnings.warn(
        f"Could not load contest paths from registry: {e}. "
        f"Falling back to direct CSIRO import.",
        UserWarning
    )
    from contest.csiro.paths import get_csiro_paths
    _contest_paths = get_csiro_paths()

# CSIRO-SPECIFIC: Contest-specific dataset paths
# These use contest abstraction and maintain same names as part of the API
KAGGLE_INPUT_SCRIPTS = _contest_paths.get_kaggle_input_scripts_path(KAGGLE_INPUT) / 'scripts'
KAGGLE_INPUT_BIOMASS = _contest_paths.get_kaggle_input_path(KAGGLE_INPUT)
KAGGLE_INPUT_CSIRO_MODELS = _contest_paths.get_kaggle_input_models_path(KAGGLE_INPUT) / 'pytorch' / 'default'

# ============================================================================
# Local Path Constants
# ============================================================================

# Local base directories (relative to scripts directory)
LOCAL_OUTPUTS = Path('../output')
LOCAL_MODELS = Path('../models')
LOCAL_LOGS = Path('../logs')
LOCAL_DATASETS = Path('../output/datasets')
# CSIRO-SPECIFIC: Contest-specific local paths
LOCAL_BIOMASS = _contest_paths.local_data_root
# LOCAL_SCRIPTS is constructed from contest paths
LOCAL_SCRIPTS = Path('../csiro-scripts/scripts')

# ============================================================================
# Common File Names
# ============================================================================

SUBMISSION_FILE_NAME = 'submission.csv'
BEST_MODEL_DIR_NAME = 'best_model'
RESULTS_FILE_NAME = 'results.json'
METADATA_FILE_NAME = 'model_metadata.json'
BEST_MODEL_FILE_NAME = 'best_model.pth'
REGRESSION_MODEL_FILE_NAME = 'regression_model.pkl'

# ============================================================================
# Model Constants
# ============================================================================

# Default image size constant (used when model input size is not specified)
DEFAULT_IMAGE_SIZE = (256, 256)

# ============================================================================
# Feature Cache Path Constants
# ============================================================================

# Feature cache directory names
# CSIRO-SPECIFIC: Contest-specific feature cache directory name
FEATURE_CACHE_INPUT_DIR = _contest_paths.kaggle_input_features_dataset_name  # In /kaggle/input/
FEATURE_CACHE_WORKING_DIR = 'features'  # In /kaggle/working/

