# grid_search.py
# Grid search command builders
#
# Builds CLI command lists for various grid search pipelines:
# - Hyperparameter grid search
# - Dataset grid search
# - Regression grid search

import sys
from typing import List, Optional

from utils.system.io.paths import get_run_py_path, get_data_root_path, get_output_path


def build_hyperparameter_grid_search_command(
    model: str,
    search_type: str,
    data_root: Optional[str] = None,
    log_file: Optional[str] = None,
    metadata_path: Optional[str] = None,
    results_file: Optional[str] = None,
    previous_results_file: Optional[str] = None,
    dataset_type: Optional[str] = None
) -> List[str]:
    """
    Build command list for hyperparameter grid search.
    
    Args:
        model: Model architecture name (e.g., 'efficientnet_b3')
        search_type: Grid search type ('defaults', 'quick', 'in_depth', 'thorough', 'focused_in_depth', or 'focused_thorough')
        data_root: Data root directory (auto-detected if None)
        log_file: Log file path (auto-generated if None)
        metadata_path: Optional path to model_metadata.json
        results_file: Optional path to results.json (fallback for metadata)
        previous_results_file: Optional path to previous hyperparameter grid search results.json
                              (required for focused search types)
        
    Returns:
        List of command arguments ready for subprocess execution
    """
    if data_root is None:
        data_root = get_data_root_path()
    
    if log_file is None:
        log_file = get_output_path('hyperparameter_grid_search_output.log')
    
    run_py = get_run_py_path()
    
    cmd = [
        sys.executable,
        run_py,
        'hyperparameter_grid_search',
        '--data-root', data_root,
        '--model', model,
        '--search-type', search_type,
        '--log-file', log_file
    ]
    
    # Add metadata path if provided
    if metadata_path:
        cmd.extend(['--metadata-path', metadata_path])
    elif results_file:
        cmd.extend(['--results-file', results_file])
    
    # Add previous results file for focused searches
    if previous_results_file:
        cmd.extend(['--previous-results-file', previous_results_file])
    
    # Add dataset type if provided
    if dataset_type:
        cmd.extend(['--dataset-type', dataset_type])
    
    return cmd


def build_dataset_grid_search_command(
    model: str,
    data_root: Optional[str] = None,
    log_file: Optional[str] = None,
    dataset_type: Optional[str] = None
) -> List[str]:
    """
    Build command list for dataset grid search.
    
    Args:
        model: Model architecture name (e.g., 'efficientnet_b3')
        data_root: Data root directory (auto-detected if None)
        log_file: Log file path (auto-generated if None)
        dataset_type: Dataset type ('split' or 'full', default: 'split')
        
    Returns:
        List of command arguments ready for subprocess execution
    """
    if data_root is None:
        data_root = get_data_root_path()
    
    if log_file is None:
        log_file = get_output_path('grid_search_output.log')
    
    run_py = get_run_py_path()
    
    cmd = [
        sys.executable,
        run_py,
        'dataset_grid_search',
        '--data-root', data_root,
        '--model', model,
        '--preprocessing', '',  # Empty = test all preprocessing combinations
        '--data-augmentation', '',  # Empty = test all augmentation combinations
        '--log-file', log_file
    ]
    
    # Add dataset type if provided
    if dataset_type:
        cmd.extend(['--dataset-type', dataset_type])
    
    return cmd


def build_regression_grid_search_command(
    feature_filename: str,
    regression_model_type: str,
    search_type: str = 'quick',
    data_root: Optional[str] = None,
    log_file: Optional[str] = None
) -> List[str]:
    """
    Build command list for regression grid search.
    
    Args:
        feature_filename: Feature filename (e.g., 'variant_0100_features.npz')
        regression_model_type: Type of regression model ('lgbm', 'xgboost', 'ridge')
        search_type: Grid search type ('defaults', 'quick', 'in_depth', 'thorough')
        data_root: Optional data root directory
        log_file: Optional log file path
    
    Returns:
        List of command arguments for subprocess
    """
    run_py = get_run_py_path()
    cmd = [sys.executable, str(run_py), 'regression_grid_search']
    
    cmd.extend(['--feature-filename', feature_filename])
    cmd.extend(['--regression-model-type', regression_model_type])
    cmd.extend(['--search-type', search_type])
    
    if data_root:
        cmd.extend(['--data-root', data_root])
    
    if log_file:
        cmd.extend(['--log-file', log_file])
    
    return cmd

