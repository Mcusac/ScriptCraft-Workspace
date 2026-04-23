"""
Data loading for training workflow.
Uses streaming loaders to avoid loading all data into memory at once.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Union, Optional

from preprocessing.data_prep import load_training_data
from preprocessing.data_streaming import (
    stream_sequences,
    load_embeddings_memmap,
    stream_labels,
    get_all_sequences_dict
)
from config import ONTOLOGY_CODES
from config.training import LOAD_LABELS_PER_ONTOLOGY, FREE_FEATURES_AFTER_ONTOLOGY
from utils.logging import get_logger

logger = get_logger(__name__)


def load_training_data_streaming(data_dir: Path, 
                                use_streaming: bool = True) -> Tuple[Dict[str, str], pd.DataFrame, pd.DataFrame]:
    """
    Load training data using streaming if enabled, otherwise use standard loader.
    
    Args:
        data_dir: Path to data/input/Train directory
        use_streaming: If True, use streaming (collects all chunks into dict for compatibility)
        
    Returns:
        tuple: (train_seqs, train_terms, train_taxonomy)
    """
    if use_streaming:
        # For now, collect all chunks into dict (maintains compatibility)
        # Future: could yield chunks directly
        logger.info("Loading sequences using streaming...")
        train_seqs = {}
        for chunk in stream_sequences(data_dir):
            train_seqs.update(chunk)
        logger.info(f"   ✓ Loaded {len(train_seqs):,} sequences via streaming")
    else:
        # Use standard loader (backward compatibility)
        train_seqs, train_terms, train_taxonomy = load_training_data(data_dir)
        return train_seqs, train_terms, train_taxonomy
    
    # Load terms and taxonomy (small, can load into memory)
    train_terms = pd.read_csv(data_dir / 'train_terms.tsv', sep='\t', 
                              names=['protein', 'term', 'ontology'])
    train_taxonomy = pd.read_csv(data_dir / 'train_taxonomy.tsv', sep='\t',
                                 names=['protein', 'taxon'])
    
    return train_seqs, train_terms, train_taxonomy


def extract_features_streaming(train_seqs: Dict[str, str],
                               model_config: Dict,
                               use_streaming: bool = True) -> Tuple[Union[np.ndarray, Path], List[str]]:
    """
    Extract features using unified extraction interface with automatic memory optimization.
    
    Args:
        train_seqs: Dict mapping protein_id -> sequence
        model_config: Model configuration dict
        use_streaming: If True, use chunked feature extraction (always True for unified interface)
        
    Returns:
        tuple: (X_train, y_train_proteins) where X_train may be np.ndarray or Path (memmap)
    """
    from preprocessing.feature_extraction import extract_features
    from config.features import validate_feature_availability, INDIVIDUAL_FEATURES
    
    # Parse feature configuration
    from config.features import parse_model_feature_config
    feature_type, features = parse_model_feature_config(model_config)
    logger.info(f"Feature type: {feature_type}")
    
    # Validate embedding availability for fused embeddings
    if feature_type == 'fused_embeddings' and features:
        print(f"   Features: {features}")
        emb_features = [f for f in features if INDIVIDUAL_FEATURES.get(f, {}).get('type') == 'embedding']
        ok, missing = validate_feature_availability(emb_features)
        if not ok:
            raise FileNotFoundError("Missing embedding files: " + ", ".join(missing))
    
    # Use unified extraction interface - FORCE memmap to save RAM
    logger.info("Extracting features using unified interface (auto-optimized for memory)...")
    X_train, y_train_proteins = extract_features(
        sequences=train_seqs,
        config=model_config,
        datatype='train',
        force_memmap=True  # Force memmap to save RAM (features stay on disk)
    )
    
    # If X_train is still an array (not memmap), convert it to memmap
    if isinstance(X_train, np.ndarray):
        from utils.memory_efficient import save_features_memmap_with_metadata
        from config.paths import DATA_OUTPUT_DIR
        
        logger.info("   Converting features to memmap to save RAM...")
        memmap_dir = DATA_OUTPUT_DIR / 'memmap_cache'
        memmap_dir.mkdir(parents=True, exist_ok=True)
        memmap_path = memmap_dir / f'features_train_{id(X_train)}.npy'
        X_train_path = save_features_memmap_with_metadata(X_train, memmap_path)
        logger.info(f"   ✓ Features saved to memmap: {X_train_path}")
        
        # Delete original array to free RAM
        del X_train
        import gc
        gc.collect()
        
        # Return path instead of array
        X_train = X_train_path
    
    return X_train, y_train_proteins


def prepare_labels_streaming(train_terms: pd.DataFrame,
                            y_train_proteins: List[str],
                            ont_codes: List[str],
                            use_per_ontology: bool = None) -> Tuple[Dict, Dict]:
    """
    Prepare labels using per-ontology loading if enabled.
    
    Args:
        train_terms: DataFrame with protein, term, ontology columns
        y_train_proteins: List of protein IDs in training order
        ont_codes: List of ontology codes to process
        use_per_ontology: If True, load labels per-ontology (defaults to config)
        
    Returns:
        tuple: (mlb_dict, y_train_dict)
    """
    if use_per_ontology is None:
        use_per_ontology = LOAD_LABELS_PER_ONTOLOGY
    
    from preprocessing.data_prep import prepare_ontology_labels
    
    if use_per_ontology:
        # Load labels per-ontology on-demand (saves memory)
        logger.info("Loading labels per-ontology on-demand...")
        mlb_dict = {}
        y_train_dict = {}
        
        for ont_code in ont_codes:
            mlb, y_ont = stream_labels(
                train_terms, y_train_proteins, ont_code
            )
            mlb_dict[ont_code] = mlb
            y_train_dict[ont_code] = y_ont
    else:
        # Load all labels upfront (backward compatibility)
        mlb_dict, y_train_dict = prepare_ontology_labels(
            train_terms, y_train_proteins, ont_codes
        )
    
    return mlb_dict, y_train_dict

