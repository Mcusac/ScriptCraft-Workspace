# factory.py
# Factory functions for creating Ensemble objects

import logging
import torch
from pathlib import Path
from typing import Dict, List, Optional

from config.config import Config
from .ensemble import Ensemble
from .results_loader import load_results_from_files, find_top_n_models
from .model_loader import ModelConfig, load_ensemble_models
from .methods import create_ensembling_method

logger = logging.getLogger(__name__)


def create_ensemble_from_results(
    config: Config,
    results_files: Optional[List[str]] = None,
    top_n: int = 3,
    method: str = 'weighted_average',
    fallback_paths: Optional[List[str]] = None,
    device: Optional[torch.device] = None
) -> Ensemble:
    """
    Create ensemble from results files.
    
    Factory function that:
    1. Loads results from files
    2. Finds top N models
    3. Loads all models
    4. Creates Ensemble object
    
    Args:
        results_files: Optional list of results file paths.
                     If None, auto-detects from default locations.
        top_n: Number of top models to ensemble (default: 3)
        config: Configuration object with model and paths settings
        method: Ensembling method name ('simple_average', 'weighted_average', 'ranked_average', or 'percentile_average')
        fallback_paths: Optional list of additional paths to search for results files
        device: Optional device to load models on. If None, uses config.device
        
    Returns:
        Ensemble object ready for inference
        
    Raises:
        FileNotFoundError: If no results files found
        ValueError: If no valid models found or invalid parameters
        RuntimeError: If model loading fails
    
    Example:
        Auto-detect results and create ensemble with top 3 models:
        ```python
        from config.config import Config
        from modeling.ensembling import create_ensemble_from_results
        
        config = Config.from_json('config.json')
        ensemble = create_ensemble_from_results(config, top_n=3, method='weighted_average')
        predictions = ensemble.predict(test_images)
        ```
        
        Explicit results file path:
        ```python
        ensemble = create_ensemble_from_results(
            config,
            results_files=['outputs/dataset_grid_search/gridsearch_results.json'],
            top_n=5,
            method='ranked_average'
        )
        ```
    """
    from utils.system import get_device
    
    if device is None:
        device = get_device(config.device.device)
    
    logger.info(f"Creating ensemble with top_n={top_n}, method={method}")
    
    # Load results
    all_results = load_results_from_files(results_files, fallback_paths)
    
    # Find top N models
    top_variants = find_top_n_models(all_results, top_n=top_n)
    
    if not top_variants:
        raise ValueError("No valid models found in results")
    
    # Create model configs
    model_configs = []
    for variant in top_variants:
        # Get variant info in format expected by get_best_variant_info
        variant_id = variant.get('variant_id')
        best_fold, best_fold_score = None, None
        
        try:
            from modeling.utils import get_variant_best_fold
            best_fold, best_fold_score = get_variant_best_fold(variant)
        except Exception as e:
            logger.warning(f"Could not get best fold for {variant_id}: {e}")
            continue
        
        # Resolve preprocessing_list and augmentation_list from data_manipulation.combo_id
        from modeling.utils.metadata.data_manipulation_loader import (
            extract_preprocessing_augmentation_from_variant
        )
        preprocessing_list, augmentation_list = extract_preprocessing_augmentation_from_variant(variant)
        
        variant_info = {
            'variant_id': variant_id,
            'best_fold': best_fold,
            'best_fold_score': best_fold_score,
            'cv_score': variant.get('cv_score'),
            'preprocessing_list': preprocessing_list,
            'augmentation_list': augmentation_list,
            'dataset_type': variant.get('dataset_type', 'split'),
            'variant': variant  # Store full variant for debugging
        }
        
        # Try to find model path for this variant
        from .model_loader import find_model_path_for_variant
        model_path = find_model_path_for_variant(config, variant_id, best_fold)
        
        if not model_path:
            logger.warning(f"Could not find model path for variant {variant_id}, skipping")
            continue
        
        # Extract model name from variant
        model_name = variant.get('model_name')
        if not model_name:
            model_name = config.model.name
        
        logger.info(f"Added model config: {variant_id} (fold {best_fold}, cv={variant.get('cv_score', 'N/A')})")
        
        # Create ModelConfig
        model_config = ModelConfig(
            variant_info=variant_info,
            model_path=model_path,
            model_name=model_name,
            submission_score=variant.get('submission_score')
        )
        model_configs.append(model_config)
    
    if not model_configs:
        raise ValueError("No valid model configs created")
    
    logger.info(f"Prepared {len(model_configs)} model configs for loading")
    
    # Load models
    models = load_ensemble_models(model_configs, config, device)
    
    # Create ensembling method
    ensembling_method = create_ensembling_method(method)
    
    # Create ensemble
    ensemble = Ensemble(
        models=models,
        model_configs=model_configs,
        ensembling_method=ensembling_method,
        device=device,
        score_type='cv'  # Default to CV scores
    )
    
    logger.info(
        f"Created ensemble with {len(models)} models using {method} method"
    )
    
    return ensemble


