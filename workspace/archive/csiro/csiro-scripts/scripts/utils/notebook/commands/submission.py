# submission.py
# Submission command builder
#
# Builds CLI command list for submission pipeline

import sys
from typing import List, Optional
from pathlib import Path

from utils.system.io.paths import get_run_py_path, get_data_root_path


def _build_base_command_parts(
    command_name: str,
    data_root: Optional[str] = None,
    dataset_type: Optional[str] = None
) -> List[str]:
    """
    Build base command parts: executable, run_py, command_name, --data-root, optionally --dataset-type.
    
    Args:
        command_name: CLI command name (e.g., 'submit')
        data_root: Data root directory (auto-detected if None)
        dataset_type: Optional dataset type ('full' or 'split')
        
    Returns:
        Base command list with no None values
    """
    if data_root is None:
        data_root = get_data_root_path()
    
    cmd = [
        str(sys.executable),
        str(get_run_py_path()),
        command_name,
        '--data-root',
        str(data_root)
    ]
    
    if dataset_type:
        cmd.extend(['--dataset-type', str(dataset_type)])
    
    return cmd


def build_end_to_end_submission_command(
    model: str,
    model_path: Optional[str] = None,
    model_name: Optional[str] = None,
    dataset_type: Optional[str] = None,
    data_root: Optional[str] = None
) -> List[str]:
    """
    Build submission command for end-to-end trained models.
    
    Args:
        model: Model architecture name (e.g., 'efficientnet_b3') - required
        model_path: Optional explicit model checkpoint path
        model_name: Optional model name for model-specific folder structure
        dataset_type: Optional dataset type ('full' or 'split')
        data_root: Optional data root directory (auto-detected if None)
        
    Returns:
        List of command arguments ready for subprocess execution
    """
    cmd = _build_base_command_parts('submit', data_root, dataset_type)
    cmd.extend(['--model', str(model)])
    
    if model_path:
        cmd.extend(['--model-path', str(model_path)])
    if model_name:
        cmd.extend(['--model-name', str(model_name)])
    
    return cmd


def build_regression_submission_command(
    model_name: str,
    model_path: Optional[str] = None,
    dataset_type: Optional[str] = None,
    data_root: Optional[str] = None
) -> List[str]:
    """
    Build submission command for regression models.
    
    Feature extraction model name is parsed from feature_filename in model metadata
    (feature_filename encodes both model_id and combo_id).
    
    Args:
        model_name: Regression model type (e.g., 'lgbm', 'xgboost', 'ridge') - required
        model_path: Optional explicit model checkpoint path
        dataset_type: Optional dataset type ('full' or 'split')
        data_root: Optional data root directory (auto-detected if None)
        
    Returns:
        List of command arguments ready for subprocess execution
    """
    cmd = _build_base_command_parts('submit', data_root, dataset_type)
    cmd.extend(['--model-name', str(model_name)])
    
    if model_path:
        cmd.extend(['--model-path', str(model_path)])
    
    return cmd


def detect_submission_model_path(
    submission_model_path: Optional[str],
    model_type: str = 'end_to_end'
) -> Optional[str]:
    """
    Detect model path for submission, checking working directory first.
    
    Checks for freshly exported models in /kaggle/working/best_model/ with priority
    over explicit paths. Handles both end-to-end and regression models.
    
    Args:
        submission_model_path: Optional explicit model path from configuration
        model_type: Model type ('end_to_end' or 'regression')
        
    Returns:
        Detected model path (string) or None if auto-detection should be used
    """
    # Check for freshly exported model (highest priority)
    working_dir = Path('/kaggle/working/best_model')
    
    if model_type == 'end_to_end':
        # Check for end-to-end model first, then regression model
        working_model = working_dir / 'best_model.pth'
        working_regression_model = working_dir / 'regression_model.pkl'
        
        if submission_model_path is None and working_model.exists():
            detected_path = str(working_model.parent)
            print(f"✅ Found freshly exported model in working directory")
            print(f"   Using: {detected_path}\n")
            return detected_path
        elif submission_model_path is None and working_regression_model.exists():
            detected_path = str(working_regression_model.parent)
            print(f"✅ Found freshly exported regression model in working directory")
            print(f"   Using: {detected_path}\n")
            return detected_path
        elif submission_model_path is None:
            print(f"🔍 Auto-detecting model from /kaggle/input/csiro-models/\n")
            return None
        else:
            print(f"📍 Using explicit model path: {submission_model_path}\n")
            return submission_model_path
    
    elif model_type == 'regression':
        # Check for regression model only
        working_regression_model = working_dir / 'regression_model.pkl'
        
        if submission_model_path is None and working_regression_model.exists():
            detected_path = str(working_regression_model.parent)
            print(f"✅ Found freshly exported regression model in working directory")
            print(f"   Using: {detected_path}\n")
            return detected_path
        elif submission_model_path is None:
            print(f"🔍 Auto-detecting regression model from /kaggle/input/csiro-models/\n")
            return None
        else:
            print(f"📍 Using explicit model path: {submission_model_path}\n")
            return submission_model_path
    
    else:
        # Unknown model type - just return explicit path or None
        if submission_model_path is None:
            print(f"🔍 Auto-detecting model from /kaggle/input/csiro-models/\n")
            return None
        else:
            print(f"📍 Using explicit model path: {submission_model_path}\n")
            return submission_model_path
