# train_export.py
# Train/export command builders
#
# Builds CLI command lists for training and export pipelines:
# - End-to-end training (Cell 2a)
# - Feature extraction + regression training (Cell 2b)
# - Multi-variant regression training (Cell 2c)

import sys
from typing import List, Optional

from utils.system.io.paths import get_run_py_path, get_data_root_path


def build_train_and_export_command(
    model: str,
    results_file: str,
    dataset_type: str,
    data_root: Optional[str] = None,
    selected_variant_id: Optional[str] = None,
    fresh_train: bool = False,
    export_only: bool = False
) -> List[str]:
    """
    Build command list for end-to-end train and export pipeline (Cell 2a).
    
    Args:
        model: Model architecture name (e.g., 'efficientnet_b3')
        results_file: Path to grid search results.json file
        dataset_type: Dataset type ('full' or 'split')
        data_root: Data root directory (auto-detected if None)
        selected_variant_id: Optional variant ID to use instead of best
        fresh_train: Whether to start fresh (delete directory if all folds complete)
        export_only: Whether to skip training and just export existing model
        
    Returns:
        List of command arguments ready for subprocess execution
    """
    if data_root is None:
        data_root = get_data_root_path()
    
    run_py = get_run_py_path()
    
    cmd = [
        sys.executable,
        run_py,
        'train_and_export',
        '--data-root', data_root,
        '--model', model,
        '--results-file', results_file,
        '--dataset-type', dataset_type,
    ]
    
    # Add --variant-id if specified (otherwise uses best variant)
    if selected_variant_id:
        cmd.extend(['--variant-id', selected_variant_id])
    
    # Add flags based on mode (mutually exclusive)
    if export_only:
        cmd.append('--export-only')
    elif fresh_train:
        cmd.append('--fresh-train')
    
    return cmd


def build_feature_extraction_train_command(
    model: str,
    feature_extraction_model: str,
    regression_model_type: str,
    dataset_type: str,
    data_root: Optional[str] = None,
    regression_model_variant_id: Optional[str] = None,
    extract_features: bool = True,
    fresh_train: bool = False,
    export_only: bool = False,
    data_manipulation_combo: Optional[str] = None
) -> List[str]:
    """
    Build command list for feature extraction + regression training pipeline (Cell 2b).
    
    Args:
        model: Model architecture name (e.g., 'efficientnet_b3')
        feature_extraction_model: Model for feature extraction (e.g., 'dinov2_base', 'timm_efficientnet_b3', or path like '/kaggle/input/dinov2/pytorch/base/1'). Model names are automatically converted to pretrained paths.
        regression_model_type: Regression model type ('lgbm', 'xgboost', 'ridge')
        dataset_type: Dataset type ('full' or 'split')
        data_root: Data root directory (auto-detected if None)
        regression_model_variant_id: Optional regression model variant ID to use instead of best
        extract_features: Whether to extract features from scratch (True) or load from cache (False)
        fresh_train: Whether to start fresh (delete directory if all folds complete)
        export_only: Whether to skip training and just export existing model
        data_manipulation_combo: Optional combo ID (e.g., 'combo_00', 'combo_63') to use for data prep
        
    Returns:
        List of command arguments ready for subprocess execution
    """
    if data_root is None:
        data_root = get_data_root_path()
    
    run_py = get_run_py_path()
    
    cmd = [
        sys.executable,
        run_py,
        'train_and_export',
        '--data-root', data_root,
        '--model', model,
        '--dataset-type', dataset_type,
        '--feature-extraction-mode',  # Enable feature extraction mode
        '--feature-extraction-model', feature_extraction_model,
        '--regression-model-type', regression_model_type,
    ]
    
    # Add --regression-model-variant-id if provided
    if regression_model_variant_id is not None:
        cmd.extend(['--regression-model-variant-id', regression_model_variant_id])
    
    # Add --extract-features flag based on extract_features parameter
    if extract_features:
        cmd.append('--extract-features')
    else:
        cmd.append('--no-extract-features')
    
    # Add --data-manipulation-combo if provided
    if data_manipulation_combo:
        cmd.extend(['--data-manipulation-combo', data_manipulation_combo])
    
    # Add flags based on mode (mutually exclusive)
    if export_only:
        cmd.append('--export-only')
    elif fresh_train:
        cmd.append('--fresh-train')
    
    return cmd


def build_multi_variant_regression_train_command(
    model: str,
    feature_extraction_model: str,
    regression_model_type: str,
    model_ids: List[str],
    dataset_type: str,
    data_root: Optional[str] = None,
    extract_features: bool = True,
    fresh_train: bool = False,
    data_manipulation_combo: Optional[str] = None
) -> List[str]:
    """
    Build command list for multi-variant regression training pipeline (Cell 2c).
    
    Args:
        model: Model architecture name (e.g., 'efficientnet_b3')
        feature_extraction_model: Model for feature extraction (e.g., 'dinov2_base')
        regression_model_type: Regression model type ('lgbm', 'xgboost', 'ridge')
        model_ids: List of model_id strings from gridsearch_metadata.json (e.g., ["080", "083", "086"])
        dataset_type: Dataset type ('full' or 'split')
        data_root: Data root directory (auto-detected if None)
        extract_features: Whether to extract features from scratch (True) or load from cache (False)
        fresh_train: Whether to start fresh (delete directory if all folds complete)
        data_manipulation_combo: Optional combo ID (e.g., 'combo_00', 'combo_63') to use for data prep
        
    Returns:
        List of command arguments ready for subprocess execution
    """
    if data_root is None:
        data_root = get_data_root_path()
    
    run_py = get_run_py_path()
    
    # Convert model_ids to comma-separated string
    model_ids_str = ','.join(model_ids)
    
    cmd = [
        sys.executable,
        run_py,
        'multi_variant_regression_train',
        '--data-root', data_root,
        '--model', model,
        '--dataset-type', dataset_type,
        '--feature-extraction-model', feature_extraction_model,
        '--regression-model-type', regression_model_type,
        '--model-ids', model_ids_str,
    ]
    
    # Add --extract-features flag based on extract_features parameter
    if extract_features:
        cmd.append('--extract-features')
    else:
        cmd.append('--no-extract-features')
    
    # Add --data-manipulation-combo if provided
    if data_manipulation_combo:
        cmd.extend(['--data-manipulation-combo', data_manipulation_combo])
    
    # Add --fresh-train flag if specified
    if fresh_train:
        cmd.append('--fresh-train')
    
    return cmd
