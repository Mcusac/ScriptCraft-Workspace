# submit_lightweight.py
# Lightweight submission pipeline for offline use (Pipeline A)

import logging
from pathlib import Path
from typing import Optional

from config.config import Config
from pipelines.atomic.test_only import test_pipeline
from utils.config import apply_preprocessing_to_config, apply_augmentation_to_config, validate_pipeline_config
from modeling.utils import load_model_metadata
from modeling.utils.finding import LightweightSubmissionModelFinder

logger = logging.getLogger(__name__)


def submit_lightweight_pipeline(
    config: Config,
    model_path: Optional[str] = None,
    metadata_path: Optional[str] = None,
    results_file: Optional[str] = None,
    model_name: Optional[str] = None
) -> None:
    """
    Lightweight submission pipeline for offline use.
    
    Works with uploaded model checkpoint + metadata.
    Searches for model in /kaggle/input/csiro-models/pytorch/default/{version}/best_model.pth
    Uses model_metadata.json for preprocessing/augmentation config.
    Falls back to results.json if metadata not available.
    
    Args:
        config: Configuration object with model, data, paths, and device settings.
                Must have all required attributes configured.
        model_path: Optional explicit model path. If None, searches for model.
                   Must exist if provided.
        metadata_path: Optional explicit metadata path. If None, searches for metadata.
                      Must exist if provided.
        results_file: Optional results.json path (fallback if metadata not found).
                     Must exist if provided.
        
    Returns:
        None. Generates submission file as side effect.
        
    Raises:
        ValueError: If config is None or all model/metadata paths are invalid.
        FileNotFoundError: If model checkpoint cannot be found.
        RuntimeError: If submission generation fails.
    """
    # Validate config
    validate_pipeline_config(config, required_sections=['data', 'paths'])
    
    # Search for model checkpoint
    finder = LightweightSubmissionModelFinder()
    found_model_path, found_metadata_path = finder.find_model(
        model_path=model_path,
        config=config,
        model_name=model_name
    )
    
    # Use explicit metadata path if provided
    if metadata_path:
        found_metadata_path = Path(metadata_path)
    
    # Load metadata with fallback logic
    metadata = load_model_metadata(
        metadata_path=found_metadata_path,
        results_file=Path(results_file) if results_file else None,
        model_path=found_model_path
    )
    
    preprocessing_list = metadata['preprocessing_list']
    augmentation_list = metadata['augmentation_list']
    best_fold = metadata['best_fold']
    
    # Check if this is a regression model (feature extraction mode)
    is_regression_model = found_model_path.suffix == '.pkl'
    
    # Generate submission
    if is_regression_model:
        # Regression model (feature extraction mode)
        logger.info("Generating submission using regression model...")
        
        # Get feature_filename from exported metadata (primary source)
        feature_filename = metadata.get('feature_filename')
        variant_id = metadata.get('variant_id')
        regression_model_type = metadata.get('regression_model_type')
        
        # If feature_filename not in exported metadata, try fallback to grid search metadata
        if not feature_filename:
            if not variant_id or not regression_model_type:
                raise ValueError(
                    f"feature_filename not found in exported metadata and cannot fallback: "
                    f"variant_id={variant_id}, regression_model_type={regression_model_type}. "
                    f"Please ensure the exported model_metadata.json contains 'feature_filename'."
                )
            
            # Fallback: lookup from regression grid search metadata
            logger.info(f"feature_filename not in exported metadata, looking up from grid search metadata...")
            from modeling.utils.metadata.regression_metadata import load_regression_gridsearch_results
            try:
                # Try to find results for this variant_id in gridsearch_metadata.json
                results = load_regression_gridsearch_results(
                    regression_model_type=regression_model_type,
                    variant_id=variant_id
                )
                if results:
                    # Use the result with highest cv_score
                    best_result = max(results, key=lambda x: x.get('cv_score', -float('inf')))
                    feature_filename = best_result.get('feature_filename')
                    if feature_filename:
                        logger.info(
                            f"Found feature_filename from grid search metadata: {feature_filename} "
                            f"(cv_score: {best_result.get('cv_score', 0):.4f})"
                        )
                    else:
                        raise ValueError(f"feature_filename not found in grid search result for variant {variant_id}")
                else:
                    raise ValueError(f"No grid search results found for variant {variant_id}")
            except Exception as e:
                raise ValueError(
                    f"Could not load feature_filename from grid search metadata: {e}. "
                    f"Please ensure the exported model_metadata.json contains 'feature_filename'."
                )
        
        # Parse feature_filename to get feature extraction model and data manipulation info
        from modeling.feature_extraction import parse_feature_filename_to_extraction_info
        try:
            extraction_info = parse_feature_filename_to_extraction_info(feature_filename)
            feature_extraction_model_name = extraction_info['model_name']
            preprocessing_list = extraction_info['preprocessing_list']
            augmentation_list = extraction_info['augmentation_list']
            
            logger.info(f"Parsed feature_filename '{feature_filename}':")
            logger.info(f"  Feature extraction model: {feature_extraction_model_name}")
            logger.info(f"  Data manipulation combo: {extraction_info['combo_id']}")
            logger.info(f"  Preprocessing: {preprocessing_list if preprocessing_list else '[]'}")
            logger.info(f"  Augmentation: {augmentation_list if augmentation_list else '[]'}")
        except Exception as e:
            raise ValueError(
                f"Failed to parse feature_filename '{feature_filename}': {e}. "
                f"Please ensure the feature_filename is valid (e.g., 'variant_0100_features.npz')."
            )
        
        # Set dataset_type to 'split' (default for regression - feature extraction handles splitting)
        dataset_type = 'split'
        config.data.dataset_type = dataset_type
        logger.info(f"Using dataset_type: 'split' (default for regression models)")
        
        # Apply preprocessing and augmentation to config (from feature extraction)
        # This is CRITICAL - must match what was used during feature extraction
        if preprocessing_list or augmentation_list:
            logger.info("Applying preprocessing and augmentation configuration from feature extraction...")
            apply_preprocessing_to_config(config, preprocessing_list)
            apply_augmentation_to_config(config, augmentation_list)
        
        from modeling.testing import create_regression_submission
        from utils.system import get_device
        
        device = get_device(config.device.device)
        test_csv_path = Path(config.data.data_root) / config.data.test_csv
        output_path = Path(config.paths.output_dir) / config.paths.submission_file
        
        submission_df = create_regression_submission(
            regression_model_path=str(found_model_path),
            feature_extraction_model_name=feature_extraction_model_name,
            test_csv_path=str(test_csv_path),
            data_root=config.data.data_root,
            config=config,
            device=device,
            output_path=str(output_path)
        )
    else:
        # End-to-end PyTorch model (existing path)
        logger.info("Generating submission using end-to-end model...")
        
        # Determine dataset_type with priority: command-line > metadata > default
        # Command-line argument (config.data.dataset_type) takes precedence as explicit user intent
        # Note: command_router always sets config.data.dataset_type from --dataset-type argument
        dataset_type_from_config = getattr(config.data, 'dataset_type', 'split')  # Default to 'split'
        dataset_type_from_metadata = metadata.get('dataset_type', None)
        
        # Check if command-line was explicitly provided by comparing with metadata
        # If they differ, command-line takes precedence (user's explicit intent)
        if dataset_type_from_metadata and dataset_type_from_config != dataset_type_from_metadata:
            # Command-line differs from metadata - use command-line and warn
            dataset_type = dataset_type_from_config
            source = "command-line argument"
            logger.warning(
                f"⚠️  Dataset type mismatch detected:\n"
                f"   Command-line: '{dataset_type}' (will be used)\n"
                f"   Metadata: '{dataset_type_from_metadata}' (from training)\n"
                f"   Using command-line value. Ensure this matches how the model was trained!"
            )
        elif dataset_type_from_metadata:
            # Use metadata value (what was saved during training) - matches command-line or no command-line provided
            dataset_type = dataset_type_from_metadata
            source = "metadata (from training)"
        else:
            # No metadata available - use command-line or default
            dataset_type = dataset_type_from_config
            source = "command-line argument" if dataset_type_from_config != 'split' else "default (split)"
        
        # Set dataset_type in config (CRITICAL - must match what was used during training)
        config.data.dataset_type = dataset_type
        logger.info(f"Using dataset_type: '{dataset_type}' (from {source})")
        
        # Apply preprocessing and augmentation to config
        # This is CRITICAL - must match what was used during training
        if preprocessing_list or augmentation_list:
            logger.info("Applying preprocessing and augmentation configuration...")
            apply_preprocessing_to_config(config, preprocessing_list)
            apply_augmentation_to_config(config, augmentation_list)
        
        submission_df = test_pipeline(
            config=config,
            model_path=str(found_model_path),
            fold=best_fold
        )
    
    logger.info("="*60)
    logger.info("✅ Submission generated successfully!")
    logger.info(f"  Model: {found_model_path}")
    if is_regression_model:
        logger.info(f"  Regression Model Type: {regression_model_type}")
        logger.info(f"  Feature Filename: {feature_filename}")
        logger.info(f"  Feature Extraction Model: {feature_extraction_model_name}")
    logger.info(f"  Dataset Type: {config.data.dataset_type}")
    logger.info(f"  Preprocessing: {preprocessing_list if preprocessing_list else '[]'}")
    logger.info(f"  Augmentation: {augmentation_list if augmentation_list else '[]'}")
    logger.info(f"  Submission shape: {submission_df.shape}")
    
    # Verify submission file format and contents
    logger.info(f"\n📋 Submission file verification:")
    logger.info(f"  Path: {Path(config.paths.output_dir) / config.paths.submission_file}")
    logger.info(f"  Shape: {submission_df.shape}")
    logger.info(f"  Columns: {submission_df.columns.tolist()}")
    logger.info(f"  Target value range: [{submission_df['target'].min():.2f}, {submission_df['target'].max():.2f}]")
    logger.info(f"  ✅ Submission file is ready!")
    logger.info(f"{'='*60}")

