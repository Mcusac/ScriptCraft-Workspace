#!/usr/bin/env python3
"""
LGBM Hyperparameter Analysis Script

Analyzes grid search results from metadata files to identify hyperparameter
patterns and recommend focused grid search ranges for further tuning.
"""

import json
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Any
import sys

# Add csiro-scripts to path for imports
sys.path.insert(0, str(Path(__file__).parent / "csiro-scripts" / "scripts"))

try:
    from utils.system import load_json_file
except ImportError:
    # Fallback if import fails
    def load_json_file(file_path, **kwargs):
        with open(file_path, 'r') as f:
            return json.load(f)


# Import shared utilities
try:
    from hyperparameter_utils import (
        LGBM_HYPERPARAMETERS,
        load_and_join_metadata as utils_load_and_join,
        extract_tested_values
    )
except ImportError:
    # Fallback if import fails (when running from different directory)
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from hyperparameter_utils import (
        LGBM_HYPERPARAMETERS,
        load_and_join_metadata as utils_load_and_join,
        extract_tested_values
    )


def load_and_join_metadata(
    metadata_path: str,
    gridsearch_path: str
) -> List[Dict[str, Any]]:
    """
    Load both metadata files and join by variant_id.
    
    Uses shared utility but adds logging for missing records.
    
    Args:
        metadata_path: Path to metadata.json
        gridsearch_path: Path to gridsearch_metadata.json
        
    Returns:
        List of combined records with hyperparameters and scores
    """
    print("Loading metadata files...")
    combined = utils_load_and_join(metadata_path, gridsearch_path)
    
    # Load separately to check for missing records
    metadata = load_json_file(metadata_path)
    gridsearch = load_json_file(gridsearch_path)
    
    metadata_dict = {item['variant_id']: item for item in metadata}
    gridsearch_dict = {item['variant_id']: item for item in gridsearch}
    
    missing_metadata = []
    missing_gridsearch = []
    
    for variant_id in set(list(metadata_dict.keys()) + list(gridsearch_dict.keys())):
        meta_item = metadata_dict.get(variant_id)
        grid_item = gridsearch_dict.get(variant_id)
        
        if meta_item and not grid_item:
            missing_gridsearch.append(variant_id)
        elif grid_item and not meta_item:
            missing_metadata.append(variant_id)
    
    print(f"Loaded {len(combined)} combined records")
    if missing_metadata:
        print(f"Warning: {len(missing_metadata)} gridsearch results missing metadata")
    if missing_gridsearch:
        print(f"Warning: {len(missing_gridsearch)} metadata entries missing gridsearch results")
    
    return combined


def calculate_parameter_statistics(
    combined_data: List[Dict[str, Any]],
    param_name: str
) -> Dict[str, Any]:
    """
    Calculate statistics for a specific hyperparameter.
    
    Args:
        combined_data: Combined metadata and results
        param_name: Name of hyperparameter to analyze
        
    Returns:
        Dictionary with statistics
    """
    # Extract parameter values and scores
    param_scores = []
    for record in combined_data:
        param_value = record.get('hyperparameters', {}).get(param_name)
        cv_score = record.get('cv_score')
        
        if param_value is not None and cv_score is not None:
            # Handle NaN scores
            if isinstance(cv_score, float) and (cv_score != cv_score):
                continue
            param_scores.append((param_value, cv_score))
    
    if not param_scores:
        return {'error': f'No valid data for {param_name}'}
    
    # Group by parameter value
    value_groups = defaultdict(list)
    for param_value, score in param_scores:
        value_groups[param_value].append(score)
    
    # Calculate statistics per value
    value_stats = {}
    for value, scores in value_groups.items():
        value_stats[value] = {
            'count': len(scores),
            'mean': statistics.mean(scores),
            'median': statistics.median(scores),
            'std': statistics.stdev(scores) if len(scores) > 1 else 0.0,
            'min': min(scores),
            'max': max(scores)
        }
    
    # Calculate overall correlation (if numeric)
    param_values = [pv for pv, _ in param_scores]
    scores = [s for _, s in param_scores]
    
    try:
        # Check if parameter is numeric
        numeric_values = [float(v) for v in param_values]
        # Simple correlation calculation
        if len(set(numeric_values)) > 1:
            correlation = calculate_correlation(numeric_values, scores)
        else:
            correlation = None
    except (ValueError, TypeError):
        correlation = None
    
    # Overall statistics
    all_scores = [s for _, s in param_scores]
    
    return {
        'parameter': param_name,
        'unique_values': len(value_stats),
        'total_records': len(param_scores),
        'value_statistics': value_stats,
        'correlation': correlation,
        'overall_score_stats': {
            'mean': statistics.mean(all_scores),
            'median': statistics.median(all_scores),
            'std': statistics.stdev(all_scores) if len(all_scores) > 1 else 0.0,
            'min': min(all_scores),
            'max': max(all_scores)
        }
    }


