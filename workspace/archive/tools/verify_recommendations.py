#!/usr/bin/env python3
"""
Comprehensive Hyperparameter Recommendation Verification Tool

This tool:
1. Verifies that recommendations don't duplicate already-tested values
2. Identifies which recommendations are new
3. Generates improved recommendations focusing on NEW, untested values near top performers
4. Verifies duplicate detection in metadata
5. Creates clean recommendations excluding existing combinations
"""

import json
import statistics
import math
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any

# Import shared utilities
try:
    from hyperparameter_utils import (
        normalize_hyperparameters,
        find_duplicates_in_metadata,
        generate_combinations,
        filter_out_existing_combinations,
        extract_tested_values,
        load_and_join_metadata
    )
except ImportError:
    # Fallback if running from different directory
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from hyperparameter_utils import (
        normalize_hyperparameters,
        find_duplicates_in_metadata,
        generate_combinations,
        filter_out_existing_combinations,
        extract_tested_values,
        load_and_join_metadata
    )

# Load tested values from metadata
metadata_path = Path("csiro-metadata/lgbm/metadata.json")
with open(metadata_path, 'r') as f:
    metadata = json.load(f)

# Extract all tested hyperparameter values
tested_values = defaultdict(set)
for record in metadata:
    hyperparams = record.get('hyperparameters', {})
    for param in ['n_estimators', 'learning_rate', 'num_leaves', 'max_depth', 
                  'min_child_samples', 'subsample', 'colsample_bytree']:
        value = hyperparams.get(param)
        if value is not None:
            tested_values[param].add(value)

# Convert sets to sorted lists for comparison
tested_values = {k: sorted(list(v)) for k, v in tested_values.items()}

# Load recommendations
recommendations_path = Path("lgbm_clean_recommendations.json")
with open(recommendations_path, 'r') as f:
    recommendations = json.load(f)

# Load current 'quick' search config
current_quick = {
    'n_estimators': [50, 100, 200],
    'learning_rate': [0.005, 0.01, 0.02],
    'num_leaves': [31, 63, 127],
    'max_depth': [-1, 7],
    'min_child_samples': [10, 30],
    'subsample': [0.8, 0.9, 1.0],
    'colsample_bytree': [0.8, 0.9, 1.0],
}

print("="*80)
print("RECOMMENDATION VERIFICATION")
print("="*80)

print("\nTested Values (from metadata):")
for param, values in tested_values.items():
    print(f"  {param}: {values}")

print("\nCurrent 'quick' Search Config:")
for param, values in current_quick.items():
    print(f"  {param}: {values}")

print("\nRecommendations:")
for param, values in recommendations.items():
    print(f"  {param}: {values}")

print("\n" + "="*80)
print("ANALYSIS: New vs Already Tested")
print("="*80)

all_new = True
for param in recommendations.keys():
    rec_values = recommendations[param]
    tested_set = set(tested_values.get(param, []))
    current_set = set(current_quick.get(param, []))
    
    new_values = [v for v in rec_values if v not in tested_set]
    already_tested = [v for v in rec_values if v in tested_set]
    in_current_config = [v for v in rec_values if v in current_set]
    
    print(f"\n{param}:")
    print(f"  Recommended: {rec_values}")
    if new_values:
        print(f"  [NEW] Not tested: {new_values}")
    if already_tested:
        print(f"  [WARNING] Already tested: {already_tested}")
    if in_current_config:
        print(f"  [CURRENT] In current 'quick' config: {in_current_config}")
    
    if already_tested:
        all_new = False

print("\n" + "="*80)
if all_new:
    print("[PASS] All recommendations contain NEW values not yet tested!")
else:
    print("[WARNING] Some recommendations duplicate already-tested values")
print("="*80)

# Check if recommendations are based on top performers
print("\n" + "="*80)
print("TOP PERFORMER ANALYSIS")
print("="*80)

# Load gridsearch metadata to get scores
gridsearch_path = Path("csiro-metadata/lgbm/gridsearch_metadata.json")
with open(gridsearch_path, 'r') as f:
    gridsearch = json.load(f)

# Create lookup
metadata_dict = {item['variant_id']: item for item in metadata}
gridsearch_dict = {item['variant_id']: item for item in gridsearch}

