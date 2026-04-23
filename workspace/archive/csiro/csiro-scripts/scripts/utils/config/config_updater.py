# config_updater.py
# Configuration update utilities

import logging
from typing import Optional, List

from config.config import Config
from ..data.preprocessing_utils import (
    parse_preprocessing_list,
    parse_augmentation_list,
    validate_preprocessing_names,
    validate_augmentation_names
)
from .config_validator import validate_config_section

logger = logging.getLogger(__name__)


def apply_data_model_overrides(
    config: Config,
    data_root: Optional[str] = None,
    model_name: Optional[str] = None
) -> None:
    """
    Apply data and model name overrides to config.
    
    Args:
        config: Config object to update. Must not be None.
        data_root: Optional data root directory override.
        model_name: Optional model name override.
    """
    if data_root:
        config.data.data_root = data_root
    
    if model_name:
        config.model.name = model_name


def apply_preprocessing_to_config(config: Config, preprocessing_list: List[str], suppress_default_logging: bool = False) -> None:
    """
    Update config.data with selected preprocessing.
    
    Essential preprocessing operations (resize, normalize) are always applied automatically
    and should not be included in preprocessing_list. Only optional preprocessing techniques
    should be specified.
    
    Args:
        config: Configuration object to update. Must not be None and must have config.data attribute.
        preprocessing_list: List of optional preprocessing technique names.
                          If empty, only essential preprocessing (resize, normalize) will be applied.
        suppress_default_logging: If True, don't log when preprocessing_list is empty.
                                 Useful when grid search results will override this later.
        
    Raises:
        ValueError: If config is None, config.data is None, or preprocessing_list contains invalid names.
        TypeError: If preprocessing_list is not a list.
    """
    # Validate inputs
    validate_config_section(config, 'data')
    
    if not isinstance(preprocessing_list, list):
        raise TypeError(f"preprocessing_list must be list, got {type(preprocessing_list)}")
    
    if not preprocessing_list:
        # Empty list means only essential preprocessing (resize, normalize) will be applied automatically
        config.data.preprocessing_list = []
    else:
        validate_preprocessing_names(preprocessing_list)
        config.data.preprocessing_list = preprocessing_list.copy()  # Copy to avoid external modification
        logger.info(f"Applied preprocessing: {', '.join(preprocessing_list)}")


def apply_augmentation_to_config(config: Config, augmentation_list: List[str], suppress_default_logging: bool = False) -> None:
    """
    Update config.data with selected augmentation.
    
    Args:
        config: Configuration object to update. Must not be None and must have config.data attribute.
        augmentation_list: List of augmentation technique names.
                          If empty, disables augmentation.
        suppress_default_logging: If True, don't log "using none" message when augmentation_list is empty.
                                 Useful when grid search results will override this later.
        
    Raises:
        ValueError: If config is None, config.data is None, or augmentation_list contains invalid names.
        TypeError: If augmentation_list is not a list.
    """
    # Validate inputs
    validate_config_section(config, 'data')
    
    if not isinstance(augmentation_list, list):
        raise TypeError(f"augmentation_list must be list, got {type(augmentation_list)}")
    
    if not augmentation_list:
        config.data.augmentation_list = []
        config.data.use_augmentation = False
        if not suppress_default_logging:
            logger.info("No augmentation specified, using none")
    else:
        validate_augmentation_names(augmentation_list)
        config.data.augmentation_list = augmentation_list.copy()  # Copy to avoid external modification
        config.data.use_augmentation = True
        logger.info(f"Applied augmentation: {', '.join(augmentation_list)}")


def apply_preprocessing_augmentation_from_args(
    config: Config,
    preprocessing: Optional[str] = None,
    data_augmentation: Optional[str] = None
) -> None:
    """
    Apply preprocessing and augmentation from CLI arguments to config.
    
    Only applies if explicitly provided (non-empty string).
    Empty strings mean "not specified" - don't apply defaults here.
    This allows grid search results to be loaded later without misleading "using default" messages.
    
    Args:
        config: Config object to update. Must not be None.
        preprocessing: Optional comma-separated preprocessing list (e.g., "resize,normalize").
        data_augmentation: Optional comma-separated augmentation list (e.g., "geometric_transformations").
    """
    if preprocessing is not None and preprocessing.strip():
        preprocessing_list = parse_preprocessing_list(preprocessing)
        apply_preprocessing_to_config(config, preprocessing_list)
    
    if data_augmentation is not None and data_augmentation.strip():
        augmentation_list = parse_augmentation_list(data_augmentation)
        apply_augmentation_to_config(config, augmentation_list)


def apply_training_parameter_overrides(
    config: Config,
    batch_size: Optional[int] = None,
    learning_rate: Optional[float] = None
) -> None:
    """
    Apply training parameter overrides to config.
    
    Args:
        config: Config object to update. Must not be None.
        batch_size: Optional batch size override.
        learning_rate: Optional learning rate override.
    """
    if batch_size is not None:
        config.training.batch_size = batch_size
    if learning_rate is not None:
        config.training.learning_rate = learning_rate


def apply_dataset_config_to_config(
    config: Config,
    preprocessing_list: List[str],
    augmentation_list: List[str]
) -> None:
    """
    Apply dataset configuration (preprocessing and augmentation) to config.
    
    Essential preprocessing operations (resize, normalize) are always applied automatically.
    If preprocessing_list is empty, only essential preprocessing will be applied.
    
    Args:
        config: Configuration object to update. Must not be None.
        preprocessing_list: List of optional preprocessing technique names.
                          If empty, only essential preprocessing (resize, normalize) will be applied.
        augmentation_list: List of augmentation technique names.
                          If empty, disables augmentation.
    """
    # Apply preprocessing (empty list means only essential preprocessing will be applied)
    apply_preprocessing_to_config(config, preprocessing_list)
    
    # Apply augmentation
    apply_augmentation_to_config(config, augmentation_list)


def apply_combo_to_config(config: Config, combo_id: str) -> None:
    """
    Apply data manipulation combo to config by loading combo details from metadata.
    
    Loads preprocessing_list and augmentation_list for the given combo_id and
    applies them to config using apply_dataset_config_to_config().
    
    Args:
        config: Configuration object to update. Must not be None.
        combo_id: Combo ID string (e.g., 'combo_00', 'combo_63').
    
    Raises:
        FileNotFoundError: If metadata directory not found.
        ValueError: If combo_id not found in metadata or config is None.
    """
    if config is None:
        raise ValueError("config cannot be None")
    
    if not combo_id or not isinstance(combo_id, str):
        raise ValueError(f"combo_id must be a non-empty string, got {combo_id}")
    
    # Find metadata directory
    from modeling.utils.metadata.data_manipulation_loader import (
        find_metadata_dir,
        get_combo_details
    )
    
    metadata_dir = find_metadata_dir()
    if not metadata_dir:
        raise FileNotFoundError(
            "csiro-metadata directory not found. Cannot load combo details. "
            "Expected: /kaggle/input/csiro-metadata (Kaggle) or ../csiro-metadata (local)"
        )
    
    # Load combo details
    combo_details = get_combo_details(combo_id, metadata_dir)
    preprocessing_list = combo_details['preprocessing_list']
    augmentation_list = combo_details['augmentation_list']
    
    # Apply to config
    logger.info(f"Applying data manipulation combo '{combo_id}': preprocessing={preprocessing_list}, augmentation={augmentation_list}")
    apply_dataset_config_to_config(config, preprocessing_list, augmentation_list)

