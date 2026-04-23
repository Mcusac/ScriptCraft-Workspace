"""
Get all averages workflow for CAFA 6 protein function prediction.
Generates all 7 ensemble method submissions in one run.
"""

import time
from pathlib import Path
from typing import List, Optional

from config import PREDICTION_SETTINGS
from config.ensemble import get_available_ensemble_methods
from utils.logging import setup_logging, get_logger
from utils.cli_utils import build_ensemble_kwargs
from pipelines.workflows.submission_averaging import run_submission_averaging


logger = get_logger(__name__)


def run_get_all_averages(submission_files: List[str],
                        weights: Optional[List[float]] = None,
                        power_default: Optional[float] = None,
                        percentile_default: Optional[float] = None,
                        output_prefix: Optional[str] = None) -> List[str]:
    """
    Generate all 7 ensemble method submissions in one run.
    
    Args:
        submission_files: List of paths to submission files
        weights: Optional weights for weighted_average (default: equal weights)
        power_default: Default power for power_average method (default: from config)
        percentile_default: Default percentile for percentile method (default: from config)
        output_prefix: Optional prefix for output filenames (default: auto-generated)
        
    Returns:
        List[str]: Paths to all 7 generated submission files
        
    Methods generated:
        1. average (simple mean)
        2. weighted_average (equal weights if not specified)
        3. max (maximum probability)
        4. geometric_mean
        5. rank_average
        6. power_average (power=power_default)
        7. percentile (percentile=percentile_default)
    """
    setup_logging()
    logger.info("Starting Get All Averages Workflow")
    logger.info("=" * 60)
    
    start_time = time.time()
    
    # Get defaults from config if not provided
    pred_settings = PREDICTION_SETTINGS
    if power_default is None:
        power_default = pred_settings['submission_averaging_power_default']
    if percentile_default is None:
        percentile_default = pred_settings['submission_averaging_percentile_default']
    
    # Generate output prefix if not provided
    if output_prefix is None:
        # Extract model info from first submission filename
        first_file = Path(submission_files[0]).stem
        # Try to extract meaningful prefix (e.g., "LR_All1.1" -> "lr11")
        output_prefix = "avg"
        logger.info(f"Using default output prefix: {output_prefix}")
    
    # Get list of all ensemble methods from config
    available_methods = get_available_ensemble_methods()
    
    # Build methods list dynamically from config
    methods = []
    for method_key in available_methods:
        ensemble_kwargs = build_ensemble_kwargs(
            method_key,
            power=power_default,
            percentile=percentile_default
        )
        methods.append((method_key, method_key, ensemble_kwargs))
    
    output_files = []
    
    logger.info(f"Generating {len(methods)} ensemble method submissions...")
    logger.info(f"Submission files: {len(submission_files)}")
    for i, filepath in enumerate(submission_files, 1):
        logger.info(f"  {i}. {Path(filepath).name}")
    
    for method_idx, (method_name, method_key, method_kwargs) in enumerate(methods, 1):
        logger.info(f"\n[{method_idx}/{len(methods)}] Generating {method_name} submission...")
        logger.info("=" * 60)
        
        # Prepare output name
        output_name = f"{output_prefix}_method_{method_name}.tsv"
        
        # Prepare weights for weighted_average
        method_weights = weights if method_key == 'weighted_average' else None
        
        try:
            result_path = run_submission_averaging(
                submission_files=submission_files,
                weights=method_weights,
                output_name=output_name,
                ensemble_method=method_key,
                **method_kwargs
            )
            output_files.append(result_path)
            logger.info(f"✓ {method_name} submission generated: {result_path}")
        except Exception as e:
            logger.error(f"❌ Failed to generate {method_name} submission: {e}")
            logger.exception("Error details:")
            # Continue with other methods even if one fails
            continue
    
    total_time = time.time() - start_time
    logger.info("\n" + "=" * 60)
    logger.info("Get All Averages Complete!")
    logger.info(f"Total time: {total_time:.1f}s")
    logger.info(f"Generated {len(output_files)}/{len(methods)} submissions")
    logger.info("\nGenerated files:")
    for i, filepath in enumerate(output_files, 1):
        logger.info(f"  {i}. {filepath}")
    
    return output_files

