"""
Structured feature extraction for CAFA 6 protein function prediction.
Loads taxonomy, PPI, and top_terms features from the consolidated embeddings dataset.
"""

import numpy as np
from typing import Tuple, Optional
from pathlib import Path
from tqdm.auto import tqdm

from preprocessing.feature_engineering.embeddings import align_embeddings


def load_taxonomy_features(datatype: str = 'train',
                          taxonomy_level: str = 'default',
                          use_memmap: bool = None) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load taxonomy features for proteins.
    
    Args:
        datatype: 'train' or 'test'
        taxonomy_level: 'default', 'highlevel', or 'top500'
        use_memmap: If True, load as memmap; if False, load full array; if None, use config default
    
    Returns:
        (features_array, protein_ids)
    """
    from config.paths import FEATURE_PATHS, CAFA6_EMBEDDINGS_DIR
    from config.training import USE_MEMORY_MAPPED_EMBEDDINGS
    
    if use_memmap is None:
        use_memmap = USE_MEMORY_MAPPED_EMBEDDINGS
    
    # Determine taxonomy path based on level
    if taxonomy_level == 'highlevel':
        taxonomy_path = FEATURE_PATHS.get('taxonomy_highlevel', 
                                          CAFA6_EMBEDDINGS_DIR / 'taxonomy_highlevel')
    elif taxonomy_level == 'top500':
        taxonomy_path = FEATURE_PATHS.get('taxonomy_top500',
                                         CAFA6_EMBEDDINGS_DIR / 'taxonomy_top500')
    else:
        taxonomy_path = FEATURE_PATHS.get('taxonomy',
                                         CAFA6_EMBEDDINGS_DIR / 'taxonomy')
    
    # Try different file naming conventions
    possible_files = [
        (taxonomy_path / f'{datatype}.npy', taxonomy_path / f'{datatype}_ids.npy'),
        (taxonomy_path / f'{datatype}_features.npy', taxonomy_path / f'{datatype}_ids.npy'),
        (taxonomy_path / f'{datatype}_taxonomy.npy', CAFA6_EMBEDDINGS_DIR / f'{datatype}_sequences_ids.npy' if datatype == 'train' else CAFA6_EMBEDDINGS_DIR / 'testsuperset_ids.npy'),
    ]
    
    for features_path, ids_path in possible_files:
        if features_path.exists() and ids_path.exists():
            # Load features
            if use_memmap:
                features = np.load(features_path, mmap_mode='r')
            else:
                features = np.load(features_path)
                if features.dtype != np.float32:
                    features = features.astype(np.float32)
            
            # Load IDs
            ids = np.load(ids_path)
            
            print(f"   Loaded taxonomy ({taxonomy_level}) {datatype}: {features.shape} (dtype: {features.dtype})")
            return features, ids
    
    raise FileNotFoundError(
        f"Could not find taxonomy features for {datatype} at level {taxonomy_level}.\n"
        f"Tried paths: {[str(p[0]) for p in possible_files]}"
    )


def load_ppi_features(datatype: str = 'train',
                     use_memmap: bool = None) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load protein-protein interaction features.
    
    Args:
        datatype: 'train' or 'test'
        use_memmap: If True, load as memmap; if False, load full array; if None, use config default
    
    Returns:
        (features_array, protein_ids)
    """
    from config.paths import FEATURE_PATHS, CAFA6_EMBEDDINGS_DIR
    from config.training import USE_MEMORY_MAPPED_EMBEDDINGS
    
    if use_memmap is None:
        use_memmap = USE_MEMORY_MAPPED_EMBEDDINGS
    
    ppi_path = FEATURE_PATHS.get('ppi', CAFA6_EMBEDDINGS_DIR / 'ppi')
    
    # Try different file naming conventions
    possible_files = [
        (ppi_path / f'{datatype}.npy', ppi_path / f'{datatype}_ids.npy'),
        (ppi_path / f'{datatype}_features.npy', ppi_path / f'{datatype}_ids.npy'),
        (ppi_path / f'{datatype}_ppi.npy', CAFA6_EMBEDDINGS_DIR / f'{datatype}_sequences_ids.npy' if datatype == 'train' else CAFA6_EMBEDDINGS_DIR / 'testsuperset_ids.npy'),
    ]
    
    for features_path, ids_path in possible_files:
        if features_path.exists() and ids_path.exists():
            # Load features
            if use_memmap:
                features = np.load(features_path, mmap_mode='r')
            else:
                features = np.load(features_path)
                if features.dtype != np.float32:
                    features = features.astype(np.float32)
            
            # Load IDs
            ids = np.load(ids_path)
            
            print(f"   Loaded PPI {datatype}: {features.shape} (dtype: {features.dtype})")
            return features, ids
    
    raise FileNotFoundError(
        f"Could not find PPI features for {datatype}.\n"
        f"Tried paths: {[str(p[0]) for p in possible_files]}"
    )


