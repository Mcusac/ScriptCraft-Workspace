# validator.py
# Validation utilities for regression metadata

import logging
from typing import Dict, Any, Optional

from .finder import find_variant_by_hyperparameters

logger = logging.getLogger(__name__)


def ensure_correct_variant_id(
    regression_model_type: str,
    hyperparameters: Dict[str, Any],
    current_variant_id: Optional[str] = None
) -> str:
    """
    Ensure variant_id matches the hyperparameters in metadata.json.
    
    Looks up the correct variant_id from metadata.json based on hyperparameters.
    This function MUST be used to determine variant_id - it looks up by hyperparameters,
    NOT by model_index or any sequential logic.
    
    If a matching variant is found, returns its variant_id. If a mismatch is detected
    (current_variant_id doesn't match the found variant), raises ValueError.
    If not found and current_variant_id is provided, raises ValueError (variant must exist).
    If not found and no current_variant_id, raises ValueError.
    
    Args:
        regression_model_type: Type of regression model ('lgbm', 'xgboost', 'ridge')
        hyperparameters: Hyperparameters dictionary to match
        current_variant_id: Optional current variant_id to validate against
        
    Returns:
        Correct variant_id from metadata.json (looked up by hyperparameters)
        
    Raises:
        ValueError: If no matching variant found, or if current_variant_id doesn't match found variant
    """
    if not hyperparameters:
        raise ValueError(
            "Hyperparameters cannot be empty when ensuring correct variant_id. "
            "variant_id must be determined by looking up hyperparameters in metadata.json."
        )
    
    logger.debug(
        f"Looking up variant_id for hyperparameters: {hyperparameters} "
        f"(current_variant_id: {current_variant_id})"
    )
    
    existing_variant = find_variant_by_hyperparameters(
        regression_model_type=regression_model_type,
        hyperparameters=hyperparameters
    )
    
    if existing_variant is not None:
        correct_variant_id = existing_variant['variant_id']
        logger.info(
            f"Found matching variant in metadata.json: {correct_variant_id} "
            f"for hyperparameters: {hyperparameters}"
        )
        
        if current_variant_id and current_variant_id != correct_variant_id:
            # CRITICAL: Mismatch detected - this should never happen if code is correct
            error_msg = (
                f"Variant ID mismatch detected! "
                f"Current: {current_variant_id}, Correct: {correct_variant_id}. "
                f"Hyperparameters: {hyperparameters}. "
                f"variant_id must match the variant in metadata.json with these hyperparameters. "
                f"This indicates a bug in variant_id assignment logic."
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        return correct_variant_id
    
    # No matching variant found - this is an error
    error_msg = (
        f"No matching variant found in metadata.json for hyperparameters: {hyperparameters}. "
        f"Variant must exist in metadata.json before saving grid search results. "
        f"Current variant_id: {current_variant_id}. "
        f"Please ensure the variant is defined in metadata.json first."
    )
    logger.error(error_msg)
    raise ValueError(error_msg)
