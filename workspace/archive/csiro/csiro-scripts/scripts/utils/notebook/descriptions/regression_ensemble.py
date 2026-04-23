# regression_ensemble.py
# Regression ensemble description builder
#
# Builds formatted description for regression ensemble pipeline

from typing import Dict, Any


def build_regression_ensemble_description(
    ensemble_config: Dict[str, Any],
    log_file: str,
    dataset_type: str = None
) -> str:
    """
    Build formatted description for regression ensemble pipeline.
    
    Args:
        ensemble_config: Configuration dict
        log_file: Log file path
        dataset_type: Dataset type
        
    Returns:
        Formatted description string
    """
    model_types = ensemble_config.get('model_types', [])
    method = ensemble_config.get('method', 'weighted_average')
    score_type = ensemble_config.get('score_type', 'cv')
    model_indices = ensemble_config.get('model_indices', {})
    
    # Count total models
    total_models = sum(len(indices) for indices in model_indices.values())
    
    description = f"""
{'='*60}
Regression Ensemble Pipeline
{'='*60}
Model Types: {', '.join(model_types)}
Total Models: {total_models}
Ensembling Method: {method}
Score Type: {score_type}
Dataset Type: {dataset_type or 'split'}
Log File: {log_file}
{'='*60}
"""
    
    return description.strip()
