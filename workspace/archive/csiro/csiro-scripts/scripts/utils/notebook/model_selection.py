# model_selection.py
# Model selection utilities for regression ensemble and stacking
#
# Provides functions to resolve model paths from configuration,
# load top N models from grid search results, and validate model selections.

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

logger = logging.getLogger(__name__)


def load_gridsearch_metadata(
    regression_model_type: str,
    metadata_dir: Optional[Path] = None
) -> List[Dict[str, Any]]:
    """
    Load grid search metadata for a regression model type.
    
    Args:
        regression_model_type: Type of regression model ('lgbm', 'xgboost', 'ridge')
        metadata_dir: Optional metadata directory (auto-detected if None)
        
    Returns:
        List of variant result dictionaries from gridsearch_metadata.json
        
    Raises:
        FileNotFoundError: If metadata file not found
    """
    if metadata_dir is None:
        from modeling.utils.metadata.data_manipulation_loader import find_metadata_dir, get_writable_metadata_dir
        
        # Try input directory first, then working directory
        input_dir = find_metadata_dir()
        if input_dir and str(input_dir).startswith('/kaggle/input'):
            metadata_dir = input_dir / regression_model_type
            if not (metadata_dir / 'gridsearch_metadata.json').exists():
                # Fallback to working directory
                metadata_dir = get_writable_metadata_dir() / regression_model_type
        else:
            metadata_dir = get_writable_metadata_dir() / regression_model_type
    
    metadata_file = metadata_dir / 'gridsearch_metadata.json'
    
    if not metadata_file.exists():
        raise FileNotFoundError(
            f"Grid search metadata not found: {metadata_file}\n"
            f"Please run regression grid search (Cell 1c) first."
        )
    
    with open(metadata_file, 'r') as f:
        results = json.load(f)
    
    logger.info(f"Loaded {len(results)} results from {metadata_file}")
    return results


def get_top_n_variants(
    regression_model_type: str,
    top_n: int,
    metadata_dir: Optional[Path] = None
) -> List[Dict[str, Any]]:
    """
    Get top N variants from grid search results.
    
    Args:
        regression_model_type: Type of regression model
        top_n: Number of top variants to return
        metadata_dir: Optional metadata directory
        
    Returns:
        List of top N variant dictionaries, sorted by cv_score (descending)
    """
    results = load_gridsearch_metadata(regression_model_type, metadata_dir)
    
    # Filter successful results (with cv_score)
    valid_results = [
        r for r in results
        if r.get('cv_score') is not None
        and not (isinstance(r.get('cv_score'), float) and (r['cv_score'] != r['cv_score']))  # Not NaN
    ]
    
    if not valid_results:
        raise ValueError(f"No valid results found for {regression_model_type}")
    
    # Sort by cv_score (descending)
    sorted_results = sorted(
        valid_results,
        key=lambda x: x.get('cv_score', -float('inf')),
        reverse=True
    )
    
    top_results = sorted_results[:top_n]
    
    logger.info(
        f"Selected top {len(top_results)} {regression_model_type} variants "
        f"(from {len(valid_results)} valid)"
    )
    
    return top_results


def get_variant_id_from_index(
    regression_model_type: str,
    variant_index: int,
    metadata_dir: Optional[Path] = None
) -> str:
    """
    Get variant_id from variant_index (looks up directly from metadata.json).
    
    .. deprecated:: 
        This function is deprecated. Use `get_variant_info_from_model_id()` instead,
        which correctly looks up models by model_id from gridsearch_metadata.json.
        The model_index from gridsearch_metadata.json does NOT match variant_index
        from metadata.json, causing incorrect model selection.
    
    This function looks up variant_id by variant_index from metadata.json,
    similar to how REGRESSION_MODEL_VARIANT_ID works with variant_id strings.
    The variant_index is NOT a rank - it's the actual variant_index value from metadata.json.
    
    Args:
        regression_model_type: Type of regression model ('lgbm', 'xgboost', 'ridge')
        variant_index: Variant index value from metadata.json (e.g., 79, 82, 85)
        metadata_dir: Optional metadata directory (auto-detected if None)
        
    Returns:
        variant_id string (e.g., 'variant_0079')
        
    Raises:
        ValueError: If variant_index not found in metadata.json
        FileNotFoundError: If metadata file not found
    """
    if metadata_dir is None:
        from modeling.utils.metadata.data_manipulation_loader import find_metadata_dir, get_writable_metadata_dir
        
        # Try input directory first, then working directory
        input_dir = find_metadata_dir()
        if input_dir and str(input_dir).startswith('/kaggle/input'):
            metadata_dir = input_dir / regression_model_type
            if not (metadata_dir / 'metadata.json').exists():
                # Fallback to working directory
                metadata_dir = get_writable_metadata_dir() / regression_model_type
        else:
            metadata_dir = get_writable_metadata_dir() / regression_model_type
    
    metadata_file = metadata_dir / 'metadata.json'
    
    if not metadata_file.exists():
        raise FileNotFoundError(
            f"Regression metadata file not found: {metadata_file}\n"
            f"Please ensure metadata.json exists for {regression_model_type}."
        )
    
    # Load metadata.json
    with open(metadata_file, 'r') as f:
        variants = json.load(f)
    
    # Find variant by variant_index
    variant = None
    for v in variants:
        if v.get('variant_index') == variant_index:
            variant = v
            break
    
    if variant is None:
        available_indices = [v.get('variant_index') for v in variants if v.get('variant_index') is not None]
        raise ValueError(
            f"Variant index {variant_index} not found in metadata.json for {regression_model_type}.\n"
            f"  Checked file: {metadata_file}\n"
            f"  Available variant indices: {sorted(set(available_indices))[:20]}..."  # Show first 20
        )
    
    variant_id = variant.get('variant_id')
    if not variant_id:
        raise ValueError(
            f"Variant at index {variant_index} has no variant_id in metadata.json. "
            f"This may indicate corrupted metadata."
        )
    
    logger.info(
        f"Looked up variant_index {variant_index} → variant_id {variant_id} "
        f"from {metadata_file}"
    )
    
    return variant_id


