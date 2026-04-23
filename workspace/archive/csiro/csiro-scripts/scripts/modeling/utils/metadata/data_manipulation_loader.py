# data_manipulation_loader.py
# Utilities for loading and resolving data manipulation combo IDs

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from utils.system.io import load_json_file, is_kaggle_environment
from config.path_constants import KAGGLE_INPUT

logger = logging.getLogger(__name__)

# Essential preprocessing operations that are always applied
# These should NOT be included in combo_id metadata since they're in all combinations
ESSENTIAL_PREPROCESSING = {'resize', 'normalize'}


def filter_essential_preprocessing(preprocessing_list: List[str]) -> List[str]:
    """
    Filter out essential preprocessing operations from preprocessing list.
    
    Essential operations (resize, normalize) are always applied and should not
    be included in combo_id metadata since they appear in all combinations.
    
    Args:
        preprocessing_list: List of preprocessing technique names.
    
    Returns:
        Filtered list with only optional preprocessing techniques.
    """
    return [p for p in preprocessing_list if p not in ESSENTIAL_PREPROCESSING]


def find_metadata_dir() -> Optional[Path]:
    """
    Find the csiro-metadata directory for reading.
    
    Searches in priority order:
    1. /kaggle/input/csiro-metadata (Kaggle environment - read-only, curated)
    2. /kaggle/working/csiro-metadata (Kaggle environment - writable, in-progress)
    3. ../csiro-metadata (local environment)
    
    Returns:
        Path to metadata directory if found, None otherwise.
    """
    if is_kaggle_environment():
        # Check input first (curated/uploaded metadata)
        input_metadata_dir = KAGGLE_INPUT / 'csiro-metadata'
        if input_metadata_dir.exists():
            return input_metadata_dir
        
        # Fallback to working directory (writable, in-progress)
        from config.path_constants import KAGGLE_WORKING
        working_metadata_dir = KAGGLE_WORKING / 'csiro-metadata'
        if working_metadata_dir.exists():
            return working_metadata_dir
    else:
        metadata_dir = Path('../csiro-metadata')
        if metadata_dir.exists():
            return metadata_dir
    
    return None


def get_writable_metadata_dir() -> Path:
    """
    Get the writable csiro-metadata directory for writing.
    
    In Kaggle environment, always returns /kaggle/working/csiro-metadata.
    In local environment, returns ../csiro-metadata.
    
    Creates the directory if it doesn't exist.
    
    Returns:
        Path to writable metadata directory.
    """
    from utils.system import ensure_dir
    from config.path_constants import KAGGLE_WORKING
    
    if is_kaggle_environment():
        writable_dir = KAGGLE_WORKING / 'csiro-metadata'
    else:
        writable_dir = Path('../csiro-metadata')
    
    ensure_dir(writable_dir)
    return writable_dir


def load_data_manipulation_combos(metadata_dir: Path) -> Dict[str, Dict]:
    """
    Load data manipulation combos from metadata directory.
    
    Args:
        metadata_dir: Path to csiro-metadata directory (e.g., /kaggle/input/csiro-metadata).
    
    Returns:
        Dictionary mapping combo_id to combo details:
        {
            'combo_000': {
                'combo_id': 'combo_000',
                'combo_index': 0,
                'preprocessing_list': [],
                'augmentation_list': []
            },
            ...
        }
    
    Raises:
        FileNotFoundError: If metadata.json doesn't exist in data_manipulation subdirectory.
        ValueError: If metadata file is invalid.
    """
    combos_path = metadata_dir / 'data_manipulation' / 'metadata.json'
    
    if not combos_path.exists():
        raise FileNotFoundError(
            f"Data manipulation metadata not found: {combos_path}\n"
            f"Expected location: {metadata_dir}/data_manipulation/metadata.json"
        )
    
    combos_list = load_json_file(combos_path, expected_type=list, file_type="Data manipulation combos JSON")
    
    # Convert list to dict for easier lookup
    combos_dict = {}
    for combo in combos_list:
        combo_id = combo.get('combo_id')
        if not combo_id:
            raise ValueError(f"Invalid combo entry: missing combo_id. Entry: {combo}")
        combos_dict[combo_id] = combo
    
    logger.debug(f"Loaded {len(combos_dict)} data manipulation combos from {combos_path}")
    
    return combos_dict


def get_combo_details(combo_id: str, metadata_dir: Path) -> Dict[str, List[str]]:
    """
    Get preprocessing and augmentation lists for a given combo_id.
    
    Args:
        combo_id: Combo ID string (e.g., 'combo_000').
        metadata_dir: Path to csiro-metadata directory.
    
    Returns:
        Dictionary with preprocessing_list and augmentation_list:
        {
            'preprocessing_list': [...],
            'augmentation_list': [...]
        }
    
    Raises:
        FileNotFoundError: If metadata file doesn't exist.
        ValueError: If combo_id is not found.
    """
    combos = load_data_manipulation_combos(metadata_dir)
    
    if combo_id not in combos:
        available_ids = ', '.join(sorted(combos.keys())[:10])
        raise ValueError(
            f"Combo ID '{combo_id}' not found in data manipulation metadata.\n"
            f"Available combo IDs (first 10): {available_ids}..."
        )
    
    combo = combos[combo_id]
    
    return {
        'preprocessing_list': combo.get('preprocessing_list', []),
        'augmentation_list': combo.get('augmentation_list', [])
    }


