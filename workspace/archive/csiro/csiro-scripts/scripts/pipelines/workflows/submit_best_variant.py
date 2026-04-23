# submit_best_variant.py
# Pipeline to generate submission using best variant from dataset grid search

import logging
from pathlib import Path
from typing import Optional

from config.config import Config
from pipelines.atomic.test_only import test_pipeline
from modeling.utils import get_best_variant_info
from modeling.utils.finding import GridSearchModelFinder
from utils.config import apply_preprocessing_to_config, apply_augmentation_to_config, validate_pipeline_config

logger = logging.getLogger(__name__)


def submit_best_variant_pipeline(
    config: Config,
    variant_id: Optional[str] = None,
    results_file: Optional[str] = None
) -> None:
    """
    Generate submission using the best variant from dataset grid search.
    
    Args:
        config: Configuration object with model, data, paths, and device settings.
                Must have all required attributes configured.
        variant_id: Optional variant ID to use instead of finding best (e.g., "variant_0067").
                    Must be valid variant ID if provided.
        results_file: Optional path to results.json file. If None, uses default location.
                     Must exist and contain valid results if provided.
        
    Returns:
        None. Generates submission file as side effect.
        
    Raises:
        ValueError: If config is None, variant_id is invalid, or results_file is invalid.
        FileNotFoundError: If results_file doesn't exist or model checkpoint not found.
        RuntimeError: If variant information cannot be loaded or submission generation fails.
    """
    # Validate config
    validate_pipeline_config(config, required_sections=['paths', 'data'])
    
    if variant_id is not None and not isinstance(variant_id, str):
        raise TypeError(f"variant_id must be string, got {type(variant_id)}")
    # Determine results file path
    if results_file is None:
        results_file = str(Path(config.paths.output_dir) / 'dataset_grid_search' / 'gridsearch_results.json')
    
    results_path = Path(results_file)
    
    logger.info(f"Loading variant information from: {results_path}")
    
    # Get best variant info
    try:
        variant_info = get_best_variant_info(results_path, variant_id=variant_id)
    except Exception as e:
        logger.error(f"Failed to load variant information: {e}")
        raise
    
    variant = variant_info['variant']
    best_fold = variant_info['best_fold']
    best_fold_score = variant_info['best_fold_score']
    preprocessing_list = variant_info['preprocessing_list']
    augmentation_list = variant_info['augmentation_list']
    cv_score = variant_info['cv_score']
    variant_id_used = variant_info['variant_id']
    
    logger.info("="*60)
    logger.info(f"Using variant: {variant_id_used}")
    logger.info(f"  CV Score: {cv_score:.4f}")
    logger.info(f"  Best Fold: {best_fold} (score: {best_fold_score:.4f})")
    logger.info(f"  Preprocessing: {preprocessing_list if preprocessing_list else '[]'}")
    logger.info(f"  Augmentation: {augmentation_list if augmentation_list else '[]'}")
    logger.info(f"{'='*60}\n")
    
    # Search for model in multiple locations
    finder = GridSearchModelFinder()
    model_path = finder.find_model(
        variant_id=variant_id_used,
        best_fold=best_fold,
        config=config
    )
    
    logger.info(f"Using model checkpoint: {model_path}")
    
    # Apply preprocessing and augmentation to config
    # This is CRITICAL - must match what was used during training
    logger.info("Applying preprocessing and augmentation configuration...")
    apply_preprocessing_to_config(config, preprocessing_list)
    apply_augmentation_to_config(config, augmentation_list)
    
    # Update model directory only if using grid search structure
    # (not needed when using model from input dataset)
    original_model_dir = config.paths.model_dir
    is_grid_search_model = 'dataset_grid_search' in str(model_path)
    
    if is_grid_search_model:
        variant_model_dir = str(Path(config.paths.model_dir) / 'dataset_grid_search' / variant_id_used)
        config.paths.model_dir = variant_model_dir
    
    try:
        # Generate submission using test_pipeline
        logger.info("Generating submission...")
        submission_df = test_pipeline(
            config=config,
            model_path=str(model_path),
            fold=best_fold
        )
        
        logger.info("="*60)
        logger.info("Submission generated successfully!")
        logger.info(f"  Variant: {variant_id_used}")
        logger.info(f"  CV Score: {cv_score:.4f}")
        logger.info(f"  Best Fold: {best_fold} (score: {best_fold_score:.4f})")
        logger.info(f"  Submission shape: {submission_df.shape}")
        logger.info(f"{'='*60}")
        
    finally:
        # Restore original model directory
        config.paths.model_dir = original_model_dir