def get_variant_info_from_model_id(
    regression_model_type: str,
    model_id: str,
    metadata_dir: Optional[Path] = None
) -> Tuple[str, str, Optional[float]]:
    """
    Get variant_id, feature_filename, and cv_score from model_id.
    
    Looks up model_id in gridsearch_metadata.json to get the complete model information.
    This is the correct way to identify models for training, as model_id uniquely
    identifies a trained model configuration with its variant_id and feature_filename.
    
    Args:
        regression_model_type: Type of regression model ('lgbm', 'xgboost', 'ridge')
        model_id: Model ID string from gridsearch_metadata.json (e.g., "080", "083")
        metadata_dir: Optional metadata directory (auto-detected if None)
        
    Returns:
        Tuple of (variant_id, feature_filename, cv_score)
        - variant_id: Variant ID string (e.g., 'variant_0079')
        - feature_filename: Feature filename (e.g., 'variant_0163_features.npz')
        - cv_score: CV score (float or None)
        
    Raises:
        ValueError: If model_id not found in gridsearch_metadata.json
        FileNotFoundError: If metadata file not found
    """
    results = load_gridsearch_metadata(regression_model_type, metadata_dir)
    
    # Find model by model_id
    model_info = None
    for r in results:
        if r.get('model_id') == model_id:
            model_info = r
            break
    
    if model_info is None:
        available_ids = [r.get('model_id') for r in results if r.get('model_id')]
        raise ValueError(
            f"Model ID '{model_id}' not found in gridsearch_metadata.json for {regression_model_type}.\n"
            f"  Available model IDs (first 20): {sorted(set(available_ids))[:20]}..."
        )
    
    variant_id = model_info.get('variant_id')
    feature_filename = model_info.get('feature_filename')
    cv_score = model_info.get('cv_score')
    
    if not variant_id:
        raise ValueError(
            f"Model ID '{model_id}' has no variant_id in gridsearch_metadata.json. "
            f"This may indicate corrupted metadata."
        )
    
    if not feature_filename:
        raise ValueError(
            f"Model ID '{model_id}' has no feature_filename in gridsearch_metadata.json. "
            f"This may indicate corrupted metadata."
        )
    
    logger.info(
        f"Looked up model_id '{model_id}' → variant_id {variant_id}, "
        f"feature_filename {feature_filename}, cv_score={cv_score}"
    )
    
    return variant_id, feature_filename, cv_score


