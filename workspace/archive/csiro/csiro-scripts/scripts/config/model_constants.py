# model_constants.py
# Model name to pretrained weights mapping
#
# This module maps MODEL_NAME (used for organizing results/checkpoints) to
# MODEL (pretrained weights path/name used for training initialization).
#
# MODEL_NAME: Used for organizing model metadata and trained checkpoints
#   - Model metadata: csiro-metadata/{MODEL_NAME}/metadata.json
#   - Trained checkpoints: csiro-models/pytorch/{MODEL_NAME}/{version}/
#
# MODEL: Pretrained weights path/name for training initialization
#   - DINOv2: Path to pretrained weights (e.g., '/kaggle/input/dinov2/pytorch/base/1')
#   - Timm: Model name string (e.g., 'efficientnet_b3')
#
# This centralizes model configuration to follow DRY principles and makes it
# easy to add new models without modifying notebooks or multiple files.

from typing import Dict, Optional

# Model ID mapping for feature file naming
# Maps MODEL_NAME to 2-digit ID for feature filename generation
MODEL_ID_MAP: Dict[str, str] = {
    'dinov2_base': '01',
    'dinov2_large': '02',
    'timm_efficientnet_b3': '03',
    # Add more models as needed:
    # 'timm_resnet50': '03',
}

# Mapping from MODEL_NAME to pretrained weights path/name
MODEL_NAME_TO_PRETRAINED: Dict[str, str] = {
    # DINOv2 models (offline pretrained weights)
    'dinov2_base': '/kaggle/input/dinov2/pytorch/base/1',
    'dinov2_large': '/kaggle/input/dinov2/pytorch/large/1',
    # Alternative (online): 'dinov2_base': 'facebook/dinov2-base',
    # 'dinov2_large': 'facebook/dinov2-large',
    
    # Timm models (model name strings)
    'timm_efficientnet_b3': 'efficientnet_b3',
    # Add more timm models as needed:
    # 'timm_resnet50': 'resnet50',
    # 'timm_vit_base': 'vit_base_patch16_224',
}


def get_pretrained_weights_path(model_name: str) -> str:
    """
    Get pretrained weights path/name from MODEL_NAME.
    
    This function provides a single source of truth for mapping model names
    (used for organization) to pretrained weights (used for training).
    
    Args:
        model_name: Model name used for organizing results/checkpoints
                   (e.g., 'dinov2_base', 'timm_efficientnet_b3')
    
    Returns:
        Pretrained weights path (for DINOv2) or model name (for timm).
        Falls back to extracting timm name if model_name starts with 'timm_'.
        Falls back to model_name itself if no mapping found.
    
    Examples:
        >>> get_pretrained_weights_path('dinov2_base')
        '/kaggle/input/dinov2/pytorch/base/1'
        >>> get_pretrained_weights_path('timm_efficientnet_b3')
        'efficientnet_b3'
        >>> get_pretrained_weights_path('timm_resnet50')
        'resnet50'  # Auto-extracted from 'timm_resnet50'
        >>> get_pretrained_weights_path('custom_model')
        'custom_model'  # Fallback: used as-is
    """
    # Check explicit mapping first
    if model_name in MODEL_NAME_TO_PRETRAINED:
        return MODEL_NAME_TO_PRETRAINED[model_name]
    
    # Auto-extract timm model name if starts with 'timm_'
    if model_name.startswith('timm_'):
        return model_name.replace('timm_', '')
    
    # Fallback: use model_name directly
    return model_name


def get_model_name_from_pretrained(pretrained_path: str) -> Optional[str]:
    """
    Reverse lookup: Get MODEL_NAME from pretrained weights path/name.
    
    Useful for inferring MODEL_NAME when only MODEL is known.
    
    Args:
        pretrained_path: Pretrained weights path or model name
    
    Returns:
        MODEL_NAME if found in mapping, None otherwise
    
    Examples:
        >>> get_model_name_from_pretrained('/kaggle/input/dinov2/pytorch/base/1')
        'dinov2_base'
        >>> get_model_name_from_pretrained('efficientnet_b3')
        'timm_efficientnet_b3'
    """
    # Reverse lookup in mapping
    for model_name, pretrained in MODEL_NAME_TO_PRETRAINED.items():
        if pretrained == pretrained_path:
            return model_name
    
    # If pretrained_path is a timm model name, construct MODEL_NAME
    # (This is a best-effort guess - may not always be correct)
    if not pretrained_path.startswith('/') and not '/' in pretrained_path:
        # Looks like a timm model name
        return f'timm_{pretrained_path}'
    
    return None


def get_model_id(model_name: str) -> str:
    """
    Get 2-digit model ID from MODEL_NAME for feature filename generation.
    
    Model IDs are used in feature file naming: variant_{model_id}{combo_numeric}_features.npz
    
    Args:
        model_name: Model name used for organizing results/checkpoints
                   (e.g., 'dinov2_base', 'timm_efficientnet_b3')
    
    Returns:
        Two-digit model ID string (e.g., '01', '02').
        Raises ValueError if model_name is not in MODEL_ID_MAP.
    
    Examples:
        >>> get_model_id('dinov2_base')
        '01'
        >>> get_model_id('timm_efficientnet_b3')
        '02'
    
    Raises:
        ValueError: If model_name is not found in MODEL_ID_MAP.
    """
    if model_name not in MODEL_ID_MAP:
        available_models = ', '.join(sorted(MODEL_ID_MAP.keys()))
        raise ValueError(
            f"Model '{model_name}' not found in MODEL_ID_MAP.\n"
            f"Available models: {available_models}\n"
            f"Add '{model_name}' to MODEL_ID_MAP in config/model_constants.py"
        )
    
    return MODEL_ID_MAP[model_name]

