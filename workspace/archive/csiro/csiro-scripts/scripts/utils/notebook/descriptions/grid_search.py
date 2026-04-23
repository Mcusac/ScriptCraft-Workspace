# grid_search.py
# Grid search description builders
#
# Builds formatted description strings for various grid search pipelines:
# - Hyperparameter grid search
# - Dataset grid search
# - Regression grid search

from typing import Dict, List, Any, Optional

from ..core import _detect_model_type, print_config_section


def build_hyperparameter_grid_search_description(
    model: str,
    search_type: str,
    param_grid: Dict[str, List[Any]],
    total_combinations: int,
    log_file: str,
    results_file: str,
    metadata_path: Optional[str] = None,
    dataset_config_source: Optional[str] = None,
    previous_results_file: Optional[str] = None,
    base_combinations: Optional[int] = None,
    dataset_type: Optional[str] = None
) -> str:
    """
    Build formatted description string for hyperparameter grid search.
    
    Args:
        model: Model architecture name
        search_type: Grid search type
        param_grid: Parameter grid dictionary
        total_combinations: Total number of combinations to test
        log_file: Log file path
        results_file: Results file path (where results will be saved)
        metadata_path: Optional metadata path (for dataset config display)
        dataset_config_source: Optional dataset config source path (for display, alternative to metadata_path)
        previous_results_file: Optional previous results file path (for focused searches)
        base_combinations: Optional base combination count (for showing reduction statistics)
        dataset_type: Dataset type ('full' or 'split')
        
    Returns:
        Formatted description string
    """
    description = (
        f"Running HYPERPARAMETER grid search:\n"
        f"\nTesting all hyperparameter combinations with {model}\n"
        f"Search type: {search_type}\n"
    )
    
    # Add reduction statistics for focused searches
    if base_combinations is not None and base_combinations > total_combinations:
        reduction_ratio = total_combinations / base_combinations
        reduction_percent = (1 - reduction_ratio) * 100
        description += (
            f"Base grid combinations: {base_combinations:,}\n"
            f"Focused grid combinations: {total_combinations:,}\n"
            f"Reduction: {reduction_percent:.1f}% ({base_combinations:,} → {total_combinations:,})\n"
        )
    else:
        description += f"This will test {total_combinations:,} combinations\n"
    
    description += (
        f"Results saved incrementally to: {results_file}\n"
        f"Output streamed to: {log_file}\n"
        f"\n📋 Hyperparameters being searched:\n"
    )
    
    for param_name, param_values in param_grid.items():
        description += f"   - {param_name}: {param_values}\n"
    
    # Detect model type for appropriate warning
    model_type = _detect_model_type(model)
    
    # Build model-specific warning message
    if model_type == 'dinov2_hf':
        model_warning = (
            f"\n⚠️ Model Architecture: {model}\n"
            f"   HuggingFace format detected - weights will be loaded from the specified path\n"
            f"   Make sure Cell 0 downloaded weights for the correct model"
        )
    else:  # timm (EfficientNet, etc.)
        model_warning = (
            f"\n⚠️ Model Architecture: {model}\n"
            f"   Timm will load model-specific pretrained weights for this architecture\n"
            f"   Each model (b0, b3, b4) has its own weights - they are NOT interchangeable\n"
            f"   Make sure Cell 0 downloaded weights for the correct model"
        )
    
    description += model_warning
    
    if metadata_path:
        description += f"\n\n📁 Using dataset config from: {metadata_path}\n"
    elif dataset_config_source:
        description += f"\n\n📁 Using dataset config from: {dataset_config_source}\n"
    else:
        description += f"\n\n⚠️  Using default dataset config (no preprocessing/augmentation)\n"
        description += f"   (Pipeline will auto-detect metadata if available)\n"
    
    if previous_results_file:
        description += f"\n🎯 Using focused grid based on: {previous_results_file}\n"
    
    return description


def build_dataset_grid_search_description(
    model: str,
    total_variants: int,
    log_file: str,
    results_file: str,
    dataset_type: Optional[str] = None
) -> str:
    """
    Build formatted description string for dataset grid search.
    
    Args:
        model: Model architecture name
        total_variants: Total number of variants to test
        log_file: Log file path
        results_file: Results file path
        dataset_type: Dataset type ('full' or 'split')
        
    Returns:
        Formatted description string
    """
    dataset_type_str = dataset_type or 'split'
    
    # Detect model type for appropriate warning
    model_type = _detect_model_type(model)
    
    # Build model-specific warning message
    if model_type == 'dinov2_hf':
        model_warning = (
            f"   HuggingFace format detected - weights will be loaded from the specified path\n"
            f"   Make sure Cell 0 downloaded weights for the correct model"
        )
    else:  # timm (EfficientNet, etc.)
        model_warning = (
            f"   Timm will load model-specific pretrained weights for this architecture\n"
            f"   Each model (b0, b3, b4) has its own weights - they are NOT interchangeable\n"
            f"   Make sure Cell 0 downloaded weights for the correct model"
        )
    
    description = (
        f"Running DATASET grid search (preprocessing/augmentation):\n"
        f"\nTesting all preprocessing/augmentation combinations with {model}\n"
        f"Dataset type: {dataset_type_str}\n"
        f"This will test {total_variants} combinations (computed dynamically)\n"
        f"Results saved incrementally to: {results_file}\n"
        f"Output streamed to: {log_file}\n"
        f"\n⚠️ Model Architecture: {model}\n"
        f"{model_warning}"
    )
    return description


def build_regression_grid_search_description(
    feature_filename: str,
    regression_model_type: str,
    search_type: str
) -> None:
    """
    Print formatted description for regression grid search.
    
    Args:
        feature_filename: Feature filename
        regression_model_type: Type of regression model
        search_type: Grid search type
    """
    print_config_section(
        "🔍 REGRESSION GRID SEARCH",
        {
            "Feature file": feature_filename,
            "Regression model": regression_model_type,
            "Search type": search_type
        }
    )