def find_combo_id(
    preprocessing_list: List[str],
    augmentation_list: List[str],
    metadata_dir: Path
) -> Optional[str]:
    """
    Find existing combo_id for given preprocessing and augmentation lists.
    
    Essential preprocessing (resize, normalize) is automatically filtered out
    since it's always applied and shouldn't be in combo metadata.
    
    Args:
        preprocessing_list: List of preprocessing technique names (may include essential).
        augmentation_list: List of augmentation technique names.
        metadata_dir: Path to csiro-metadata directory.
    
    Returns:
        Combo ID string if found (e.g., 'combo_000'), None otherwise.
    """
    combos = load_data_manipulation_combos(metadata_dir)
    
    # Filter out essential preprocessing (always applied, not in metadata)
    optional_preprocessing = filter_essential_preprocessing(preprocessing_list)
    
    # Normalize lists (sort for comparison)
    pre_sorted = tuple(sorted(optional_preprocessing))
    aug_sorted = tuple(sorted(augmentation_list))
    
    # Search for matching combo
    for combo_id, combo in combos.items():
        # Filter essential preprocessing from stored combo for consistent matching
        combo_pre_raw = combo.get('preprocessing_list', [])
        combo_pre_filtered = filter_essential_preprocessing(combo_pre_raw)
        combo_pre = tuple(sorted(combo_pre_filtered))
        combo_aug = tuple(sorted(combo.get('augmentation_list', [])))
        
        if combo_pre == pre_sorted and combo_aug == aug_sorted:
            return combo_id
    
    return None


def get_or_create_combo_id(
    preprocessing_list: List[str],
    augmentation_list: List[str],
    metadata_dir: Path
) -> str:
    """
    Get existing combo_id or create a new one for given preprocessing and augmentation lists.
    
    Essential preprocessing (resize, normalize) is automatically filtered out
    since it's always applied and shouldn't be in combo metadata.
    
    If combo doesn't exist, creates a new entry with the next sequential combo_id.
    
    Args:
        preprocessing_list: List of preprocessing technique names (may include essential).
        augmentation_list: List of augmentation technique names.
        metadata_dir: Path to csiro-metadata directory.
    
    Returns:
        Combo ID string (e.g., 'combo_000').
    """
    import json
    
    # Filter out essential preprocessing (always applied, not in metadata)
    optional_preprocessing = filter_essential_preprocessing(preprocessing_list)
    
    # Try to find existing combo (with filtered preprocessing)
    existing_id = find_combo_id(preprocessing_list, augmentation_list, metadata_dir)
    if existing_id:
        return existing_id
    
    # Combo doesn't exist - create new one
    combos_path = metadata_dir / 'data_manipulation' / 'metadata.json'
    combos_list = load_json_file(combos_path, expected_type=list, file_type="Data manipulation combos JSON")
    
    # Find next combo_index
    max_index = max((combo.get('combo_index', 0) for combo in combos_list), default=-1)
    next_index = max_index + 1
    next_combo_id = f'combo_{next_index:03d}'
    
    # Create new combo entry (only optional preprocessing, not essential)
    new_combo = {
        'combo_id': next_combo_id,
        'combo_index': next_index,
        'preprocessing_list': sorted(optional_preprocessing),
        'augmentation_list': sorted(augmentation_list)
    }
    
    # Append to list and save
    combos_list.append(new_combo)
    combos_path.write_text(json.dumps(combos_list, indent=2))
    
    logger.info(f"Created new combo: {next_combo_id} (preprocessing={optional_preprocessing}, augmentation={augmentation_list})")
    
    return next_combo_id


def extract_preprocessing_augmentation_from_variant(
    variant: Dict,
    metadata_dir: Optional[Path] = None
) -> Tuple[List[str], List[str]]:
    """
    Extract preprocessing_list and augmentation_list from a variant result.
    
    Handles both new format (data_manipulation.combo_id) and resolves combo_id.
    Does NOT support old format (direct preprocessing_list/augmentation_list) - clean break.
    
    Args:
        variant: Variant dictionary from results.
        metadata_dir: Optional metadata directory path. If None, attempts to find automatically.
    
    Returns:
        Tuple of (preprocessing_list, augmentation_list).
    
    Raises:
        ValueError: If variant has data_manipulation but combo_id cannot be resolved.
        KeyError: If variant is missing required fields.
    """
    data_manipulation = variant.get('data_manipulation')
    
    if data_manipulation:
        combo_id = data_manipulation.get('combo_id')
        if not combo_id:
            raise ValueError(f"Variant {variant.get('variant_id', 'unknown')} has data_manipulation but no combo_id")
        
        if metadata_dir is None:
            metadata_dir = find_metadata_dir()
        
        if not metadata_dir:
            raise FileNotFoundError(
                "Cannot resolve combo_id: metadata directory not found. "
                "Expected: /kaggle/input/csiro-metadata (Kaggle) or ../csiro-metadata (local)"
            )
        
        combo_details = get_combo_details(combo_id, metadata_dir)
        return combo_details['preprocessing_list'], combo_details['augmentation_list']
    else:
        # No data_manipulation field - this should not happen with new format
        raise ValueError(
            f"Variant {variant.get('variant_id', 'unknown')} missing data_manipulation field. "
            "All variants must use data_manipulation.combo_id format."
        )

