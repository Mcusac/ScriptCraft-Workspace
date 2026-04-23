# regression_ensemble.py
# Regression ensemble command builder
#
# Builds CLI command list for regression ensemble pipeline

import sys
import json
from typing import List, Dict, Any

from utils.system.io.paths import get_run_py_path, get_data_root_path, get_output_path


def build_regression_ensemble_command(
    ensemble_config: Dict[str, Any],
    data_root: str = None,
    log_file: str = None,
    dataset_type: str = None
) -> List[str]:
    """
    Build command list for regression ensemble pipeline.
    
    Args:
        ensemble_config: Configuration dict with model_types, model_indices, method, score_type
        data_root: Data root directory (auto-detected if None)
        log_file: Log file path (auto-generated if None)
        dataset_type: Dataset type ('full' or 'split')
        
    Returns:
        List of command arguments ready for subprocess execution
    """
    if data_root is None:
        data_root = get_data_root_path()
    
    if log_file is None:
        log_file = get_output_path('regression_ensemble_output.log')
    
    run_py = get_run_py_path()
    
    cmd = [
        sys.executable,
        run_py,
        'regression_ensemble',
        '--data-root', data_root,
        '--ensemble-config', json.dumps(ensemble_config),
        '--log-file', log_file
    ]
    
    if dataset_type:
        cmd.extend(['--dataset-type', dataset_type])
    
    return cmd
