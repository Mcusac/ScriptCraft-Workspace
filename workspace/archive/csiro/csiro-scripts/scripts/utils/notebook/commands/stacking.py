# stacking.py
# Stacking command builder
#
# Builds CLI command list for stacking pipeline

import sys
import json
from typing import List, Dict, Any

from utils.system.io.paths import get_run_py_path, get_data_root_path, get_output_path


def build_stacking_command(
    stacking_config: Dict[str, Any],
    data_root: str = None,
    log_file: str = None,
    dataset_type: str = None
) -> List[str]:
    """
    Build command list for stacking pipeline.
    
    Args:
        stacking_config: Configuration dict with model_types, model_indices, meta_model_alpha, n_folds
        data_root: Data root directory (auto-detected if None)
        log_file: Log file path (auto-generated if None)
        dataset_type: Dataset type ('full' or 'split')
        
    Returns:
        List of command arguments ready for subprocess execution
    """
    if data_root is None:
        data_root = get_data_root_path()
    
    if log_file is None:
        log_file = get_output_path('stacking_output.log')
    
    run_py = get_run_py_path()
    
    cmd = [
        sys.executable,
        run_py,
        'stacking',
        '--data-root', data_root,
        '--stacking-config', json.dumps(stacking_config),
        '--log-file', log_file
    ]
    
    if dataset_type:
        cmd.extend(['--dataset-type', dataset_type])
    
    return cmd


def build_stacking_ensemble_command(
    stacking_ensemble_config: Dict[str, Any],
    data_root: str = None,
    log_file: str = None,
    dataset_type: str = None
) -> List[str]:
    """
    Build command list for stacking ensemble pipeline.
    
    Args:
        stacking_ensemble_config: Configuration dict with model_types, ensemble_configs, meta_model_alpha, n_folds
        data_root: Data root directory (auto-detected if None)
        log_file: Log file path (auto-generated if None)
        dataset_type: Dataset type ('full' or 'split')
        
    Returns:
        List of command arguments ready for subprocess execution
    """
    if data_root is None:
        data_root = get_data_root_path()
    
    if log_file is None:
        log_file = get_output_path('stacking_ensemble_output.log')
    
    run_py = get_run_py_path()
    
    cmd = [
        sys.executable,
        run_py,
        'stacking_ensemble',
        '--data-root', data_root,
        '--stacking-ensemble-config', json.dumps(stacking_ensemble_config),
        '--log-file', log_file
    ]
    
    if dataset_type:
        cmd.extend(['--dataset-type', dataset_type])
    
    return cmd


def build_hybrid_stacking_command(
    hybrid_stacking_config: Dict[str, Any],
    data_root: str = None,
    log_file: str = None,
    dataset_type: str = None
) -> List[str]:
    """
    Build command list for hybrid stacking pipeline.
    
    Args:
        hybrid_stacking_config: Configuration dict with regression_ensembles, end_to_end_ensembles, meta_model_alpha, n_folds
        data_root: Data root directory (auto-detected if None)
        log_file: Log file path (auto-generated if None)
        dataset_type: Dataset type ('full' or 'split')
        
    Returns:
        List of command arguments ready for subprocess execution
    """
    if data_root is None:
        data_root = get_data_root_path()
    
    if log_file is None:
        log_file = get_output_path('hybrid_stacking_output.log')
    
    run_py = get_run_py_path()
    
    cmd = [
        sys.executable,
        run_py,
        'hybrid_stacking',
        '--data-root', data_root,
        '--hybrid-stacking-config', json.dumps(hybrid_stacking_config),
        '--log-file', log_file
    ]
    
    if dataset_type:
        cmd.extend(['--dataset-type', dataset_type])
    
    return cmd
