# feature_cache.py
# Feature caching utilities for saving and loading extracted features
# Allows extracting features once and reusing for multiple regression model experiments

import logging
import numpy as np
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
import json

from config.config import Config
from config.path_constants import FEATURE_CACHE_INPUT_DIR, FEATURE_CACHE_WORKING_DIR
from utils.system.io import is_kaggle_environment

logger = logging.getLogger(__name__)

# Track where features were saved in this session (for prioritizing working directory)
_session_saved_paths: Dict[str, Path] = {}


def generate_feature_filename(model_id: str, combo_id: str) -> str:
    """
    Generate feature filename based on model ID and combo ID.
    
    Args:
        model_id: Two-digit model ID (e.g., '01' for dinov2_base).
        combo_id: Combo ID string (e.g., 'combo_00').
    
    Returns:
        Filename string: variant_{model_id}{combo_numeric}_features.npz
        Example: variant_0100_features.npz (model 01, combo_00 -> "00")
    
    Raises:
        ValueError: If combo_id format is invalid.
    """
    # Extract numeric part from combo_id (e.g., "combo_00" -> "00")
    if not combo_id.startswith('combo_'):
        raise ValueError(f"Invalid combo_id format: {combo_id}. Expected format: combo_XX")
    
    try:
        combo_numeric = combo_id.replace('combo_', '')
        # Convert to int and back to 2-digit string (e.g., "00" -> "00", "01" -> "01")
        combo_numeric_2digit = f"{int(combo_numeric):02d}"
    except ValueError:
        raise ValueError(f"Invalid combo_id numeric part: {combo_id}")
    
    filename = f"variant_{model_id}{combo_numeric_2digit}_features.npz"
    logger.debug(f"Generated feature filename: {filename} (model_id={model_id}, combo_id={combo_id})")
    
    return filename


def parse_feature_filename(filename: str) -> Tuple[str, str]:
    """
    Parse feature filename to extract model_id and combo_id.
    
    Reverse of generate_feature_filename(). Extracts model ID and combo ID
    from a feature filename.
    
    Args:
        filename: Feature filename (e.g., 'variant_0100_features.npz').
    
    Returns:
        Tuple of (model_id, combo_id):
        - model_id: Two-digit model ID (e.g., '01')
        - combo_id: Combo ID string (e.g., 'combo_00')
    
    Raises:
        ValueError: If filename format is invalid.
    
    Examples:
        >>> parse_feature_filename('variant_0100_features.npz')
        ('01', 'combo_00')
        >>> parse_feature_filename('variant_0201_features.npz')
        ('02', 'combo_01')
    """
    if not filename.startswith('variant_'):
        raise ValueError(f"Invalid feature filename format: {filename}. Expected format: variant_XXXX_features.npz")
    
    if not filename.endswith('_features.npz'):
        raise ValueError(f"Invalid feature filename format: {filename}. Expected format: variant_XXXX_features.npz")
    
    # Extract the middle part: variant_XXXX_features.npz -> XXXX
    try:
        # Remove 'variant_' prefix and '_features.npz' suffix
        middle_part = filename.replace('variant_', '').replace('_features.npz', '')
        
        if len(middle_part) != 4:
            raise ValueError(f"Invalid feature filename format: {filename}. Expected 4 digits after 'variant_'")
        
        # First 2 digits are model_id, last 2 digits are combo_numeric
        model_id = middle_part[:2]
        combo_numeric = middle_part[2:]
        
        # Convert combo_numeric to combo_id (e.g., "00" -> "combo_00")
        combo_id = f"combo_{combo_numeric}"
        
        logger.debug(f"Parsed feature filename: {filename} -> model_id={model_id}, combo_id={combo_id}")
        
        return model_id, combo_id
        
    except (ValueError, IndexError) as e:
        raise ValueError(f"Failed to parse feature filename: {filename}. Error: {e}")


def get_model_name_from_model_id(model_id: str) -> str:
    """
    Convert model_id to model_name using reverse lookup in MODEL_ID_MAP.
    
    Args:
        model_id: Two-digit model ID (e.g., '01')
    
    Returns:
        Model name (e.g., 'dinov2_base')
    
    Raises:
        ValueError: If model_id not found in MODEL_ID_MAP
    """
    from config.model_constants import MODEL_ID_MAP
    
    # Reverse lookup: find model_name where MODEL_ID_MAP[model_name] == model_id
    for model_name, mapped_id in MODEL_ID_MAP.items():
        if mapped_id == model_id:
            return model_name
    
    available_ids = ', '.join(sorted(set(MODEL_ID_MAP.values())))
    raise ValueError(
        f"Model ID '{model_id}' not found in MODEL_ID_MAP.\n"
        f"Available model IDs: {available_ids}\n"
        f"Add the model to MODEL_ID_MAP in config/model_constants.py"
    )


