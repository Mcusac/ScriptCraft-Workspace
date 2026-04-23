# model_loader.py
# Multi-model loading for ensemble inference
#
# This module provides higher-level orchestration for loading multiple models for ensemble inference.
# It builds on top of lower-level utilities:
# - model_finder_utils: Finds model checkpoint paths (uses strategy pattern internally)
# - checkpoint: Loads model weights from checkpoints
# - best_variant_utils: Extracts variant information from results
#
# Architecture:
# - find_model_path_for_variant: Finds model path for a single variant (uses model_finder_utils)
# - load_ensemble_models: Orchestrates loading multiple models with validation
# - ModelConfig: Configuration class for ensemble model metadata
#
# Responsibility boundaries:
# - This module: Multi-model orchestration, ensemble-specific validation, model creation
# - model_finder_utils: Finding model paths in various locations (strategy pattern)
# - checkpoint: Loading model weights from checkpoint files
# - metadata_loader_utils: Loading model metadata (preprocessing, augmentation, etc.)

import logging
import torch
from pathlib import Path
from typing import Any, Dict, List, Optional

from modeling.models import create_model
from modeling.training.utils.checkpoint import load_model_from_checkpoint
from modeling.utils import get_variant_best_fold
from modeling.utils.finding import GridSearchModelFinder
from config.config import Config

logger = logging.getLogger(__name__)


def find_model_path_for_variant(
    variant_info: Dict[str, Any],
    config: Config
) -> Path:
    """
    Find model checkpoint path for a variant.
    
    This is a higher-level orchestrator that:
    1. Extracts variant_id and best_fold from variant_info
    2. Delegates to GridSearchModelFinder
       (which uses strategy pattern internally to search multiple locations)
    
    Args:
        variant_info: Dictionary with variant information, including:
                     - 'variant_id': Variant ID string
                     - 'best_fold': Best fold index (optional, will compute if missing)
                     - 'variant': Full variant dictionary (required if best_fold missing)
        config: Configuration object with paths
        
    Returns:
        Path to model checkpoint
        
    Raises:
        FileNotFoundError: If model checkpoint cannot be found
        ValueError: If variant_info is missing required fields
    """
    variant_id = variant_info.get('variant_id')
    if not variant_id:
        raise ValueError("variant_info must contain 'variant_id'")
    
    # Get best fold if not provided
    best_fold = variant_info.get('best_fold')
    if best_fold is None:
        variant = variant_info.get('variant')
        if not variant:
            raise ValueError("variant_info must contain either 'best_fold' or 'variant'")
        best_fold, _ = get_variant_best_fold(variant)
        logger.info(f"Computed best_fold={best_fold} for variant {variant_id}")
    
    # Use existing utility to find model
    finder = GridSearchModelFinder()
    model_path = finder.find_model(
        variant_id=variant_id,
        best_fold=best_fold,
        config=config
    )
    
    return model_path


class ModelConfig:
    """
    Configuration for a single model in the ensemble.
    
    Stores variant information and model path for loading.
    """
    
    def __init__(
        self,
        variant_info: Dict[str, Any],
        model_path: Path,
        model_name: str,
        submission_score: Optional[float] = None
    ):
        """
        Initialize model configuration.
        
        Args:
            variant_info: Dictionary with variant information
            model_path: Path to model checkpoint
            model_name: Name of model architecture (must match across all models)
            submission_score: Optional submission score for this model
        """
        self.variant_info = variant_info
        self.model_path = model_path
        self.model_name = model_name
        self.variant_id = variant_info.get('variant_id')
        self.cv_score = variant_info.get('cv_score')
        self.submission_score = submission_score
        self.preprocessing_list = variant_info.get('preprocessing_list', [])
        self.augmentation_list = variant_info.get('augmentation_list', [])
        self.dataset_type = variant_info.get('dataset_type', 'full')


def load_ensemble_models(
    model_configs: List[ModelConfig],
    config: Config,
    device: torch.device
) -> List[torch.nn.Module]:
    """
    Load multiple models from variant info for ensemble inference.
    
    This is a higher-level orchestrator that:
    1. Validates all models have the same architecture
    2. Creates model instances using modeling.models.create_model
    3. Loads weights using checkpoint.load_model_from_checkpoint
    4. Manages memory by loading models sequentially
    
    Models are loaded sequentially to manage memory. All models must have
    the same architecture (validated).
    
    Responsibility: This function orchestrates the ensemble loading process.
    It delegates to:
    - modeling.models.create_model: Model architecture creation
    - checkpoint.load_model_from_checkpoint: Weight loading from checkpoints
    
    Args:
        model_configs: List of ModelConfig objects, one per model
        config: Configuration object (model.name will be validated against model_configs)
        device: Device to load models on
        
    Returns:
        List of loaded models, ready for inference (in eval mode)
        
    Raises:
        ValueError: If models have different architectures or configs are invalid
        FileNotFoundError: If any model checkpoint cannot be found
        RuntimeError: If model loading fails
    """
    if not model_configs:
        raise ValueError("model_configs cannot be empty")
    
    # Validate all models have same architecture
    model_names = [mc.model_name for mc in model_configs]
    unique_names = set(model_names)
    if len(unique_names) > 1:
        raise ValueError(
            f"All models in ensemble must have same architecture. "
            f"Found: {unique_names}"
        )
    
    model_name = model_names[0]
    
    # Validate config matches
    if config.model.name != model_name:
        logger.warning(
            f"Config model name ({config.model.name}) doesn't match ensemble models ({model_name}). "
            f"Using ensemble model name."
        )
        config.model.name = model_name
    
    models = []
    
    logger.info(f"Loading {len(model_configs)} models for ensemble...")
    
    for idx, model_config in enumerate(model_configs, 1):
        logger.info(
            f"Loading model {idx}/{len(model_configs)}: "
            f"{model_config.variant_id} (cv_score={model_config.cv_score:.4f})"
        )
        
        # Create model instance (pretrained=False since we load from checkpoint)
        original_pretrained = config.model.pretrained
        try:
            config.model.pretrained = False
            model = create_model(config)
        finally:
            config.model.pretrained = original_pretrained
        
        model.to(device)
        model.eval()
        
        # Load checkpoint
        try:
            checkpoint_meta = load_model_from_checkpoint(
                model=model,
                path=model_config.model_path,
                device=device
            )
            logger.info(
                f"  Loaded from {model_config.model_path}\n"
                f"  Best score: {checkpoint_meta['best_score']:.4f}\n"
                f"  Epochs: {checkpoint_meta['completed_epochs']}"
            )
        except Exception as e:
            raise RuntimeError(
                f"Failed to load model {model_config.variant_id} from {model_config.model_path}: {e}"
            )
        
        models.append(model)
    
    logger.info(f"Successfully loaded {len(models)} models for ensemble")
    
    return models

