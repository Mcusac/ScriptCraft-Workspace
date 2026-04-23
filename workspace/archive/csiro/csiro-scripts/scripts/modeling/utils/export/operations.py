# model_export_utils.py
# Utilities for exporting and preparing models for download/submission
#
# This module provides both atomic operations and scenario-specific export functions.
# Atomic operations (at bottom) perform single, focused tasks.
# Scenario-specific functions (at top) orchestrate atomic operations for specific use cases.
#
# Architecture:
# - Atomic operations: copy_model_checkpoint, write_metadata_file, copy_results_file
# - Scenario functions: export_from_training_dir, export_from_grid_search, export_from_single_checkpoint

import shutil
import logging
from pathlib import Path
from typing import Dict, Any

from ...training.utils.results import find_trained_model_path
from utils.system.io import save_json_file
from config.config import Config

logger = logging.getLogger(__name__)


# ============================================================================
# Scenario-Specific Export Functions
# ============================================================================

def export_from_training_dir(
    model_dir: Path,
    export_dir: Path,
    metadata: Dict[str, Any]
) -> None:
    """
    Export model from just-trained model directory.
    
    This function handles the export of models from a training directory
    structure (fold_0/, fold_1/, etc.) to a flat export structure.
    Supports both regular PyTorch checkpoints and feature extraction regression models.
    
    Args:
        model_dir: Base model directory containing fold checkpoints
        export_dir: Destination directory for export
        metadata: Complete metadata dictionary
        
    Raises:
        FileNotFoundError: If model checkpoint not found
        RuntimeError: If export fails
    """
    # Find model checkpoint
    model_path, best_fold_used = find_trained_model_path(model_dir, metadata.get('best_fold'))
    
    # Ensure metadata has correct best_fold
    metadata['best_fold'] = best_fold_used
    
    # Determine export filename based on model type
    if model_path.suffix == '.pkl':
        # Feature extraction regression model
        export_filename = 'regression_model.pkl'
    else:
        # Regular PyTorch checkpoint
        export_filename = 'best_model.pth'
    
    # Perform atomic export operations
    copy_model_checkpoint(model_path, export_dir / export_filename)
    write_metadata_file(metadata, export_dir / 'model_metadata.json')
    
    logger.info("✅ Model exported from training directory")
    logger.info(f"   Model: {export_dir / export_filename}")
    logger.info(f"   Metadata: {export_dir / 'model_metadata.json'}")


def export_from_grid_search(
    variant_id: str,
    best_fold: int,
    export_dir: Path,
    metadata: Dict[str, Any],
    config: Config
) -> None:
    """
    Export model from grid search structure.
    
    Args:
        variant_id: Variant ID (e.g., 'combo_0000', 'variant_0067')
        best_fold: Best fold number
        export_dir: Destination directory for export
        metadata: Complete metadata dictionary
        config: Configuration object with paths
        
    Raises:
        FileNotFoundError: If model checkpoint not found
    """
    from ..finding import GridSearchModelFinder
    
    # Find model using centralized finder
    finder = GridSearchModelFinder()
    model_path = finder.find_model(
        variant_id=variant_id,
        best_fold=best_fold,
        config=config
    )
    
    # Perform atomic export operations
    copy_model_checkpoint(model_path, export_dir / 'best_model.pth')
    write_metadata_file(metadata, export_dir / 'model_metadata.json')
    
    logger.info("✅ Model exported from grid search")
    logger.info(f"   Variant: {variant_id}, Fold: {best_fold}")
    logger.info(f"   Model: {export_dir / 'best_model.pth'}")


def export_from_single_checkpoint(
    checkpoint_path: Path,
    export_dir: Path,
    metadata: Dict[str, Any]
) -> None:
    """
    Export model from a single checkpoint file.
    
    Args:
        checkpoint_path: Path to source checkpoint file
        export_dir: Destination directory for export
        metadata: Complete metadata dictionary
        
    Raises:
        FileNotFoundError: If checkpoint doesn't exist
    """
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")
    
    # Perform atomic export operations
    copy_model_checkpoint(checkpoint_path, export_dir / 'best_model.pth')
    write_metadata_file(metadata, export_dir / 'model_metadata.json')
    
    logger.info("✅ Model exported from checkpoint")
    logger.info(f"   Source: {checkpoint_path}")
    logger.info(f"   Destination: {export_dir}")


# ============================================================================
# Historical Note: Legacy Functions Removed
# ============================================================================
# The following legacy functions were removed in a previous refactoring.
# Use modern export functions instead:
# - prepare_best_model_for_download() -> use export_from_grid_search() + MetadataBuilder
# - export_single_training_model() -> use export_from_training_dir() or export_from_single_checkpoint()


# ============================================================================
# Atomic Operations
# ============================================================================

def copy_model_checkpoint(source: Path, dest: Path) -> None:
    """
    Atomic operation: Copy model checkpoint file.
    
    This is a single-responsibility function that only copies a checkpoint file.
    It does not handle directory creation, metadata, or validation.
    
    Args:
        source: Path to source checkpoint file
        dest: Path to destination checkpoint file (must include filename)
        
    Raises:
        FileNotFoundError: If source doesn't exist
        OSError: If copy fails
    """
    if not source.exists():
        raise FileNotFoundError(f"Source checkpoint not found: {source}")
    
    # Ensure destination directory exists
    dest.parent.mkdir(parents=True, exist_ok=True)
    
    # Copy file
    shutil.copy2(source, dest)
    logger.debug(f"Copied checkpoint: {source} -> {dest}")


def write_metadata_file(metadata: Dict[str, Any], dest: Path) -> None:
    """
    Atomic operation: Write metadata dictionary to JSON file.
    
    This is a single-responsibility function that only writes metadata.
    It does not handle directory creation or validation.
    
    Args:
        metadata: Metadata dictionary to write
        dest: Path to destination JSON file (must include filename)
        
    Raises:
        OSError: If write fails
    """
    # Ensure destination directory exists
    dest.parent.mkdir(parents=True, exist_ok=True)
    
    # Write JSON file using centralized utility
    save_json_file(metadata, dest, file_type="Model metadata JSON")
    logger.debug(f"Wrote metadata: {dest}")


def copy_results_file(source: Path, dest: Path) -> None:
    """
    Atomic operation: Copy results.json file.
    
    This is a single-responsibility function that only copies a results file.
    It does not handle directory creation or validation.
    
    Args:
        source: Path to source results.json file
        dest: Path to destination results.json file (must include filename)
        
    Raises:
        FileNotFoundError: If source doesn't exist
        OSError: If copy fails
    """
    if not source.exists():
        raise FileNotFoundError(f"Source results file not found: {source}")
    
    # Ensure destination directory exists
    dest.parent.mkdir(parents=True, exist_ok=True)
    
    # Copy file
    shutil.copy2(source, dest)
    logger.debug(f"Copied results file: {source} -> {dest}")
