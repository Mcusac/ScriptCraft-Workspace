"""
Prediction settings for CAFA 6 protein function prediction.
"""

from typing import List, Optional
from .features import BATCH_SIZE_CONFIG
from .ensemble import (
    DEFAULT_ENSEMBLE_METHOD,
    get_ensemble_default
)

# Prediction Constants
MAX_PREDICTIONS_PER_PROTEIN = 1500  # Maximum predictions per protein in submission
SUBMISSION_SORT_CHUNK_SIZE = 1000000  # Chunk size for sorting large submission files
VALIDATION_SAMPLE_SIZE = 1000  # Number of lines to sample for submission validation
DEFAULT_THRESHOLD = 0.5  # Default threshold for threshold optimization

# Progress update intervals
PREDICTION_PROGRESS_INTERVALS = {
    "batch": 15,  # Progress update every N batches
    "predictions": 1000000,  # Progress update every N predictions
    "proteins": 50000,  # Progress update every N proteins
    "chunks": 10,  # Progress update every N chunks
    "large_file": 10000000  # Progress update for very large files
}

# Ensemble workflow constants
ENSEMBLE_GC_COLLECT_INTERVAL = 5  # Force gc.collect() every N batches in ensemble workflow

# Metrics calculation constants
BINARY_PREDICTION_THRESHOLD: float = 0.5  # Threshold for converting probabilities to binary predictions (final predictions)
VALIDATION_METRICS_THRESHOLD: float = 0.01  # Lower threshold for F1 calculation during training/validation (multi-label classification)
METRICS_EPSILON: float = 1e-10  # Epsilon for division by zero protection in metrics calculations

# Prediction Settings (batch sizes reference centralized config)
PREDICTION_SETTINGS = {
    "batch_size": BATCH_SIZE_CONFIG["prediction_pipeline"]["protein_processing"],
    "prediction_threshold": 0.015,
    "max_preds_per_ont": 350,
    "write_batch_size": BATCH_SIZE_CONFIG["prediction_pipeline"]["write_buffer"],
    # Ensemble-specific settings
    "ensemble_batch_size": 10000,  # Process 10K proteins at a time for ensemble
    "ensemble_prediction_threshold": 0.01,  # Threshold for ensemble predictions
    "ensemble_max_preds_per_ont": 1500,  # Max predictions per ontology for ensemble
    # Submission averaging defaults (from config/ensemble.py)
    "submission_averaging_power_default": get_ensemble_default("power_average", "power"),
    "submission_averaging_percentile_default": get_ensemble_default("percentile", "percentile"),
    "default_ensemble_method": DEFAULT_ENSEMBLE_METHOD,
    # Threshold optimization settings
    "enable_threshold_optimization": False,  # Enable IA-weighted threshold optimization
    "threshold_grid": [i/100 for i in range(1, 51)],  # 0.01 to 0.50 in 0.01 steps
    # Prediction propagation settings
    "propagate_predictions": False,  # Propagate predictions up GO graph after prediction
    "prediction_propagation_iterations": 3,  # Number of propagation iterations
    # Output naming settings
    "extra_output_name": None,  # Optional descriptive filename for copy of submission.tsv (None or "" to disable)
}


def get_extra_output_name(override: Optional[str] = None) -> Optional[str]:
    """
    Get extra_output_name from config, with optional override.
    Returns None if config value is None or empty string (disabled).
    
    Args:
        override: Optional value to override config setting
        
    Returns:
        Optional[str]: Extra output name if set, None otherwise
    """
    if override is not None:
        # Allow explicit override (including empty string to disable)
        return override if override else None
    
    value = PREDICTION_SETTINGS.get("extra_output_name")
    # Return None if value is None or empty string
    return value if value else None

