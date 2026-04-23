"""
GOA (Gene Ontology Annotation) negative propagation post-processing.
Filters predictions based on negative annotations from GOA database.

Based on the approach from the high-scoring reference notebook (0.364 score).
"""

import pandas as pd
import numpy as np
from collections import defaultdict
from pathlib import Path
from typing import Set, Dict, Tuple, Optional
from tqdm.auto import tqdm
from utils.utils_common import open_text_file


def parse_obo(go_obo_path: str) -> Tuple[Dict[str, set], Dict[str, set]]:
    """
    Parse GO ontology structure from .obo file.
    
    Args:
        go_obo_path: Path to go-basic.obo file
    
    Returns:
        (parents_map, children_map) - dictionaries mapping GO terms to parent/child sets
    """
    parents = defaultdict(set)
    children = defaultdict(set)
    
    if not Path(go_obo_path).exists():
        print(f"   [WARNING] OBO file not found: {go_obo_path}")
        return parents, children
    
    with open(go_obo_path, "r") as f:
        cur_id = None
        for line in f:
            line = line.strip()
            if line == "[Term]":
                cur_id = None
            elif line.startswith("id: "):
                cur_id = line.split("id: ")[1].strip()
            elif line.startswith("is_a: "):
                pid = line.split()[1].strip()
                if cur_id:
                    parents[cur_id].add(pid)
                    children[pid].add(cur_id)
            elif line.startswith("relationship: part_of "):
                parts = line.split()
                if len(parts) >= 3:
                    pid = parts[2].strip()
                    if cur_id:
                        parents[cur_id].add(pid)
                        children[pid].add(cur_id)
    
    print(f"   [INFO] Parsed OBO: {len(parents)} nodes with parents")
    return parents, children


def get_descendants(go_id: str, children_map: Dict[str, set]) -> Set[str]:
    """
    Get all descendants of a GO term (recursive traversal).
    
    Args:
        go_id: GO term ID
        children_map: Dictionary mapping GO terms to their children
    
    Returns:
        Set of descendant GO term IDs
    """
    desc = set()
    stack = [go_id]
    while stack:
        cur = stack.pop()
        for child in children_map.get(cur, []):
            if child not in desc:
                desc.add(child)
                stack.append(child)
    return desc


def load_goa_annotations(goa_path: str, version: str = "228") -> pd.DataFrame:
    """
    Load GOA annotations from TSV file.
    
    Args:
        goa_path: Base path to GOA annotations directory
        version: GOA version (default: "228")
    
    Returns:
        DataFrame with columns: protein_id, go_term, qualifier
    """
    goa_file = Path(goa_path) / f'goa_uniprot_ver{version}.tsv'
    
    if not goa_file.exists():
        # Try alternative naming
        goa_file = Path(goa_path) / f'goa_uniprot_ver{version}.csv'
    
    if not goa_file.exists():
        raise FileNotFoundError(
            f"GOA annotations file not found: {goa_file}\n"
            f"Expected: {Path(goa_path) / f'goa_uniprot_ver{version}.tsv'}"
        )
    
    print(f"   [INFO] Loading GOA annotations from: {goa_file}")
    
    # Read TSV or CSV
    sep = '\t' if goa_file.suffix == '.tsv' else ','
    goa_df = pd.read_csv(goa_file, sep=sep, dtype=str)
    
    # Ensure required columns exist
    required_cols = ['protein_id', 'go_term', 'qualifier']
    if not all(col in goa_df.columns for col in required_cols):
        # Try alternative column names
        if len(goa_df.columns) >= 3:
            goa_df.columns = required_cols[:len(goa_df.columns)]
        else:
            raise ValueError(
                f"GOA file must have columns: {required_cols}\n"
                f"Found: {list(goa_df.columns)}"
            )
    
    print(f"   [INFO] Loaded {len(goa_df):,} GOA annotations")
    return goa_df