# Get top 20 performers
combined = []
for variant_id in set(list(metadata_dict.keys()) + list(gridsearch_dict.keys())):
    meta_item = metadata_dict.get(variant_id)
    grid_item = gridsearch_dict.get(variant_id)
    if meta_item and grid_item:
        cv_score = grid_item.get('cv_score')
        if cv_score is not None:
            try:
                if isinstance(cv_score, float) and (cv_score != cv_score):  # NaN check
                    continue
                combined.append({
                    'variant_id': variant_id,
                    'hyperparameters': meta_item.get('hyperparameters', {}),
                    'cv_score': cv_score
                })
            except:
                pass

# Sort by score
combined.sort(key=lambda x: x.get('cv_score', -float('inf')), reverse=True)
top_20 = combined[:20]

print(f"\nTop 20 performers and their hyperparameters:")
for i, config in enumerate(top_20[:10], 1):
    print(f"\n{i}. Score: {config['cv_score']:.6f}")
    for param in ['n_estimators', 'learning_rate', 'num_leaves', 'max_depth', 
                  'min_child_samples', 'subsample', 'colsample_bytree']:
        value = config['hyperparameters'].get(param, 'N/A')
        print(f"   {param}: {value}")

# Check if recommendations align with top performers
print("\n" + "="*80)
print("RECOMMENDATION ALIGNMENT WITH TOP PERFORMERS")
print("="*80)

for param in recommendations.keys():
    rec_values = set(recommendations[param])
    top_values = set()
    for config in top_20:
        value = config['hyperparameters'].get(param)
        if value is not None:
            top_values.add(value)
    
    overlap = rec_values.intersection(top_values)
    print(f"\n{param}:")
    print(f"  Recommended: {sorted(list(rec_values))}")
    print(f"  In top 20: {sorted(list(top_values))}")
    print(f"  Overlap: {sorted(list(overlap)) if overlap else 'None'}")
    if not overlap:
        print(f"  [WARNING] No overlap with top 20 performers!")


