# execution.py
# Execution logic for regression grid search variants

import logging
import numpy as np
from typing import Dict, List, Any, Optional, Tuple

from config.config import Config
from modeling.models import RegressionModel
from modeling.training.feature_extraction_trainer import split_features_by_fold
from modeling.evaluation.metrics import calc_metric
from modeling.utils import create_grid_search_result_dict, create_grid_search_error_result_dict
from modeling.utils import VARIANT_ID_FORMAT
from modeling.utils.metadata.regression_metadata import (
    find_variant_by_hyperparameters,
    save_regression_variant_definition,
    save_regression_gridsearch_result,
    ensure_correct_variant_id
)

logger = logging.getLogger(__name__)


def execute_single_regression_combination(
    idx: int,
    variant_index: int,
    combination: tuple,
    param_names: List[str],
    total_combinations: int,
    config: Config,
    all_features: np.ndarray,
    all_targets: np.ndarray,
    fold_assignments: np.ndarray,
    feature_filename: str,
    regression_model_type: str
) -> Tuple[Optional[Dict[str, Any]], bool]:
    """
    Execute a single regression hyperparameter combination.
    
    Args:
        idx: Index of combination in grid (0-based, used for logging only)
        variant_index: Pre-calculated variant_index for this combination (sequential, not grid position)
        combination: Hyperparameter combination tuple
        param_names: List of parameter names
        total_combinations: Total number of combinations
        config: Base configuration object
        all_features: All features array (N_total, feat_dim)
        all_targets: All targets array (N_total, 3)
        fold_assignments: Fold assignments array (N_total,)
        feature_filename: Feature filename used for training (e.g., 'variant_0100_features.npz')
        regression_model_type: Type of regression model ('lgbm', 'xgboost', 'ridge')
    
    Returns:
        Tuple of (result_dict, was_skipped). result_dict is None if combination was skipped.
    """
    hyperparameters = dict(zip(param_names, combination))
    
    logger.info("="*60)
    logger.info(f"Combination {idx+1}/{total_combinations}")
    logger.info(f"Hyperparameters: {hyperparameters}")
    logger.info(f"{'='*60}")
    
    # Check metadata.json for existing variant with matching hyperparameters (for DRY)
    # Base class already handles skipping completed combinations from gridsearch_metadata.json
    existing_variant = None
    max_retries = 2
    for attempt in range(max_retries):
        try:
            existing_variant = find_variant_by_hyperparameters(
                regression_model_type=regression_model_type,
                hyperparameters=hyperparameters
            )
            break  # Success, exit retry loop
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(
                    f"Attempt {attempt + 1} failed to check for existing variant definition: {e}. "
                    f"Retrying..."
                )
            else:
                logger.warning(
                    f"Failed to check for existing variant definition after {max_retries} attempts: {e}. "
                    f"Creating new variant."
                )
    
    # Determine variant_id (reuse if exists in metadata.json for DRY, otherwise create new)
    # CRITICAL: variant_id must match the variant in metadata.json with these hyperparameters
    # Always use sequential variant_index from base class (never override)
    if existing_variant is not None:
        # Reuse variant_id to avoid duplicate variant definitions in metadata.json
        variant_id = existing_variant['variant_id']
        logger.info(
            f"Found existing variant_id: {variant_id} (variant_index: {variant_index}) "
            f"for hyperparameters: {hyperparameters}"
        )
    else:
        # Create new variant_id using sequential variant_index
        variant_id = VARIANT_ID_FORMAT.format(index=variant_index)
        logger.info(
            f"Creating new variant: {variant_id} (variant_index: {variant_index}) "
            f"for hyperparameters: {hyperparameters}"
        )
    
    # CRITICAL: Validate variant_id against hyperparameters for existing variants
    # For new variants, validation happens after saving the variant definition
    # This ensures variant_id matches the variant in metadata.json with these hyperparameters
    if existing_variant is not None:
        # Validate existing variant - it should match hyperparameters
        logger.debug(f"Validating existing variant_id {variant_id} against hyperparameters")
        try:
            validated_variant_id = ensure_correct_variant_id(
                regression_model_type=regression_model_type,
                hyperparameters=hyperparameters,
                current_variant_id=variant_id
            )
            if validated_variant_id != variant_id:
                # This should never happen if code is correct, but log as error if it does
                logger.error(
                    f"Variant ID validation changed variant_id: {variant_id} -> {validated_variant_id}. "
                    f"This indicates a bug in variant_id assignment logic."
                )
                variant_id = validated_variant_id
            else:
                logger.debug(f"Variant ID validation passed: {variant_id} matches hyperparameters")
        except ValueError as e:
            # Existing variant but validation failed - this is a critical error
            logger.error(
                f"CRITICAL: Existing variant {variant_id} validation failed: {e}. "
                f"This should never happen - variant_id must match hyperparameters."
            )
            raise
    else:
        # New variant - validation will happen after saving variant definition
        # This is expected, we'll create it below and validate then
        logger.debug(
            f"New variant {variant_id} will be created and validated after saving to metadata.json"
        )
    
    try:
        # Get number of folds from config
        n_folds = config.cv.n_folds
        
        # Perform cross-validation
        fold_scores = []
        for fold in range(n_folds):
            logger.info(f"\nFold {fold+1}/{n_folds}")
            
            # Split features by fold
            train_features, val_features, train_targets, val_targets = split_features_by_fold(
                all_features, all_targets, fold_assignments, fold
            )
            
            # Create regression model with hyperparameters
            regression_model = RegressionModel(
                model_type=regression_model_type,
                model_params=hyperparameters,
                random_state=config.seed
            )
            
            # Train on training fold
            regression_model.fit(train_features, train_targets)
            
            # Evaluate on validation fold
            val_predictions = regression_model.predict(val_features)
            weighted_r2, r2_scores = calc_metric(val_predictions, val_targets)
            fold_score = weighted_r2
            fold_scores.append(fold_score)
            
            logger.info(f"Fold {fold+1} score: {fold_score:.4f}")
        
        # Calculate average CV score
        cv_score = np.mean(fold_scores)
        logger.info("="*60)
        logger.info(f"Average CV Score: {cv_score:.4f}")
        logger.info(f"Fold scores: {[f'{s:.4f}' for s in fold_scores]}")
        logger.info(f"{'='*60}")
        
        # Create result with unified format
        from ...utils.helpers import create_variant_specific_data
        variant_specific_data = create_variant_specific_data(
            config=config,
            hyperparameters=hyperparameters,
            feature_filename=feature_filename
        )
        result = create_grid_search_result_dict(
            variant_index=variant_index,
            variant_id=variant_id,
            cv_score=cv_score,
            fold_scores=fold_scores,
            batch_size_used=None,  # Not applicable for regression models
            batch_size_reduced=False,
            variant_specific_data=variant_specific_data
        )
        
        # Save variant to regression model metadata files
        try:
            # CRITICAL: Ensure hyperparameters are present before saving
            assert hyperparameters is not None, "hyperparameters must not be None when saving grid search results"
            assert len(hyperparameters) > 0, "hyperparameters must not be empty when saving grid search results"
            
            # If this is a new variant, save the definition to metadata.json first
            if existing_variant is None:
                logger.info(
                    f"Saving new variant definition: {variant_id} with hyperparameters: {hyperparameters}"
                )
                # Save variant definition - returns actual variant_index and variant_id used
                # (may differ from passed-in values if sequential index was recalculated)
                actual_variant_index, actual_variant_id = save_regression_variant_definition(
                    regression_model_type=regression_model_type,
                    variant_index=variant_index,
                    variant_id=variant_id,
                    hyperparameters=hyperparameters
                )
                # Update variant_index and variant_id to match what was actually saved
                if actual_variant_index != variant_index or actual_variant_id != variant_id:
                    logger.info(
                        f"Variant index/id updated during save: "
                        f"variant_index {variant_index} -> {actual_variant_index}, "
                        f"variant_id {variant_id} -> {actual_variant_id}"
                    )
                    variant_index = actual_variant_index
                    variant_id = actual_variant_id
                    # Update result dict with corrected values
                    result['variant_index'] = variant_index
                    result['variant_id'] = variant_id
                logger.info(f"Saved variant definition: {variant_id} to metadata.json")
            else:
                logger.debug(
                    f"Using existing variant definition: {variant_id} (already in metadata.json)"
                )
            
            # Always save the training result to gridsearch_metadata.json
            # CRITICAL: hyperparameters is REQUIRED - variant_id must match variant in metadata.json
            logger.info(
                f"Saving grid search result: variant_id={variant_id}, "
                f"feature_filename={feature_filename}, cv_score={cv_score:.4f}"
            )
            save_regression_gridsearch_result(
                regression_model_type=regression_model_type,
                variant_id=variant_id,
                feature_filename=feature_filename,
                cv_score=cv_score,
                fold_scores=fold_scores,
                hyperparameters=hyperparameters  # REQUIRED - used to validate variant_id
            )
            logger.info(
                f"Successfully saved grid search result: variant_id={variant_id} "
                f"validated against hyperparameters in metadata.json"
            )
        except ValueError as e:
            # ValueError from ensure_correct_variant_id - this is a critical error
            logger.error(
                f"CRITICAL: Failed to save variant to metadata files due to variant_id mismatch: {e}. "
                f"variant_id: {variant_id}, hyperparameters: {hyperparameters}"
            )
            raise  # Re-raise - this is a critical error that should not be silently ignored
        except Exception as e:
            logger.error(
                f"Failed to save variant to metadata files: {e}. "
                f"variant_id: {variant_id}, hyperparameters: {hyperparameters}",
                exc_info=True
            )
            raise  # Re-raise to ensure errors are not silently ignored
        
        return result, False
        
    except KeyboardInterrupt:
        logger.warning(f"\n⚠️ KeyboardInterrupt received during combination {variant_id}")
        logger.warning("Saving current progress before exiting...")
        raise
    
    except Exception as e:
        logger.error(f"Error training combination {variant_id}: {e}", exc_info=True)
        
        # Create error result
        from ...utils.helpers import create_variant_specific_data
        variant_specific_data = create_variant_specific_data(
            config=config,
            hyperparameters=hyperparameters,
            feature_filename=feature_filename
        )
        result = create_grid_search_error_result_dict(
            variant_index=variant_index,
            variant_id=variant_id,
            error=str(e),
            batch_size_used=None,
            batch_size_reduced=False,
            variant_specific_data=variant_specific_data
        )
        
        logger.warning(f"Error result will be saved (combination can be retried on resume)")
        return result, False

