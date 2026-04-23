# ensemble.py
# Ensemble command builder
#
# Builds CLI command list for ensemble pipeline

import sys
import json
from typing import List, Optional, Dict

from utils.system.io.paths import get_run_py_path, get_data_root_path, get_output_path


def build_ensemble_command(
    model: str,
    model_paths: List[str],
    method: str = 'weighted_average',
    score_type: str = 'cv',
    data_root: Optional[str] = None,
    log_file: Optional[str] = None,
    submission_scores: Optional[Dict[str, float]] = None,
    dataset_type: Optional[str] = None
) -> List[str]:
    """
    Build command list for ensemble pipeline.
    
    Args:
        model: Model architecture name (e.g., 'efficientnet_b3')
        model_paths: List of model directory paths (containing best_model.pth and model_metadata.json)
        method: Ensembling method ('simple_average', 'weighted_average', 'ranked_average', 'percentile_average')
        score_type: Score type for weighting ('cv', 'submission', 'combined')
        data_root: Data root directory (auto-detected if None)
        log_file: Log file path (auto-generated if None)
        submission_scores: Optional dict mapping model paths to submission scores
        dataset_type: Dataset type ('full' or 'split')
        
    Returns:
        List of command arguments ready for subprocess execution
    """
    if data_root is None:
        data_root = get_data_root_path()
    
    if log_file is None:
        log_file = get_output_path('ensemble_output.log')
    
    run_py = get_run_py_path()
    
    cmd = [
        sys.executable,
        run_py,
        'ensemble',
        '--data-root', data_root,
        '--model', model,
        '--model-paths', ','.join(model_paths),
        '--method', method,
        '--score-type', score_type,
        '--log-file', log_file
    ]
    
    # Add submission scores if provided
    if submission_scores:
        cmd.extend(['--submission-scores', json.dumps(submission_scores)])
    
    # Add dataset type if provided
    if dataset_type:
        cmd.extend(['--dataset-type', dataset_type])
    
    return cmd