def generate_improved_recommendations(
    tested_values: Dict[str, List[Any]],
    top_performers: List[Dict[str, Any]],
    current_quick: Dict[str, List[Any]]
) -> Dict[str, List[Any]]:
    """
    Generate improved recommendations focusing on NEW, untested values
    near top performers.
    
    Args:
        tested_values: Dictionary of tested parameter values
        top_performers: List of top performing configurations
        current_quick: Current 'quick' search config values
        
    Returns:
        Dictionary of improved recommendations with only NEW values
    """
    # Extract top performer parameter values
    top_param_values = defaultdict(set)
    for config in top_performers:
        hyperparams = config.get('hyperparameters', {})
        for param in ['n_estimators', 'learning_rate', 'num_leaves', 'max_depth',
                      'min_child_samples', 'subsample', 'colsample_bytree']:
            value = hyperparams.get(param)
            if value is not None:
                top_param_values[param].add(value)
    
    # Convert to lists and get statistics
    top_param_stats = {}
    for param, values in top_param_values.items():
        try:
            numeric_values = [float(v) for v in values]
            top_param_stats[param] = {
                'values': sorted(numeric_values),
                'min': min(numeric_values),
                'max': max(numeric_values),
                'median': statistics.median(numeric_values),
                'is_numeric': True
            }
        except (ValueError, TypeError):
            top_param_stats[param] = {
                'values': sorted(list(values)),
                'is_numeric': False
            }
    
    recommendations = {}
    tested_sets = {k: set(v) for k, v in tested_values.items()}
    current_sets = {k: set(v) for k, v in current_quick.items()}
    
    # Generate recommendations for each parameter
    for param in ['n_estimators', 'learning_rate', 'num_leaves', 'max_depth',
                  'min_child_samples', 'subsample', 'colsample_bytree']:
        tested_set = tested_sets.get(param, set())
        current_set = current_sets.get(param, set())
        stats = top_param_stats.get(param, {})
        
        new_values = []
        
        if stats.get('is_numeric', False):
            top_min = stats['min']
            top_max = stats['max']
            top_median = stats.get('median', (top_min + top_max) / 2)
            
            if param == 'n_estimators':
                # Top performers use 50, explore lower (40-45)
                candidates = [40, 42, 45]
                new_values = [v for v in candidates if v not in tested_set and v not in current_set]
                # If all candidates tested, try slightly different
                if not new_values:
                    candidates = [38, 43, 47]
                    new_values = [v for v in candidates if v not in tested_set and v not in current_set]
                    
            elif param == 'learning_rate':
                # Top performers use 0.005, explore lower (0.004-0.0045)
                candidates = [0.004, 0.0042, 0.0045]
                new_values = [round(v, 4) for v in candidates if round(v, 4) not in tested_set and round(v, 4) not in current_set]
                if not new_values:
                    candidates = [0.0038, 0.0043, 0.0047]
                    new_values = [round(v, 4) for v in candidates if round(v, 4) not in tested_set and round(v, 4) not in current_set]
                    
            elif param == 'num_leaves':
                # Top performers use 31-127, explore higher (137, 150+)
                candidates = [137, 150, 175, 200]
                new_values = [v for v in candidates if v not in tested_set and v not in current_set]
                if not new_values:
                    candidates = [140, 160, 180]
                    new_values = [v for v in candidates if v not in tested_set and v not in current_set]
                    
            elif param == 'max_depth':
                # Top performers use 7, explore higher (8, 9)
                candidates = [8, 9]
                new_values = [v for v in candidates if v not in tested_set and v not in current_set]
                if not new_values:
                    candidates = [10]
                    new_values = [v for v in candidates if v not in tested_set and v not in current_set]
                    
            elif param == 'min_child_samples':
                # Top performers use 30, explore around it (25, 31, 35)
                candidates = [25, 31, 35]
                new_values = [v for v in candidates if v not in tested_set and v not in current_set]
                if not new_values:
                    candidates = [28, 32, 33]
                    new_values = [v for v in candidates if v not in tested_set and v not in current_set]
                    
            elif param == 'subsample':
                # Top performers use 0.8-1.0, explore lower (0.75, 0.78)
                candidates = [0.75, 0.78]
                new_values = [round(v, 2) for v in candidates if round(v, 2) not in tested_set and round(v, 2) not in current_set]
                if not new_values:
                    candidates = [0.72, 0.77]
                    new_values = [round(v, 2) for v in candidates if round(v, 2) not in tested_set and round(v, 2) not in current_set]
                    
            elif param == 'colsample_bytree':
                # Top performers use 0.8-0.9, explore lower (0.75, 0.78)
                candidates = [0.75, 0.78]
                new_values = [round(v, 2) for v in candidates if round(v, 2) not in tested_set and round(v, 2) not in current_set]
                if not new_values:
                    candidates = [0.72, 0.77]
                    new_values = [round(v, 2) for v in candidates if round(v, 2) not in tested_set and round(v, 2) not in current_set]
        
        # Ensure we have at least some values
        if not new_values:
            # Fallback: use top performer values that aren't tested
            top_values = stats.get('values', [])
            new_values = [v for v in top_values if v not in tested_set and v not in current_set]
        
        # Remove duplicates and sort
        new_values = sorted(list(set(new_values)))
        if new_values:
            recommendations[param] = new_values
    
    return recommendations


def create_clean_recommendations(new_combos: List[Dict[str, Any]]) -> Dict[str, List[Any]]:
    """
    Create a clean recommendations file from new combinations.
    
    Extracts unique parameter values from new combinations.
    """
    if not new_combos:
        return {}
    
    # Collect all unique values per parameter
    param_values = defaultdict(set)
    
    for combo in new_combos:
        for param, value in combo.items():
            param_values[param].add(value)
    
    # Convert to sorted lists
    recommendations = {
        param: sorted(list(values))
        for param, values in param_values.items()
    }
    
    return recommendations


