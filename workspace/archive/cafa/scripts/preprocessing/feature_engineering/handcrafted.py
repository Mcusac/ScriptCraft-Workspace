"""
Feature engineering for protein sequences.
Extracted from starter_model.py for modularity and reusability.
"""

import numpy as np
from collections import Counter
from typing import Dict, List, Tuple
import warnings
import os
from concurrent.futures import ThreadPoolExecutor
warnings.filterwarnings('ignore')

# Constants for amino acid properties
AA_WEIGHTS = {
    'A': 89.1, 'C': 121.2, 'D': 133.1, 'E': 147.1, 'F': 165.2,
    'G': 75.1, 'H': 155.2, 'I': 131.2, 'K': 146.2, 'L': 131.2,
    'M': 149.2, 'N': 132.1, 'P': 115.1, 'Q': 146.2, 'R': 174.2,
    'S': 105.1, 'T': 119.1, 'V': 117.1, 'W': 204.2, 'Y': 181.2
}

HYDROPATHY_VALUES = {
    'A': 1.8, 'C': 2.5, 'D': -3.5, 'E': -3.5, 'F': 2.8,
    'G': -0.4, 'H': -3.2, 'I': 4.5, 'K': -3.9, 'L': 3.8,
    'M': 1.9, 'N': -3.5, 'P': -1.6, 'Q': -3.5, 'R': -4.5,
    'S': -0.8, 'T': -0.7, 'V': 4.2, 'W': -0.9, 'Y': -1.3
}

# Amino acid groups for CTD features
AA_GROUPS = {
    'hydrophobic': set('AILMFWYV'),
    'polar': set('RKHDESTQNC'),
    'positive': set('RKH'),
    'negative': set('DE'),
    'neutral_polar': set('STNQ'),
    'aromatic': set('FWY'),
    'aliphatic': set('ILV'),
    'small': set('ACDGNPSTV')
}


def calculate_physicochemical_properties(seq: str) -> np.ndarray:
    """
    Calculate advanced physicochemical properties.
    
    Args:
        seq: Amino acid sequence string
        
    Returns:
        Array of 8 physicochemical properties
    """
    if not seq or len(seq) == 0:
        return np.zeros(8)
    
    aa_counts = Counter(seq)
    length = len(seq)
    
    # Molecular weight (precise values from amino-acids.md)
    mol_weight = sum(aa_counts.get(aa, 0) * AA_WEIGHTS.get(aa, 0) for aa in aa_counts)
    
    # Aliphatic index
    aliphatic = (aa_counts.get('A', 0) + 2.9 * aa_counts.get('V', 0) + 
                 3.9 * (aa_counts.get('I', 0) + aa_counts.get('L', 0))) / length
    
    # Instability index (simplified)
    instability = sum(aa_counts.get(aa, 0) for aa in 'DEKRH') / length * 100
    
    # Charge properties
    positive = sum(aa_counts.get(aa, 0) for aa in 'RKH') / length
    negative = sum(aa_counts.get(aa, 0) for aa in 'DE') / length
    net_charge = positive - negative
    
    # Hydropathy (GRAVY)
    gravy = sum(aa_counts.get(aa, 0) * HYDROPATHY_VALUES.get(aa, 0) 
                for aa in aa_counts) / length
    
    # Aromaticity
    aromaticity = sum(aa_counts.get(aa, 0) for aa in 'FWY') / length
    
    return np.array([np.log1p(mol_weight), aliphatic, instability, positive, 
                     negative, net_charge, gravy, aromaticity])


def extract_kmer_features(seq, k=2):
    """Extract k-mer frequency features"""
    if not seq or len(seq) < k:
        return {}
    
    kmers = [seq[i:i+k] for i in range(len(seq) - k + 1)]
    kmer_counts = Counter(kmers)
    total = len(kmers)
    
    return {kmer: count / total for kmer, count in kmer_counts.items()}