def calculate_correlation(x: List[float], y: List[float]) -> float:
    """
    Calculate Pearson correlation coefficient.
    
    Args:
        x: First variable
        y: Second variable
        
    Returns:
        Correlation coefficient
    """
    n = len(x)
    if n < 2:
        return 0.0
    
    mean_x = statistics.mean(x)
    mean_y = statistics.mean(y)
    
    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    sum_sq_x = sum((x[i] - mean_x) ** 2 for i in range(n))
    sum_sq_y = sum((y[i] - mean_y) ** 2 for i in range(n))
    
    denominator = (sum_sq_x * sum_sq_y) ** 0.5
    
    if denominator == 0:
        return 0.0
    
    return numerator / denominator


def identify_top_performers(
    combined_data: List[Dict[str, Any]],
    top_n: int = 20
) -> List[Dict[str, Any]]:
    """
    Identify top N performing configurations.
    
    Args:
        combined_data: Combined metadata and results
        top_n: Number of top performers to return
        
    Returns:
        List of top N configurations sorted by cv_score
    """
    # Filter valid scores
    valid_data = [
        r for r in combined_data
        if r.get('cv_score') is not None
        and not (isinstance(r.get('cv_score'), float) and (r['cv_score'] != r['cv_score']))
    ]
    
    # Sort by cv_score (descending)
    sorted_data = sorted(
        valid_data,
        key=lambda x: x.get('cv_score', -float('inf')),
        reverse=True
    )
    
    return sorted_data[:top_n]