def resolve_model_paths_from_config(
    ensemble_config: Dict[str, Any],
    base_model_dir: Optional[str] = None,
    auto_detect: bool = False
) -> Tuple[List[str], List[float], List[str]]:
    """
    Resolve model paths from ensemble configuration.
    
    Models are already trained and uploaded to Kaggle, so we reference them by their
    version number in the path structure (/kaggle/input/csiro-models/scikitlearn/{type}/{version}/),
    not by their rank/index in grid search metadata.
    
    Args:
        ensemble_config: Configuration dict with 'model_types' and 'model_versions'
        base_model_dir: Base directory for models (default: '/kaggle/input/csiro-models/')
        auto_detect: If True, auto-detect top models from grid search
        
    Returns:
        Tuple of (model_paths, cv_scores, model_types) lists
        
    Raises:
        ValueError: If configuration is invalid or models not found
    """
    if base_model_dir is None:
        base_model_dir = '/kaggle/input/csiro-models/'
    
    model_types = ensemble_config.get('model_types', [])
    model_versions = ensemble_config.get('model_versions', {})
    
    if not model_types:
        raise ValueError("model_types cannot be empty in ensemble_config")
    
    model_paths = []
    cv_scores = []
    resolved_model_types = []
    
    if auto_detect:
        # Auto-detect from grid search metadata
        logger.info("Auto-detecting top models from grid search metadata...")
        for model_type in model_types:
            if model_type not in model_versions:
                logger.warning(f"No versions specified for {model_type}, skipping")
                continue
            
            versions = model_versions[model_type]
            if not versions:
                logger.warning(f"Empty versions list for {model_type}, skipping")
                continue
            
            # Get top variants from grid search
            top_variants = get_top_n_variants(model_type, max(versions))
            
            # Select variants by 1-indexed rank
            for idx in versions:
                if idx < 1 or idx > len(top_variants):
                    logger.warning(
                        f"Index {idx} out of range for {model_type} "
                        f"(have {len(top_variants)} variants), skipping"
                    )
                    continue
                
                variant = top_variants[idx - 1]  # Convert to 0-indexed
                variant_id = variant.get('variant_id')
                
                if not variant_id:
                    logger.warning(f"Variant at index {idx} has no variant_id, skipping")
                    continue
                
                # Try to find model path (may not exist if not uploaded)
                model_path = Path(base_model_dir) / 'scikitlearn' / model_type / variant_id
                model_file = model_path / 'regression_model.pkl'
                
                if not model_file.exists():
                    logger.warning(f"Model not found: {model_file}, skipping")
                    continue
                
                cv_score = variant.get('cv_score')
                model_paths.append(str(model_path))
                cv_scores.append(cv_score)
                resolved_model_types.append(model_type)
                
                # Format CV score for logging
                cv_score_str = f"{cv_score:.6f}" if cv_score is not None else 'N/A'
                logger.info(
                    f"Auto-detected {model_type} variant {idx}: {variant_id} "
                    f"(cv_score={cv_score_str})"
                )
    else:
        # New behavior: use explicit model versions from uploaded models
        logger.info("Using explicit configuration (uploaded models by version)...")
        
        for model_type in model_types:
            if model_type not in model_versions:
                logger.warning(f"No versions specified for {model_type}, skipping")
                continue
            
            versions = model_versions[model_type]
            if not versions:
                logger.warning(f"Empty versions list for {model_type}, skipping")
                continue
            
            logger.info(f"  {model_type}: model versions {versions} from /kaggle/input/csiro-models/scikitlearn/{model_type}/")
            
            # Resolve each version from uploaded model path
            for version in versions:
                # Path to uploaded model: /kaggle/input/csiro-models/scikitlearn/{type}/{version}/
                model_path = Path(base_model_dir) / 'scikitlearn' / model_type / str(version)
                model_file = model_path / 'regression_model.pkl'
                metadata_file = model_path / 'model_metadata.json'
                
                # Validate model exists (uploaded models should be in input directory)
                if not model_file.exists():
                    raise FileNotFoundError(
                        f"Uploaded model not found: {model_path}\n"
                        f"Expected path: /kaggle/input/csiro-models/scikitlearn/{model_type}/{version}/\n"
                        f"Please ensure model version {version} has been uploaded."
                    )
                
                if not metadata_file.exists():
                    logger.warning(f"Metadata file not found: {metadata_file}, using default CV score")
                    cv_score = None
                else:
                    # Load CV score from metadata (saved when model was exported)
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                    cv_score = metadata.get('cv_score')
                
                model_paths.append(str(model_path))
                cv_scores.append(cv_score)
                resolved_model_types.append(model_type)
                
                # Format CV score for logging
                cv_score_str = f"{cv_score:.6f}" if cv_score is not None else 'N/A'
                logger.info(
                    f"  Resolved {model_type} version {version}: {model_path} "
                    f"(cv_score={cv_score_str})"
                )
    
    if not model_paths:
        raise ValueError(
            "No valid model paths resolved from configuration. "
            "Please check model_types and model_versions."
        )
    
    logger.info(f"Resolved {len(model_paths)} model paths for ensemble")
    return model_paths, cv_scores, resolved_model_types


def validate_model_paths(
    model_paths: List[str],
    require_same_feature_model: bool = True
) -> None:
    """
    Validate that all model paths exist and are consistent.
    
    Args:
        model_paths: List of model directory paths
        require_same_feature_model: If True, verify all models use same feature extraction model
        
    Raises:
        FileNotFoundError: If any model file not found
        ValueError: If models are inconsistent
    """
    feature_models = []
    
    for model_path in model_paths:
        model_path_obj = Path(model_path)
        
        # Check for regression model file
        model_file = model_path_obj / 'regression_model.pkl'
        if not model_file.exists():
            if model_path_obj.suffix == '.pkl' and model_path_obj.exists():
                model_file = model_path_obj
                model_path_obj = model_file.parent
            else:
                raise FileNotFoundError(f"Regression model not found: {model_path}")
        
        # Check for metadata file
        metadata_file = model_path_obj / 'model_metadata.json'
        if not metadata_file.exists():
            logger.warning(f"Metadata file not found: {metadata_file}")
            continue
        
        # Load metadata to check feature extraction model
        if require_same_feature_model:
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            
            feature_filename = metadata.get('feature_filename')
            if feature_filename:
                feature_models.append(feature_filename)
    
    # Verify all use same feature extraction model
    if require_same_feature_model and feature_models:
        unique_features = set(feature_models)
        if len(unique_features) > 1:
            raise ValueError(
                f"Models use different feature extraction variants: {unique_features}\n"
                f"All models in ensemble must use the same feature extraction setup."
            )
    
    logger.info(f"Validated {len(model_paths)} model paths")
