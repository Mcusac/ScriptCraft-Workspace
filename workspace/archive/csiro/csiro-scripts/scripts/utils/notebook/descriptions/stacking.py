# stacking.py
# Stacking description builder
#
# Builds formatted description for stacking pipeline

from typing import Dict, Any


def build_stacking_description(
    stacking_config: Dict[str, Any],
    log_file: str,
    dataset_type: str = None
) -> str:
    """
    Build formatted description for stacking pipeline.
    
    Args:
        stacking_config: Configuration dict
        log_file: Log file path
        dataset_type: Dataset type
        
    Returns:
        Formatted description string
    """
    model_types = stacking_config.get('model_types', [])
    meta_model_alpha = stacking_config.get('meta_model_alpha', 10.0)
    n_folds = stacking_config.get('n_folds', 5)
    model_indices = stacking_config.get('model_indices', {})
    
    # Count total models
    total_models = sum(len(indices) for indices in model_indices.values())
    
    description = f"""
    {'='*60}
    Stacking Pipeline
    {'='*60}
    Base Model Types: {', '.join(model_types)}
    Total Base Models: {total_models}
    Meta-Model: Ridge (alpha={meta_model_alpha})
    Number of Folds: {n_folds}
    Dataset Type: {dataset_type or 'split'}
    Log File: {log_file}
    {'='*60}
    """
    
    return description.strip()


def build_stacking_ensemble_description(
    stacking_ensemble_config: Dict[str, Any],
    log_file: str,
    dataset_type: str = None
) -> str:
    """
    Build formatted description for stacking ensemble pipeline.
    
    Args:
        stacking_ensemble_config: Configuration dict
        log_file: Log file path
        dataset_type: Dataset type
        
    Returns:
        Formatted description string
    """
    model_types = stacking_ensemble_config.get('model_types', [])
    meta_model_alpha = stacking_ensemble_config.get('meta_model_alpha', 10.0)
    n_folds = stacking_ensemble_config.get('n_folds', 5)
    ensemble_configs = stacking_ensemble_config.get('ensemble_configs', {})
    
    # Count total models across all ensembles
    total_models = sum(
        len(ensemble_configs.get(model_type, {}).get('model_versions', []))
        for model_type in model_types
    )
    
    description = f"""
{'='*60}
Stacking Ensemble Pipeline
{'='*60}
Base Model Types: {', '.join(model_types)}
Total Base Models: {total_models} (across {len(model_types)} ensembles)
Meta-Model: Ridge (alpha={meta_model_alpha})
Number of Folds: {n_folds}
Dataset Type: {dataset_type or 'split'}
Log File: {log_file}
{'='*60}
"""
    
    return description.strip()


def build_hybrid_stacking_description(
    hybrid_stacking_config: Dict[str, Any],
    log_file: str,
    dataset_type: str = None
) -> str:
    """
    Build formatted description for hybrid stacking pipeline.
    
    Args:
        hybrid_stacking_config: Configuration dict
        log_file: Log file path
        dataset_type: Dataset type
        
    Returns:
        Formatted description string
    """
    regression_ensembles = hybrid_stacking_config.get('regression_ensembles', {})
    end_to_end_ensembles = hybrid_stacking_config.get('end_to_end_ensembles', {})
    meta_model_alpha = hybrid_stacking_config.get('meta_model_alpha', 10.0)
    n_folds = hybrid_stacking_config.get('n_folds', 5)
    
    # Count regression models
    regression_model_types = regression_ensembles.get('model_types', [])
    regression_ensemble_configs = regression_ensembles.get('ensemble_configs', {})
    regression_total = sum(
        len(regression_ensemble_configs.get(model_type, {}).get('model_versions', []))
        for model_type in regression_model_types
    )
    
    # Count end-to-end models
    end_to_end_ensemble_configs = end_to_end_ensembles.get('ensemble_configs', {})
    end_to_end_total = sum(
        len(ensemble_config.get('model_versions', []))
        for ensemble_config in end_to_end_ensemble_configs.values()
    )
    
    description = f"""
{'='*60}
Hybrid Stacking Pipeline
{'='*60}
Regression Ensembles: {len(regression_model_types)} types, {regression_total} total models
  Types: {', '.join(regression_model_types) if regression_model_types else 'None'}
End-to-End Ensembles: {len(end_to_end_ensemble_configs)} ensembles, {end_to_end_total} total models
  Model: {end_to_end_ensembles.get('model_name', 'N/A')}
Meta-Model: Ridge (alpha={meta_model_alpha})
Number of Folds: {n_folds}
Dataset Type: {dataset_type or 'split'}
Log File: {log_file}
{'='*60}
"""
    
    return description.strip()
