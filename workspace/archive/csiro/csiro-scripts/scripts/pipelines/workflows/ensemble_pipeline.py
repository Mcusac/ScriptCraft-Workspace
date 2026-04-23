# ensemble_pipeline.py
# Pipeline to generate submission using ensemble of top N models

import logging
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Optional, Dict

from config.config import Config
from modeling.ensembling import create_ensemble_from_results, create_ensemble_from_paths
from modeling.testing import expand_predictions_to_submission_format, validate_predictions_shape
from modeling.utils import save_submission_file
from utils.config import validate_pipeline_config
from utils.system import get_device

logger = logging.getLogger(__name__)


def ensemble_pipeline(
    config: Config,
    results_files: Optional[List[str]] = None,
    top_n: int = 3,
    method: str = 'weighted_average',
    fallback_paths: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Generate submission using ensemble of top N models from grid search results.
    
    Pipeline flow:
    1. Determine results files (default: check working directory, then input paths)
    2. Load top N models from results
    3. Load all models
    4. Run inference with each model
    5. Combine predictions using selected method
    6. Generate submission file
    
    Args:
        config: Configuration object with model, data, paths, and device settings.
                Must have all required attributes configured.
        results_files: Optional list of results file paths.
                      If None, auto-detects from default locations.
        top_n: Number of top models to ensemble (default: 3).
               Must be positive integer.
        method: Ensembling method: 'simple_average', 'weighted_average', 'ranked_average', or 'percentile_average' (default: 'weighted_average').
        fallback_paths: Optional list of additional paths to search for results files.
        
    Returns:
        Submission DataFrame with columns: sample_id, target.
        Contains N * 5 rows where N is number of unique test images.
        
    Raises:
        ValueError: If config is None, top_n is invalid, or method is unknown.
        FileNotFoundError: If no results files found or models cannot be loaded.
        RuntimeError: If inference or submission generation fails.
    """
    # Validate config
    validate_pipeline_config(config, required_sections=['data', 'paths', 'cv', 'model'])
    
    if not isinstance(top_n, int) or top_n < 1:
        raise ValueError(f"top_n must be positive integer, got {top_n}")
    
    valid_methods = ['simple_average', 'weighted_average', 'ranked_average', 'percentile_average']
    if method not in valid_methods:
        raise ValueError(
            f"method must be one of {valid_methods}, got {method}"
        )
    
    logger.info("="*60)
    logger.info("Ensemble Pipeline")
    logger.info(f"{'='*60}")
    logger.info(f"  Top N models: {top_n}")
    logger.info(f"  Method: {method}")
    logger.info(f"  Model: {config.model.name}")
    
    # Get device
    device = get_device(config.device.device)
    logger.info(f"  Device: {device}")
    
    # Create ensemble
    logger.info("\nCreating ensemble...")
    ensemble = create_ensemble_from_results(
        config=config,
        results_files=results_files,
        top_n=top_n,
        method=method,
        fallback_paths=fallback_paths,
        device=device
    )
    
    logger.info(f"\nEnsemble created with {len(ensemble.models)} models")
    
    # Run inference with ensemble using individual preprocessing per model
    test_csv_path = Path(config.data.data_root) / config.data.test_csv
    data_root = config.data.data_root
    
    logger.info(f"\nRunning ensemble inference on test set...")
    logger.info(f"  Test CSV: {test_csv_path}")
    logger.info(f"  Data root: {data_root}")
    logger.info(f"  Each model will use its own preprocessing from metadata")
    
    # Run inference with each model using its own preprocessing
    predictions = ensemble.predict_with_individual_preprocessing(
        test_csv_path=str(test_csv_path),
        data_root=data_root,
        config=config
    )
    
    logger.info(f"Inference complete. Predictions shape: {predictions.shape}")
    
    # Get number of unique images for validation
    from dataset_manipulation import load_and_validate_test_data
    unique_images = load_and_validate_test_data(str(test_csv_path))
    
    # Validate predictions shape
    validate_predictions_shape(predictions, len(unique_images), expected_cols=3)
    
    # Expand to submission format
    logger.info("\nExpanding predictions to submission format...")
    submission_df = expand_predictions_to_submission_format(
        predictions=predictions,
        test_csv_path=str(test_csv_path)
    )
    
    # Save submission
    output_path = save_submission_file(submission_df, config)
    
    logger.info("="*60)
    logger.info("✅ Ensemble submission generated successfully!")
    logger.info("="*60)
    logger.info(f"  Models used: {len(ensemble.models)}")
    logger.info(f"  Method: {method}")
    logger.info(f"  Submission shape: {submission_df.shape}")
    logger.info(f"  Output: {output_path}")
    
    return submission_df


def ensemble_pipeline_from_paths(
    config: Config,
    model_paths: List[str],
    method: str = 'weighted_average',
    submission_scores: Optional[Dict[str, float]] = None,
    score_type: str = 'cv'
) -> pd.DataFrame:
    """
    Generate submission using ensemble of models from direct paths.
    
    Pipeline flow:
    1. Validate all model paths exist and contain required files
    2. Load all models from specified paths
    3. Run inference with each model
    4. Combine predictions using selected method
    5. Generate submission file
    
    Args:
        config: Configuration object with model, data, paths, and device settings.
                Must have all required attributes configured.
        model_paths: List of model base paths (directories containing best_model.pth and model_metadata.json).
                     Example: ['/kaggle/input/csiro-models/pytorch/default/8', ...]
        method: Ensembling method: 'simple_average', 'weighted_average', 'ranked_average', or 'percentile_average' (default: 'weighted_average').
        submission_scores: Optional dictionary mapping model_path -> submission_score
        score_type: Which scores to use for weighting: 'cv', 'submission', 'combined' (default: 'cv')
        
    Returns:
        Submission DataFrame with columns: sample_id, target.
        Contains N * 5 rows where N is number of unique test images.
        
    Raises:
        ValueError: If config is None, model_paths is empty, or method is unknown.
        FileNotFoundError: If any model path doesn't exist or is missing required files.
        RuntimeError: If inference or submission generation fails.
    """
    # Validate config
    validate_pipeline_config(config, required_sections=['data', 'paths', 'cv', 'model'])
    
    if not model_paths:
        raise ValueError("model_paths cannot be empty")
    
    valid_methods = ['simple_average', 'weighted_average', 'ranked_average', 'percentile_average']
    if method not in valid_methods:
        raise ValueError(
            f"method must be one of {valid_methods}, got {method}"
        )
    
    logger.info("="*60)
    logger.info("Ensemble Pipeline (from paths)")
    logger.info(f"{'='*60}")
    logger.info(f"  Models: {len(model_paths)}")
    logger.info(f"  Method: {method}")
    logger.info(f"  Score Type: {score_type}")
    
    # Run diagnostics if submission_scores provided
    if submission_scores:
        from modeling.utils import analyze_ensemble_weights, print_diagnostic_summary
        
        logger.info("\nRunning ensemble diagnostics...")
        diagnostics = analyze_ensemble_weights(
            model_paths=model_paths,
            submission_scores=submission_scores,
            score_type=score_type
        )
        print_diagnostic_summary(diagnostics)
    
    # Get device
    device = get_device(config.device.device)
    logger.info(f"  Device: {device}")
    
    # Create ensemble
    logger.info("\nCreating ensemble from model paths...")
    ensemble = create_ensemble_from_paths(
        model_paths=model_paths,
        config=config,
        method=method,
        device=device,
        submission_scores=submission_scores,
        score_type=score_type
    )
    
    logger.info(f"\nEnsemble created with {len(ensemble.models)} models")
    
    # Run inference with ensemble using individual preprocessing per model
    test_csv_path = Path(config.data.data_root) / config.data.test_csv
    data_root = config.data.data_root
    
    logger.info(f"\nRunning ensemble inference on test set...")
    logger.info(f"  Test CSV: {test_csv_path}")
    logger.info(f"  Data root: {data_root}")
    logger.info(f"  Each model will use its own preprocessing from metadata")
    
    # Run inference with each model using its own preprocessing
    predictions = ensemble.predict_with_individual_preprocessing(
        test_csv_path=str(test_csv_path),
        data_root=data_root,
        config=config
    )
    
    logger.info(f"Inference complete. Predictions shape: {predictions.shape}")
    
    # Get number of unique images for validation
    from dataset_manipulation import load_and_validate_test_data
    unique_images = load_and_validate_test_data(str(test_csv_path))
    
    # Validate predictions shape
    validate_predictions_shape(predictions, len(unique_images), expected_cols=3)
    
    # Expand to submission format
    logger.info("\nExpanding predictions to submission format...")
    submission_df = expand_predictions_to_submission_format(
        predictions=predictions,
        test_csv_path=str(test_csv_path)
    )
    
    # Save submission
    output_path = save_submission_file(submission_df, config)
    
    logger.info("="*60)
    logger.info("✅ Ensemble submission generated successfully!")
    logger.info("="*60)
    logger.info(f"  Models used: {len(ensemble.models)}")
    logger.info(f"  Method: {method}")
    logger.info(f"  Submission shape: {submission_df.shape}")
    logger.info(f"  Output: {output_path}")
    
    return submission_df