def create_ensemble_from_paths(
    model_paths: List[str],
    config: Config,
    method: str = 'weighted_average',
    device: Optional[torch.device] = None,
    submission_scores: Optional[Dict[str, float]] = None,
    score_type: str = 'cv'
) -> Ensemble:
    """
    Create ensemble from direct model paths.
    
    Factory function that:
    1. Validates all model paths exist and contain required files
    2. Loads metadata from each model directory
    3. Creates ModelConfig objects from metadata
    4. Loads all models
    5. Creates Ensemble object
    
    Args:
        model_paths: List of model base paths (directories containing best_model.pth and model_metadata.json).
                    Example: ['/kaggle/input/csiro-models/pytorch/default/8', ...]
        config: Configuration object with model and paths settings
        method: Ensembling method name ('simple_average', 'weighted_average', 'ranked_average', or 'percentile_average')
        device: Optional device to load models on. If None, uses config.device
        submission_scores: Optional dictionary mapping model_path -> submission_score
        score_type: Which scores to use for weighting: 'cv', 'submission', 'combined' (default: 'cv')
        
    Returns:
        Ensemble object ready for inference
        
    Raises:
        FileNotFoundError: If any model path doesn't exist or is missing required files
        ValueError: If no valid models found, models have different architectures, or invalid parameters
        RuntimeError: If model loading fails
    
    Example:
        Create ensemble from explicit model paths:
        ```python
        from config.config import Config
        from modeling.ensembling import create_ensemble_from_paths
        
        config = Config.from_json('config.json')
        model_paths = [
            '/kaggle/input/csiro-models/pytorch/default/8',
            '/kaggle/input/csiro-models/pytorch/default/12',
            '/kaggle/input/csiro-models/pytorch/default/15'
        ]
        ensemble = create_ensemble_from_paths(model_paths, config, method='weighted_average')
        predictions = ensemble.predict(test_images)
        ```
        
        Using submission scores for weighting:
        ```python
        submission_scores = {
            '/kaggle/input/csiro-models/pytorch/default/8': 0.95,
            '/kaggle/input/csiro-models/pytorch/default/12': 0.96,
            '/kaggle/input/csiro-models/pytorch/default/15': 0.94
        }
        ensemble = create_ensemble_from_paths(
            model_paths,
            config,
            method='weighted_average',
            submission_scores=submission_scores,
            score_type='submission'
        )
        ```
    """
    from utils.system import get_device
    from modeling.utils import load_model_metadata
    
    if device is None:
        device = get_device(config.device.device)
    
    if not model_paths:
        raise ValueError("model_paths cannot be empty")
    
    logger.info(f"Creating ensemble from {len(model_paths)} model paths, method={method}")
    
    # Validate all paths and collect model configs
    model_configs = []
    model_names = set()
    
    for idx, model_base_path in enumerate(model_paths, 1):
        base_path = Path(model_base_path)
        
        if not base_path.exists():
            raise FileNotFoundError(
                f"Model path {idx}/{len(model_paths)} does not exist: {base_path}"
            )
        
        if not base_path.is_dir():
            raise ValueError(
                f"Model path {idx}/{len(model_paths)} is not a directory: {base_path}"
            )
        
        # Find best_model.pth
        model_file = base_path / 'best_model.pth'
        if not model_file.exists():
            raise FileNotFoundError(
                f"Model checkpoint not found in {base_path}: {model_file}\n"
                f"Expected: {base_path}/best_model.pth"
            )
        
        # Load metadata
        metadata_file = base_path / 'model_metadata.json'
        if not metadata_file.exists():
            raise FileNotFoundError(
                f"Model metadata not found in {base_path}: {metadata_file}\n"
                f"Expected: {base_path}/model_metadata.json"
            )
        
        logger.info(f"Loading model {idx}/{len(model_paths)}: {base_path}")
        
        # Load metadata
        metadata = load_model_metadata(
            metadata_path=metadata_file,
            results_file=None,
            model_path=model_file
        )
        
        # Extract model info from metadata
        model_name = None
        cv_score = None
        
        # Try to load full metadata JSON to get model_name and cv_score
        try:
            import json
            with open(metadata_file, 'r') as f:
                full_metadata = json.load(f)
                model_name = full_metadata.get('model_name')
                cv_score = full_metadata.get('cv_score')
        except Exception as e:
            logger.warning(f"Could not load full metadata from {metadata_file}: {e}")
        
        # Use config model name if not in metadata
        if not model_name:
            model_name = config.model.name
            logger.info(f"  Using model name from config: {model_name}")
        else:
            logger.info(f"  Model name from metadata: {model_name}")
        
        model_names.add(model_name)
        
        # Get preprocessing and augmentation from metadata
        preprocessing_list = metadata.get('preprocessing_list', [])
        augmentation_list = metadata.get('augmentation_list', [])
        best_fold = metadata.get('best_fold', 0)
        dataset_type = metadata.get('dataset_type', 'full')
        
        logger.info(f"  CV score: {cv_score if cv_score is not None else 'N/A'}")
        logger.info(f"  Dataset Type: {dataset_type}")
        logger.info(f"  Preprocessing: {preprocessing_list if preprocessing_list else '[]'}")
        logger.info(f"  Augmentation: {augmentation_list if augmentation_list else '[]'}")
        logger.info(f"  Best fold: {best_fold}")
        
        # Create variant_info dict (similar to create_ensemble_from_results)
        variant_info = {
            'variant_id': f"model_path_{idx}",
            'best_fold': best_fold,
            'best_fold_score': None,  # Not available from metadata alone
            'cv_score': cv_score,
            'preprocessing_list': preprocessing_list,
            'augmentation_list': augmentation_list,
            'dataset_type': dataset_type,
            'variant': None  # Not available from direct paths
        }
        
        # Get submission score if provided
        submission_score = None
        if submission_scores:
            submission_score = submission_scores.get(model_base_path)
            logger.info(f"  Submission score: {submission_score if submission_score is not None else 'N/A'}")
            if submission_score is None:
                logger.warning(f"  WARNING: No submission score found for path: {model_base_path}")
                logger.warning(f"  Available keys in submission_scores: {list(submission_scores.keys())}")
        else:
            logger.info(f"  Submission score: Not provided (submission_scores is None)")
        
        # Create ModelConfig
        model_config = ModelConfig(
            variant_info=variant_info,
            model_path=model_file,
            model_name=model_name,
            submission_score=submission_score
        )
        model_configs.append(model_config)
    
    # Validate all models have same architecture
    if len(model_names) > 1:
        raise ValueError(
            f"All models in ensemble must have same architecture. "
            f"Found: {model_names}"
        )
    
    model_name = list(model_names)[0]
    
    # Update config if needed
    if config.model.name != model_name:
        logger.warning(
            f"Config model name ({config.model.name}) doesn't match ensemble models ({model_name}). "
            f"Using ensemble model name."
        )
        config.model.name = model_name
    
    if not model_configs:
        raise ValueError("No valid model configs created")
    
    logger.info(f"Prepared {len(model_configs)} model configs for loading")
    
    # Load models
    models = load_ensemble_models(model_configs, config, device)
    
    # Create ensembling method
    ensembling_method = create_ensembling_method(method)
    
    # Create ensemble
    ensemble = Ensemble(
        models=models,
        model_configs=model_configs,
        ensembling_method=ensembling_method,
        device=device,
        score_type=score_type
    )
    
    logger.info(
        f"Created ensemble with {len(models)} models using {method} method"
    )
    
    return ensemble
