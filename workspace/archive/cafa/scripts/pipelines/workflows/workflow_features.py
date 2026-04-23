"""
Workflow feature extraction utilities for CAFA 6 protein function prediction.
Handles feature extraction and feature configuration comparison.
"""

from typing import Dict, List, Tuple, Optional, Any, Union
from pathlib import Path
import numpy as np

from preprocessing.feature_extraction import extract_features


def extract_features_for_model(sequences: Dict[str, str],
                              protein_ids: List[str],
                              config: Dict) -> np.ndarray:
    """
    Extract features for a model configuration.
    Uses unified feature extraction interface with automatic memory optimization.
    
    Args:
        sequences: Dict mapping protein_id -> sequence
        protein_ids: List of protein IDs to extract features for
        config: Model configuration dict
        
    Returns:
        np.ndarray: Feature matrix (n_samples, n_features)
        
    Note:
        For large datasets, this may return a memmap path. The caller should handle
        both np.ndarray and Path return types, or ensure small batch sizes.
    """
    # Use unified extraction interface
    features_result, _ = extract_features(
        sequences=sequences,
        config=config,
        protein_ids=protein_ids,
        datatype='test',
        force_memmap=False  # For prediction batches, prefer arrays (batches are small)
    )
    
    # Handle memmap path (shouldn't happen for small batches, but handle gracefully)
    if isinstance(features_result, Path):
        from utils.memory_efficient import load_features_memmap
        return np.array(load_features_memmap(features_result))
    
    return features_result


def get_feature_cache_key(feature_type: str, features: Optional[List[str]]) -> Tuple:
    """
    Generate cache key for feature extraction.
    
    Args:
        feature_type: Feature type ('fused_embeddings', 'hand_crafted')
        features: Optional list of feature names
        
    Returns:
        tuple: Cache key for feature extraction
    """
    if feature_type == 'fused_embeddings' and features:
        return ('fused', tuple(sorted(features)))
    else:
        return ('handcrafted',)


def make_hashable_for_comparison(val: Any) -> Any:
    """
    Convert value to hashable form for comparison.
    Converts lists to tuples recursively.
    
    Args:
        val: Value to make hashable
        
    Returns:
        Hashable value (tuples instead of lists)
    """
    if isinstance(val, list):
        return tuple(make_hashable_for_comparison(v) for v in val)
    elif isinstance(val, tuple):
        return tuple(make_hashable_for_comparison(v) for v in val)
    return val


def compare_feature_configs_across_ontologies(feature_configs: Dict[str, Tuple[str, Optional[List[str]]]]) -> Tuple[bool, str, Optional[List[str]]]:
    """
    Compare feature configs across ontologies to determine if all are the same.
    
    Args:
        feature_configs: Dict mapping ont_code -> (feature_type, features)
        
    Returns:
        tuple: (all_same, feature_type, features)
               - all_same: True if all ontologies use the same config
               - feature_type: The feature type (if all same) or first ontology's type
               - features: The features list (if all same) or first ontology's features
    """
    if not feature_configs:
        return (True, 'hand_crafted', None)
    
    # Convert lists to tuples for hashable comparison
    config_values = [make_hashable_for_comparison(val) for val in feature_configs.values()]
    
    if len(set(config_values)) == 1:
        # All same - use single config
        feature_type, features = list(feature_configs.values())[0]
        return (True, feature_type, features)
    else:
        # Different per ontology - return first ontology's config
        feature_type, features = list(feature_configs.values())[0]
        return (False, feature_type, features)