def main():
    """Main function with comprehensive verification and recommendation generation."""
    metadata_path = Path("csiro-metadata/lgbm/metadata.json")
    gridsearch_path = Path("csiro-metadata/lgbm/gridsearch_metadata.json")
    
    print("="*80)
    print("COMPREHENSIVE HYPERPARAMETER RECOMMENDATION VERIFICATION")
    print("="*80)
    
    # Load metadata
    print("\n1. Loading metadata...")
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    print(f"   Loaded {len(metadata)} variant entries")
    
    # Check for duplicates in metadata
    print("\n2. Checking for duplicates in metadata...")
    duplicates = find_duplicates_in_metadata(metadata)
    
    if duplicates:
        print(f"   WARNING: FOUND {len(duplicates)} DUPLICATE HYPERPARAMETER COMBINATIONS!")
        print(f"   This indicates duplicate detection may not be working correctly.\n")
        
        # Show first 5 duplicates
        print("   First 5 duplicate combinations:")
        for i, (sig, variants) in enumerate(list(duplicates.items())[:5], 1):
            print(f"\n   {i}. Signature: {sig}")
            for variant in variants[:2]:  # Show first 2 variants per duplicate
                print(f"      - {variant.get('variant_id')} (index: {variant.get('variant_index')})")
        
        if len(duplicates) > 5:
            print(f"\n   ... and {len(duplicates) - 5} more duplicates")
    else:
        print("   OK: No duplicates found - duplicate detection is working correctly")
    
    # Extract tested values using shared utility
    tested_values = extract_tested_values(metadata)
    
    # Load gridsearch metadata and get top performers
    print("\n3. Loading gridsearch results and identifying top performers...")
    with open(gridsearch_path, 'r') as f:
        gridsearch = json.load(f)
    
    # Create lookup and get top performers
    metadata_dict = {item['variant_id']: item for item in metadata}
    gridsearch_dict = {item['variant_id']: item for item in gridsearch}
    
    combined = []
    for variant_id in set(list(metadata_dict.keys()) + list(gridsearch_dict.keys())):
        meta_item = metadata_dict.get(variant_id)
        grid_item = gridsearch_dict.get(variant_id)
        if meta_item and grid_item:
            cv_score = grid_item.get('cv_score')
            if cv_score is not None:
                try:
                    if isinstance(cv_score, float) and (cv_score != cv_score):  # NaN check
                        continue
                    combined.append({
                        'variant_id': variant_id,
                        'hyperparameters': meta_item.get('hyperparameters', {}),
                        'cv_score': cv_score
                    })
                except:
                    pass
    
    # Sort by score
    combined.sort(key=lambda x: x.get('cv_score', -float('inf')), reverse=True)
    top_20 = combined[:20]
    print(f"   Identified top 20 performers (scores: {top_20[0]['cv_score']:.6f} to {top_20[-1]['cv_score']:.6f})")
    
    # Load current recommendations and 'quick' config
    recommendations_path = Path("lgbm_clean_recommendations.json")
    if recommendations_path.exists():
        with open(recommendations_path, 'r') as f:
            recommendations = json.load(f)
    else:
        recommendations = {}
    
    current_quick = {
        'n_estimators': [50, 100, 200],
        'learning_rate': [0.005, 0.01, 0.02],
        'num_leaves': [31, 63, 127],
        'max_depth': [-1, 7],
        'min_child_samples': [10, 30],
        'subsample': [0.8, 0.9, 1.0],
        'colsample_bytree': [0.8, 0.9, 1.0],
    }
    
    print("\n4. Analyzing current recommendations...")
    print("\nTested Values (from metadata):")
    for param, values in tested_values.items():
        print(f"  {param}: {values}")
    
    print("\nCurrent 'quick' Search Config:")
    for param, values in current_quick.items():
        print(f"  {param}: {values}")
    
    if recommendations:
        print("\nCurrent Recommendations:")
        for param, values in recommendations.items():
            print(f"  {param}: {values}")
        
        print("\n" + "="*80)
        print("ANALYSIS: New vs Already Tested")
        print("="*80)
        
        all_new = True
        for param in recommendations.keys():
            rec_values = recommendations[param]
            tested_set = set(tested_values.get(param, []))
            current_set = set(current_quick.get(param, []))
            
            new_values = [v for v in rec_values if v not in tested_set]
            already_tested = [v for v in rec_values if v in tested_set]
            in_current_config = [v for v in rec_values if v in current_set]
            
            print(f"\n{param}:")
            print(f"  Recommended: {rec_values}")
            if new_values:
                print(f"  [NEW] Not tested: {new_values}")
            if already_tested:
                print(f"  [WARNING] Already tested: {already_tested}")
            if in_current_config:
                print(f"  [CURRENT] In current 'quick' config: {in_current_config}")
            
            if already_tested:
                all_new = False
        
        print("\n" + "="*80)
        if all_new:
            print("[PASS] All recommendations contain NEW values not yet tested!")
        else:
            print("[WARNING] Some recommendations duplicate already-tested values")
        print("="*80)
        
        # Check combinations for duplicates
        print("\n5. Checking recommended combinations for duplicates...")
        all_combos = generate_combinations(recommendations)
        new_combos, existing_combos = filter_out_existing_combinations(all_combos, metadata)
        print(f"   Total combinations: {len(all_combos)}")
        print(f"   New combinations: {len(new_combos)}")
        print(f"   Already tested: {len(existing_combos)}")
        
        if existing_combos:
            print(f"\n   First 3 existing combinations (will be skipped):")
            for i, item in enumerate(existing_combos[:3], 1):
                combo = item['combination']
                variant_id = item['variant_id']
                print(f"   {i}. {combo} -> {variant_id}")
    
    # Generate improved recommendations
    print("\n" + "="*80)
    print("6. GENERATING IMPROVED RECOMMENDATIONS")
    print("="*80)
    
    improved_recommendations = generate_improved_recommendations(
        tested_values, top_20, current_quick
    )
    
    print("\nImproved Recommendations (NEW values only, near top performers):")
    for param, values in improved_recommendations.items():
        print(f"  {param}: {values}")
    
    # Verify improved recommendations
    print("\n" + "="*80)
    print("VERIFICATION OF IMPROVED RECOMMENDATIONS")
    print("="*80)
    
    all_new_improved = True
    for param, values in improved_recommendations.items():
        tested_set = set(tested_values.get(param, []))
        current_set = set(current_quick.get(param, []))
        
        new_values = [v for v in values if v not in tested_set and v not in current_set]
        already_tested = [v for v in values if v in tested_set]
        in_current = [v for v in values if v in current_set]
        
        print(f"\n{param}: {values}")
        if new_values:
            print(f"  [NEW] Untested: {new_values}")
        if already_tested:
            print(f"  [WARNING] Already tested: {already_tested}")
            all_new_improved = False
        if in_current:
            print(f"  [WARNING] In current config: {in_current}")
            all_new_improved = False
    
    print("\n" + "="*80)
    if all_new_improved:
        print("[PASS] All improved recommendations are NEW and untested!")
    else:
        print("[WARNING] Some improved recommendations still have issues")
    print("="*80)
    
    # Create clean recommendations from improved ones
    print("\n7. Creating clean recommendations from improved values...")
    improved_combos = generate_combinations(improved_recommendations)
    new_improved_combos, existing_improved_combos = filter_out_existing_combinations(improved_combos, metadata)
    clean_recommendations = create_clean_recommendations(new_improved_combos)
    
    if clean_recommendations:
        total_new = math.prod(len(v) for v in clean_recommendations.values())
        print(f"   Clean recommendations:")
        for param, values in clean_recommendations.items():
            print(f"     {param}: {values} ({len(values)} values)")
        print(f"   Total new combinations: {total_new}")
        
        # Save clean recommendations (only if different from current)
        clean_output_path = Path("lgbm_clean_recommendations.json")
        current_recs = {}
        if clean_output_path.exists():
            with open(clean_output_path, 'r') as f:
                current_recs = json.load(f)
        
        if clean_recommendations != current_recs:
            with open(clean_output_path, 'w') as f:
                json.dump(clean_recommendations, f, indent=2)
            print(f"\n   Updated clean recommendations saved to: {clean_output_path}")
        else:
            print(f"\n   Clean recommendations unchanged (already up to date)")
    else:
        print("   WARNING: No new combinations from improved recommendations!")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Metadata entries: {len(metadata)}")
    if duplicates:
        unique_count = len(metadata) - sum(len(v)-1 for v in duplicates.values())
        print(f"Unique hyperparameter combinations: {unique_count}")
        print(f"Duplicate combinations found: {len(duplicates)}")
    else:
        print(f"Unique hyperparameter combinations: {len(metadata)}")
    if recommendations:
        print(f"Current recommended combinations: {len(all_combos) if 'all_combos' in locals() else 0}")
        print(f"New combinations to test: {len(new_combos) if 'new_combos' in locals() else 0}")
    if improved_recommendations:
        print(f"Improved recommended combinations: {len(improved_combos) if 'improved_combos' in locals() else 0}")
        print(f"New improved combinations: {len(new_improved_combos) if 'new_improved_combos' in locals() else 0}")
    print("="*80)


if __name__ == "__main__":
    main()
