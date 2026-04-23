# export_scenario_handlers.py
# Scenario handlers for different export sources
#
# This module contains handlers for determining the source model and metadata
# for different export scenarios. These handlers are used by export_model.py
# orchestrator to prepare data before delegating to export utilities.

import logging
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

from config.config import Config
from ..results.best_variant import get_best_variant_info
from ..finding import (
    LightweightSubmissionModelFinder,
    GridSearchModelFinder
)
from .metadata_builder import MetadataBuilder
from modeling.training.utils import find_trained_model_path
from config.model_constants import get_model_name_from_pretrained

logger = logging.getLogger(__name__)


def handle_just_trained_model(
    model_dir: str,
    config: Config,
    variant_id: Optional[str] = None,
    variant_info: Optional[Dict[str, Any]] = None
) -> Tuple[Path, Dict[str, Any]]:
    """
    Handle export from just-trained model directory.
    
    Args:
        model_dir: Path to just-trained model directory
        config: Configuration object
        variant_id: Optional variant ID
        variant_info: Optional variant info dictionary from training
        
    Returns:
        Tuple of (model_path, metadata_dict)
        
    Raises:
        FileNotFoundError: If model directory not found
    """
    from modeling.training.utils.checkpoint_scores import extract_scores_from_checkpoint
    from .metadata_builder import prepare_regression_model_metadata_dict
    
    model_dir_path = Path(model_dir)
    if not model_dir_path.exists():
        raise FileNotFoundError(f"Model directory not found: {model_dir_path}")
    
    # Find model checkpoint
    model_path, best_fold = find_trained_model_path(model_dir_path)
    
    # Check if this is a regression model (.pkl file)
    if model_path.suffix == '.pkl':
        # Regression model: use regression-specific metadata
        if not config.model.regression_model_type:
            raise ValueError(
                "regression_model_type must be set in config for regression model export"
            )
        
        # Extract scores from checkpoint
        cv_score, fold_scores, extracted_best_fold = extract_scores_from_checkpoint(model_path)
        
        # Use best_fold from find_trained_model_path (more reliable)
        best_fold_used = best_fold if best_fold is not None else extracted_best_fold
        best_fold_score = fold_scores[best_fold_used] if best_fold_used < len(fold_scores) else cv_score
        
        # Extract feature_filename from variant_info or try to construct from config
        feature_filename = None
        if variant_info:
            feature_filename = variant_info.get('feature_filename')
        
        # If not in variant_info, try to construct from config
        if not feature_filename and config.model.feature_extraction_mode:
            try:
                from config.model_constants import get_model_id, get_model_name_from_pretrained
                from modeling.feature_extraction import generate_feature_filename
                from ..metadata.data_manipulation_loader import find_metadata_dir, find_combo_id
                
                # Get feature extraction model name
                feature_extraction_model_name = config.model.feature_extraction_model_name
                if feature_extraction_model_name and ('/' in feature_extraction_model_name or feature_extraction_model_name.startswith('/')):
                    # Convert path to model name
                    resolved_name = get_model_name_from_pretrained(feature_extraction_model_name)
                    if resolved_name:
                        feature_extraction_model_name = resolved_name
                
                # Get combo_id from preprocessing/augmentation
                preprocessing_list = config.data.preprocessing_list or []
                augmentation_list = config.data.augmentation_list or []
                
                metadata_dir = find_metadata_dir()
                if metadata_dir:
                    combo_id = find_combo_id(preprocessing_list, augmentation_list, metadata_dir)
                    if combo_id:
                        model_id = get_model_id(feature_extraction_model_name)
                        feature_filename = generate_feature_filename(model_id, combo_id)
                        logger.info(f"Constructed feature_filename from config: {feature_filename}")
            except Exception as e:
                logger.warning(f"Could not construct feature_filename from config: {e}")
        
        if not feature_filename:
            raise ValueError(
                "feature_filename is required for regression model export. "
                "Provide it in variant_info or ensure config has feature_extraction_model_name and data manipulation settings."
            )
        
        # Extract hyperparameters from variant_info or use defaults
        hyperparameters = {}
        if variant_info:
            hyperparameters = variant_info.get('hyperparameters', {})
        
        # Get variant_id and variant_index
        variant_id_used = variant_id or (variant_info.get('variant_id') if variant_info else None)
        variant_index_used = variant_info.get('variant_index') if variant_info else 0
        
        # Validate required fields
        if not variant_id_used:
            raise ValueError("variant_id is required for regression model export. Provide it in variant_info or as parameter.")
        if not feature_filename:
            raise ValueError("feature_filename is required for regression model export. Provide it in variant_info or ensure config has feature_extraction_model_name and data manipulation settings.")
        
        # Build regression-specific metadata (does NOT include preprocessing_list/augmentation_list or dataset_type)
        metadata = prepare_regression_model_metadata_dict(
            regression_model_type=config.model.regression_model_type,
            cv_score=cv_score,
            fold_scores=fold_scores,
            hyperparameters=hyperparameters,
            feature_filename=feature_filename,
            variant_id=variant_id_used,
            variant_index=variant_index_used,
            best_fold=best_fold_used,
            best_fold_score=best_fold_score
        )
        
        logger.info(f"Built regression model metadata: regression_model_type={config.model.regression_model_type}, feature_filename={feature_filename}")
        
    else:
        # Regular PyTorch model: use standard MetadataBuilder
        builder = MetadataBuilder(model_name=config.model.name)
        
        # If we have variant_info (from training with a specific variant), use it for complete metadata
        if variant_info:
            metadata = builder.from_variant_info(variant_info)
            # Ensure best_fold from training is used (may differ from variant_info if training found better fold)
            if metadata:
                metadata['best_fold'] = best_fold
        else:
            # Fallback to extracting from checkpoint
            metadata = builder.from_checkpoint(model_path, config)
            if metadata:
                metadata['best_fold'] = best_fold
                # Add variant_id if provided (even if not in checkpoint)
                if variant_id:
                    metadata['variant_id'] = variant_id
    
    return model_path, metadata


