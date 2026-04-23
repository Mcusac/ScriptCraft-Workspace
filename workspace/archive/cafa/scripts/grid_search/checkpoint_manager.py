"""
Checkpoint management for grid search operations.
Provides reusable functions for saving, loading, and validating grid search checkpoints.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import numpy as np

from utils.logging import get_logger

logger = get_logger(__name__)


def convert_numpy_types(obj: Any) -> Any:
    """
    Convert numpy types to Python native types for JSON serialization.
    
    Args:
        obj: Object that may contain numpy types
        
    Returns:
        Object with numpy types converted to Python types
    """
    if isinstance(obj, (np.integer, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_numpy_types(item) for item in obj]
    return obj


def normalize_param_combo(hyperparams: Dict[str, Any], exclude_keys: Optional[List[str]] = None) -> Tuple:
    """
    Normalize parameter combination to a comparable tuple.
    Excludes specified keys (e.g., 'epochs') and sorts for consistent comparison.
    
    Args:
        hyperparams: Dictionary of hyperparameters
        exclude_keys: List of keys to exclude from normalization (default: ['epochs'])
        
    Returns:
        Sorted tuple of (key, value) pairs for comparison
    """
    if exclude_keys is None:
        exclude_keys = ['epochs']
    
    # Filter out excluded keys and sort for consistent comparison
    filtered = {k: v for k, v in hyperparams.items() if k not in exclude_keys}
    return tuple(sorted((k, v) for k, v in filtered.items()))


def validate_checkpoint(
    checkpoint: Dict[str, Any],
    param_grid: Dict[str, List],
    cv: Optional[int] = None,
    grid_search_epochs: Optional[int] = None
) -> Tuple[bool, Optional[str]]:
    """
    Validate that checkpoint matches current grid search settings.
    
    Args:
        checkpoint: Loaded checkpoint dictionary
        param_grid: Current parameter grid
        cv: Current CV folds setting (optional)
        grid_search_epochs: Current grid search epochs setting (optional)
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if checkpoint is compatible, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if checkpoint.get('param_grid') != param_grid:
        return False, "param_grid doesn't match current param_grid"
    
    if cv is not None and checkpoint.get('cv_folds') != cv:
        return False, "cv_folds doesn't match current cv"
    
    if grid_search_epochs is not None and checkpoint.get('grid_search_epochs') != grid_search_epochs:
        return False, "grid_search_epochs doesn't match current setting"
    
    return True, None


def save_checkpoint(
    output_dir: Path,
    model_name: str,
    ont_code: str,
    param_grid: Dict[str, List],
    all_results: List[Dict[str, Any]],
    best_params: Optional[Dict[str, Any]],
    best_score: float,
    tested_combinations: List[Dict[str, Any]],
    total_combinations: int,
    cv: int,
    grid_search_epochs: Optional[int] = None,
    **extra_metadata: Any
) -> Path:
    """
    Save checkpoint after each parameter combination completes.
    
    Args:
        output_dir: Directory to save checkpoint
        model_name: Model name for file naming
        ont_code: Ontology code
        param_grid: Parameter grid dictionary
        all_results: Results collected so far
        best_params: Best parameters found so far
        best_score: Best score found so far
        tested_combinations: List of parameter dicts already tested
        total_combinations: Total number of combinations
        cv: Number of CV folds
        grid_search_epochs: Grid search epochs setting (optional, for NN models)
        **extra_metadata: Additional metadata to include in checkpoint
        
    Returns:
        Path to saved checkpoint file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"grid_search_checkpoint_{model_name}_{ont_code}_{timestamp}.json"
    filepath = output_dir / filename
    
    checkpoint = {
        'model_name': model_name,
        'ont_code': ont_code,
        'param_grid': param_grid,
        'all_results': all_results,
        'best_params': best_params,
        'best_score': float(best_score),
        'tested_combinations': tested_combinations,
        'total_combinations': total_combinations,
        'n_combinations_tested': len(tested_combinations),
        'timestamp': datetime.now().isoformat(),
        'cv_folds': cv,
        **extra_metadata
    }
    
    # Add grid_search_epochs if provided
    if grid_search_epochs is not None:
        checkpoint['grid_search_epochs'] = grid_search_epochs
    
    # Convert numpy types to Python types for JSON serialization
    clean_checkpoint = json.loads(json.dumps(checkpoint, default=convert_numpy_types))
    
    with open(filepath, 'w') as f:
        json.dump(clean_checkpoint, f, indent=2)
    
    logger.debug(f"   💾 Checkpoint saved: {filepath}")
    return filepath


def load_checkpoint(
    checkpoint_path: Optional[Path],
    output_dir: Path,
    model_name: str,
    ont_code: str
) -> Optional[Dict[str, Any]]:
    """
    Load checkpoint file. Auto-detects latest checkpoint if path not provided.
    
    Args:
        checkpoint_path: Explicit path to checkpoint file (None = auto-detect)
        output_dir: Directory to search for checkpoints
        model_name: Model name for pattern matching
        ont_code: Ontology code for pattern matching
        
    Returns:
        Loaded checkpoint dict or None if not found
    """
    if checkpoint_path is not None:
        # Use explicit path
        if checkpoint_path.exists():
            logger.info(f"   📂 Loading checkpoint from: {checkpoint_path}")
            with open(checkpoint_path, 'r') as f:
                checkpoint = json.load(f)
            return checkpoint
        else:
            logger.warning(f"   ⚠️  Checkpoint file not found: {checkpoint_path}")
            return None
    
    # Auto-detect: find latest checkpoint matching pattern
    pattern = f"grid_search_checkpoint_{model_name}_{ont_code}_*.json"
    checkpoint_files = list(output_dir.glob(pattern))
    
    if not checkpoint_files:
        logger.info(f"   📂 No checkpoint found (pattern: {pattern})")
        return None
    
    # Sort by timestamp in filename (more reliable than file modification time)
    # Filename format: grid_search_checkpoint_{model_name}_{ont_code}_{YYYYMMDD_HHMMSS}.json
    def extract_timestamp(filepath: Path) -> str:
        """Extract timestamp from filename for sorting."""
        # Get the timestamp part: YYYYMMDD_HHMMSS
        name = filepath.stem  # filename without .json
        parts = name.split('_')
        if len(parts) >= 6:
            # Format: grid_search_checkpoint_{model}_{ont}_{date}_{time}
            # Join last two parts (date and time)
            return '_'.join(parts[-2:])
        return '00000000_000000'  # Fallback for malformed names
    
    checkpoint_files.sort(key=extract_timestamp, reverse=True)
    latest_checkpoint = checkpoint_files[0]
    
    logger.info(f"   📂 Auto-detected checkpoint: {latest_checkpoint.name}")
    with open(latest_checkpoint, 'r') as f:
        checkpoint = json.load(f)
    
    return checkpoint

