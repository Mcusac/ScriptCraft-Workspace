# pipeline.py
# Dataset grid search pipeline for finding optimal preprocessing/augmentation combinations

import logging

from config.config import Config
from utils.data import get_max_augmentation_variant
from utils.config import validate_pipeline_config
from utils.system import load_json_file, ProgressTracker
from ..utils.constants import BEST_VARIANT_FILE_DATASET
from ..utils.hyperparameters import get_default_hyperparameters
from .grid_search_class import DatasetGridSearch
# Variant key creation now handled by GridSearchBase
from modeling import find_metadata_dir, extract_preprocessing_augmentation_from_variant

logger = logging.getLogger(__name__)


def dataset_grid_search_pipeline(config: Config) -> None:
    """
    Run dataset grid search to find optimal preprocessing/augmentation combination.

    Tests all combinations of optional preprocessing and augmentation methods, saving
    results incrementally for resumability. Can be interrupted and resumed safely.

    The number of combinations is computed dynamically based on available optional
    preprocessing methods (excluding 'resize' and 'normalize' which are always applied)
    and all augmentation methods. Each generates a power set, and the cartesian product
    gives the total grid size.

    Note: Only optional preprocessing methods are varied in the grid. 'resize' and 'normalize'
    are always applied automatically and do not contribute to the variation count.

    Args:
        config: Base configuration object with training, model, data, cv, paths, device, and grid_search settings.
                Must have all required attributes configured.

    Returns:
        None. Results are saved to output/dataset_grid_search_{dataset_type}/gridsearch_results.json.
        Best variant summary is saved to output/dataset_grid_search_{dataset_type}/best_dataset_variant.json.
        Where {dataset_type} is 'full' or 'split' based on config.data.dataset_type.

    Raises:
        ValueError: If config is None or missing required attributes.
        FileNotFoundError: If train.csv doesn't exist.
        RuntimeError: If grid search setup fails.
    """
    # Validate config
    validate_pipeline_config(config, required_sections=["data", "cv", "paths", "grid_search"])

    # Create grid search instance
    grid_search = DatasetGridSearch(config)
    
    # Setup environment using base class
    base_model_dir, grid_search_dir, device, device_info = grid_search.setup_environment()
    results_file = grid_search.setup_results_file()
    
    # Get dataset variant grid
    variant_grid = grid_search._generate_variant_grid()
    total_variants = len(variant_grid)
    logger.info(f"Total dataset variants to test: {total_variants}")

    # Load completed variants using base class
    keep_top_n = config.grid_search.keep_top_variants
    completed_variants, skipped_variants, top_variants, starting_index = grid_search.load_completed_variants(keep_top_n)

    # Run grid search
    best_score = -float("inf")
    best_variant = None
    if top_variants:
        best_variant = top_variants[0]
        best_score = best_variant.get("cv_score", -float("inf"))
        logger.info(f"Best score from existing results: {best_score:.4f}")

    # Initialize progress tracker
    progress_tracker = ProgressTracker(config.progress)
    # Calculate initial progress (number of already completed variants)
    initial_progress = len(completed_variants)
    grid_bar_id = progress_tracker.create_bar(
        bar_id="dataset_grid_search",
        total=total_variants,
        desc="Dataset Grid Search",
        level=1,
        unit="variant",
        initial=initial_progress
    )

    # Run grid search using base class template method
    best_score, best_variant = grid_search.run_grid_search(
        variant_grid=variant_grid,
        progress_tracker=progress_tracker,
        grid_bar_id=grid_bar_id,
        best_score=best_score,
        best_variant=best_variant,
        keep_top_n=keep_top_n
    )

    # Save final results and best variant summary
    # Reload from file to get accurate count and find actual best variant
    if results_file.exists():
        all_results = load_json_file(results_file, expected_type=list, file_type="Results JSON")
        # Count variants by status
        completed_count = len([r for r in all_results if r.get("cv_score") is not None])
        skipped_count = len([r for r in all_results if r.get("skipped", False)])
        failed_count = len(
            [r for r in all_results if r.get("cv_score") is None and not r.get("skipped", False)]
        )
        total_count = len(all_results)

        # Find actual best variant from ALL results (not just in-memory top N)
        from modeling.utils import find_best_variant

        actual_best_variant = find_best_variant(all_results)
        if actual_best_variant:
            actual_best_score = actual_best_variant.get("cv_score", -float("inf"))
            # Use the actual best from all results, not the in-memory tracked one
            best_variant = actual_best_variant
            best_score = actual_best_score
            logger.info(f"Found best variant from all results: score {best_score:.4f}")
    else:
        completed_count = 0
        skipped_count = 0
        failed_count = 0
        total_count = 0

    best_variant_file = grid_search_dir / BEST_VARIANT_FILE_DATASET
    from utils.system import save_json_file
    save_json_file(
        {
            "best_score": best_score,
            "best_variant": best_variant,
            "total_variants": total_variants,
            "completed_variants": completed_count,
            "skipped_variants": skipped_count,
            "failed_variants": failed_count,
            "total_attempted": total_count,
        },
        best_variant_file,
        file_type="Best variant JSON"
    )

    logger.info("="*60)
    logger.info("Dataset grid search complete!")
    logger.info(f"Best score: {best_score:.4f}")
    if best_variant:
        metadata_dir = find_metadata_dir()
        try:
            best_prep, best_aug = extract_preprocessing_augmentation_from_variant(best_variant, metadata_dir)
            logger.info(f"Best preprocessing: {best_prep}")
            logger.info(f"Best augmentation: {best_aug}")
        except (ValueError, FileNotFoundError) as e:
            logger.warning(f"Cannot extract preprocessing/augmentation from best variant: {e}")
    logger.info(f"Successfully completed: {completed_count}/{total_variants} variants")
    if skipped_count > 0:
        logger.info(
            "Skipped variants: "
            f"{skipped_count} (persistent OOM - can retry later with different settings)"
        )
    if failed_count > 0:
        logger.info(f"Failed variants: {failed_count} (will be retried on resume)")
    logger.info(f"Results saved to: {results_file}")
    logger.info(f"Best variant saved to: {best_variant_file}")

    # Display best variant summary
    if best_variant:
        metadata_dir = find_metadata_dir()
        logger.info("="*60)
        logger.info("🏆 Best Grid Search Result Summary:")
        logger.info(f"   Score: {best_score:.4f}")
        try:
            best_prep, best_aug = extract_preprocessing_augmentation_from_variant(best_variant, metadata_dir)
            logger.info(f"   Preprocessing: {best_prep}")
            logger.info(f"   Augmentation: {best_aug}")
        except (ValueError, FileNotFoundError) as e:
            logger.warning(f"   Cannot extract preprocessing/augmentation: {e}")
        logger.info(f"   Variant ID: {best_variant.get('variant_id', 'N/A')}")
        logger.info(f"   📁 Full results: {results_file}")
        logger.info(f"{'='*60}")

    # Final cleanup using base class method
    grid_search.run_final_cleanup()


