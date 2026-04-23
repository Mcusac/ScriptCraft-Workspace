"""
Memory-efficient batch feature extraction for CAFA 6 protein function prediction.
Processes features in chunks to avoid loading all data into memory at once.
"""

import numpy as np
from typing import Dict, List, Tuple, Generator, Optional, Union
from pathlib import Path

from utils.utils_common import cleanup_memory

from preprocessing.feature_engineering import extract_handcrafted_parallel
from preprocessing.data_streaming import load_embeddings_memmap
from preprocessing.feature_engineering.embeddings import align_embeddings
from config.features import BATCH_SIZE_CONFIG, get_embedding_feature_types, INDIVIDUAL_FEATURES, HANDCRAFTED_FEATURE_KEY


def extract_features_batch(train_seqs: Dict[str, str],
                          protein_ids: List[str],
                          feature_type: str = 'hand_crafted') -> np.ndarray:
    """
    Extract features for a batch of sequences.
    
    Args:
        train_seqs: Dict mapping protein_id -> sequence
        protein_ids: List of protein IDs to extract features for
        feature_type: 'hand_crafted' or 'embeddings'
        
    Returns:
        np.ndarray: Feature matrix (n_samples, n_features)
    """
    if feature_type == 'hand_crafted':
        # Use shared parallel extraction helper
        return extract_handcrafted_parallel(train_seqs, protein_ids)
    else:
        raise ValueError(f"Feature type '{feature_type}' not supported in batch extraction. Use 'hand_crafted'.")


def stream_features(train_seqs: Dict[str, str],
                   feature_type: str = 'hand_crafted',
                   chunk_size: Optional[int] = None) -> Generator[Tuple[np.ndarray, List[str]], None, None]:
    """
    Stream features in chunks to avoid loading all into memory.
    
    Args:
        train_seqs: Dict mapping protein_id -> sequence
        feature_type: 'hand_crafted' or 'embeddings'
        chunk_size: Number of proteins per chunk (defaults to config)
        
    Yields:
        tuple: (feature_matrix, protein_ids) for current chunk
    """
    if chunk_size is None:
        chunk_size = BATCH_SIZE_CONFIG["data_loading"]["feature_chunk_size"]
    
    protein_ids = list(train_seqs.keys())
    total_proteins = len(protein_ids)
    chunk_count = 0
    
    print(f"   Streaming features in chunks of {chunk_size:,}...")
    
    for i in range(0, total_proteins, chunk_size):
        chunk_ids = protein_ids[i:i+chunk_size]
        chunk_seqs = {pid: train_seqs[pid] for pid in chunk_ids}
        
        # Extract features for this chunk
        if feature_type == 'hand_crafted':
            features = extract_features_batch(chunk_seqs, chunk_ids, feature_type)
        else:
            raise ValueError(f"Feature type '{feature_type}' not supported in streaming. Use 'hand_crafted'.")
        
        chunk_count += 1
        print(f"      Yielding chunk {chunk_count} ({len(chunk_ids):,} proteins, shape: {features.shape})...")
        
        yield features, chunk_ids
        
        # Free memory
        del features, chunk_seqs
        cleanup_memory()
    
    print(f"   ✓ Streamed {chunk_count} chunks of features")


def extract_fused_features_chunked(train_seqs: Dict[str, str],
                                  features: List[str],
                                  datatype: str = 'train',
                                  chunk_size: Optional[int] = None,
                                  save_as_memmap: Optional[bool] = None) -> Tuple[Union[np.ndarray, Path], List[str]]:
    """
    DEPRECATED: Use preprocessing.feature_extraction.extract_features() instead.
    This function's functionality has been moved to the unified feature extraction interface.
    
    Extract fused features in chunks: embeddings + handcrafted.
    Uses memory-mapped embeddings to avoid loading full arrays.
    
    Args:
        train_seqs: Dict mapping protein_id -> sequence
        features: List of feature keys to use (e.g., ['protbert','esm2','hc'])
        datatype: 'train' or 'test'
        chunk_size: Number of proteins per chunk (defaults to config)
        save_as_memmap: If True, save features as memmap instead of returning full array.
                       If None, auto-detect based on dataset size (>2GB threshold).
        
    Returns:
        (X_fused, aligned_proteins) - Feature matrix (or memmap path) and protein IDs
    """
    raise NotImplementedError(
        "extract_fused_features_chunked is deprecated. "
        "Use preprocessing.feature_extraction.extract_features() with "
        "config={'feature_type': 'fused_embeddings', 'features': [...]} "
        "for unified feature extraction with automatic memory optimization (chunking, memmap)."
    )

