# ensemble.py
# Ensemble description builder
#
# Builds formatted description string for ensemble pipeline

from typing import List, Optional, Dict


def build_ensemble_description(
    model: str,
    model_paths: List[str],
    method: str,
    score_type: str,
    log_file: str,
    model_configs: Optional[Dict[str, Optional[float]]] = None,
    dataset_type: Optional[str] = None
) -> str:
    """
    Build formatted description string for ensemble pipeline.
    
    Args:
        model: Model architecture name
        model_paths: List of model directory paths
        method: Ensembling method
        score_type: Score type for weighting
        log_file: Log file path
        model_configs: Optional dict mapping paths to submission scores (for display)
        dataset_type: Dataset type ('full' or 'split')
        
    Returns:
        Formatted description string
    """
    dataset_type_str = dataset_type or 'split'
    description = (
        f"Running ENSEMBLE pipeline:\n"
        f"\nCombining {len(model_paths)} models using {method}\n"
        f"Model architecture: {model}\n"
        f"Dataset type: {dataset_type_str}\n"
        f"Score type: {score_type}\n"
        f"Model paths:\n"
    )
    for idx, path in enumerate(model_paths, 1):
        score_info = ""
        if model_configs and path in model_configs and model_configs[path] is not None:
            score_info = f" (submission: {model_configs[path]})"
        description += f"  {idx}. {path}{score_info}\n"
    description += (
        f"\nOutput streamed to: {log_file}\n"
        f"\nPipeline will:\n"
        f"  1. Validate all model paths and load metadata\n"
        f"  2. Load all models\n"
        f"  3. Run inference with each model\n"
        f"  4. Combine predictions using {method} with {score_type} scores\n"
        f"  5. Generate submission.csv"
    )
    if model_configs and any(score is not None for score in model_configs.values()):
        description += f"\n\n📊 Using submission scores for weighting (score_type={score_type})"
        description += "\n   Diagnostics will show CV vs submission score comparison"
    return description

