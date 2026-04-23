# pipeline.py
# Main hyperparameter grid search pipeline orchestration

import logging
from typing import Optional

from config.config import Config
from utils.system import save_json_file
from ...utils.constants import (
    SEARCH_TYPE_THOROUGH,
    BEST_HYPERPARAMETERS_FILE
)
# Execution now handled by GridSearchBase._run_variant()
from .grid_search_class import HyperparameterGridSearch
# Variant key creation now handled by GridSearchBase

logger = logging.getLogger(__name__)


def hyperparameter_grid_search_pipeline(
    config: Config,
    search_type: str = SEARCH_TYPE_THOROUGH,
    metadata_path: Optional[str] = None,
    results_file: Optional[str] = None,
    previous_results_file: Optional[str] = None
) -> None:
    """
    Run hyperparameter grid search using fixed dataset configuration from saved model.
    
    Loads dataset configuration (preprocessing/augmentation) from model metadata,
    then searches over training hyperparameters. All variants use the same dataset
    configuration but different hyperparameters.
    
    Args:
        config: Base configuration object with training, model, data, cv, paths, device, and grid_search settings.
                Must have all required attributes configured.
        search_type: Type of grid search (default: 'thorough').
                    Must be one of: 'defaults', 'quick', 'in_depth', 'thorough', 'focused_in_depth', or 'focused_thorough'.
                    - 'defaults': Single combination with all default hyperparameters (baseline, very fast)
                    - 'quick': Small grid (varies learning_rate, batch_size, optimizer)
                    - 'in_depth': Medium grid (varies more hyperparameters)
                    - 'thorough': Comprehensive grid (varies all hyperparameters)
                    - 'focused_in_depth': Focused in-depth grid based on previous results
                    - 'focused_thorough': Focused thorough grid based on previous results
        metadata_path: Optional path to model_metadata.json. If not provided, will auto-detect from Kaggle inputs.
        results_file: Optional path to results.json from dataset grid search (fallback for metadata).
        previous_results_file: Optional path to previous hyperparameter grid search results.json.
                              Required for 'focused_in_depth' and 'focused_thorough' search types.
                              Used to narrow the search space based on top performers.
        
    Returns:
        None. Results are saved to output/hyperparameter_grid_search/gridsearch_results.json.
        Best hyperparameters summary is saved to output/hyperparameter_grid_search/best_hyperparameters.json.
        
    Note on Results Files:
        - All search types append to the same unified file: gridsearch_results.json
        - Already-tested combinations are automatically skipped across all search types
        - This allows progressive refinement: quick → in_depth → thorough without duplicate work
        - When using focused searches, specify previous_results_file pointing to the previous search's results
        
    Raises:
        ValueError: If config is None, search_type is invalid, or config missing required attributes.
        FileNotFoundError: If train.csv doesn't exist or previous_results_file is missing for focused searches.
        RuntimeError: If grid search setup fails.
    """
    # Create grid search instance
    grid_search = HyperparameterGridSearch(
        config=config,
        search_type=search_type,
        metadata_path=metadata_path,
        results_file=results_file,
        previous_results_file=previous_results_file
    )
    
    # Setup environment using base class (but we still need metadata loading)
    base_model_dir, grid_search_dir, device, device_info = grid_search.setup_environment()
    results_file_path = grid_search.setup_results_file()
    
    # Load metadata (hyperparameter-specific)
    metadata_dict, preprocessing_list, augmentation_list = grid_search.setup_metadata()
    
    # Setup parameter grid (hyperparameter-specific)
    param_grid, all_combinations = grid_search.setup_parameter_grid()
    total_combinations = len(all_combinations)
    
    # Load completed variants using base class
    keep_top_n = config.grid_search.keep_top_variants
    completed_variants, skipped_variants, top_variants, starting_index = grid_search.load_completed_variants(keep_top_n)
    
    # Extract best score and hyperparameters from top_variants (if any)
    best_score = -float("inf")
    best_hyperparameters = None
    if top_variants:
        best_variant = top_variants[0]
        best_score = best_variant.get("cv_score", -float("inf"))
        best_hyperparameters = best_variant.get("hyperparameters")
        logger.info(f"Best score from existing results: {best_score:.4f}")
    
    # Load all results for in-memory tracking (needed for best score updates during loop)
    from utils.system import load_json_file
    results = []
    if results_file_path.exists():
        results = load_json_file(results_file_path, expected_type=list, file_type="Results JSON")
    
    # Run grid search using base class template method
    best_score, best_variant = grid_search.run_grid_search(
        variant_grid=all_combinations,
        progress_tracker=None,  # Hyperparameter doesn't use progress tracker
        grid_bar_id=None,
        best_score=best_score,
        best_variant=None,
        keep_top_n=keep_top_n
    )
    
    # Extract best_hyperparameters from best_variant
    if best_variant:
        best_hyperparameters = best_variant.get('hyperparameters')
    
    # Final cleanup using base class method
    grid_search.run_final_cleanup()
    
    # Save best hyperparameters summary (unified across all search types)
    best_hyperparams_file = grid_search_dir / BEST_HYPERPARAMETERS_FILE
    save_json_file(
        {
            'best_score': best_score,
            'best_hyperparameters': best_hyperparameters,
            'preprocessing_list': preprocessing_list,
            'augmentation_list': augmentation_list,
            'search_type': search_type,
            'total_combinations': total_combinations,
            'completed_combinations': len([r for r in results if r.get('cv_score') is not None])
        },
        best_hyperparams_file,
        file_type="Best hyperparameters JSON"
    )
    
    logger.info("="*60)
    logger.info("Hyperparameter grid search complete!")
    logger.info(f"Best score: {best_score:.4f}")
    logger.info(f"Best hyperparameters: {best_hyperparameters}")
    logger.info(f"Results saved to: {results_file_path}")
    logger.info(f"Best hyperparameters saved to: {best_hyperparams_file}")
    logger.info(f"{'='*60}")

