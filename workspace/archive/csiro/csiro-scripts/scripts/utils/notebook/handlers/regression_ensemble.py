# regression_ensemble.py
# Regression ensemble result handler
#
# Handles results from regression ensemble pipeline execution

import logging
from typing import Dict, Any, List

from ..core import handle_command_result

logger = logging.getLogger(__name__)


def handle_regression_ensemble_result(
    returncode: int,
    stdout_lines: List[str],
    log_file: str,
    ensemble_config: Dict[str, Any]
) -> None:
    """
    Handle regression ensemble pipeline result.
    
    Args:
        returncode: Process return code
        stdout_lines: Standard output lines
        log_file: Log file path
        ensemble_config: Ensemble configuration used
    """
    if returncode != 0:
        logger.error(f"Regression ensemble pipeline failed with return code {returncode}")
        handle_command_result(returncode, stdout_lines, "Regression ensemble pipeline")
        return
    
    logger.info("="*60)
    logger.info("Regression Ensemble Pipeline Completed Successfully")
    logger.info("="*60)
    logger.info(f"  Model types: {ensemble_config.get('model_types', [])}")
    logger.info(f"  Method: {ensemble_config.get('method', 'weighted_average')}")
    logger.info(f"  Log file: {log_file}")
    logger.info("\n✅ Submission file generated successfully!")
    logger.info("   Check output directory for submission.csv")
