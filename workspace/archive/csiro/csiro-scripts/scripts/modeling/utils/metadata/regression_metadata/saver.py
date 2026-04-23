# saver.py
# Save operations for regression metadata

import logging
from typing import Dict, List, Any, Optional, Tuple

from utils.system.io import load_json_file, save_json_file
from ..data_manipulation_loader import get_writable_metadata_dir
from ...results.variants import VARIANT_ID_FORMAT
from .cache import _load_cached_input_metadata, _load_cached_input_gridsearch
from .validator import ensure_correct_variant_id

logger = logging.getLogger(__name__)


def save_regression_variant_definition(
    regression_model_type: str,
    variant_index: int,
    variant_id: str,
    hyperparameters: Dict[str, Any]
) -> Tuple[int, str]:
    """
    Save regression model variant definition to metadata.json.
    
    Saves only hyperparameter definitions (variant_index, variant_id, hyperparameters).
    This is the static, reusable definition that can be tested on multiple feature files.
    
    For new variants, calculates sequential variant_index to ensure no gaps, regardless
    of the passed-in variant_index value.
    
    Args:
        regression_model_type: Type of regression model ('lgbm', 'xgboost', 'ridge')
        variant_index: Suggested variant index (may be overridden for sequential numbering)
        variant_id: Suggested variant identifier (may be updated to match calculated index)
        hyperparameters: Model-specific hyperparameters dictionary
    
    Returns:
        Tuple of (actual_variant_index, actual_variant_id) that were saved.
        These may differ from the passed-in values if sequential index was recalculated.
    
    Raises:
        FileNotFoundError: If csiro-metadata directory not found
        ValueError: If regression_model_type is invalid
    """
    # Validate regression model type
    valid_types = {'lgbm', 'xgboost', 'ridge'}
    if regression_model_type not in valid_types:
        raise ValueError(
            f"Invalid regression_model_type: {regression_model_type}. "
            f"Must be one of: {valid_types}"
        )
    
    # Get writable metadata directory (for writing)
    working_dir = get_writable_metadata_dir()
    
    # Path to regression model metadata file in working directory
    metadata_file = working_dir / regression_model_type / 'metadata.json'
    
    # Load existing metadata from both locations (input first, then working)
    # Use cached input metadata to avoid reloading on every iteration
    variants = _load_cached_input_metadata(regression_model_type)
    
    # Also check working directory and merge (working takes precedence for duplicates)
    if metadata_file.exists():
        working_variants = load_json_file(
            metadata_file, expected_type=list, file_type="Regression metadata JSON"
        )
        # Merge: add working variants, but skip if variant_id already exists from input
        existing_ids = {v.get('variant_id') for v in variants}
        for v in working_variants:
            if v.get('variant_id') not in existing_ids:
                variants.append(v)
        if working_variants:
            logger.info(f"Merged {len(working_variants)} variants from working metadata directory")
    
    # Create directory if it doesn't exist
    metadata_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Find variant in list
    for v in variants:
        if v.get('variant_id') == variant_id:
            # Check if old format (has cv_score or feature_filename)
            if 'cv_score' in v or 'feature_filename' in v:
                logger.warning(
                    f"Variant {variant_id} in old format detected. "
                    f"Migrating to new format (removing cv_score, fold_scores, feature_filename)..."
                )
                # Remove old fields
                v.pop('cv_score', None)
                v.pop('fold_scores', None)
                v.pop('feature_filename', None)
    
    # Check if variant already exists (by variant_id)
    existing_idx = None
    for idx, v in enumerate(variants):
        if v.get('variant_id') == variant_id:
            existing_idx = idx
            break
    
    if existing_idx is not None:
        # Update existing variant - use existing variant_index to maintain consistency
        existing_variant_index = variants[existing_idx].get('variant_index')
        if existing_variant_index != variant_index:
            logger.warning(
                f"Variant {variant_id} exists with different variant_index. "
                f"Preserving existing variant_index {existing_variant_index} (ignoring passed-in {variant_index})"
            )
            variant_index = existing_variant_index
            # Update variant_id to match the preserved variant_index
            variant_id = VARIANT_ID_FORMAT.format(index=variant_index)
        
        # Create variant entry with preserved variant_index
        variant_entry = {
            'variant_index': variant_index,
            'variant_id': variant_id,
            'hyperparameters': hyperparameters
        }
        logger.info(f"Updating existing variant {variant_id} in metadata")
        variants[existing_idx] = variant_entry
    else:
        # Add new variant - calculate sequential variant_index to ensure no gaps
        # Find max variant_index in existing variants
        max_index = -1
        for v in variants:
            v_index = v.get('variant_index')
            if v_index is not None and isinstance(v_index, int):
                max_index = max(max_index, v_index)
        
        # Use max_index + 1 for sequential numbering (ignore passed-in variant_index)
        sequential_index = max_index + 1
        if sequential_index != variant_index:
            logger.info(
                f"Calculating sequential variant_index for new variant: "
                f"max existing index={max_index}, using sequential index={sequential_index} "
                f"(ignoring passed-in variant_index={variant_index})"
            )
            variant_index = sequential_index
            # Update variant_id to match the calculated sequential variant_index
            variant_id = VARIANT_ID_FORMAT.format(index=variant_index)
        
        # Create variant entry with sequential variant_index
        variant_entry = {
            'variant_index': variant_index,
            'variant_id': variant_id,
            'hyperparameters': hyperparameters
        }
        variants.append(variant_entry)
        logger.info(f"Added new variant {variant_id} (variant_index={variant_index}) to metadata")
    
    # Save metadata file
    save_json_file(variants, metadata_file, file_type="Regression metadata JSON")
    logger.info(f"Saved regression variant definition to {metadata_file}")
    
    # Return the actual variant_index and variant_id used (may differ from passed-in values)
    return variant_index, variant_id


