# stacking.py
# Stacking result handler
#
# Handles results from stacking pipeline execution

import logging
from typing import Dict, Any, List

from ..core import handle_command_result

logger = logging.getLogger(__name__)


def handle_stacking_result(
    returncode: int,
    stdout_lines: List[str],
    log_file: str,
    stacking_config: Dict[str, Any]
) -> None:
    """
    Handle stacking pipeline result.
    
    Args:
        returncode: Process return code
        stdout_lines: Standard output lines
        log_file: Log file path
        stacking_config: Stacking configuration used
    """
    if returncode != 0:
        logger.error(f"Stacking pipeline failed with return code {returncode}")
        handle_command_result(returncode, stdout_lines, "Stacking pipeline")
        return
    
    logger.info("="*60)
    logger.info("Stacking Pipeline Completed Successfully")
    logger.info("="*60)
    logger.info(f"  Model types: {stacking_config.get('model_types', [])}")
    logger.info(f"  Meta-model alpha: {stacking_config.get('meta_model_alpha', 10.0)}")
    logger.info(f"  Number of folds: {stacking_config.get('n_folds', 5)}")
    logger.info(f"  Log file: {log_file}")
    logger.info("\n✅ Submission file generated successfully!")
    logger.info("   Check output directory for submission.csv")


def handle_stacking_ensemble_result(
    returncode: int,
    stdout_lines: List[str],
    log_file: str,
    stacking_ensemble_config: Dict[str, Any]
) -> None:
    """
    Handle stacking ensemble pipeline result.
    
    Args:
        returncode: Process return code
        stdout_lines: Standard output lines
        log_file: Log file path
        stacking_ensemble_config: Stacking ensemble configuration used
    """
    if returncode != 0:
        logger.error(f"Stacking ensemble pipeline failed with return code {returncode}")
        handle_command_result(returncode, stdout_lines, "Stacking ensemble pipeline")
        return
    
    logger.info("="*60)
    logger.info("Stacking Ensemble Pipeline Completed Successfully")
    logger.info("="*60)
    logger.info(f"  Model types: {stacking_ensemble_config.get('model_types', [])}")
    logger.info(f"  Meta-model alpha: {stacking_ensemble_config.get('meta_model_alpha', 10.0)}")
    logger.info(f"  Number of folds: {stacking_ensemble_config.get('n_folds', 5)}")
    logger.info(f"  Log file: {log_file}")
    logger.info("\n✅ Submission file generated successfully!")
    logger.info("   Check output directory for submission.csv")


def handle_hybrid_stacking_result(
    returncode: int,
    stdout_lines: List[str],
    log_file: str,
    hybrid_stacking_config: Dict[str, Any]
) -> None:
    """
    Handle hybrid stacking pipeline result.
    
    Args:
        returncode: Process return code
        stdout_lines: Standard output lines
        log_file: Log file path
        hybrid_stacking_config: Hybrid stacking configuration used
    """
    if returncode != 0:
        logger.error(f"Hybrid stacking pipeline failed with return code {returncode}")
        handle_command_result(returncode, stdout_lines, "Hybrid stacking pipeline")
        return
    
    regression_ensembles = hybrid_stacking_config.get('regression_ensembles', {})
    end_to_end_ensembles = hybrid_stacking_config.get('end_to_end_ensembles', {})
    
    logger.info("="*60)
    logger.info("Hybrid Stacking Pipeline Completed Successfully")
    logger.info("="*60)
    logger.info(f"  Regression ensembles: {regression_ensembles.get('model_types', [])}")
    logger.info(f"  End-to-end ensembles: {end_to_end_ensembles.get('model_name', 'N/A')}")
    logger.info(f"  Meta-model alpha: {hybrid_stacking_config.get('meta_model_alpha', 10.0)}")
    logger.info(f"  Number of folds: {hybrid_stacking_config.get('n_folds', 5)}")
    logger.info(f"  Log file: {log_file}")
    logger.info("\n✅ Submission file generated successfully!")
    logger.info("   Check output directory for submission.csv")