def load_top_terms_features(datatype: str = 'train',
                           aspect: Optional[str] = None,
                           use_memmap: bool = None) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load top GO terms by aspect features.
    
    Args:
        datatype: 'train' or 'test'
        aspect: Optional GO aspect filter ('F', 'P', 'C', or None for all)
        use_memmap: If True, load as memmap; if False, load full array; if None, use config default
    
    Returns:
        (features_array, protein_ids)
    """
    from config.paths import FEATURE_PATHS, CAFA6_EMBEDDINGS_DIR
    from config.training import USE_MEMORY_MAPPED_EMBEDDINGS
    
    if use_memmap is None:
        use_memmap = USE_MEMORY_MAPPED_EMBEDDINGS
    
    top_terms_path = FEATURE_PATHS.get('top_terms_by_aspect',
                                      CAFA6_EMBEDDINGS_DIR / 'top_terms_by_aspect')
    
    # Try different file naming conventions
    if aspect:
        possible_files = [
            (top_terms_path / f'{datatype}_{aspect}.npy', top_terms_path / f'{datatype}_{aspect}_ids.npy'),
            (top_terms_path / f'{datatype}_features_{aspect}.npy', top_terms_path / f'{datatype}_ids.npy'),
        ]
    else:
        possible_files = [
            (top_terms_path / f'{datatype}.npy', top_terms_path / f'{datatype}_ids.npy'),
            (top_terms_path / f'{datatype}_features.npy', top_terms_path / f'{datatype}_ids.npy'),
            (top_terms_path / f'{datatype}_top_terms.npy', CAFA6_EMBEDDINGS_DIR / f'{datatype}_sequences_ids.npy' if datatype == 'train' else CAFA6_EMBEDDINGS_DIR / 'testsuperset_ids.npy'),
        ]
    
    for features_path, ids_path in possible_files:
        if features_path.exists() and ids_path.exists():
            # Load features
            if use_memmap:
                features = np.load(features_path, mmap_mode='r')
            else:
                features = np.load(features_path)
                if features.dtype != np.float32:
                    features = features.astype(np.float32)
            
            # Load IDs
            ids = np.load(ids_path)
            
            aspect_str = f" ({aspect})" if aspect else ""
            print(f"   Loaded top_terms{aspect_str} {datatype}: {features.shape} (dtype: {features.dtype})")
            return features, ids
    
    raise FileNotFoundError(
        f"Could not find top_terms features for {datatype}{f' (aspect: {aspect})' if aspect else ''}.\n"
        f"Tried paths: {[str(p[0]) for p in possible_files]}"
    )


def align_structured_features(features: np.ndarray,
                             feature_ids: np.ndarray,
                             target_ids: list) -> Tuple[np.ndarray, list]:
    """
    Align structured features to target protein order.
    Wrapper around align_embeddings for consistency.
    
    Args:
        features: Feature array (n_proteins, n_features)
        feature_ids: Protein IDs for features
        target_ids: Target protein IDs in desired order
    
    Returns:
        (aligned_features, aligned_ids)
    """
    return align_embeddings(features, feature_ids, target_ids)

