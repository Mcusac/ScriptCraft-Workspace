"""
GO (Gene Ontology) graph utilities for CAFA 6 protein function prediction.
Provides functions for parsing OBO files, ancestor lookup, and label/prediction propagation.
"""

from pathlib import Path
from typing import Dict, Set, List, Tuple, Optional
from collections import defaultdict
import numpy as np

try:
    import obonet
    import networkx as nx
    OBNET_AVAILABLE = True
except ImportError:
    OBNET_AVAILABLE = False


def parse_obo_file(obo_path: Path) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
    """
    Parse GO OBO file into parents and children maps.
    
    Uses obonet library if available, otherwise falls back to manual parsing.
    
    Args:
        obo_path: Path to go-basic.obo file
        
    Returns:
        tuple: (parents_map, children_map)
            - parents_map: dict mapping term_id -> set of parent term_ids
            - children_map: dict mapping term_id -> set of child term_ids
    """
    if not obo_path.exists():
        raise FileNotFoundError(f"OBO file not found: {obo_path}")
    
    parents_map = defaultdict(set)
    children_map = defaultdict(set)
    
    if OBNET_AVAILABLE:
        # Use obonet for parsing (faster and more robust)
        try:
            graph = obonet.read_obo(str(obo_path))
            
            for term_id in graph.nodes():
                # Get all parent terms via is_a and part_of relationships
                for parent_id in graph.predecessors(term_id):
                    parents_map[term_id].add(parent_id)
                    children_map[parent_id].add(term_id)
            
            print(f"[go_utils] Parsed OBO using obonet: {len(parents_map)} nodes with parents")
            return dict(parents_map), dict(children_map)
        except Exception as e:
            print(f"[go_utils] obonet parsing failed, falling back to manual parsing: {e}")
    
    # Manual parsing fallback (matches notebook approach)
    with open(obo_path, 'r', encoding='utf-8') as f:
        cur_id = None
        for line in f:
            line = line.strip()
            if line == "[Term]":
                cur_id = None
            elif line.startswith("id: "):
                cur_id = line.split("id: ")[1].strip()
            elif line.startswith("is_a: "):
                parts = line.split()
                if len(parts) >= 2:
                    parent_id = parts[1].strip()
                    if cur_id:
                        parents_map[cur_id].add(parent_id)
                        children_map[parent_id].add(cur_id)
            elif line.startswith("relationship: part_of "):
                parts = line.split()
                if len(parts) >= 3:
                    parent_id = parts[2].strip()
                    if cur_id:
                        parents_map[cur_id].add(parent_id)
                        children_map[parent_id].add(cur_id)
    
    print(f"[go_utils] Parsed OBO manually: {len(parents_map)} nodes with parents")
    return dict(parents_map), dict(children_map)


def get_ancestors(go_id: str, parents_map: Dict[str, Set[str]]) -> Set[str]:
    """
    Get all ancestor terms for a GO ID by traversing up the ontology graph.
    
    Args:
        go_id: GO term ID (e.g., 'GO:0003674')
        parents_map: Dictionary mapping term_id -> set of parent term_ids
        
    Returns:
        set: All ancestor GO term IDs (including transitive ancestors)
    """
    ancestors = set()
    stack = [go_id]
    
    while stack:
        current = stack.pop()
        for parent in parents_map.get(current, []):
            if parent not in ancestors:
                ancestors.add(parent)
                stack.append(parent)
    
    return ancestors


def propagate_labels_up(protein_terms_dict: Dict[str, List[str]], 
                       parents_map: Dict[str, Set[str]]) -> Dict[str, List[str]]:
    """
    Propagate protein labels up the GO graph by adding ancestor terms.
    
    For each protein, if it has a term, it also implicitly has all ancestor terms.
    This function adds those implicit ancestor terms to the label set.
    
    Args:
        protein_terms_dict: Dictionary mapping protein_id -> list of GO term IDs
        parents_map: Dictionary mapping term_id -> set of parent term_ids
        
    Returns:
        dict: Updated protein_terms_dict with propagated labels
    """
    propagated = {}
    
    for protein_id, terms in protein_terms_dict.items():
        term_set = set(terms)
        extra_ancestors = set()
        
        # For each term, get all its ancestors
        for term in list(term_set):
            ancestors = get_ancestors(term, parents_map)
            extra_ancestors |= ancestors
        
        # Combine original terms with ancestors
        propagated[protein_id] = sorted(term_set | extra_ancestors)
    
    return propagated


def propagate_predictions_batch(pred_batch: np.ndarray,
                               parents_map: Dict[str, Set[str]],
                               classes_list: List[str],
                               iterations: int = 3) -> np.ndarray:
    """
    Propagate predictions up the GO graph in batch.
    
    For each prediction, if a child term has a high score, propagate it to parent terms
    (using max operation: parent score = max(parent_score, child_score)).
    
    Args:
        pred_batch: Prediction probabilities, shape (batch_size, n_classes), dtype float32
        parents_map: Dictionary mapping term_id -> set of parent term_ids
        classes_list: List of GO term IDs in the same order as pred_batch columns
        iterations: Number of propagation iterations (default: 3)
        
    Returns:
        np.ndarray: Updated pred_batch with propagated predictions, same shape
    """
    if pred_batch.shape[1] != len(classes_list):
        raise ValueError(f"pred_batch columns ({pred_batch.shape[1]}) must match classes_list length ({len(classes_list)})")
    
    # Create restricted parents map (only include terms that are in classes_list)
    restricted_parents = {}
    term_to_idx = {term: idx for idx, term in enumerate(classes_list)}
    
    for term in classes_list:
        restricted_parents[term] = set()
        for parent in parents_map.get(term, []):
            if parent in term_to_idx:
                restricted_parents[term].add(parent)
    
    # Create index mapping for efficient lookup
    idx_map = {idx: classes_list[idx] for idx in range(len(classes_list))}
    
    # Propagate iteratively
    for iteration in range(iterations):
        changed = False
        
        # For each child term, update parent terms
        for child_idx in range(len(classes_list)):
            child_term = idx_map[child_idx]
            child_scores = pred_batch[:, child_idx]
            
            # Update each parent of this child
            for parent_term in restricted_parents.get(child_term, []):
                parent_idx = term_to_idx[parent_term]
                
                # Update parent where child's score exceeds parent's score
                mask = child_scores > pred_batch[:, parent_idx]
                if mask.any():
                    pred_batch[mask, parent_idx] = child_scores[mask]
                    changed = True
        
        # Early stopping if no changes
        if not changed:
            break
    
    return pred_batch

