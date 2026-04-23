#!/usr/bin/env python3
"""
Shared utilities for hyperparameter analysis and verification tools.

This module provides common functions used across multiple tools to reduce
code duplication and improve maintainability.
"""

from typing import Dict, List, Any, Tuple
from collections import defaultdict
import json


# LGBM hyperparameters to analyze
LGBM_HYPERPARAMETERS = [
    'n_estimators',
    'learning_rate',
    'num_leaves',
    'max_depth',
    'min_child_samples',
    'subsample',
    'colsample_bytree'
]


def normalize_hyperparameters(hyperparams: Dict[str, Any]) -> Tuple:
    """
    Normalize hyperparameters to a comparable signature.
    
    This matches the normalization used across tools for consistent comparison.
    
    Args:
        hyperparams: Dictionary of hyperparameters
        
    Returns:
        Tuple of normalized values in consistent order
    """
    param_order = LGBM_HYPERPARAMETERS
    
    normalized = []
    for param in param_order:
        value = hyperparams.get(param)
        if value is None:
            normalized.append(None)
        elif param in ['learning_rate', 'subsample', 'colsample_bytree']:
            # Round floats to 4 decimal places for consistent comparison
            normalized.append(round(float(value), 4))
        elif param in ['n_estimators', 'num_leaves', 'max_depth', 'min_child_samples']:
            # Convert to int (handles -1 for max_depth)
            normalized.append(int(value))
        else:
            normalized.append(value)
    
    return tuple(normalized)


def find_duplicates_in_metadata(metadata: List[Dict[str, Any]]) -> Dict[Tuple, List[Dict[str, Any]]]:
    """
    Find all duplicate hyperparameter combinations in metadata.
    
    Args:
        metadata: List of metadata entries with hyperparameters
        
    Returns:
        Dictionary mapping normalized signature to list of variant entries with that signature
    """
    signature_to_variants = defaultdict(list)
    
    for entry in metadata:
        hyperparams = entry.get('hyperparameters', {})
        if hyperparams:
            signature = normalize_hyperparameters(hyperparams)
            signature_to_variants[signature].append(entry)
    
    # Filter to only duplicates (more than one variant with same signature)
    duplicates = {
        sig: variants
        for sig, variants in signature_to_variants.items()
        if len(variants) > 1
    }
    
    return duplicates


def load_and_join_metadata(
    metadata_path: str,
    gridsearch_path: str
) -> List[Dict[str, Any]]:
    """
    Load both metadata files and join by variant_id.
    
    Args:
        metadata_path: Path to metadata.json
        gridsearch_path: Path to gridsearch_metadata.json
        
    Returns:
        List of combined records with hyperparameters and scores
    """
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    with open(gridsearch_path, 'r') as f:
        gridsearch = json.load(f)
    
    # Create lookup dictionaries
    metadata_dict = {item['variant_id']: item for item in metadata}
    gridsearch_dict = {item['variant_id']: item for item in gridsearch}
    
    # Join data
    combined = []
    for variant_id in set(list(metadata_dict.keys()) + list(gridsearch_dict.keys())):
        meta_item = metadata_dict.get(variant_id)
        grid_item = gridsearch_dict.get(variant_id)
        
        if meta_item and grid_item:
            combined.append({
                'variant_id': variant_id,
                'variant_index': meta_item.get('variant_index'),
                'hyperparameters': meta_item.get('hyperparameters', {}),
                'cv_score': grid_item.get('cv_score'),
                'fold_scores': grid_item.get('fold_scores', []),
                'feature_filename': grid_item.get('feature_filename')
            })
    
    return combined


def extract_tested_values(metadata: List[Dict[str, Any]]) -> Dict[str, List[Any]]:
    """
    Extract all tested hyperparameter values from metadata.
    
    Args:
        metadata: List of metadata entries
        
    Returns:
        Dictionary mapping parameter names to sorted lists of tested values
    """
    tested_values = defaultdict(set)
    
    for record in metadata:
        hyperparams = record.get('hyperparameters', {})
        for param in LGBM_HYPERPARAMETERS:
            value = hyperparams.get(param)
            if value is not None:
                tested_values[param].add(value)
    
    # Convert sets to sorted lists
    return {k: sorted(list(v)) for k, v in tested_values.items()}


def generate_combinations(recommendations: Dict[str, List[Any]]) -> List[Dict[str, Any]]:
    """
    Generate all hyperparameter combinations from recommendations.
    
    Args:
        recommendations: Dictionary mapping parameter names to lists of values
        
    Returns:
        List of all possible hyperparameter combination dictionaries
    """
    import itertools
    
    param_names = list(recommendations.keys())
    value_lists = [recommendations[param] for param in param_names]
    
    combinations = []
    for combo in itertools.product(*value_lists):
        combination_dict = dict(zip(param_names, combo))
        combinations.append(combination_dict)
    
    return combinations


def filter_out_existing_combinations(
    recommended_combos: List[Dict[str, Any]],
    metadata: List[Dict[str, Any]]
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Filter out combinations that already exist in metadata.
    
    Args:
        recommended_combos: List of recommended hyperparameter combinations
        metadata: List of metadata entries with existing hyperparameters
        
    Returns:
        Tuple of (new_combinations, existing_combinations)
    """
    # Build set of existing signatures
    existing_signatures = set()
    existing_map = {}  # signature -> variant_id for reporting
    
    for entry in metadata:
        hyperparams = entry.get('hyperparameters', {})
        if hyperparams:
            signature = normalize_hyperparameters(hyperparams)
            existing_signatures.add(signature)
            if signature not in existing_map:
                existing_map[signature] = entry.get('variant_id')
    
    new_combos = []
    existing_combos = []
    
    for combo in recommended_combos:
        signature = normalize_hyperparameters(combo)
        if signature in existing_signatures:
            existing_combos.append({
                'combination': combo,
                'variant_id': existing_map.get(signature)
            })
        else:
            new_combos.append(combo)
    
    return new_combos, existing_combos
