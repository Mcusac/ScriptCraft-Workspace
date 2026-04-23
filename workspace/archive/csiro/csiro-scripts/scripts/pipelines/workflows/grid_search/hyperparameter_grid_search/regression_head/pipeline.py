# pipeline.py
# Main regression grid search pipeline orchestration

import logging

from config.config import Config
from utils.system import save_json_file
from .setup import setup_regression_grid_search
from .grid_search_class import RegressionGridSearch
# Execution now handled by GridSearchBase._run_variant()

logger = logging.getLogger(__name__)


def regression_grid_search_pipeline(
    config: Config,
    feature_filename: str,
    regression_model_type: str,
    search_type: str = 'quick'
) -> None:
    """
    Run regression grid search using pre-extracted features.
    
    Loads features from a feature file and searches over regression model
    hyperparameters. All variants use the same features but different hyperparameters.
    
    Args:
        config: Base configuration object with data, cv, paths, and grid_search settings.
                Must have all required attributes configured.
        feature_filename: Feature filename (e.g., "variant_0100_features.npz").
                         Features must be pre-extracted and saved.
        regression_model_type: Type of regression model ('lgbm', 'xgboost', 'ridge').
        search_type: Type of grid search (default: 'quick').
                    Must be one of: 'defaults', 'quick', 'in_depth', 'thorough'.
                    - 'defaults': Single combination with all default hyperparameters (baseline)
                    - 'quick': Small grid (varies key hyperparameters)
                    - 'in_depth': Medium grid (varies more hyperparameters)
                    - 'thorough': Comprehensive grid (varies all hyperparameters)
    
    Returns:
        None. Results are saved to csiro-metadata/{regression_model_type}/gridsearch_metadata.json.
        Best hyperparameters summary is saved to output/regression_grid_search/{regression_model_type}/best_hyperparameters.json.
    
    Raises:
        ValueError: If config is None, search_type is invalid, or config missing required attributes.
        FileNotFoundError: If feature file doesn't exist.
        RuntimeError: If grid search setup fails.
    """
    # Create grid search instance
    grid_search = RegressionGridSearch(config=config, regression_model_type=regression_model_type)
    
    # Setup environment using base class (but regression has custom directory structure)
    base_model_dir, grid_search_dir, device, device_info = grid_search.setup_environment()
    
    # Setup regression-specific components (feature loading, parameter grid)
    (
        all_features,
        all_targets,
        fold_assignments,
        feature_metadata,
        feature_filename,
        grid_search_dir,
        param_grid,
        all_combinations,
        starting_index
    ) = setup_regression_grid_search(
        config, feature_filename, regression_model_type, search_type, grid_search_dir
    )
    
    # Setup feature data in grid search instance
    param_names = list(param_grid.keys())
    grid_search.setup_features(
        all_features=all_features,
        all_targets=all_targets,
        fold_assignments=fold_assignments,
        feature_filename=feature_filename,
        param_names=param_names,
        param_grid=param_grid
    )
    
    # Load completed variants using base class
    keep_top_n = config.grid_search.keep_top_variants
    completed_variants, skipped_variants, top_variants, starting_index = grid_search.load_completed_variants(keep_top_n)
    
    # Initialize best_score and best_hyperparameters with default values
    best_score = -float("inf")
    best_hyperparameters = None
    
    # Extract best score and hyperparameters from top_variants (if any)
    if top_variants:
        best_variant = top_variants[0]
        best_score = best_variant.get("cv_score", -float("inf"))
        best_hyperparameters = best_variant.get("hyperparameters")
        logger.info(f"Best score from existing results: {best_score:.4f}")
    
    total_combinations = len(all_combinations)
    
    # Run grid search using base class template method
    best_score, best_variant = grid_search.run_grid_search(
        variant_grid=all_combinations,
        progress_tracker=None,  # Regression doesn't use progress tracker
        grid_bar_id=None,
        best_score=best_score,
        best_variant=None,
        keep_top_n=keep_top_n
    )
    
    # Extract best_hyperparameters from best_variant
    # If best_variant doesn't have hyperparameters, get them from metadata.json using variant_id
    if best_variant:
        best_hyperparameters = best_variant.get('hyperparameters')
        if not best_hyperparameters:
            # Try to get hyperparameters from metadata.json using variant_id
            variant_id = best_variant.get('variant_id')
            if variant_id:
                try:
                    from modeling.utils.metadata.regression_metadata import get_writable_metadata_dir
                    from utils.system.io import load_json_file
                    working_dir = get_writable_metadata_dir() / regression_model_type
                    metadata_file = working_dir / 'metadata.json'
                    if metadata_file.exists():
                        variants = load_json_file(
                            metadata_file, expected_type=list, file_type="Regression metadata JSON"
                        )
                        for variant in variants:
                            if variant.get('variant_id') == variant_id:
                                best_hyperparameters = variant.get('hyperparameters')
                                if best_hyperparameters:
                                    logger.info(f"Retrieved hyperparameters from metadata.json for {variant_id}")
                                break
                except Exception as e:
                    logger.warning(f"Failed to retrieve hyperparameters from metadata.json: {e}")
    
    # Ensure best_hyperparameters is set (fallback to empty dict)
    if not best_hyperparameters:
        best_hyperparameters = {}
        logger.warning("Best hyperparameters not found - using empty dict")
    
    # Save best hyperparameters summary
    best_hyperparams_file = grid_search_dir / 'best_hyperparameters.json'
    save_json_file(
        {
            'best_score': best_score,
            'best_hyperparameters': best_hyperparameters,
            'feature_filename': feature_filename,
            'regression_model_type': regression_model_type,
            'search_type': search_type,
            'total_combinations': total_combinations
        },
        best_hyperparams_file,
        file_type="Best hyperparameters JSON"
    )
    
    logger.info("="*60)
    logger.info("Regression grid search complete!")
    logger.info(f"Best score: {best_score:.4f}")
    logger.info(f"Best hyperparameters: {best_hyperparameters}")
    logger.info(f"Results saved to metadata files")
    logger.info(f"Best hyperparameters saved to: {best_hyperparams_file}")
    logger.info(f"{'='*60}")