def calculate_ctd_features(seq):
    """Calculate Composition, Transition, Distribution features"""
    if not seq or len(seq) == 0:
        return np.zeros(21)
    
    groups = {
        'hydrophobic': set('AILMFWYV'),
        'polar': set('RKHDESTQNC'),  # All charged + polar uncharged + Cys
        'positive': set('RKH'),      # Arg, Lys, His (pKa ~6, often positive)
        'negative': set('DE'),        # Asp, Glu
        'neutral_polar': set('STNQ'), # Ser, Thr, Asn, Gln (polar uncharged)
        'aromatic': set('FWY'),
        'aliphatic': set('ILV'),
        'small': set('ACDGNPSTV')
    }
    
    features = []
    
    # Composition: fraction of each group
    for group_aas in groups.values():
        composition = sum(1 for aa in seq if aa in group_aas) / len(seq)
        features.append(composition)
    
    # Transition: frequency of transitions between groups
    for group_aas in list(groups.values())[:3]:
        transitions = sum(1 for i in range(len(seq)-1) 
                         if (seq[i] in group_aas) != (seq[i+1] in group_aas))
        features.append(transitions / (len(seq) - 1) if len(seq) > 1 else 0)
    
    # Distribution: position of first, middle, last occurrence
    for group_aas in list(groups.values())[:2]:
        positions = [i for i, aa in enumerate(seq) if aa in group_aas]
        if positions:
            features.extend([
                positions[0] / len(seq),
                positions[len(positions)//2] / len(seq),
                positions[-1] / len(seq)
            ])
        else:
            features.extend([0, 0, 0])
    
    return np.array(features)


def extract_sequence_features(seq):
    """Extract comprehensive features from amino acid sequence"""
    if not seq or len(seq) == 0:
        return np.zeros(90)
    
    # 1. Amino acid composition (20 features)
    aa_counts = Counter(seq)
    aa_freq = np.array([aa_counts.get(aa, 0) / len(seq) 
                        for aa in 'ACDEFGHIKLMNPQRSTVWY'])
    
    # 2. Basic properties (5 features)
    length = len(seq)
    hydrophobic = sum(aa_counts.get(aa, 0) for aa in 'AILMFWYV') / len(seq)
    charged = sum(aa_counts.get(aa, 0) for aa in 'DEKRH') / len(seq)
    polar = sum(aa_counts.get(aa, 0) for aa in 'STNQ') / len(seq)
    aromatic = sum(aa_counts.get(aa, 0) for aa in 'FWY') / len(seq)
    
    basic_props = np.array([np.log1p(length), hydrophobic, charged, polar, aromatic])
    
    # 3. Physicochemical properties (8 features)
    physichem = calculate_physicochemical_properties(seq)
    
    # 4. CTD features (21 features)
    ctd = calculate_ctd_features(seq)
    
    # 5. Di-peptide features (top 20 most common)
    dipeptides = extract_kmer_features(seq, k=2)
    top_dipeptides = ['AL', 'LA', 'LE', 'EA', 'AA', 'AS', 'SA', 'EL', 'LL', 'AE',
                      'SE', 'ES', 'GA', 'AG', 'VA', 'AV', 'LV', 'VL', 'LS', 'SL']
    dipeptide_freq = np.array([dipeptides.get(dp, 0) for dp in top_dipeptides])
    
    # 6. Tri-peptide features (top 10 most common)
    tripeptides = extract_kmer_features(seq, k=3)
    top_tripeptides = ['ALA', 'LEA', 'EAL', 'LAL', 'AAA', 'LLE', 'ELE', 
                       'ALE', 'GAL', 'ASA']
    tripeptide_freq = np.array([tripeptides.get(tp, 0) for tp in top_tripeptides])
    
    # 7. Sequence position features (6 features)
    n_term = seq[:30] if len(seq) > 30 else seq
    n_hydrophobic = sum(1 for aa in n_term if aa in 'AILMFWYV') / len(n_term)
    n_charged = sum(1 for aa in n_term if aa in 'DEKRH') / len(n_term)
    
    c_term = seq[-30:] if len(seq) > 30 else seq
    c_hydrophobic = sum(1 for aa in c_term if aa in 'AILMFWYV') / len(c_term)
    c_charged = sum(1 for aa in c_term if aa in 'DEKRH') / len(c_term)
    
    if len(seq) > 60:
        mid_term = seq[30:-30]
        mid_hydrophobic = sum(1 for aa in mid_term if aa in 'AILMFWYV') / len(mid_term)
        mid_charged = sum(1 for aa in mid_term if aa in 'DEKRH') / len(mid_term)
    else:
        mid_hydrophobic = hydrophobic
        mid_charged = charged
    
    position_features = np.array([n_hydrophobic, n_charged, c_hydrophobic, 
                                   c_charged, mid_hydrophobic, mid_charged])
    
    # Combine all features (Total: 90 features)
    features = np.concatenate([
        aa_freq,           # 20
        basic_props,       # 5
        physichem,         # 8
        ctd,              # 21
        dipeptide_freq,    # 20
        tripeptide_freq,   # 10
        position_features  # 6
    ])
    
    return features


def extract_handcrafted_parallel(train_seqs: Dict[str, str], 
                                 protein_ids: List[str],
                                 max_workers: int = None) -> np.ndarray:
    """
    Extract handcrafted features for multiple proteins in parallel.
    Consolidates the ThreadPoolExecutor pattern used across preprocessing modules.
    
    Args:
        train_seqs: Dict mapping protein_id -> sequence
        protein_ids: List of protein IDs to extract features for
        max_workers: Maximum number of worker threads (defaults to config)
        
    Returns:
        np.ndarray: Feature matrix (n_samples, n_features) as float32
    """
    from config.training import FEATURE_EXTRACTION_MAX_WORKERS
    
    if max_workers is None:
        max_workers = min(FEATURE_EXTRACTION_MAX_WORKERS, os.cpu_count() or 1)
    
    def extract_features_for_protein(pid):
        return extract_sequence_features(train_seqs[pid])
    
    # Use ThreadPoolExecutor for parallel feature extraction
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        features = list(executor.map(extract_features_for_protein, protein_ids))
    
    return np.array(features, dtype=np.float32)
