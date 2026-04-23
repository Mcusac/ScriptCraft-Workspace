"""
Prediction module for CAFA 6 protein function prediction.
Contains prediction and submission generation utilities.
"""

from .predict_and_submit import (
    load_test_sequences,
    make_predictions,
    post_process_submission
)
from .submission_merging import parse_submission_line
from .prediction_utils import (
    format_prediction_score,
    is_valid_score,
    validate_go_term_format,
    cleanup_temp_files,
    log_progress
)

__all__ = [
    'load_test_sequences',
    'make_predictions', 
    'post_process_submission',
    'parse_submission_line',
    'format_prediction_score',
    'is_valid_score',
    'validate_go_term_format',
    'cleanup_temp_files',
    'log_progress'
]
