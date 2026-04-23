# regression_inference.py
# Inference for regression models (two-stage: feature extraction + regression)

import pickle
import logging
from pathlib import Path

from config.config import Config
from .dataloaders import create_test_dataloader
from .submission import expand_predictions_to_submission_format, save_submission_file
from modeling.feature_extraction import FeatureExtractor
from modeling.models import create_model

logger = logging.getLogger(__name__)


def create_regression_submission(
    regression_model_path: str,
    feature_extraction_model_name: str,
    test_csv_path: str,
    data_root: str,
    config: Config,
    device,
    output_path: str = 'submission.csv'
):
    """
    Create submission using regression model (feature extraction mode).
    
    This function handles the two-stage inference process:
    1. Extract features from test images using feature extraction model
    2. Predict using regression model on extracted features
    
    Reuses existing utilities:
    - FeatureExtractor: For feature extraction
    - create_test_dataloader: For test data loading
    - expand_predictions_to_submission_format: For submission formatting
    - save_submission_file: For file saving
    
    Args:
        regression_model_path: Path to regression model .pkl file
        feature_extraction_model_name: Model name for feature extraction (e.g., 'facebook/dinov2-base')
        test_csv_path: Path to test.csv file
        data_root: Root directory for images
        config: Configuration object
        device: Device to run inference on
        output_path: Path to save submission CSV
        
    Returns:
        Submission DataFrame with columns: sample_id, target
        
    Raises:
        FileNotFoundError: If regression model file doesn't exist
        ValueError: If inputs are invalid
    """
    # Validate inputs
    regression_model_path_obj = Path(regression_model_path)
    if not regression_model_path_obj.exists():
        raise FileNotFoundError(f"Regression model not found: {regression_model_path}")
    
    if not isinstance(feature_extraction_model_name, str) or not feature_extraction_model_name:
        raise ValueError(f"feature_extraction_model_name must be non-empty string, got {feature_extraction_model_name}")
    
    # Validate that feature_extraction_model_name is not a regression model type
    from modeling.models import _is_regression_model_type
    if _is_regression_model_type(feature_extraction_model_name):
        raise ValueError(
            f"Invalid feature_extraction_model_name '{feature_extraction_model_name}': "
            f"This is a regression model type, not a feature extraction model. "
            f"Please provide a valid feature extraction model name "
            f"(e.g., 'dinov2', 'facebook/dinov2-base', 'efficientnet_b3')."
        )
    
    # Load regression model (reuse existing pattern from feature_extraction_trainer)
    logger.info(f"Loading regression model from {regression_model_path}")
    with open(regression_model_path_obj, 'rb') as f:
        regression_model = pickle.load(f)
    
    # Create feature extraction model (reuse create_model)
    logger.info(f"Creating feature extraction model: {feature_extraction_model_name}")
    
    # Convert model name to pretrained weights path (reuse existing utility)
    from config.model_constants import get_pretrained_weights_path
    pretrained_weights_path = get_pretrained_weights_path(feature_extraction_model_name)
    
    original_name = config.model.name
    original_pretrained = config.model.pretrained
    try:
        config.model.name = pretrained_weights_path  # Use converted path instead of model name
        config.model.pretrained = True
        feature_model = create_model(config)
        feature_model.to(device)
        feature_model.eval()
    except ValueError as e:
        # Re-raise with more context
        raise ValueError(
            f"Failed to create feature extraction model '{feature_extraction_model_name}': {e}\n"
            f"This may indicate that the model name is invalid or not supported. "
            f"Please ensure the feature extraction model name matches what was used during training."
        ) from e
    finally:
        config.model.name = original_name  # Restore
        config.model.pretrained = original_pretrained
    
    # Extract features (reuse FeatureExtractor)
    logger.info("Extracting features from test images...")
    feature_extractor = FeatureExtractor(feature_model, device)
    test_loader = create_test_dataloader(
        test_csv_path=test_csv_path,
        data_root=data_root,
        config=config
    )
    dataset_type = getattr(config.data, 'dataset_type', 'split')
    features = feature_extractor.extract_features(test_loader, dataset_type, config=config)
    logger.info(f"Extracted features shape: {features.shape}")
    
    # Predict (regression model already handles MultiOutputRegressor)
    logger.info("Running regression model predictions...")
    predictions = regression_model.predict(features)  # Shape: (N, 3)
    logger.info(f"Predictions shape: {predictions.shape}")
    
    # Expand to submission format (reuse existing function)
    submission_df = expand_predictions_to_submission_format(
        predictions=predictions,
        test_csv_path=test_csv_path
    )
    
    # Save (reuse existing function)
    output_path_obj = save_submission_file(submission_df, config, output_path)
    
    logger.info(f"Submission shape: {submission_df.shape}")
    logger.info(f"Sample submission:\n{submission_df.head(10)}")
    
    return submission_df
