# diagnostics.py
# Main diagnostics orchestration for ensemble analysis

import logging
from pathlib import Path
from typing import Dict, List, Optional

from .score_analysis import (
    load_cv_scores_from_paths,
    compare_cv_submission_scores
)
from .weight_calculation import get_method_weights

logger = logging.getLogger(__name__)


def _format_score(score: Optional[float]) -> str:
    """
    Format a score to 4 decimal places, or return 'N/A' if score is None.
    """
    return f"{score:.4f}" if score is not None else "N/A"


def analyze_ensemble_weights(
    model_paths: List[str],
    submission_scores: Optional[Dict[str, float]] = None,
    score_type: str = 'cv'
) -> Dict[str, any]:
    """
    Analyze ensemble weights and provide diagnostic information.
    
    Args:
        model_paths: List of model base paths
        submission_scores: Optional dictionary mapping model_path -> submission_score
        score_type: Which scores to use for weighting: 'cv', 'submission', 'combined' (default: 'cv')
        
    Returns:
        Dictionary with diagnostic information:
        - model_info: List of dicts with model_path, cv_score, submission_score
        - method_weights: Dict mapping method_name -> (weights_list, info_dict)
        - cv_submission_comparison: Comparison metrics if submission_scores provided
        - recommendations: List of recommendations based on analysis
    """
    # Load CV scores
    cv_scores = load_cv_scores_from_paths(model_paths)
    
    # Build model info
    model_info = []
    for model_path in model_paths:
        cv_score = cv_scores.get(model_path)
        sub_score = submission_scores.get(model_path) if submission_scores else None
        
        model_info.append({
            'model_path': model_path,
            'cv_score': cv_score,
            'submission_score': sub_score
        })
    
    # Compare CV vs submission if both available
    cv_submission_comparison = None
    if submission_scores:
        cv_submission_comparison = compare_cv_submission_scores(cv_scores, submission_scores)
    
    # Calculate weights for each method
    method_weights = {}
    
    # Determine which scores to use
    if score_type == 'cv':
        scores_to_use = [cv_scores.get(path) for path in model_paths]
    elif score_type == 'submission' and submission_scores:
        scores_to_use = [submission_scores.get(path) for path in model_paths]
    elif score_type == 'combined' and submission_scores:
        # Weighted combination: DEFAULT_CV_WEIGHT * cv + DEFAULT_SUBMISSION_WEIGHT * submission
        from modeling.ensembling.constants import DEFAULT_CV_WEIGHT, DEFAULT_SUBMISSION_WEIGHT
        scores_to_use = []
        for path in model_paths:
            cv = cv_scores.get(path)
            sub = submission_scores.get(path)
            if cv is not None and sub is not None:
                scores_to_use.append(DEFAULT_CV_WEIGHT * cv + DEFAULT_SUBMISSION_WEIGHT * sub)
            elif cv is not None:
                scores_to_use.append(cv)
            elif sub is not None:
                scores_to_use.append(sub)
            else:
                scores_to_use.append(None)
    else:
        scores_to_use = [cv_scores.get(path) for path in model_paths]
    
    # Filter out None scores for methods that need them
    valid_indices = [i for i, s in enumerate(scores_to_use) if s is not None]
    valid_scores = [scores_to_use[i] for i in valid_indices]
    
    if valid_scores:
        for method in ['weighted_average', 'ranked_average', 'percentile_average']:
            weights, info = get_method_weights(valid_scores, method)
            # Map weights back to original model order (None for models without scores)
            full_weights = [None] * len(model_paths)
            for idx, valid_idx in enumerate(valid_indices):
                full_weights[valid_idx] = weights[idx]
            method_weights[method] = {
                'weights': full_weights,
                'info': info
            }
    
    # Generate recommendations
    recommendations = []
    
    if cv_submission_comparison:
        if cv_submission_comparison['correlation'] is not None:
            if cv_submission_comparison['correlation'] < 0.5:
                recommendations.append(
                    "Low correlation between CV and submission scores. "
                    "Consider using submission scores for weighting instead of CV scores."
                )
        
        poor_gen_models = cv_submission_comparison['models_with_poor_generalization']
        if poor_gen_models:
            recommendations.append(
                f"Found {len(poor_gen_models)} model(s) with poor generalization "
                f"(submission score significantly worse than CV). Consider removing them from ensemble."
            )
    
    # Check if ranked and percentile would give same results
    if 'ranked_average' in method_weights and 'percentile_average' in method_weights:
        ranked_weights = method_weights['ranked_average']['weights']
        percentile_weights = method_weights['percentile_average']['weights']
        if ranked_weights and percentile_weights:
            # Check if rank order is the same (would give identical results)
            ranked_info = method_weights['ranked_average']['info']
            percentile_info = method_weights['percentile_average']['info']
            if 'rank_order' in ranked_info:
                # If all scores are same rank, ranked and percentile will be identical
                if len(set(ranked_info['rank_order'])) == 1:
                    recommendations.append(
                        "All models have same rank - ranked_average and percentile_average will give identical results."
                    )
    
    return {
        'model_info': model_info,
        'method_weights': method_weights,
        'cv_submission_comparison': cv_submission_comparison,
        'recommendations': recommendations
    }