def parse_feature_filename_to_extraction_info(feature_filename: str) -> Dict[str, Any]:
    """
    Parse feature filename to extract feature extraction model and data manipulation info.
    
    Feature filename (e.g., 'variant_0100_features.npz') encodes:
    - model_id (first 2 digits: '01') → feature extraction model name
    - combo_id (last 2 digits: '00') → data manipulation combo
    
    Args:
        feature_filename: Feature filename (e.g., 'variant_0100_features.npz')
    
    Returns:
        Dictionary with:
        - model_name: Feature extraction model name (e.g., 'dinov2_base')
        - model_id: Two-digit model ID (e.g., '01')
        - combo_id: Data manipulation combo ID (e.g., 'combo_000')
        - preprocessing_list: List from data_manipulation metadata
        - augmentation_list: List from data_manipulation metadata
    
    Raises:
        ValueError: If filename format is invalid or model_id/combo_id not found
    """
    from ..utils.metadata.data_manipulation_loader import (
        find_metadata_dir,
        get_combo_details
    )
    
    # Parse model_id and combo_id from filename
    model_id, combo_id = parse_feature_filename(feature_filename)
    
    # Convert model_id to model_name
    model_name = get_model_name_from_model_id(model_id)
    
    # Get preprocessing/augmentation lists from data_manipulation metadata
    metadata_dir = find_metadata_dir()
    if not metadata_dir:
        raise FileNotFoundError(
            "csiro-metadata directory not found. "
            "Expected: /kaggle/input/csiro-metadata (Kaggle) or ../csiro-metadata (local)"
        )
    
    combo_details = get_combo_details(combo_id, metadata_dir)
    
    return {
        'model_name': model_name,
        'model_id': model_id,
        'combo_id': combo_id,
        'preprocessing_list': combo_details['preprocessing_list'],
        'augmentation_list': combo_details['augmentation_list']
    }


def get_feature_cache_paths(filename: str) -> Tuple[Path, Path]:
    """
    Get feature cache paths with priority order (input > working).
    
    Args:
        filename: Feature filename (e.g., 'variant_0100_features.npz').
    
    Returns:
        Tuple of (input_path, working_path) where:
        - input_path: Path in /kaggle/input/csiro-extracted-features/ (persistent, highest priority)
        - working_path: Path in /kaggle/working/features/ (temporary, fallback)
    """
    if is_kaggle_environment():
        input_base = Path('/kaggle/input') / FEATURE_CACHE_INPUT_DIR
        working_base = Path('/kaggle/working') / FEATURE_CACHE_WORKING_DIR
    else:
        # Local environment - use working directory structure
        input_base = Path('features_cache') / 'input'
        working_base = Path('features_cache') / 'working'
    
    input_path = input_base / filename
    working_path = working_base / filename
    
    return input_path, working_path


def find_feature_cache(filename: str) -> Optional[Path]:
    """
    Find feature cache file with priority: session-saved working > input > working.
    
    Priority order:
    1. Working directory if features were saved there in this session (freshly extracted)
    2. /kaggle/input/csiro-extracted-features/{filename} (persistent, pre-existing)
    3. /kaggle/working/features/{filename} (temporary, fallback)
    
    This ensures that when features are freshly extracted and saved to working directory
    (because input is read-only), those working directory features are used instead of
    potentially stale input directory features.
    
    Args:
        filename: Feature filename (e.g., 'variant_0100_features.npz').
    
    Returns:
        Path to cache file if found, None otherwise.
    """
    input_path, working_path = get_feature_cache_paths(filename)
    
    # Check if features were saved to working directory in this session (highest priority)
    if filename in _session_saved_paths:
        saved_path = _session_saved_paths[filename]
        if saved_path.exists():
            logger.info(f"Found feature cache from this session: {saved_path}")
            return saved_path
        else:
            # Saved path no longer exists, remove from tracking
            del _session_saved_paths[filename]
    
    # Check input directory (pre-existing features)
    if input_path.exists():
        logger.info(f"Found feature cache in input directory: {input_path}")
        return input_path
    
    # Check working directory (fallback)
    if working_path.exists():
        logger.info(f"Found feature cache in working directory: {working_path}")
        return working_path
    
    logger.debug(f"No feature cache found for filename: {filename}")
    return None


