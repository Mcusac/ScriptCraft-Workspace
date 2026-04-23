# ensemble.py
# Ensemble result handler
#
# Handles results from ensemble pipeline

import logging
from typing import List

from utils.system.io.paths import get_output_path, is_kaggle_environment
from ..core import handle_command_result

logger = logging.getLogger(__name__)


def handle_ensemble_result(
    returncode: int,
    stdout_lines: List[str],
    log_file: str,
    model_paths: List[str],
    method: str,
    score_type: str,
    model: str
) -> None:
    """
    Handle result from ensemble pipeline.
    
    Raises RuntimeError if returncode is non-zero, otherwise prints success message
    with ensemble details.
    
    Args:
        returncode: Process return code
        stdout_lines: Last N lines of stdout output
        log_file: Path to log file (for error messages)
        model_paths: List of model paths used in ensemble
        method: Ensembling method used
        score_type: Score type used for weighting
        model: Model architecture name
        
    Raises:
        RuntimeError: If returncode is non-zero
    """
    # Handle errors using standard handler
    handle_command_result(returncode, stdout_lines, "Ensemble pipeline", log_file)
    
    # Success message
    logger.info("="*60)
    logger.info("✅ Ensemble submission generated successfully!")
    logger.info("="*60)
    logger.info(f"\n📊 Ensemble details:")
    logger.info(f"   Models used: {len(model_paths)}")
    logger.info(f"   Method: {method}")
    logger.info(f"   Score type: {score_type}")
    logger.info(f"   Model architecture: {model}")
    logger.info(f"\n📁 Submission saved to:")
    if is_kaggle_environment():
        logger.info(f"   /kaggle/working/submission.csv")
    logger.info(f"   {get_output_path('submission.csv')}")
    logger.info(f"\n📥 Next steps:")
    logger.info("   1. Review submission.csv")
    logger.info("   2. Submit to Kaggle competition")
