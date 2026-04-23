# evaluation package
# Evaluation metrics and loss functions
#
# Provides evaluation metrics and loss functions for model training and validation.
#
# Components:
# - metrics: Weighted R² calculation matching competition formula exactly.
#   Computes metric over all (image, target) pairs with target-specific weights.
#   Also provides per-target R², RMSE, and MAE (RMSE/MAE are internal utilities).
# - losses: Loss function factory supporting SmoothL1Loss, MSELoss, etc.
# - post_processing: Post-processing functions for enforcing physical constraints
#   on predictions (contest-specific constraint logic).
#
# Note: Evaluation constants (target definitions, weights, order) are imported
# from config.evaluation_constants to maintain single source of truth and avoid
# circular dependencies.
#
# The weighted R² implementation matches the competition formula:
# R² = 1 - (RSS / TSS) where both are weighted sums over all (image, target) pairs.


__all__ = [
    'weighted_r2_score',
    'calc_metric',
    'r2_score_per_target',
    'get_loss_function',
    'TARGET_WEIGHTS',
    'TARGET_ORDER',
    'PRIMARY_TARGETS',
    'DERIVED_TARGETS',
    'ALL_TARGETS',
    'compute_derived_target_values',
    'post_process_biomass'
]