def save_features(
    all_features: np.ndarray,
    all_targets: np.ndarray,
    fold_assignments: np.ndarray,
    filename: str,
    config: Config,
    use_input_dir: bool = True
) -> Path:
    """
    Save extracted features to cache.
    
    Saves features for all images in a single cache file.
    Features are split by fold during training, not during caching.
    
    Attempts to save to input directory if requested, but automatically falls back
    to working directory if input directory is read-only (e.g., in Kaggle environments).
    
    Args:
        all_features: All features array (N_total, feat_dim).
        all_targets: All targets array (N_total, 3).
        fold_assignments: Fold assignments array (N_total,).
        filename: Feature filename (e.g., 'variant_0100_features.npz').
        config: Configuration object (for metadata).
        use_input_dir: If True, attempt to save to input directory first (persistent).
                       Falls back to working directory if input is read-only.
                       If False, save directly to working directory.
    
    Returns:
        Path to saved cache file.
    """
    if filename is None or not filename:
        raise ValueError("filename is required")
    if config is None:
        raise ValueError("config is required")
    if all_features is None or all_targets is None:
        raise ValueError("all_features and all_targets are required")
    if fold_assignments is None:
        raise ValueError("fold_assignments is required")
    
    input_path, working_path = get_feature_cache_paths(filename)
    
    # Prepare metadata
    metadata = {
        'filename': filename,
        'model_name': config.model.feature_extraction_model_name,
        'dataset_type': getattr(config.data, 'dataset_type', 'split'),
        'image_size': str(config.data.image_size),
        'preprocessing_list': config.data.preprocessing_list or [],
        'cache_type': 'all_features',
        'all_features_shape': list(all_features.shape),
        'all_targets_shape': list(all_targets.shape),
        'fold_assignments_shape': list(fold_assignments.shape),
        'n_samples': int(all_features.shape[0])
    }
    
    # Try to save to input directory first if requested
    if use_input_dir:
        save_path = input_path
        try:
            # Create parent directory
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save features and metadata to .npz file
            np.savez_compressed(
                save_path,
                all_features=all_features,
                all_targets=all_targets,
                fold_assignments=fold_assignments,
                metadata=json.dumps(metadata)  # Store metadata as JSON string
            )
            logger.info(f"Saved all-features cache: {save_path}")
            logger.info(f"  All features: {all_features.shape}, All targets: {all_targets.shape}")
            
            return save_path
            
        except (OSError, PermissionError) as e:
            # Check if it's a read-only filesystem error
            is_readonly = (
                isinstance(e, OSError) and e.errno == 30  # Read-only file system
            ) or isinstance(e, PermissionError)
            
            if is_readonly:
                logger.warning(f"Cannot write to input directory (read-only): {save_path}")
                logger.info(f"Falling back to working directory: {working_path}")
            else:
                # Re-raise if it's a different error
                raise
    
    # Save to working directory (either as fallback or by default)
    save_path = working_path
    
    # Create parent directory
    save_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save features and metadata to .npz file
    np.savez_compressed(
        save_path,
        all_features=all_features,
        all_targets=all_targets,
        fold_assignments=fold_assignments,
        metadata=json.dumps(metadata)  # Store metadata as JSON string
    )
    logger.info(f"Saved all-features cache: {save_path} (all: {all_features.shape})")
    
    # Track where features were saved in this session (for prioritizing working directory)
    _session_saved_paths[filename] = save_path
    
    return save_path


def load_features(
    cache_path: Path
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, Dict[str, Any]]:
    """
    Load features cache from file.
    
    Args:
        cache_path: Path to cache .npz file.
    
    Returns:
        Tuple of (all_features, all_targets, fold_assignments, metadata):
        - all_features: All features array (N_total, feat_dim)
        - all_targets: All targets array (N_total, 3)
        - fold_assignments: Fold assignments array (N_total,)
        - metadata: Dictionary with cache information
    
    Raises:
        FileNotFoundError: If cache_path doesn't exist.
        ValueError: If cache file is corrupted or invalid.
    """
    if not cache_path.exists():
        raise FileNotFoundError(f"Feature cache file not found: {cache_path}")
    
    try:
        # Load from .npz file
        data = np.load(cache_path, allow_pickle=True)
        
        # Load metadata
        metadata_str = data['metadata'].item() if 'metadata' in data else '{}'
        metadata = json.loads(metadata_str) if isinstance(metadata_str, str) else {}
        
        # Verify it's an all-features cache
        cache_type = metadata.get('cache_type', 'all_features')
        if cache_type != 'all_features':
            raise ValueError(
                f"Cache file is not an all-features cache (cache_type: {cache_type}). "
                "Only all-features caches are supported."
            )
        
        # Load all-features cache
        all_features = data['all_features']
        all_targets = data['all_targets']
        fold_assignments = data['fold_assignments']
        
        logger.info(f"Loaded all-features cache: {cache_path}")
        logger.info(f"  All features: {all_features.shape}, All targets: {all_targets.shape}")
        logger.info(f"  Metadata: {metadata.get('model_name', 'unknown')}")
        
        return all_features, all_targets, fold_assignments, metadata
        
    except Exception as e:
        raise ValueError(f"Failed to load feature cache from {cache_path}: {e}") from e