def save_regression_gridsearch_result(
    regression_model_type: str,
    variant_id: str,
    feature_filename: str,
    cv_score: float,
    fold_scores: List[float],
    hyperparameters: Dict[str, Any],
    model_index: Optional[int] = None,
    model_id: Optional[str] = None
) -> None:
    """
    Save regression grid search result to gridsearch_metadata.json.
    
    Saves training results linking variant_id to feature_filename with cv_score and fold_scores.
    Each entry represents a trained model (combination of variant + feature file) and has its own
    model_index and model_id for organization.
    
    CRITICAL: variant_id MUST match the variant in metadata.json with the same hyperparameters.
    This function validates that variant_id is correct by looking up hyperparameters in metadata.json.
    
    Args:
        regression_model_type: Type of regression model ('lgbm', 'xgboost', 'ridge')
        variant_id: Variant ID (e.g., "variant_0000") - will be validated against hyperparameters
        feature_filename: Feature filename used for training (e.g., 'variant_0100_features.npz')
        cv_score: Average cross-validation score
        fold_scores: List of scores for each fold
        hyperparameters: REQUIRED hyperparameters dictionary - used to validate/correct variant_id
        model_index: Optional model index (auto-generated if not provided)
        model_id: Optional model ID string like "000" (auto-generated if not provided)
    
    Raises:
        FileNotFoundError: If csiro-metadata directory not found
        ValueError: If regression_model_type is invalid, hyperparameters is missing, or variant_id doesn't match
    """
    # Validate regression model type
    valid_types = {'lgbm', 'xgboost', 'ridge'}
    if regression_model_type not in valid_types:
        raise ValueError(
            f"Invalid regression_model_type: {regression_model_type}. "
            f"Must be one of: {valid_types}"
        )
    
    # Validate hyperparameters is provided (REQUIRED)
    if hyperparameters is None:
        raise ValueError(
            "hyperparameters is REQUIRED when saving grid search results. "
            "variant_id must be validated against hyperparameters from metadata.json."
        )
    
    if not hyperparameters:
        raise ValueError(
            "hyperparameters cannot be empty. "
            "variant_id must be determined by looking up hyperparameters in metadata.json."
        )
    
    # CRITICAL: Always validate variant_id against hyperparameters
    # This ensures variant_id matches the variant in metadata.json with these hyperparameters
    logger.info(
        f"Validating variant_id {variant_id} against hyperparameters: {hyperparameters}"
    )
    try:
        variant_id = ensure_correct_variant_id(
            regression_model_type=regression_model_type,
            hyperparameters=hyperparameters,
            current_variant_id=variant_id
        )
        logger.info(f"Variant ID validated: {variant_id} matches hyperparameters in metadata.json")
    except ValueError as e:
        # Re-raise as-is (ensure_correct_variant_id already has detailed error messages)
        raise
    except Exception as e:
        # Unexpected error - wrap and re-raise
        raise RuntimeError(
            f"Failed to validate variant_id from metadata.json: {e}. "
            f"variant_id: {variant_id}, hyperparameters: {hyperparameters}"
        ) from e
    
    # Get writable metadata directory (for writing)
    metadata_dir = get_writable_metadata_dir()
    
    # Path to grid search metadata file
    gridsearch_file = metadata_dir / regression_model_type / 'gridsearch_metadata.json'
    
    # Load existing grid search results from both locations (input first, then working)
    # Use cached input gridsearch metadata to avoid reloading on every iteration
    results = _load_cached_input_gridsearch(regression_model_type)
    
    # Also check working directory and merge (working takes precedence for duplicates)
    if gridsearch_file.exists():
        working_results = load_json_file(
            gridsearch_file, expected_type=list, file_type="Regression gridsearch metadata JSON"
        )
        # Merge: add working results, but skip if variant_id+feature_filename already exists from input
        existing_keys = {(r.get('variant_id'), r.get('feature_filename')) for r in results}
        for r in working_results:
            key = (r.get('variant_id'), r.get('feature_filename'))
            if key not in existing_keys:
                results.append(r)
        if working_results:
            logger.info(f"Merged {len(working_results)} results from working gridsearch metadata")
    
    # Create directory if it doesn't exist
    gridsearch_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Check if result already exists (by variant_id + feature_filename)
    existing_idx = None
    for idx, r in enumerate(results):
        if (r.get('variant_id') == variant_id and 
            r.get('feature_filename') == feature_filename):
            existing_idx = idx
            break
    
    # Auto-generate model_index and model_id if not provided
    if model_index is None:
        if existing_idx is not None:
            # Use existing model_index
            model_index = results[existing_idx].get('model_index')
            if model_index is None:
                # Fallback: use highest existing index + 1
                existing_indices = [r.get('model_index', -1) for r in results if r.get('model_index') is not None]
                model_index = max(existing_indices) + 1 if existing_indices else 0
        else:
            # New entry: use highest existing index + 1
            existing_indices = [r.get('model_index', -1) for r in results if r.get('model_index') is not None]
            model_index = max(existing_indices) + 1 if existing_indices else 0
    
    if model_id is None:
        # Format model_id as 3-digit string (e.g., "000", "001", "002")
        model_id = f"{model_index:03d}"
    
    # Create result entry
    result_entry = {
        'model_index': model_index,
        'model_id': model_id,
        'variant_id': variant_id,
        'feature_filename': feature_filename,
        'cv_score': cv_score,
        'fold_scores': fold_scores
    }
    
    if existing_idx is not None:
        # Update existing result (preserve model_index and model_id if they match)
        existing_model_index = results[existing_idx].get('model_index')
        if existing_model_index is not None and existing_model_index != model_index:
            logger.warning(
                f"Updating result with different model_index: "
                f"existing={existing_model_index}, new={model_index}. "
                f"Using new model_index."
            )
        logger.info(
            f"Updating existing grid search result: model_id={model_id}, "
            f"{variant_id} on {feature_filename}"
        )
        results[existing_idx] = result_entry
    else:
        # Add new result
        results.append(result_entry)
        logger.info(
            f"Added new grid search result: model_id={model_id}, "
            f"{variant_id} on {feature_filename} (cv_score: {cv_score:.4f})"
        )
    
    # Save grid search metadata file
    save_json_file(results, gridsearch_file, file_type="Regression gridsearch metadata JSON")
    logger.info(f"Saved grid search result to {gridsearch_file}")