def print_diagnostic_summary(diagnostics: Dict[str, any]) -> None:
    """
    Print a formatted diagnostic summary to logs.
    
    Args:
        diagnostics: Output from analyze_ensemble_weights()
    """
    logger.info("="*60)
    logger.info("ENSEMBLE DIAGNOSTICS")
    logger.info("="*60)
    
    # Model info
    logger.info("\n📊 Model Information:")
    for idx, model_info in enumerate(diagnostics['model_info'], 1):
        path = model_info['model_path']
        cv = model_info['cv_score']
        sub = model_info['submission_score']
        cv_str = _format_score(cv)
        sub_str = _format_score(sub)

        logger.info(f"  {idx}. {Path(path).name}")
        logger.info(f"     CV Score: {cv_str}")
        logger.info(f"     Submission Score: {sub_str}")
        if cv is not None and sub is not None:
            gap = sub - cv
            logger.info(f"     Gap (sub - cv): {gap:+.4f}")
    
    # CV vs Submission comparison
    comparison = diagnostics.get('cv_submission_comparison')
    if comparison:
        logger.info("\n📈 CV vs Submission Comparison:")
        if comparison['correlation'] is not None:
            logger.info(f"  Correlation: {comparison['correlation']:.4f}")
        if comparison['avg_gap'] is not None:
            logger.info(f"  Average Gap: {comparison['avg_gap']:+.4f}")
        
        poor_gen = comparison['models_with_poor_generalization']
        if poor_gen:
            logger.info(f"  ⚠️  Models with poor generalization: {len(poor_gen)}")
            for model in poor_gen:
                logger.info(f"     - {Path(model['model_path']).name}: gap = {model['gap']:+.4f}")
    
    # Method weights
    method_weights = diagnostics.get('method_weights', {})
    if method_weights:
        logger.info("\n⚖️  Ensemble Method Weights:")
        for method_name, method_data in method_weights.items():
            weights = method_data['weights']
            info = method_data['info']
            
            logger.info(f"\n  {method_name}:")
            logger.info(f"    Normalized Weights: {[f'{w:.4f}' if w is not None else 'N/A' for w in weights]}")
            
            if 'rank_order' in info:
                logger.info(f"    Rank Order: {info['rank_order']}")
            if 'percentiles' in info:
                logger.info(f"    Percentiles: {[f'{p:.2f}%' for p in info['percentiles']]}")
    
    # Recommendations
    recommendations = diagnostics.get('recommendations', [])
    if recommendations:
        logger.info("\n💡 Recommendations:")
        for rec in recommendations:
            logger.info(f"  - {rec}")
    
    logger.info("="*60)