def test_max_augmentation_pipeline(config: Config) -> None:
    """
    Test the maximally augmented dataset variant (all preprocessing + all augmentation).
    
    This is a quick test mode that trains a single variant with all preprocessing and
    augmentation methods enabled, without running the full grid search. The result is
    saved to the same results file format as the full grid search, so it integrates
    seamlessly with existing infrastructure.
    
    If this variant has already been tested (found in results file), the function will
    skip training and just report the existing result. Future grid searches will
    automatically skip this variant if it's already been tested.
    
    This mode is useful for:
    - Quick validation of maximum augmentation's impact on generalization
    - Testing with large models where full grid search is time-prohibitive
    - Building up results incrementally for later grid search continuation
    
    Args:
        config: Base configuration object with training, model, data, cv, paths, device, and grid_search settings.
                Must have all required attributes configured.
    
    Returns:
        None. Results are saved to output/dataset_grid_search_{dataset_type}/gridsearch_results.json.
        Best variant summary is updated if this variant becomes the new best.
        Where {dataset_type} is 'full' or 'split' based on config.data.dataset_type.
    
    Raises:
        ValueError: If config is None or missing required attributes.
        FileNotFoundError: If train.csv doesn't exist.
        RuntimeError: If setup fails.
    """
    # Validate config
    validate_pipeline_config(config, required_sections=["data", "cv", "paths", "grid_search"])
    
    # Create grid search instance
    grid_search = DatasetGridSearch(config)
    
    # Setup environment using base class
    base_model_dir, grid_search_dir, device, device_info = grid_search.setup_environment()
    results_file = grid_search.setup_results_file()
    
    # Get max augmentation variant
    preprocessing_list, augmentation_list = get_max_augmentation_variant()
    logger.info("="*60)
    logger.info("Max Augmentation Quick Test Mode")
    logger.info(f"{'='*60}")
    logger.info(f"Testing variant with all preprocessing and augmentation enabled")
    logger.info(f"Preprocessing: {preprocessing_list}")
    logger.info(f"Augmentation: {augmentation_list}")
    logger.info(f"{'='*60}\n")
    
    # Load completed variants using base class
    keep_top_n = config.grid_search.keep_top_variants
    completed_variants, skipped_variants, top_variants, starting_index = grid_search.load_completed_variants(keep_top_n)
    
    # Create variant key to check if already tested (using class method for consistency)
    default_hyperparameters = get_default_hyperparameters()
    variant = (preprocessing_list, augmentation_list)
    variant_key = grid_search._create_variant_key(variant)
    
    # Check if already completed
    if variant_key in completed_variants:
        logger.info("✅ Max augmentation variant already tested!")
        # Find the existing result
        for r in top_variants:
            r_key = grid_search._create_variant_key_from_result(r)
            if r_key is None:
                continue
            if r_key == variant_key:
                cv_score = r.get("cv_score")
                variant_id = r.get("variant_id", "N/A")
                logger.info(f"   Variant ID: {variant_id}")
                logger.info(f"   CV Score: {cv_score:.4f}" if cv_score is not None else "   CV Score: N/A")
                logger.info(f"   Results file: {results_file}")
                logger.info("\n💡 This variant will be automatically skipped in future grid searches.")
                return
    
    # Check if skipped
    if variant_key in skipped_variants:
        logger.warning("⚠️ Max augmentation variant was previously skipped due to persistent OOM")
        logger.warning("   This variant can be retried later with different settings (e.g., smaller model)")
        logger.info(f"   Results file: {results_file}")
        return
    
    # Run the single variant using base class method
    logger.info("🚀 Training max augmentation variant...")
    variant = (preprocessing_list, augmentation_list)
    cv_score, fold_scores, result, variant_model_dir = grid_search._run_variant(
        variant=variant,
        variant_index=starting_index,
        total_variants=1  # Only testing 1 variant
    )
    
    variant_id = result.get("variant_id", f"variant_{starting_index:04d}")
    
    # Save result to file using base class method
    grid_search.save_variant_result(result)
    
    # Handle skipped variants
    if result.get("skipped", False):
        logger.warning("⚠️ Max augmentation variant was skipped due to persistent OOM")
        logger.warning("   This variant can be retried later with different settings (e.g., smaller model)")
        logger.info(f"   Results file: {results_file}")
        return
    
    # Update best variant summary
    if results_file.exists():
        all_results = load_json_file(results_file, expected_type=list, file_type="Results JSON")
        from modeling.utils import find_best_variant
        
        actual_best_variant = find_best_variant(all_results)
        if actual_best_variant:
            actual_best_score = actual_best_variant.get("cv_score", -float("inf"))
            best_variant = actual_best_variant
            best_score = actual_best_score
        else:
            best_variant = result if cv_score is not None else None
            best_score = cv_score if cv_score is not None else -float("inf")
    else:
        best_variant = result if cv_score is not None else None
        best_score = cv_score if cv_score is not None else -float("inf")
    
    best_variant_file = grid_search_dir / BEST_VARIANT_FILE_DATASET
    from utils.system import save_json_file
    save_json_file(
        {
            "best_score": best_score,
            "best_variant": best_variant,
            "total_variants": 1,
            "completed_variants": 1 if cv_score is not None else 0,
            "skipped_variants": 1 if result.get("skipped", False) else 0,
            "failed_variants": 0 if cv_score is not None else 1,
            "total_attempted": 1,
        },
        best_variant_file,
        file_type="Best variant JSON"
    )
    
    # Display results
    logger.info("="*60)
    logger.info("Max Augmentation Quick Test Complete!")
    if cv_score is not None:
        logger.info(f"✅ CV Score: {cv_score:.4f}")
        logger.info(f"   Fold scores: {fold_scores}")
        logger.info(f"   Variant ID: {variant_id}")
        logger.info(f"   Preprocessing: {preprocessing_list}")
        logger.info(f"   Augmentation: {augmentation_list}")
        logger.info(f"\n💡 This result is saved and will be automatically skipped in future grid searches.")
    else:
        logger.warning("❌ Training failed - check logs for details")
        logger.info(f"   Variant ID: {variant_id}")
        logger.info(f"   Error: {result.get('error', 'Unknown error')}")
    logger.info(f"Results saved to: {results_file}")
    logger.info(f"Best variant saved to: {best_variant_file}")
    logger.info(f"{'='*60}")
    
    # Cleanup checkpoints using base class method
    grid_search.run_final_cleanup()


