# finder.py
# Query and find operations for regression metadata

import logging
from typing import Dict, Any, Optional

from utils.system.io import load_json_file
from ..data_manipulation_loader import find_metadata_dir
from .loader import load_regression_gridsearch_results

logger = logging.getLogger(__name__)


def get_best_variant_for_feature(
    regression_model_type: str,
    feature_filename: str
) -> Optional[Dict[str, Any]]:
    """
    Get best variant for a specific feature file.
    
    Args:
        regression_model_type: Type of regression model ('lgbm', 'xgboost', 'ridge')
        feature_filename: Feature filename to find best variant for
        
    Returns:
        Dictionary with best result, or None if no results found
        
    Raises:
        FileNotFoundError: If metadata directory not found
        ValueError: If regression_model_type is invalid
    """
    results = load_regression_gridsearch_results(
        regression_model_type=regression_model_type,
        feature_filename=feature_filename
    )
    
    if not results:
        return None
    
    # Find result with highest cv_score
    best_result = max(results, key=lambda x: x.get('cv_score', -float('inf')))
    return best_result


def find_variant_by_hyperparameters(
    regression_model_type: str,
    hyperparameters: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Find existing variant with matching hyperparameters.
    
    Compares hyperparameters exactly, handling normalization for float/int comparisons.
    Returns the first matching variant found in metadata.json.
    
    Args:
        regression_model_type: Type of regression model ('lgbm', 'xgboost', 'ridge')
        hyperparameters: Hyperparameters dictionary to match
        
    Returns:
        Dictionary with 'variant_id' and 'variant_index' if found, None otherwise.
        
    Raises:
        FileNotFoundError: If metadata directory not found
        ValueError: If regression_model_type is invalid
    """
    # Validate regression model type
    valid_types = {'lgbm', 'xgboost', 'ridge'}
    if regression_model_type not in valid_types:
        raise ValueError(
            f"Invalid regression_model_type: {regression_model_type}. "
            f"Must be one of: {valid_types}"
        )
    
    # Find metadata directory (check both input and working)
    metadata_dir = find_metadata_dir()
    if metadata_dir is None:
        return None
    
    # Check both input and working directories
    input_metadata_file = None
    working_metadata_file = None
    
    if str(metadata_dir).startswith('/kaggle/input'):
        input_metadata_file = metadata_dir / regression_model_type / 'metadata.json'
        from config.path_constants import KAGGLE_WORKING
        working_metadata_file = KAGGLE_WORKING / 'csiro-metadata' / regression_model_type / 'metadata.json'
    else:
        working_metadata_file = metadata_dir / regression_model_type / 'metadata.json'
    
    # Load variants from both locations
    variants = []
    if input_metadata_file and input_metadata_file.exists():
        variants = load_json_file(
            input_metadata_file, expected_type=list, file_type="Regression metadata JSON"
        )
    
    if working_metadata_file and working_metadata_file.exists():
        working_variants = load_json_file(
            working_metadata_file, expected_type=list, file_type="Regression metadata JSON"
        )
        # Merge: add working variants, but skip if variant_id already exists
        existing_ids = {v.get('variant_id') for v in variants}
        for v in working_variants:
            if v.get('variant_id') not in existing_ids:
                variants.append(v)
    
    if not variants:
        return None
    
    # Normalize hyperparameters for comparison (convert int to float for numeric values)
    def normalize_value(v):
        """Normalize numeric values for comparison."""
        if isinstance(v, (int, float)):
            return float(v)
        return v
    
    def normalize_hyperparams(hp):
        """Normalize hyperparameters dictionary with sorted keys for consistent comparison."""
        if not hp:
            return {}
        # Sort keys to avoid dict ordering issues
        return {k: normalize_value(v) for k, v in sorted(hp.items())}
    
    normalized_target = normalize_hyperparams(hyperparameters)
    
    if not normalized_target:
        logger.warning("Empty hyperparameters provided for variant lookup")
        return None
    
    # Compare each variant's hyperparameters
    for variant in variants:
        variant_hp = variant.get('hyperparameters', {})
        if not variant_hp:
            continue
        
        normalized_variant_hp = normalize_hyperparams(variant_hp)
        
        # Check if all keys match and values match (using sorted dict comparison)
        if normalized_target == normalized_variant_hp:
            variant_id = variant.get('variant_id')
            variant_index = variant.get('variant_index')
            if variant_id and variant_index is not None:
                logger.info(
                    f"Found existing variant with matching hyperparameters: "
                    f"{variant_id} (variant_index: {variant_index})"
                )
                return {
                    'variant_id': variant_id,
                    'variant_index': variant_index
                }
    
    # Log when no match is found for debugging
    logger.debug(
        f"No matching variant found for hyperparameters: {hyperparameters}. "
        f"Searched {len(variants)} variants."
    )
    return None