def extract_negative_annotations(goa_df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract negative annotations (NOT qualifiers) from GOA DataFrame.
    
    Args:
        goa_df: GOA annotations DataFrame
    
    Returns:
        DataFrame with only negative annotations (NOT qualifiers)
    """
    negative_df = goa_df[goa_df['qualifier'].str.contains('NOT', na=False)].copy()
    negative_df = negative_df.drop(columns=['qualifier']).drop_duplicates()
    
    print(f"   [INFO] Found {len(negative_df):,} negative annotations")
    return negative_df


def propagate_negative_annotations(goa_annotations_path: str,
                                  go_obo_path: str,
                                  output_negative_keys: bool = True) -> Set[str]:
    """
    Build set of negative protein-GO pairs from GOA annotations.
    
    Logic:
    1. Load GOA annotations with NOT qualifiers
    2. Parse GO ontology structure
    3. For each negative annotation, propagate to all descendants
    4. Return set of 'protein_id_GO:term' keys to filter
    
    Args:
        goa_annotations_path: Path to GOA annotations directory
        go_obo_path: Path to go-basic.obo file
        output_negative_keys: If True, return set of keys; else dict
    
    Returns:
        set: Negative prediction keys (protein_id_GO:term format)
    """
    print("\n🔬 Building negative annotation set from GOA...")
    
    # Parse ontology
    print("   [1/3] Parsing GO ontology structure...")
    parents_map, children_map = parse_obo(go_obo_path)
    
    # Load GOA annotations
    print("   [2/3] Loading GOA annotations...")
    goa_df = load_goa_annotations(goa_annotations_path)
    
    # Filter negative annotations (NOT qualifiers)
    print("   [3/3] Extracting and propagating negative annotations...")
    negative_df = extract_negative_annotations(goa_df)
    
    # Group by protein
    negative_dict = negative_df.groupby('protein_id')['go_term'].apply(list).to_dict()
    
    # Propagate negatives to descendants
    propagated = {}
    for protein_id, terms in tqdm(negative_dict.items(), desc="Propagating negatives"):
        neg_set = set(terms)
        for term in terms:
            # Add all descendants
            neg_set |= get_descendants(term, children_map)
        propagated[protein_id] = sorted(neg_set)
    
    # Convert to prediction keys
    print("   [4/4] Converting to prediction keys...")
    negative_keys = set()
    for protein_id, terms in propagated.items():
        for term in terms:
            negative_keys.add(f"{protein_id}_{term}")
    
    print(f"   [✅] Total unique negative protein-GO pairs: {len(negative_keys):,}")
    return negative_keys


def filter_submission_with_goa(submission_path: str,
                               negative_keys: Set[str],
                               output_path: str) -> str:
    """
    Filter submission file to remove negative annotations.
    
    Args:
        submission_path: Path to raw submission TSV
        negative_keys: Set of negative protein_GO keys
        output_path: Path for filtered submission
    
    Returns:
        Path to filtered submission
    """
    print(f"\n🔬 Filtering submission with {len(negative_keys):,} negative keys...")
    
    filtered_count = 0
    total_count = 0
    kept_count = 0
    
    with open_text_file(submission_path, 'r') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:
        
        for line in tqdm(infile, desc="Filtering predictions"):
            total_count += 1
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                protein_id = parts[0]
                go_term = parts[1]
                pred_key = f"{protein_id}_{go_term}"
                
                if pred_key not in negative_keys:
                    outfile.write(line)
                    kept_count += 1
                else:
                    filtered_count += 1
    
    print(f"   [✅] Filtered {filtered_count:,} / {total_count:,} predictions")
    print(f"   [✅] Kept {kept_count:,} predictions ({kept_count/total_count*100:.2f}%)")
    
    return output_path


def apply_goa_filtering(submission_path: str,
                       goa_annotations_path: str,
                       go_obo_path: str,
                       output_path: Optional[str] = None) -> str:
    """
    Complete GOA filtering pipeline: build negative keys and filter submission.
    
    Args:
        submission_path: Path to raw submission TSV
        goa_annotations_path: Path to GOA annotations directory
        go_obo_path: Path to go-basic.obo file
        output_path: Optional output path (default: submission_path with '_filtered' suffix)
    
    Returns:
        Path to filtered submission
    """
    if output_path is None:
        output_path = str(Path(submission_path).with_suffix('')) + '_filtered.tsv'
    
    # Build negative keys
    negative_keys = propagate_negative_annotations(
        goa_annotations_path,
        go_obo_path
    )
    
    # Filter submission
    filtered_path = filter_submission_with_goa(
        submission_path,
        negative_keys,
        output_path
    )
    
    return filtered_path

