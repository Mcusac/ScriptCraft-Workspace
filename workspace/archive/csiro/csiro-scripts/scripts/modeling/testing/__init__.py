# __init__.py
# Testing package
#
# Provides inference and submission generation utilities organized into focused modules.
#
# Components:
# - dataloaders: Test dataloader creation
# - inference: Core inference execution for end-to-end models
# - tta: Test-time augmentation inference
# - validation: Prediction shape validation
# - submission: Submission format conversion and file I/O
# - regression_inference: Two-stage inference (feature extraction + regression)
#
# All modules follow Single Responsibility Principle for better maintainability.


__all__ = [
    # Dataloaders
    'create_test_dataloader',
    # Inference
    'run_inference',
    'run_inference_with_tta',
    # Validation
    'validate_predictions_shape',
    # Submission
    'expand_predictions_to_submission_format',
    'save_submission_file',
    'create_submission',
    # Regression inference
    'create_regression_submission',
]