"""
Submission averaging workflow for CAFA 6 protein function prediction.
Combines multiple submission files by averaging their prediction scores.
"""

import time
from pathlib import Path
from typing import List, Optional

from utils.logging import setup_logging, get_logger
from config import get_extra_output_name
from prediction.submission_averaging import (
    average_submissions,
    validate_submission_format
)
from prediction.submission_merging import merge_submissions_outer
from prediction.predict_and_submit import post_process_submission
from pipelines.workflows.workflow_paths import setup_workflow_paths


logger = get_logger(__name__)


def run_submission_averaging(submission_files: List[str],
                            weights: Optional[List[float]] = None,
                            output_name: Optional[str] = None,
                            ensemble_method: str = 'average',
                            prefer_submission: Optional[str] = None,
                            extra_output_name: Optional[str] = None,
                            **ensemble_kwargs) -> str:
    """
    Run submission averaging workflow.
    
    Args:
        submission_files: List of paths to submission files
        weights: Optional weights for weighted_average method
        output_name: Optional custom output filename
        ensemble_method: Ensemble method ('average', 'weighted_average', 'max', 
                       'geometric_mean', 'rank_average', 'power_average', 'percentile')
        prefer_submission: For merge method, which submission to prefer ('submission1' or 'submission2')
        extra_output_name: Optional filename for a descriptive copy of submission.tsv
        **ensemble_kwargs: Additional method-specific parameters:
            - power (float): Power for power_average method (default: 1.0)
            - percentile (float): Percentile for percentile method (default: 75.0)
        
    Returns:
        str: Path to final ensembled submission file
    """
    setup_logging()
    logger.info("Starting Submission Averaging Workflow")
    logger.info("=" * 60)
    
    start_time = time.time()
    
    # Validate input files
    logger.info(f"Validating {len(submission_files)} submission files...")
    valid_files = []
    
    for i, filepath in enumerate(submission_files, 1):
        logger.info(f"Validating [{i}/{len(submission_files)}]: {Path(filepath).name}")
        is_valid, issues = validate_submission_format(filepath)
        
        if is_valid:
            logger.info("      ✓ Valid")
            valid_files.append(filepath)
        else:
            logger.error("      ❌ Invalid submission file:")
            for issue in issues:
                    logger.error(f"         - {issue}")
    
    if not valid_files:
        raise ValueError("No valid submission files found")
    
    if len(valid_files) < len(submission_files):
        logger.warning(f"Using {len(valid_files)}/{len(submission_files)} valid files")
    
    # Validate weights if provided
    if weights is not None:
        from utils.cli_utils import validate_and_adjust_weights
        # Adjust weights to match valid files
        if len(weights) != len(valid_files):
            logger.warning("Adjusting weights to match valid files")
            valid_indices = [i for i, f in enumerate(submission_files) if f in valid_files]
            weights = [weights[i] for i in valid_indices]
        weights = validate_and_adjust_weights(weights, len(valid_files))
        logger.info(f"Normalized weights: {weights}")
    
    # Set up output directory
    _, output_dir = setup_workflow_paths(test=False)
    
    # Handle merge method (for 2 submissions) vs ensemble method (for 3+ submissions)
    if len(valid_files) == 2 and ensemble_method == 'merge':
        # Use outer merge strategy
        logger.info("Merging 2 submissions using outer merge...")
        prefer = prefer_submission if prefer_submission in ['submission1', 'submission2'] else 'submission2'
        temp_path = output_dir / 'temp_merged_submission.tsv'
        
        averaged_path = merge_submissions_outer(
            submission1_path=valid_files[0],
            submission2_path=valid_files[1],
            output_path=str(temp_path),
            prefer=prefer
        )
    else:
        # Use ensemble/averaging methods
        logger.info(f"Ensembling submissions using method: {ensemble_method}...")
        temp_path = output_dir / 'temp_averaged_submission.tsv'
        
        averaged_path = average_submissions(
            submission_files=valid_files,
            weights=weights,
            output_path=str(temp_path),
            ensemble_method=ensemble_method,
            **ensemble_kwargs
        )
    
    # Post-process (propagation, validation, term limits)
    logger.info("Post-processing averaged submission...")
    # Use config value if extra_output_name not provided
    final_extra_output_name = get_extra_output_name(extra_output_name)
    final_path = post_process_submission(
        temp_submission_path=averaged_path,
        output_dir=output_dir,
        output_name=output_name,
        extra_output_name=final_extra_output_name
    )
    
    total_time = time.time() - start_time
    logger.info("Submission Averaging Complete!")
    logger.info(f"Total time: {total_time:.1f}s")
    logger.info(f"Final submission: {final_path}")
    
    return str(final_path)

