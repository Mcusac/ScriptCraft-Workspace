# grid_search.py
# Grid search result handlers
#
# Handles results from various grid search pipelines:
# - Hyperparameter grid search
# - Dataset grid search
# - Regression grid search

import logging
from typing import List, Optional, Dict, Any
from pathlib import Path

from utils.system.io.paths import get_output_path
from utils.system.io.files import load_json_file

logger = logging.getLogger(__name__)


def handle_hyperparameter_grid_search_result(
    returncode: int,
    stdout_lines: List[str],
    log_file: str
) -> None:
    """
    Handle result from hyperparameter grid search command.
    
    Raises RuntimeError if returncode is non-zero, otherwise prints success message.
    
    Args:
        returncode: Process return code
        stdout_lines: Last N lines of stdout output
        log_file: Path to log file (for error messages)
        
    Raises:
        RuntimeError: If returncode is non-zero
    """
    if returncode != 0:
        error_msg = f"Hyperparameter grid search failed with return code {returncode}"
        if stdout_lines:
            error_msg += f"\n\nLast {len(stdout_lines)} lines of output:\n" + "\n".join(stdout_lines)
        error_msg += f"\n\nFull output available in: {log_file}"
        raise RuntimeError(error_msg)
    
    # Success message
    logger.info("="*60)
    logger.info("✅ Hyperparameter grid search complete!")
    logger.info("="*60)
    # Note: We don't know the search_type here, so we show the directory
    logger.info(f"\n📊 Results saved to: {get_output_path('output/hyperparameter_grid_search/')}")
    logger.info("   (All search types append to: gridsearch_results.json)")
    logger.info("   (Already-tested combinations are automatically skipped)")
    logger.info("   Next: Use best hyperparameters for final model training")


def handle_dataset_grid_search_result(
    returncode: int,
    stdout_lines: List[str],
    log_file: str,
    dataset_type: Optional[str] = None
) -> None:
    """
    Handle result from dataset grid search command.
    
    Raises RuntimeError if returncode is non-zero, otherwise prints success message.
    
    Args:
        returncode: Process return code
        stdout_lines: Last N lines of stdout output
        log_file: Path to log file (for error messages)
        dataset_type: Dataset type ('full' or 'split')
        
    Raises:
        RuntimeError: If returncode is non-zero
    """
    if returncode != 0:
        error_msg = f"Grid search failed with return code {returncode}"
        if stdout_lines:
            error_msg += f"\n\nLast {len(stdout_lines)} lines of output:\n" + "\n".join(stdout_lines)
        error_msg += f"\n\nFull output available in: {log_file}"
        raise RuntimeError(error_msg)
    
    dataset_type_str = dataset_type or 'split'
    logger.info("="*60)
    logger.info("✅ Dataset grid search complete!")
    logger.info("="*60)
    logger.info(f"\n📊 Results saved to: {get_output_path(f'output/dataset_grid_search_{dataset_type_str}/gridsearch_results.json')}")
    logger.info("   Next: Run Cell 2a (train and export) to train and export the best model")


def handle_regression_grid_search_result(
    regression_model_type: str,
    results_file: Optional[str] = None
) -> Dict[str, Any]:
    """
    Handle regression grid search results and display summary.
    
    Args:
        regression_model_type: Type of regression model
        results_file: Optional path to results file (auto-detects if None)
    
    Returns:
        Dictionary with best result information
    
    Raises:
        FileNotFoundError: If results file not found
    """
    if results_file is None:
        # Auto-detect results file from metadata directory
        # Regression grid search uses gridsearch_metadata.json in metadata directory
        from modeling.utils.metadata.regression_metadata import get_writable_metadata_dir
        
        working_dir = get_writable_metadata_dir() / regression_model_type
        results_file = str(working_dir / 'gridsearch_metadata.json')
    
    results_path = Path(results_file)
    if not results_path.exists():
        raise FileNotFoundError(f"Results file not found: {results_file}")
    
    # Load results from gridsearch_metadata.json
    results = load_json_file(
        results_path, expected_type=list, file_type="Regression gridsearch metadata JSON"
    )
    
    # Filter successful results (only those with cv_score)
    successful_results = [r for r in results if r.get('cv_score') is not None]
    
    if not successful_results:
        logger.warning("No successful results found in regression grid search")
        return {}
    
    # Find best result
    best_result = max(successful_results, key=lambda x: x.get('cv_score', -float('inf')))
    
    # Get hyperparameters from metadata.json if not in result
    hyperparameters = best_result.get('hyperparameters')
    if not hyperparameters:
        variant_id = best_result.get('variant_id')
        if variant_id:
            try:
                from modeling.utils.metadata.regression_metadata import get_writable_metadata_dir
                working_dir = get_writable_metadata_dir() / regression_model_type
                metadata_file = working_dir / 'metadata.json'
                if metadata_file.exists():
                    variants = load_json_file(
                        metadata_file, expected_type=list, file_type="Regression metadata JSON"
                    )
                    for variant in variants:
                        if variant.get('variant_id') == variant_id:
                            hyperparameters = variant.get('hyperparameters')
                            if hyperparameters:
                                best_result['hyperparameters'] = hyperparameters
                                break
            except Exception as e:
                logger.warning(f"Failed to retrieve hyperparameters from metadata.json: {e}")
    
    logger.info("="*60)
    logger.info("REGRESSION GRID SEARCH RESULTS")
    logger.info(f"{'='*60}")
    logger.info(f"Total combinations tested: {len(successful_results)}")
    logger.info(f"Best CV Score: {best_result.get('cv_score', 0):.4f}")
    logger.info(f"Best Variant ID: {best_result.get('variant_id', 'unknown')}")
    logger.info(f"Best Hyperparameters: {best_result.get('hyperparameters', {})}")
    feature_filename = best_result.get('feature_filename', 'unknown')
    logger.info(f"Feature Filename: {feature_filename}")
    logger.info(f"{'='*60}\n")
    
    return best_result

