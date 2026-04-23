"""
Memory-efficient streaming data loaders for CAFA 6 protein function prediction.
Uses generators and memory-mapped files to avoid loading all data into memory at once.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Generator, Optional
from Bio import SeqIO
from sklearn.preprocessing import MultiLabelBinarizer

from config.paths import DATA_INPUT_DIR
from config.features import BATCH_SIZE_CONFIG


def stream_sequences(data_dir: Path, chunk_size: Optional[int] = None) -> Generator[Dict[str, str], None, None]:
    """
    Stream training sequences in chunks to avoid loading all into memory.
    
    Args:
        data_dir: Path to data/input/Train directory
        chunk_size: Number of sequences per chunk (defaults to config)
        
    Yields:
        dict: Mapping protein_id -> sequence for current chunk
    """
    if chunk_size is None:
        chunk_size = BATCH_SIZE_CONFIG["data_loading"]["sequence_chunk_size"]
    
    # Load training terms to get target proteins
    train_terms = pd.read_csv(data_dir / 'train_terms.tsv', sep='\t', 
                              names=['protein', 'term', 'ontology'])
    target_proteins = set(train_terms['protein'].unique())
    
    current_chunk = {}
    chunk_count = 0
    
    print(f"   Streaming sequences in chunks of {chunk_size:,}...")
    
    for rec in SeqIO.parse(data_dir / 'train_sequences.fasta', 'fasta'):
        pid = rec.id.split('|')[1] if '|' in rec.id else rec.id
        if pid in target_proteins:
            current_chunk[pid] = str(rec.seq)
            
            # Yield chunk when it reaches chunk_size
            if len(current_chunk) >= chunk_size:
                chunk_count += 1
                print(f"      Yielding chunk {chunk_count} ({len(current_chunk):,} sequences)...")
                yield current_chunk
                current_chunk = {}
    
    # Yield remaining sequences
    if current_chunk:
        chunk_count += 1
        print(f"      Yielding final chunk {chunk_count} ({len(current_chunk):,} sequences)...")
        yield current_chunk
    
    print(f"   ✓ Streamed {chunk_count} chunks of sequences")


def load_embeddings_memmap(embedding_type: str, 
                          datatype: str = 'train',
                          base_path: Optional[Path] = None) -> Tuple[np.memmap, np.ndarray]:
    """
    Load embeddings using memory-mapped files (read-only, on-disk access).
    This avoids loading entire embedding arrays into memory.
    
    Wrapper around consolidated load_embedding_data() with use_memmap=True.
    
    Args:
        embedding_type: 'protbert', 'esm2', or 't5'
        datatype: 'train' or 'test'
        base_path: Optional base path override
        
    Returns:
        tuple: (embeddings_memmap, ids_array)
    """
    from preprocessing.feature_engineering.embeddings import load_embedding_data
    
    # Use consolidated function with memmap enabled
    return load_embedding_data(embedding_type, datatype, use_memmap=True, base_path=base_path)


def stream_labels(train_terms: pd.DataFrame, 
                 y_train_proteins: List[str],
                 ont_code: str,
                 propagate_labels: bool = False,
                 top_k_labels: Optional[int] = None) -> Tuple[MultiLabelBinarizer, np.ndarray]:
    """
    Load labels for a single ontology on-demand.
    This avoids creating label matrices for all ontologies upfront.
    
    Args:
        train_terms: DataFrame with protein, term, ontology columns
        y_train_proteins: List of protein IDs in training order
        ont_code: Ontology code ('F', 'P', 'C')
        propagate_labels: If True, propagate labels up GO graph
        top_k_labels: If specified, restrict to top-K most frequent terms
        
    Returns:
        tuple: (mlb, y_ont) - MultiLabelBinarizer and label matrix
    """
    from config import get_ontology_name
    from config.training import PROPAGATE_TRAIN_LABELS, TOP_K_LABELS
    from collections import Counter
    
    # Use config defaults if not provided
    if propagate_labels is None:
        propagate_labels = PROPAGATE_TRAIN_LABELS
    if top_k_labels is None:
        top_k_labels = TOP_K_LABELS
    
    ont_name = get_ontology_name(ont_code)
    print(f"   Loading labels for {ont_name} ({ont_code})...")
    
    # Filter terms for this ontology
    ont_terms = train_terms[train_terms['ontology'] == ont_code]
    
    # Create protein-to-terms mapping
    protein_terms = ont_terms.groupby('protein')['term'].apply(list).to_dict()
    
    # Propagate labels up GO graph if enabled
    if propagate_labels:
        from utils.go_utils import parse_obo_file, propagate_labels_up
        obo_path = DATA_INPUT_DIR / 'Train' / 'go-basic.obo'
        if obo_path.exists():
            print(f"      Propagating {ont_name} labels up GO graph...")
            parents_map, _ = parse_obo_file(obo_path)
            protein_terms = propagate_labels_up(protein_terms, parents_map)
        else:
            print(f"      ⚠️  Warning: OBO file not found at {obo_path}, skipping label propagation")
    
    # Top-K label selection
    if top_k_labels is not None and top_k_labels > 0:
        all_term_counts = Counter()
        for terms in protein_terms.values():
            all_term_counts.update(terms)
        
        top_terms = set([term for term, _ in all_term_counts.most_common(top_k_labels)])
        print(f"      Restricting to top-{top_k_labels} most frequent GO terms ({len(top_terms)} unique)")
        
        filtered_protein_terms = {}
        for pid, terms in protein_terms.items():
            filtered_protein_terms[pid] = [t for t in terms if t in top_terms]
        protein_terms = filtered_protein_terms
    
    # Align with training order
    labels_list = [protein_terms.get(pid, []) for pid in y_train_proteins]
    
    # Binarize labels - keep sparse to save memory
    mlb = MultiLabelBinarizer(sparse_output=True)
    y_ont = mlb.fit_transform(labels_list)
    
    print(f"      {ont_name}: {y_ont.shape[1]} unique terms")
    
    return mlb, y_ont


def get_all_sequences_dict(data_dir: Path) -> Dict[str, str]:
    """
    Load all sequences into a dict (backward compatibility).
    Use stream_sequences() for memory-efficient loading.
    
    Args:
        data_dir: Path to data/input/Train directory
        
    Returns:
        dict: Mapping protein_id -> sequence
    """
    print("   Loading all sequences into memory (consider using stream_sequences() for large datasets)...")
    
    train_terms = pd.read_csv(data_dir / 'train_terms.tsv', sep='\t', 
                              names=['protein', 'term', 'ontology'])
    target_proteins = set(train_terms['protein'].unique())
    
    train_seqs = {}
    for rec in SeqIO.parse(data_dir / 'train_sequences.fasta', 'fasta'):
        pid = rec.id.split('|')[1] if '|' in rec.id else rec.id
        if pid in target_proteins:
            train_seqs[pid] = str(rec.seq)
    
    print(f"   ✓ Loaded {len(train_seqs):,} training sequences")
    return train_seqs

