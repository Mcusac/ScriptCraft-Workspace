# validator.py
# Checkpoint validation utilities

import logging
from pathlib import Path
from typing import Tuple

from .paths import get_fold_checkpoint_path, get_fold_regression_model_path
from .info import load_checkpoint_info, is_checkpoint_complete, load_regression_model_info

logger = logging.getLogger(__name__)


def has_incomplete_folds(model_dir: Path, n_folds: int = 5) -> bool:
    """
    Check if any folds in the training directory are incomplete.
    
    Args:
        model_dir: Base model directory. Can be string or Path object.
        n_folds: Number of folds to check
        
    Returns:
        True if any fold is incomplete or missing, False if all folds are complete
        
    Raises:
        ValueError: If model_dir is None or n_folds is invalid.
    """
    if model_dir is None:
        raise ValueError("model_dir cannot be None")
    
    model_dir_obj = Path(model_dir)
    
    if not isinstance(n_folds, int) or n_folds <= 0:
        raise ValueError(f"n_folds must be positive integer, got {n_folds}")
    
    # Check each fold
    for fold in range(n_folds):
        checkpoint_path = get_fold_checkpoint_path(model_dir_obj, fold)
        is_complete, _ = is_checkpoint_complete(checkpoint_path)
        
        if not is_complete:
            # Found incomplete or missing fold
            return True
    
    # All folds are complete
    return False


def find_best_fold(model_dir: Path, n_folds: int = 5) -> Tuple[int, float, Path]:
    """
    Find the best performing fold by checking all fold checkpoints.
    
    Supports both regular PyTorch checkpoints and feature extraction regression models.
    
    Args:
        model_dir: Base model directory
        n_folds: Number of folds to check
        
    Returns:
        Tuple of (best_fold, best_score, best_checkpoint_path)
        
    Raises:
        FileNotFoundError: If no valid checkpoints found
    """
    best_fold = None
    best_score = -float('inf')
    best_path = None
    
    for fold in range(n_folds):
        # Try regular PyTorch checkpoint first
        checkpoint_path = get_fold_checkpoint_path(model_dir, fold)
        info = load_checkpoint_info(checkpoint_path)
        
        # If no regular checkpoint, try feature extraction regression model
        if info is None:
            regression_model_path = get_fold_regression_model_path(model_dir, fold)
            metadata_path = regression_model_path.parent / 'regression_model_info.json'
            
            logger.info(f"Checking fold {fold} for regression model: {regression_model_path}")
            
            # Try to load metadata (must exist for regression models)
            if metadata_path.exists():
                logger.info(f"Fold {fold}: Found metadata file: {metadata_path}")
                info = load_regression_model_info(metadata_path)
                if info:
                    logger.info(f"Fold {fold}: Successfully loaded metadata (best_score: {info.get('best_score', 'N/A')})")
                    # Verify regression model file also exists
                    if regression_model_path.exists():
                        checkpoint_path = regression_model_path
                        logger.info(f"Found regression model for fold {fold}: {checkpoint_path} (score: {info.get('best_score', 'N/A')})")
                    else:
                        logger.warning(f"Fold {fold}: Metadata found but regression model file missing: {regression_model_path}")
                        info = None
                else:
                    logger.warning(f"Fold {fold}: Metadata file exists but failed to load or is invalid: {metadata_path}")
                    # Try to read the file to see what's wrong
                    try:
                        import json
                        with open(metadata_path, 'r') as f:
                            raw_content = f.read()
                            logger.warning(f"Fold {fold}: Metadata file content (first 200 chars): {raw_content[:200]}")
                            parsed = json.loads(raw_content)
                            logger.warning(f"Fold {fold}: Parsed metadata keys: {list(parsed.keys()) if isinstance(parsed, dict) else 'Not a dict'}")
                    except Exception as e:
                        logger.warning(f"Fold {fold}: Could not read metadata file for diagnostics: {e}")
            else:
                logger.debug(f"Fold {fold}: No checkpoint or regression model metadata found at {metadata_path}")
        
        if info and info.get('best_score', -float('inf')) > best_score:
            best_score = info['best_score']
            best_fold = fold
            best_path = checkpoint_path
    
    if best_fold is None:
        # Provide more helpful error message with detailed diagnostics
        logger.error(f"No valid checkpoints found in {model_dir}")
        logger.error(f"Checked {n_folds} folds for PyTorch checkpoints (.pth) or regression models (.pkl)")
        
        # Diagnostic: List what files actually exist and try to diagnose issues
        if model_dir.exists():
            logger.error(f"Directory exists. Contents:")
            regression_models_found = []
            metadata_files_found = []
            
            for fold_dir in sorted(model_dir.iterdir()):
                if fold_dir.is_dir() and fold_dir.name.startswith('fold_'):
                    logger.error(f"  {fold_dir.name}:")
                    for file in sorted(fold_dir.iterdir()):
                        if file.is_file():
                            logger.error(f"    - {file.name} ({file.stat().st_size} bytes)")
                            
                            # Track regression model files
                            if file.name == 'regression_model.pkl':
                                regression_models_found.append(fold_dir.name)
                            elif file.name == 'regression_model_info.json':
                                metadata_files_found.append(fold_dir.name)
                                # Try to validate the metadata file
                                try:
                                    import json
                                    with open(file, 'r') as f:
                                        metadata = json.load(f)
                                        if 'best_score' not in metadata:
                                            logger.error(f"    ⚠️  Metadata file missing 'best_score' field. Keys: {list(metadata.keys())}")
                                        else:
                                            logger.error(f"    ✓ Metadata has 'best_score': {metadata.get('best_score')}")
                                except Exception as e:
                                    logger.error(f"    ⚠️  Could not parse metadata file: {e}")
            
            # Summary of findings
            if regression_models_found:
                logger.error(f"Found {len(regression_models_found)} regression model files: {regression_models_found}")
            if metadata_files_found:
                logger.error(f"Found {len(metadata_files_found)} metadata files: {metadata_files_found}")
            
            if regression_models_found and metadata_files_found:
                logger.error("⚠️  Regression models and metadata exist but were not detected. This may indicate:")
                logger.error("    1. Metadata files are missing 'best_score' field")
                logger.error("    2. Metadata files are malformed JSON")
                logger.error("    3. File permissions issue")
        else:
            logger.error(f"Directory does not exist: {model_dir}")
        
        raise FileNotFoundError(f"No valid checkpoints found in {model_dir}")
    
    return best_fold, best_score, best_path