def analyze_parameter_trends(
    combined_data: List[Dict[str, Any]],
    param_name: str
) -> Dict[str, Any]:
    """
    Analyze trends in parameter values vs scores.
    
    Args:
        combined_data: Combined metadata and results
        param_name: Name of hyperparameter to analyze
        
    Returns:
        Dictionary with trend analysis
    """
    # Extract parameter values and scores
    param_scores = []
    for record in combined_data:
        param_value = record.get('hyperparameters', {}).get(param_name)
        cv_score = record.get('cv_score')
        
        if param_value is not None and cv_score is not None:
            if isinstance(cv_score, float) and (cv_score != cv_score):
                continue
            param_scores.append((param_value, cv_score))
    
    if not param_scores:
        return {'error': f'No valid data for {param_name}'}
    
    # Check if numeric
    try:
        numeric_values = [float(v) for v, _ in param_scores]
        is_numeric = True
    except (ValueError, TypeError):
        is_numeric = False
        numeric_values = None
    
    if is_numeric:
        # Sort by parameter value
        sorted_data = sorted(param_scores, key=lambda x: float(x[0]))
        
        # Calculate trend: compare scores at low vs high parameter values
        low_third = sorted_data[:len(sorted_data)//3]
        high_third = sorted_data[-len(sorted_data)//3:]
        
        low_scores = [s for _, s in low_third]
        high_scores = [s for _, s in high_third]
        
        low_mean = statistics.mean(low_scores)
        high_mean = statistics.mean(high_scores)
        
        trend = 'increasing' if high_mean > low_mean else 'decreasing' if high_mean < low_mean else 'stable'
        trend_strength = abs(high_mean - low_mean) / (statistics.stdev([low_mean, high_mean]) + 1e-10)
        
        return {
            'parameter': param_name,
            'is_numeric': True,
            'trend': trend,
            'trend_strength': trend_strength,
            'low_value_mean_score': low_mean,
            'high_value_mean_score': high_mean,
            'low_value_range': (float(sorted_data[0][0]), float(sorted_data[len(sorted_data)//3-1][0])),
            'high_value_range': (float(sorted_data[-len(sorted_data)//3][0]), float(sorted_data[-1][0]))
        }
    else:
        # Categorical: rank by mean score
        value_groups = defaultdict(list)
        for param_value, score in param_scores:
            value_groups[param_value].append(score)
        
        value_means = {
            value: statistics.mean(scores)
            for value, scores in value_groups.items()
        }
        
        sorted_values = sorted(value_means.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'parameter': param_name,
            'is_numeric': False,
            'value_ranking': sorted_values,
            'best_value': sorted_values[0][0] if sorted_values else None,
            'best_value_mean_score': sorted_values[0][1] if sorted_values else None
        }


def generate_focused_grid_recommendations(
    combined_data: List[Dict[str, Any]],
    tested_values: Dict[str, List[Any]],
    top_percentile: float = 0.1,
    expansion_factor: float = 1.2
) -> Dict[str, List[Any]]:
    """
    Generate focused grid search recommendations based on top performers.
    Automatically excludes already-tested values.
    
    Args:
        combined_data: Combined metadata and results
        tested_values: Dictionary of tested parameter values to exclude
        top_percentile: Top percentile to analyze (0.1 = top 10%)
        expansion_factor: Factor to expand ranges around top values
        
    Returns:
        Dictionary mapping parameter names to recommended value lists (only NEW values)
    """
    # Get top performers
    valid_data = [
        r for r in combined_data
        if r.get('cv_score') is not None
        and not (isinstance(r.get('cv_score'), float) and (r['cv_score'] != r['cv_score']))
    ]
    
    sorted_data = sorted(
        valid_data,
        key=lambda x: x.get('cv_score', -float('inf')),
        reverse=True
    )
    
    top_n = max(1, int(len(sorted_data) * top_percentile))
    top_performers = sorted_data[:top_n]
    
    recommendations = {}
    
    for param_name in LGBM_HYPERPARAMETERS:
        # Extract parameter values from top performers
        param_values = []
        for record in top_performers:
            value = record.get('hyperparameters', {}).get(param_name)
            if value is not None:
                param_values.append(value)
        
        if not param_values:
            continue
        
        # Check if numeric
        try:
            numeric_values = [float(v) for v in param_values]
            is_numeric = True
        except (ValueError, TypeError):
            is_numeric = False
        
        if is_numeric:
            min_val = min(numeric_values)
            max_val = max(numeric_values)
            median_val = statistics.median(numeric_values)
            
            # Expand range
            range_size = max_val - min_val
            if range_size == 0:
                # All values same, create small range
                center = min_val
                expanded_min = center / expansion_factor
                expanded_max = center * expansion_factor
            else:
                center = (min_val + max_val) / 2
                half_range = (range_size / 2) * expansion_factor
                expanded_min = max(0, center - half_range)
                expanded_max = center + half_range
            
            # Generate focused values
            focused_values = set()
            focused_values.update(numeric_values)  # Include original top values
            
            # Add expanded boundaries
            if expanded_min < min_val:
                focused_values.add(expanded_min)
            if expanded_max > max_val:
                focused_values.add(expanded_max)
            
            # Ensure we have a reasonable number of values
            if len(focused_values) < 3:
                # Add more values around the range
                step = (expanded_max - expanded_min) / 4
                for i in range(5):
                    val = expanded_min + i * step
                    focused_values.add(val)
            
            # Round and sort, apply constraints
            if param_name in ['learning_rate', 'subsample', 'colsample_bytree']:
                focused_values = sorted([round(v, 4) for v in focused_values])
                # Constrain subsample and colsample_bytree to [0, 1]
                if param_name in ['subsample', 'colsample_bytree']:
                    focused_values = [v for v in focused_values if 0 <= v <= 1.0]
            elif param_name == 'n_estimators':
                focused_values = sorted([int(round(v)) for v in focused_values if v > 0])
            elif param_name in ['num_leaves', 'max_depth', 'min_child_samples']:
                focused_values = sorted([int(round(v)) for v in focused_values if v > 0])
                # For max_depth, keep -1 if it was in original values
                if param_name == 'max_depth' and -1 in param_values:
                    focused_values = [-1] + [v for v in focused_values if v > 0]
            else:
                focused_values = sorted(list(focused_values))
            
            # Remove duplicates and ensure we have values
            focused_values = sorted(list(set(focused_values)))
            if not focused_values:
                # Fallback to original values if expansion failed
                focused_values = sorted(list(set(numeric_values)))
            
            # Filter out already-tested values
            tested_set = set(tested_values.get(param_name, []))
            new_values = [v for v in focused_values if v not in tested_set]
            
            # If all values were tested, generate new ones around top performers
            if not new_values and numeric_values:
                top_val = statistics.median(numeric_values)
                if param_name == 'n_estimators':
                    # Try values below top performer
                    new_values = [int(top_val * 0.8), int(top_val * 0.9)]
                elif param_name == 'learning_rate':
                    new_values = [round(top_val * 0.8, 4), round(top_val * 0.9, 4)]
                elif param_name == 'num_leaves':
                    new_values = [int(top_val * 1.1), int(top_val * 1.2)]
                elif param_name == 'max_depth' and top_val > 0:
                    new_values = [int(top_val) + 1, int(top_val) + 2]
                elif param_name == 'min_child_samples':
                    new_values = [int(top_val * 0.8), int(top_val * 1.1)]
                elif param_name in ['subsample', 'colsample_bytree']:
                    new_values = [round(max(0.5, top_val * 0.9), 2), round(max(0.5, top_val * 0.95), 2)]
                # Filter again to ensure new values aren't tested
                new_values = [v for v in new_values if v not in tested_set]
            
            if new_values:
                recommendations[param_name] = new_values
        else:
            # Categorical: keep unique values from top performers, excluding tested
            unique_values = sorted(list(set(param_values)))
            tested_set = set(tested_values.get(param_name, []))
            new_values = [v for v in unique_values if v not in tested_set]
            if new_values:
                recommendations[param_name] = new_values
    
    return recommendations


def format_statistics_table(stats: Dict[str, Any]) -> str:
    """
    Format parameter statistics as a readable table.
    
    Args:
        stats: Statistics dictionary from calculate_parameter_statistics
        
    Returns:
        Formatted string table
    """
    if 'error' in stats:
        return f"Error: {stats['error']}\n"
    
    lines = []
    lines.append(f"\n{'='*80}")
    lines.append(f"Parameter: {stats['parameter']}")
    lines.append(f"{'='*80}")
    lines.append(f"Total Records: {stats['total_records']}")
    lines.append(f"Unique Values: {stats['unique_values']}")
    
    if stats.get('correlation') is not None:
        lines.append(f"Correlation with Score: {stats['correlation']:.4f}")
    
    lines.append(f"\nOverall Score Statistics:")
    overall = stats['overall_score_stats']
    lines.append(f"  Mean:   {overall['mean']:.6f}")
    lines.append(f"  Median: {overall['median']:.6f}")
    lines.append(f"  Std:    {overall['std']:.6f}")
    lines.append(f"  Min:    {overall['min']:.6f}")
    lines.append(f"  Max:    {overall['max']:.6f}")
    
    # Top performing values
    value_stats = stats['value_statistics']
    sorted_values = sorted(
        value_stats.items(),
        key=lambda x: x[1]['mean'],
        reverse=True
    )
    
    lines.append(f"\nTop 10 Parameter Values by Mean Score:")
    lines.append(f"{'Value':<20} {'Count':<8} {'Mean':<12} {'Median':<12} {'Std':<12}")
    lines.append("-" * 80)
    
    for value, vstats in sorted_values[:10]:
        lines.append(
            f"{str(value):<20} {vstats['count']:<8} "
            f"{vstats['mean']:<12.6f} {vstats['median']:<12.6f} {vstats['std']:<12.6f}"
        )
    
    return "\n".join(lines)


def format_top_configurations(top_configs: List[Dict[str, Any]], n: int = 20) -> str:
    """
    Format top configurations as a readable table.
    
    Args:
        top_configs: List of top configurations
        n: Number to display
        
    Returns:
        Formatted string
    """
    lines = []
    lines.append(f"\n{'='*80}")
    lines.append(f"Top {min(n, len(top_configs))} Configurations")
    lines.append(f"{'='*80}")
    
    for i, config in enumerate(top_configs[:n], 1):
        lines.append(f"\n{i}. Variant: {config['variant_id']} | CV Score: {config['cv_score']:.6f}")
        hyperparams = config.get('hyperparameters', {})
        for param in LGBM_HYPERPARAMETERS:
            value = hyperparams.get(param, 'N/A')
            lines.append(f"   {param}: {value}")
    
    return "\n".join(lines)


def main():
    """Main analysis function."""
    # File paths
    metadata_path = Path("csiro-metadata/lgbm/metadata.json")
    gridsearch_path = Path("csiro-metadata/lgbm/gridsearch_metadata.json")
    
    if not metadata_path.exists():
        print(f"Error: {metadata_path} not found")
        return
    
    if not gridsearch_path.exists():
        print(f"Error: {gridsearch_path} not found")
        return
    
    # Load and join data
    combined_data = load_and_join_metadata(str(metadata_path), str(gridsearch_path))
    
    if not combined_data:
        print("Error: No combined data found")
        return
    
    # Extract tested values to exclude from recommendations
    print("\nExtracting tested hyperparameter values...")
    metadata = load_json_file(str(metadata_path))
    tested_values = extract_tested_values(metadata)
    print(f"Found tested values for {len(tested_values)} parameters")
    
    print(f"\nAnalyzing {len(combined_data)} configurations...")
    
    # Calculate overall statistics
    all_scores = [
        r['cv_score'] for r in combined_data
        if r.get('cv_score') is not None
        and not (isinstance(r.get('cv_score'), float) and (r['cv_score'] != r['cv_score']))
    ]
    
    print(f"\nOverall Score Statistics:")
    print(f"  Total valid results: {len(all_scores)}")
    print(f"  Mean:   {statistics.mean(all_scores):.6f}")
    print(f"  Median: {statistics.median(all_scores):.6f}")
    print(f"  Std:    {statistics.stdev(all_scores) if len(all_scores) > 1 else 0.0:.6f}")
    print(f"  Min:    {min(all_scores):.6f}")
    print(f"  Max:    {max(all_scores):.6f}")
    
    # Analyze each hyperparameter
    print("\n" + "="*80)
    print("HYPERPARAMETER ANALYSIS")
    print("="*80)
    
    all_stats = {}
    all_trends = {}
    
    for param_name in LGBM_HYPERPARAMETERS:
        print(f"\nAnalyzing {param_name}...")
        stats = calculate_parameter_statistics(combined_data, param_name)
        trends = analyze_parameter_trends(combined_data, param_name)
        
        all_stats[param_name] = stats
        all_trends[param_name] = trends
        
        print(format_statistics_table(stats))
        
        if 'error' not in trends:
            print(f"\nTrend Analysis for {param_name}:")
            if trends.get('is_numeric'):
                print(f"  Trend: {trends['trend']} (strength: {trends['trend_strength']:.4f})")
                print(f"  Low value range mean score: {trends['low_value_mean_score']:.6f}")
                print(f"  High value range mean score: {trends['high_value_mean_score']:.6f}")
            else:
                print(f"  Best value: {trends.get('best_value')} (mean score: {trends.get('best_value_mean_score', 0):.6f})")
    
    # Identify top performers
    print("\n" + "="*80)
    print("TOP PERFORMERS")
    print("="*80)
    
    top_20 = identify_top_performers(combined_data, top_n=20)
    print(format_top_configurations(top_20, n=20))
    
    # Generate recommendations
    print("\n" + "="*80)
    print("FOCUSED GRID SEARCH RECOMMENDATIONS")
    print("="*80)
    
    recommendations = generate_focused_grid_recommendations(
        combined_data,
        tested_values,
        top_percentile=0.1,
        expansion_factor=1.2
    )
    
    print("\nRecommended parameter ranges based on top 10% performers (NEW values only):")
    for param_name, values in recommendations.items():
        print(f"\n{param_name}:")
        print(f"  {values}")
        print(f"  ({len(values)} NEW values, excluding {len(tested_values.get(param_name, []))} tested)")
    
    # Save recommendations to JSON (final clean recommendations file)
    output_path = Path("lgbm_clean_recommendations.json")
    with open(output_path, 'w') as f:
        json.dump(recommendations, f, indent=2)
    print(f"\nRecommendations saved to: {output_path}")
    print("Note: Only NEW, untested values are included in recommendations")
    
    # Summary and decision support
    print("\n" + "="*80)
    print("SUMMARY AND RECOMMENDATIONS")
    print("="*80)
    
    best_score = max(all_scores)
    worst_score = min(all_scores)
    score_range = best_score - worst_score
    median_score = statistics.median(all_scores)
    
    print(f"\nScore Range: {worst_score:.6f} to {best_score:.6f} (range: {score_range:.6f})")
    print(f"Median Score: {median_score:.6f}")
    print(f"Best Score Improvement over Median: {best_score - median_score:.6f}")
    
    # Identify strongest correlations
    correlations = {
        param: stats.get('correlation', 0)
        for param, stats in all_stats.items()
        if stats.get('correlation') is not None
    }
    
    if correlations:
        sorted_correlations = sorted(
            correlations.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )
        print(f"\nStrongest Parameter Correlations:")
        for param, corr in sorted_correlations[:5]:
            print(f"  {param}: {corr:.4f}")
    
    # Decision recommendation
    print(f"\n{'='*80}")
    print("DECISION RECOMMENDATION")
    print(f"{'='*80}")
    
    if score_range > 0.01:  # Significant score variance
        print("+ Significant score variance detected - focused grid search recommended")
        print("  Consider running a focused grid search around the recommended ranges")
    else:
        print("! Limited score variance - may indicate:")
        print("  - Hyperparameters have limited impact on this dataset")
        print("  - Consider moving to next regression head model")
        print("  - Or investigate feature quality/data preprocessing")
    
    print(f"\nAnalysis complete!")


if __name__ == "__main__":
    main()
