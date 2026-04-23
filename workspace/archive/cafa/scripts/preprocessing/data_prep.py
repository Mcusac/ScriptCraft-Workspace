"""
Data preparation for CAFA 6 protein function prediction.
Loads training data and prepares features and labels.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from Bio import SeqIO
from sklearn.preprocessing import MultiLabelBinarizer
from preprocessing.feature_engineering import extract_sequence_features, extract_handcrafted_parallel
from config import PROGRESS_INDICATOR_INTERVAL


def load_training_data(data_dir: Path) -> Tuple[Dict[str, str], pd.DataFrame, pd.DataFrame]:
    """
    Load training sequences, terms, and taxonomy data.
    
    Args:
        data_dir: Path to data/input/Train directory
        
    Returns:
        tuple: (train_seqs, train_terms, train_taxonomy)
    """
    print("   Loading training data...")
    
    try:
        # Load training terms and taxonomy
        train_terms = pd.read_csv(data_dir / 'train_terms.tsv', sep='\t', 
                                  names=['protein', 'term', 'ontology'])
        train_taxonomy = pd.read_csv(data_dir / 'train_taxonomy.tsv', sep='\t',
                                     names=['protein', 'taxon'])
        
        # Load training sequences
        train_seqs = {}
        target_proteins = set(train_terms['protein'].unique())
        
        for rec in SeqIO.parse(data_dir / 'train_sequences.fasta', 'fasta'):
            pid = rec.id.split('|')[1] if '|' in rec.id else rec.id
            if pid in target_proteins:
                train_seqs[pid] = str(rec.seq)
        
        print(f"   ✓ Loaded {len(train_seqs):,} training sequences")
        return train_seqs, train_terms, train_taxonomy
        
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Required data file not found: {e}")
    except Exception as e:
        raise RuntimeError(f"Error loading training data: {e}")


def extract_training_features(train_seqs: Dict[str, str], 
                             feature_type: str = 'hand_crafted',
                             embedding_type: str = 'protbert',
                             embedding_data: Optional[tuple] = None) -> Tuple[np.ndarray, List[str]]:
    """
    DEPRECATED: Use preprocessing.feature_extraction.extract_features() instead.
    This function loads full arrays into memory and may cause OOM errors.
    
    Extract features for all training proteins.
    
    Args:
        train_seqs: dict mapping protein_id -> sequence
        feature_type: 'hand_crafted' or 'embeddings'
        embedding_type: which embedding to use (if feature_type='embeddings')
        embedding_data: pre-loaded (embeds, ids) tuple OR None to auto-load
        
    Returns:
        tuple: (X_train, y_train_proteins)
    """
    raise NotImplementedError(
        "extract_training_features is deprecated. "
        "Use preprocessing.feature_extraction.extract_features() for unified feature extraction "
        "with automatic memory optimization (chunking, memmap)."
    )


def extract_fused_features(train_seqs: Dict[str, str],
                          features: List[str],
                          datatype: str = 'train') -> Tuple[np.ndarray, List[str]]:
    """
    DEPRECATED: Use preprocessing.feature_extraction.extract_features() instead.
    This function loads full embedding arrays into memory and may cause OOM errors.
    Use the unified interface which automatically uses chunked extraction with memmap.
    
    Extract fused features: embeddings + handcrafted.
    
    Args:
        train_seqs: dict mapping protein_id -> sequence
        features: list of feature keys to use (e.g., ['protbert','esm2','hc'])
        datatype: 'train' or 'test'
    
    Returns:
        (X_fused, aligned_proteins)
    """
    raise NotImplementedError(
        "extract_fused_features is deprecated. "
        "Use preprocessing.feature_extraction.extract_features() with "
        "config={'feature_type': 'fused_embeddings', 'features': [...]} "
        "for unified feature extraction with automatic memory optimization."
    )


def prepare_ontology_labels(train_terms, y_train_proteins, ont_codes: List[str],
                           propagate_labels: bool = False,
                           top_k_labels: Optional[int] = None):
    """
    Prepare separate label matrices for specified ontologies.
    
    Args:
        train_terms: DataFrame with protein, term, ontology columns
        y_train_proteins: list of protein IDs in training order
        ont_codes: List of ontology codes to process (e.g., ['F', 'P', 'C'] or ['P'])
        propagate_labels: If True, propagate labels up GO graph before binarization
        top_k_labels: If specified, restrict to top-K most frequent GO terms per ontology
        
    Returns:
        tuple: (mlb_dict, y_train_dict)
    """
    print(f"\n[5/9] Preparing labels for ontologies: {ont_codes}")
    
    from config import get_all_ontologies, get_ontology_name, DATA_INPUT_DIR
    from collections import Counter
    
    # Import training config values
    from config.training import PROPAGATE_TRAIN_LABELS, TOP_K_LABELS
    
    # Use config defaults if not provided
    if propagate_labels is None:
        propagate_labels = PROPAGATE_TRAIN_LABELS
    if top_k_labels is None:
        top_k_labels = TOP_K_LABELS
    
    ontologies = get_all_ontologies()
    mlb_dict = {}
    y_train_dict = {}
    
    # Load OBO file once if label propagation is enabled
    parents_map = None
    if propagate_labels:
        from utils.go_utils import parse_obo_file, propagate_labels_up
        obo_path = DATA_INPUT_DIR / 'Train' / 'go-basic.obo'
        if obo_path.exists():
            print("   Loading GO ontology for label propagation...")
            parents_map, _ = parse_obo_file(obo_path)
        else:
            print(f"   ⚠️  Warning: OBO file not found at {obo_path}, skipping label propagation")
            propagate_labels = False
    
    for ont_code in ont_codes:
        if ont_code not in ontologies:
            raise ValueError(f"Invalid ontology code: {ont_code}. Must be one of: {list(ontologies.keys())}")
        
        ont_name = get_ontology_name(ont_code)
        print(f"   Processing {ont_name}...")
        
        # Filter terms for this ontology
        ont_terms = train_terms[train_terms['ontology'] == ont_code]
        
        # Create protein-to-terms mapping
        protein_terms = ont_terms.groupby('protein')['term'].apply(list).to_dict()
        
        # Propagate labels up GO graph if enabled
        if propagate_labels and parents_map:
            print(f"      Propagating {ont_name} labels up GO graph...")
            protein_terms = propagate_labels_up(protein_terms, parents_map)
        
        # Top-K label selection: select most frequent terms
        if top_k_labels is not None and top_k_labels > 0:
            # Count term frequencies
            all_term_counts = Counter()
            for terms in protein_terms.values():
                all_term_counts.update(terms)
            
            # Select top-K most frequent terms
            top_terms = set([term for term, _ in all_term_counts.most_common(top_k_labels)])
            print(f"      Restricting to top-{top_k_labels} most frequent GO terms ({len(top_terms)} unique)")
            
            # Filter protein labels to only include selected terms
            filtered_protein_terms = {}
            for pid, terms in protein_terms.items():
                filtered_protein_terms[pid] = [t for t in terms if t in top_terms]
            protein_terms = filtered_protein_terms
        
        # Align with training order
        labels_list = [protein_terms.get(pid, []) for pid in y_train_proteins]
        
        # Binarize labels - keep sparse to save memory
        mlb = MultiLabelBinarizer(sparse_output=True)
        y_ont = mlb.fit_transform(labels_list)
        
        mlb_dict[ont_code] = mlb
        y_train_dict[ont_code] = y_ont
        
        print(f"      {ont_name}: {y_ont.shape[1]} unique terms")
    
    return mlb_dict, y_train_dict