def infer_features_from_input_dim(input_dim: int) -> Optional[Tuple[str, List[str]]]:
    """
    Infer feature configuration from model's input dimension.
    Used when model metadata doesn't match config file (e.g., model trained with different features).
    
    Args:
        input_dim: Model's input dimension (from metadata)
        
    Returns:
        tuple: (feature_type, features_list) or None if cannot infer
               - feature_type: 'fused_embeddings' or 'hand_crafted'
               - features_list: List of feature names (e.g., ['esm2_15b', 'protbert', 'hc'])
    """
    from config.features import INDIVIDUAL_FEATURES
    
    # Common feature combinations and their expected dimensions
    # Format: (expected_dim, feature_list)
    # Allow ±10 dims tolerance for slight variations
    feature_combinations = [
        # High quality: esm2_15b + protbert + hc
        (6234, ['esm2_15b', 'protbert', 'hc']),  # 5120 + 1024 + 90
        (6230, ['esm2_15b', 'protbert', 'hc']),  # Allow slight variation
        
        # Balanced: esm2_3b + protbert + hc
        (3674, ['esm2_3b', 'protbert', 'hc']),   # 2560 + 1024 + 90
        (3670, ['esm2_3b', 'protbert', 'hc']),   # Allow slight variation
        
        # Default: protbert + esm2_650m + hc
        (2394, ['protbert', 'esm2', 'hc']),      # 1024 + 1280 + 90
        (2390, ['protbert', 'esm2', 'hc']),      # Allow slight variation
        
        # ProtBERT only + hc
        (1114, ['protbert', 'hc']),               # 1024 + 90
        (1110, ['protbert', 'hc']),               # Allow slight variation
        
        # ESM2 only + hc
        (1370, ['esm2', 'hc']),                   # 1280 + 90
        (1374, ['esm2', 'hc']),                   # Allow slight variation
        
        # Handcrafted only
        (90, ['hc']),
    ]
    
    # Find closest match (within ±10 dims tolerance)
    best_match = None
    min_diff = float('inf')
    
    for expected_dim, features in feature_combinations:
        diff = abs(input_dim - expected_dim)
        if diff < min_diff and diff <= 10:  # Within tolerance
            min_diff = diff
            best_match = features
    
    if best_match:
        return ('fused_embeddings', best_match)
    
    # If no exact match, try to infer from individual feature dimensions
    # This handles cases with custom combinations
    hc_dims = INDIVIDUAL_FEATURES.get('hc', {}).get('dimensions', 90)
    
    # Try common embedding combinations
    embedding_dims = {
        'esm2_15b': 5120,
        'esm2_3b': 2560,
        'esm2_650m': 1280,
        'esm2': 1280,
        'protbert': 1024,
        'prot_t5_xl': 1024,
    }
    
    # Try combinations of embeddings + hc
    remaining = input_dim - hc_dims
    if remaining > 0:
        # Try to find combination of embeddings that sum to remaining
        for emb_name, emb_dims in embedding_dims.items():
            if remaining == emb_dims:
                return ('fused_embeddings', [emb_name, 'hc'])
            # Try two embeddings
            for emb_name2, emb_dims2 in embedding_dims.items():
                if emb_name != emb_name2 and remaining == emb_dims + emb_dims2:
                    return ('fused_embeddings', [emb_name, emb_name2, 'hc'])
    
    return None


def calculate_expected_dimension(feature_type: str, features: Optional[List[str]]) -> Optional[int]:
    """
    Calculate expected feature dimension from feature configuration.
    
    Args:
        feature_type: Feature type ('fused_embeddings', 'hand_crafted')
        features: List of feature names (for fused_embeddings)
        
    Returns:
        int: Expected dimension or None if cannot calculate
    """
    from config.features import INDIVIDUAL_FEATURES
    
    if feature_type == 'hand_crafted':
        return INDIVIDUAL_FEATURES.get('hc', {}).get('dimensions', 90)
    
    if feature_type == 'fused_embeddings' and features:
        total = 0
        for feat in features:
            feat_info = INDIVIDUAL_FEATURES.get(feat)
            if feat_info:
                dims = feat_info.get('dimensions')
                if dims is not None:
                    total += dims
                else:
                    # Unknown dimension - cannot calculate
                    return None
            else:
                # Unknown feature - cannot calculate
                return None
        return total
    
    return None