def save_regression_variant_to_metadata(
    regression_model_type: str,
    variant_index: int,
    variant_id: str,
    cv_score: float,
    fold_scores: List[float],
    hyperparameters: Dict[str, Any],
    feature_filename: str
) -> None:
    """
    Save regression model variant to metadata files (wrapper function).
    
    This function saves both:
    1. Hyperparameter definition to metadata.json
    2. Training result to gridsearch_metadata.json
    
    Maintains backward compatibility with existing code.
    
    Args:
        regression_model_type: Type of regression model ('lgbm', 'xgboost', 'ridge')
        variant_index: Sequential variant index (0, 1, 2, ...)
        variant_id: Unique variant identifier (e.g., "variant_0000")
        cv_score: Average cross-validation score
        fold_scores: List of scores for each fold
        hyperparameters: Model-specific hyperparameters dictionary
        feature_filename: Feature filename used for training (e.g., 'variant_0100_features.npz')
    
    Raises:
        FileNotFoundError: If csiro-metadata directory not found
        ValueError: If regression_model_type is invalid
    """
    # Save variant definition (hyperparameters only)
    # Note: Return values are ignored here as this is a wrapper function
    # The actual variant_index/variant_id used will be in metadata.json
    save_regression_variant_definition(
        regression_model_type=regression_model_type,
        variant_index=variant_index,
        variant_id=variant_id,
        hyperparameters=hyperparameters
    )
    
    # Save grid search result (cv_score, fold_scores, feature_filename)
    # Pass hyperparameters to ensure variant_id is correct
    save_regression_gridsearch_result(
        regression_model_type=regression_model_type,
        variant_id=variant_id,
        feature_filename=feature_filename,
        cv_score=cv_score,
        fold_scores=fold_scores,
        hyperparameters=hyperparameters
    )