def handle_best_variant_file(
    best_variant_file: str,
    config: Config,
    export_path: Path
) -> Tuple[Path, Dict[str, Any]]:
    """
    Handle export from grid search best variant file.
    
    Loads best variant from JSON file, extracts variant information, and exports
    using modern export utilities.
    
    Args:
        best_variant_file: Path to best_dataset_variant.json
        config: Configuration object
        export_path: Export directory
        
    Returns:
        Tuple of (model_path, metadata_dict)
        
    Raises:
        RuntimeError: If export fails
        FileNotFoundError: If best variant file doesn't exist
    """
    from utils.system.io import load_json_file
    from ...training.training_results_utils import find_best_fold_from_scores
    from ..metadata.data_manipulation_loader import (
        find_metadata_dir,
        extract_preprocessing_augmentation_from_variant
    )
    from .operations import export_from_grid_search
    
    best_variant_path = Path(best_variant_file)
    
    if not best_variant_path.exists():
        raise FileNotFoundError(f"Best variant file not found: {best_variant_path}")
    
    # Load best variant JSON file (has nested 'best_variant' structure)
    best_data = load_json_file(best_variant_path, expected_type=dict, file_type="Best variant JSON")
    best_variant = best_data.get('best_variant', {})
    
    variant_id = best_variant.get('variant_id', '')
    fold_scores = best_variant.get('fold_scores', [])
    
    if not variant_id or not fold_scores:
        raise RuntimeError("Best variant data incomplete. Check grid search results.")
    
    # Find best fold from fold scores
    best_fold, best_fold_score = find_best_fold_from_scores(fold_scores)
    
    # Extract preprocessing/augmentation from variant
    preprocessing_list = []
    augmentation_list = []
    try:
        metadata_dir = find_metadata_dir()
        if metadata_dir:
            preprocessing_list, augmentation_list = extract_preprocessing_augmentation_from_variant(
                best_variant, metadata_dir
            )
        else:
            logger.warning("Metadata directory not found, cannot resolve combo_id for best variant")
    except (ValueError, FileNotFoundError) as e:
        logger.warning(f"Failed to resolve data_manipulation for best variant: {e}")
    
    # Build metadata using MetadataBuilder
    builder = MetadataBuilder(model_name=config.model.name)
    variant_info = {
        'variant_id': variant_id,
        'best_fold': best_fold,
        'best_fold_score': best_fold_score,
        'preprocessing_list': preprocessing_list,
        'augmentation_list': augmentation_list,
        'cv_score': best_data.get('best_score'),
        'fold_scores': fold_scores,
        'dataset_type': best_variant.get('dataset_type', 'full')
    }
    metadata = builder.from_variant_info(variant_info)
    
    # Export using modern export function
    export_from_grid_search(
        variant_id=variant_id,
        best_fold=best_fold,
        export_dir=export_path,
        metadata=metadata,
        config=config
    )
    
    # Validate metadata matches source
    source_cv_score = best_data.get('best_score')
    exported_cv_score = metadata.get('cv_score')
    if source_cv_score is not None and exported_cv_score is not None:
        if abs(source_cv_score - exported_cv_score) > 1e-6:
            error_msg = (
                f"❌ VALIDATION FAILED: Exported cv_score ({exported_cv_score:.6f}) "
                f"does not match source cv_score ({source_cv_score:.6f}) from best_dataset_variant.json\n"
                f"This indicates the wrong model may have been exported!"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        else:
            logger.info(f"✅ Validation passed: cv_score matches ({exported_cv_score:.6f})")
    
    return export_path / 'best_model.pth', metadata


def handle_results_file(
    results_file: str,
    variant_id: Optional[str],
    config: Config
) -> Tuple[Path, Dict[str, Any]]:
    """
    Handle export from grid search results file.
    
    Args:
        results_file: Path to results.json file
        variant_id: Optional variant ID (if None, uses best variant)
        config: Configuration object
        
    Returns:
        Tuple of (model_path, metadata_dict)
        
    Raises:
        FileNotFoundError: If results file or model not found
    """
    results_path = Path(results_file)
    if not results_path.exists():
        raise FileNotFoundError(f"Results file not found: {results_path}")
    
    # Get variant info
    variant_info = get_best_variant_info(results_path, variant_id=variant_id)
    variant = variant_info['variant']
    variant_id_used = variant_info['variant_id']
    best_fold = variant_info.get('best_fold')
    
    if best_fold is None:
        from ..results.best_variant import get_variant_best_fold
        best_fold, _ = get_variant_best_fold(variant)
    
    # Find model using centralized finder
    model_path = find_model_for_export(variant_id_used, best_fold, config)
    
    # Build metadata using MetadataBuilder
    builder = MetadataBuilder(model_name=config.model.name)
    metadata = builder.from_variant_info({
        **variant_info,
        'best_fold': best_fold
    })
    
    return model_path, metadata


def handle_auto_detect(config: Config) -> Tuple[Path, Dict[str, Any]]:
    """
    Handle auto-detect from CSIRO models or working directory.
    
    Args:
        config: Configuration object
        
    Returns:
        Tuple of (model_path, metadata_dict)
        
    Raises:
        FileNotFoundError: If no model found
    """
    # Try to find model in CSIRO models location first
    model_name = get_model_name_from_pretrained(config.model.name)
    if model_name is None:
        if '/' in config.model.name:
            parts = config.model.name.split('/')
            model_name = 'dinov2_base' if 'dinov2' in parts else (parts[-1] if parts else None)
        else:
            model_name = config.model.name
    
    finder = LightweightSubmissionModelFinder()
    existing_model_path, existing_metadata_path = finder.find_model(
        model_path=None,
        config=config,
        model_name=model_name or 'unknown'
    )
    
    if not existing_model_path or not existing_model_path.exists():
        raise FileNotFoundError(
            "No model found in CSIRO models location or working directory. "
            "Please provide explicit source (model_dir, results_file, or best_variant_file)."
        )
    
    # Build metadata using MetadataBuilder
    builder = MetadataBuilder(model_name=config.model.name)
    metadata = builder.build(
        metadata_file=existing_metadata_path,
        checkpoint_path=existing_model_path,
        config=config
    )
    
    return existing_model_path, metadata


def find_model_for_export(
    variant_id: str,
    best_fold: int,
    config: Config
) -> Path:
    """
    Find model checkpoint for export, checking multiple locations.
    
    Checks in order:
    1. CSIRO models location (/kaggle/input/csiro-models/pytorch/{model_name}/*/)
    2. Working directory (grid search structure)
    
    Args:
        variant_id: Variant ID (e.g., "combo_0000")
        best_fold: Best fold number
        config: Configuration object
        
    Returns:
        Path to model checkpoint
        
    Raises:
        FileNotFoundError: If model not found in any location
    """
    # 1. Check CSIRO models location (input datasets) - uploaded models
    try:
        model_name = get_model_name_from_pretrained(config.model.name)
        if model_name is None:
            if '/' in config.model.name:
                parts = config.model.name.split('/')
                model_name = 'dinov2_base' if 'dinov2' in parts else (parts[-1] if parts else None)
            else:
                model_name = config.model.name
        
        if model_name:
            logger.info(f"🔍 Checking CSIRO models location (/kaggle/input/csiro-models/pytorch/{model_name}/)...")
            finder = LightweightSubmissionModelFinder()
            csiro_model_path, _ = finder.find_model(
                model_path=None,
                config=config,
                model_name=model_name
            )
            if csiro_model_path and csiro_model_path.exists():
                logger.info(f"✅ Found model in CSIRO models location: {csiro_model_path}")
                return csiro_model_path
    except Exception as e:
        logger.debug(f"CSIRO models location check failed: {e}")
    
    # 2. Check working directory (grid search structure)
    try:
        logger.info(f"🔍 Checking working directory for {variant_id}, fold {best_fold}...")
        finder = GridSearchModelFinder()
        model_path = finder.find_model(
            variant_id=variant_id,
            best_fold=best_fold,
            config=config
        )
        logger.info(f"✅ Found model in working directory: {model_path}")
        return model_path
    except FileNotFoundError as e:
        logger.debug(f"Working directory check failed: {e}")
    
    # Model not found in any location
    model_name = get_model_name_from_pretrained(config.model.name) or 'unknown'
    raise FileNotFoundError(
        f"❌ Model not found for variant {variant_id}, fold {best_fold}\n\n"
        f"Checked:\n"
        f"  1. CSIRO models location: /kaggle/input/csiro-models/pytorch/{model_name}/*/best_model.pth\n"
        f"  2. Working directory: /kaggle/working/models/hyperparameter_grid_search/{variant_id}/fold_{best_fold}/best_model.pth\n"
        f"  3. Working directory: /kaggle/working/models/dataset_grid_search/{variant_id}/fold_{best_fold}/best_model.pth\n\n"
        f"Options:\n"
        f"  - Upload the trained model to a Kaggle dataset at /kaggle/input/csiro-models/pytorch/{model_name}/1/\n"
        f"  - Run the hyperparameter grid search to train the model in the working directory\n"
    )

