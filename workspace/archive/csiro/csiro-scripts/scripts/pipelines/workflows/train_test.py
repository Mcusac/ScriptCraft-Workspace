# train_test.py
# Pipeline to train and then test with best fold

import logging
from pathlib import Path

from config.config import Config
from pipelines.atomic.train_only import train_pipeline
from pipelines.atomic.test_only import test_pipeline
from modeling.training.utils import get_fold_checkpoint_path, find_best_fold_from_scores
from utils.config import validate_pipeline_config

logger = logging.getLogger(__name__)


def train_test_pipeline(config: Config) -> None:
    """
    Train model with cross-validation and then test with best fold.
    
    Args:
        config: Configuration object with training, model, data, cv, paths, and device settings.
                Must have all required attributes configured.
        
    Returns:
        None. Generates submission file as side effect.
        
    Raises:
        ValueError: If config is None or missing required attributes.
        RuntimeError: If training fails or no valid fold scores are available.
        FileNotFoundError: If best fold checkpoint doesn't exist.
    """
    # Validate config
    validate_pipeline_config(config, required_sections=['paths'])
    
    # Train
    logger.info("Starting training phase...")
    avg_cv_score, fold_scores, _ = train_pipeline(config)
    
    # Find best fold
    if not fold_scores:
        raise RuntimeError("No fold scores available. Training may have failed.")
    
    if not all(isinstance(score, (int, float)) for score in fold_scores):
        raise ValueError(f"Invalid fold_scores format: {fold_scores}")
    
    best_fold, best_score = find_best_fold_from_scores(fold_scores)
    logger.info(f"\nBest fold: {best_fold} with score: {best_score:.4f}")
    
    # Test (use best fold model)
    logger.info("\nStarting testing phase...")
    model_path = get_fold_checkpoint_path(Path(config.paths.model_dir), best_fold)
    
    if not model_path.exists():
        raise FileNotFoundError(
            f"Best fold checkpoint not found: {model_path}. "
            f"Training may have failed for fold {best_fold}."
        )
    
    test_pipeline(config, model_path=str(model_path), fold=best_fold)

