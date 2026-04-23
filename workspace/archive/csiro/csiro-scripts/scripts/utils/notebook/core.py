# core.py
# Core foundation utilities for notebook cells
#
# Provides basic utilities used across notebook operations:
# - Cell execution wrapper
# - Configuration formatting
# - Math utilities
# - GPU memory status display
# - Model type detection

import logging
import sys
from pathlib import Path
from typing import Dict, Any, List, Callable, Optional

from utils.system.io.paths import is_kaggle_environment, get_output_path
from utils import run_command_with_streaming

logger = logging.getLogger(__name__)


def calculate_total_combinations(param_grid: Dict[str, List[Any]]) -> int:
    """
    Calculate total number of combinations from a parameter grid.
    
    Args:
        param_grid: Dictionary mapping parameter names to lists of values
        
    Returns:
        Total number of combinations (product of all list lengths)
    """
    total = 1
    for values in param_grid.values():
        total *= len(values)
    return total


def print_gpu_memory_status() -> None:
    """
    Log GPU memory status if available.
    
    Gracefully handles missing torch or CUDA. Only logs in Kaggle environment.
    """
    if not is_kaggle_environment():
        return
    
    try:
        import torch
        if torch.cuda.is_available():
            from utils.system.constants import BYTES_PER_GB
            allocated = torch.cuda.memory_allocated() / BYTES_PER_GB
            reserved = torch.cuda.memory_reserved() / BYTES_PER_GB
            logger.info(f"📊 GPU Memory Status (before grid search):")
            logger.info(f"   Allocated: {allocated:.2f} GB")
            logger.info(f"   Reserved: {reserved:.2f} GB")
    except ImportError:
        # torch not available - skip GPU memory check
        pass
    except (RuntimeError, AttributeError) as e:
        # CUDA errors or attribute access issues - log but don't fail
        logger.debug(f"Could not check GPU memory status: {e}")
    except Exception as e:
        # Catch any other unexpected errors - log but don't fail
        logger.debug(f"Unexpected error checking GPU memory: {e}", exc_info=True)


def run_notebook_cell(
    cell_id: str,
    run_cells: Dict[str, bool],
    cell_function: Callable[[], None]
) -> None:
    """
    Execute a notebook cell if enabled in RUN_CELLS configuration.
    
    Checks RUN_CELLS dict and cell ID, prints skip message if disabled,
    executes callback function if enabled, and handles exceptions with context.
    
    Args:
        cell_id: Cell identifier (e.g., '1a', '2a')
        run_cells: Dictionary mapping cell IDs to boolean execution flags
        cell_function: Callback function to execute if cell is enabled
        
    Raises:
        Any exception raised by cell_function, with cell context added
    """
    if not run_cells.get(cell_id, False):
        logger.info(f"⏭️  Cell {cell_id} skipped (RUN_CELLS['{cell_id}'] = False)")
        return
    
    try:
        cell_function()
    except Exception as e:
        # Log the error once with context, then re-raise original exception
        # This avoids duplicate traceback printing
        logger.error(f"Cell {cell_id} failed: {str(e)}")
        raise


def print_config_section(title: str, config: Dict[str, Any]) -> None:
    """
    Log a formatted configuration section with consistent header formatting.
    
    Args:
        title: Section title
        config: Dictionary of configuration key-value pairs to display
                None values are skipped
    """
    logger.info("="*60)
    logger.info(title)
    logger.info(f"{'='*60}")
    for key, value in config.items():
        if value is not None:
            logger.info(f"   {key}: {value}")
    logger.info(f"{'='*60}\n")


def _detect_model_type(model: str) -> str:
    """
    Detect model type from model path/name.
    
    Args:
        model: Model architecture name or path
        
    Returns:
        Model type string: 'dinov2_hf' or 'timm'
        
    Note:
        DINOv2Model now only supports HuggingFace format. For timm-format models,
        use TimmModel instead.
    """
    model_lower = model.lower()
    
    # Check for DINOv2 (only HuggingFace format supported)
    if 'dinov2' in model_lower or 'dinov3' in model_lower:
        # DINOv2Model only supports HuggingFace format (contains '/' or is a directory path)
        if '/' in model or (Path(model).exists() and Path(model).is_dir()):
            return 'dinov2_hf'
        else:
            # Not a valid HuggingFace path - raise error
            raise ValueError(
                f"DINOv2Model only supports HuggingFace format. "
                f"Model '{model}' does not appear to be a HuggingFace path. "
                f"Use TimmModel for timm-format models."
            )
    
    # Default to timm (EfficientNet, etc.)
    return 'timm'


def handle_command_result(
    returncode: int,
    stdout_lines: List[str],
    operation_name: str,
    log_file: Optional[str] = None
) -> None:
    """
    Handle command execution result with consistent error handling.
    
    Checks returncode and raises RuntimeError with formatted message if non-zero.
    Provides consistent error messaging across all notebook cells.
    
    Args:
        returncode: Process return code (0 = success, non-zero = failure)
        stdout_lines: Last N lines of stdout output
        operation_name: Name of the operation (e.g., 'Pipeline', 'Grid search')
        log_file: Optional log file path (for error messages)
        
    Raises:
        RuntimeError: If returncode is non-zero, with formatted error message
    """
    if returncode != 0:
        # Build error message without duplicating traceback info already in stdout_lines
        error_msg = f"{operation_name} failed with return code {returncode}"
        if stdout_lines:
            # Only append output if it doesn't already contain the full traceback
            # This prevents duplicate traceback printing
            error_msg += f"\n\nOutput:\n" + "\n".join(stdout_lines)
        if log_file:
            error_msg += f"\n\nFull output available in: {log_file}"
        raise RuntimeError(error_msg)


def execute_submission_pipeline(
    cmd: List[str],
    model: str,
    dataset_type: Optional[str] = None,
    model_type_description: Optional[str] = None
) -> None:
    """
    Execute submission pipeline with consistent error handling and messaging.
    
    Runs the submission command, handles success/failure with consistent messaging,
    and prints submission file location.
    
    Args:
        cmd: Command list to execute
        model: Model architecture name (for display)
        dataset_type: Optional dataset type ('full' or 'split')
        model_type_description: Optional description of model type (e.g., 'Regression model type: lgbm')
        
    Raises:
        RuntimeError: If submission fails
    """
    # Print submission info
    logger.info(f"📤 Generating submission")
    logger.info(f"   Model architecture: {model}")
    if model_type_description:
        logger.info(f"   {model_type_description}")
    if dataset_type:
        logger.info(f"   Dataset type: {dataset_type}")
    logger.info(f"   {'='*60}\n")
    
    # Run submission pipeline
    returncode, stdout_lines = run_command_with_streaming(cmd)
    
    if returncode == 0:
        logger.info("="*60)
        logger.info("✅ Submission generated successfully!")
        logger.info("="*60)
        submission_path = get_output_path('submission.csv')
        logger.info(f"\n📋 Output: {submission_path}")
        if is_kaggle_environment():
            logger.info("   Also available at: /kaggle/working/submission.csv")
        logger.info("   Ready to submit to Kaggle competition")
    else:
        error_msg = f"\n❌ Submission failed with return code {returncode}"
        if stdout_lines:
            error_msg += f"\n   Check logs above for details"
        logger.error(error_msg)
        sys.exit(1)

