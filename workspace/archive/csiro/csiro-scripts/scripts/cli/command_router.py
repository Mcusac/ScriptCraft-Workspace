# command_router.py
# Command routing logic extracted from run.py

import argparse
import logging
from pathlib import Path
from typing import TypeVar, Callable, Dict, Optional, List, cast

from config.config import Config
from cli.commands import Command

T = TypeVar('T')

logger = logging.getLogger(__name__)

# Valid command names (for validation)
VALID_COMMANDS = {cmd.value for cmd in Command}


def _get_arg(args: argparse.Namespace, attr: str, default: Optional[T] = None) -> Optional[T]:
    """
    Extract attribute from args with default fallback.
    
    Type-safe helper for extracting optional arguments from argparse.Namespace.
    Returns the attribute value if it exists, otherwise returns the default.
    
    Args:
        args: Parsed arguments object from argparse.
        attr: Attribute name to extract.
        default: Default value if attribute doesn't exist (default: None).
        
    Returns:
        Attribute value or default. Type is inferred from default if provided.
    """
    value = getattr(args, attr, default)
    # Type cast to help type checkers understand the return type
    return cast(Optional[T], value)


def _parse_comma_separated(value: Optional[str]) -> Optional[List[str]]:
    """
    Parse comma-separated string into list of stripped non-empty strings.
    
    Helper function for consistent parsing of comma-separated command-line arguments.
    Returns None if input is None, otherwise returns list of stripped non-empty strings.
    
    Args:
        value: Comma-separated string or None.
        
    Returns:
        List of stripped strings, or None if input is None.
        Returns empty list if input is empty string after stripping.
    """
    if value is None:
        return None
    return [item.strip() for item in value.split(',') if item.strip()]


def _handle_train(args: argparse.Namespace, config: Config) -> None:
    """Handle train command."""
    from pipelines import train_pipeline
    train_pipeline(config)  # Ignore feature_filename return value (not used in train-only mode)


def _handle_test(args: argparse.Namespace, config: Config) -> None:
    """Handle test command."""
    from pipelines import test_pipeline
    test_pipeline(config, model_path=_get_arg(args, 'model_path'))


def _handle_train_test(args: argparse.Namespace, config: Config) -> None:
    """Handle train_test command."""
    from pipelines import train_test_pipeline
    train_test_pipeline(config)


def _handle_dataset_grid_search(args: argparse.Namespace, config: Config) -> None:
    """Handle dataset_grid_search command."""
    # Apply dataset_type if provided
    dataset_type = _get_arg(args, 'dataset_type', 'split')
    config.data.dataset_type = dataset_type
    
    # Check if max augmentation quick test mode is requested
    max_augmentation = getattr(args, 'max_augmentation', False)
    
    if max_augmentation:
        from pipelines import test_max_augmentation_pipeline
        test_max_augmentation_pipeline(config)
    else:
        from pipelines import dataset_grid_search_pipeline
        dataset_grid_search_pipeline(config)


def _handle_hyperparameter_grid_search(args: argparse.Namespace, config: Config) -> None:
    """Handle hyperparameter_grid_search command."""
    from pipelines import hyperparameter_grid_search_pipeline
    
    # Apply dataset_type if provided
    dataset_type = _get_arg(args, 'dataset_type', 'split')
    config.data.dataset_type = dataset_type
    
    search_type = _get_arg(args, 'search_type', 'thorough')
    metadata_path = _get_arg(args, 'metadata_path', None)
    results_file = _get_arg(args, 'results_file', None)
    previous_results_file = _get_arg(args, 'previous_results_file', None)
    
    hyperparameter_grid_search_pipeline(
        config=config,
        search_type=search_type,
        metadata_path=metadata_path,
        results_file=results_file,
        previous_results_file=previous_results_file
    )


def _handle_regression_grid_search(args: argparse.Namespace, config: Config) -> None:
    """Handle regression_grid_search command."""
    from pipelines import regression_grid_search_pipeline
    
    feature_filename = _get_arg(args, 'feature_filename')
    if not feature_filename:
        raise ValueError("--feature-filename is required for regression_grid_search")
    
    regression_model_type = _get_arg(args, 'regression_model_type', 'lgbm')
    search_type = _get_arg(args, 'search_type', 'quick')
    
    regression_grid_search_pipeline(
        config=config,
        feature_filename=feature_filename,
        regression_model_type=regression_model_type,
        search_type=search_type
    )


def _handle_cleanup_grid_search(args: argparse.Namespace, config: Config) -> None:
    """Handle cleanup_grid_search command."""
    from modeling import cleanup_grid_search_checkpoints_retroactive
    
    model_dir = _get_arg(args, 'model_dir') or config.paths.model_dir
    results_file = _get_arg(args, 'results_file') or str(
        Path(config.paths.output_dir) / 'dataset_grid_search' / 'gridsearch_results.json'
    )
    keep_top = _get_arg(args, 'keep_top', 20)
    
    logger.info(f"Running retroactive cleanup:")
    logger.info(f"  Model directory: {model_dir}")
    logger.info(f"  Results file: {results_file}")
    logger.info(f"  Keep top: {keep_top} variants")
    
    variants_deleted, bytes_freed = cleanup_grid_search_checkpoints_retroactive(
        model_base_dir=model_dir,
        results_file=results_file,
        keep_top_n=keep_top
    )
    
    logger.info(f"\nCleanup complete:")
    logger.info(f"  Variants deleted: {variants_deleted}")
    from utils.system.constants import BYTES_PER_MB
    logger.info(f"  Space freed: {bytes_freed / BYTES_PER_MB:.2f} MB")


def _handle_submit_best(args: argparse.Namespace, config: Config) -> None:
    """Handle submit_best command."""
    from pipelines import submit_best_variant_pipeline
    
    submit_best_variant_pipeline(
        config=config,
        variant_id=_get_arg(args, 'variant_id'),
        results_file=_get_arg(args, 'results_file')
    )


def _handle_train_and_export(args: argparse.Namespace, config: Config) -> None:
    """Handle train_and_export command."""
    from pipelines import train_and_export_pipeline
    import json
    
    # Apply dataset_type if provided
    dataset_type = _get_arg(args, 'dataset_type')
    if dataset_type:
        config.data.dataset_type = dataset_type
    
        # Apply feature extraction mode if provided
        feature_extraction_mode = getattr(args, 'feature_extraction_mode', False)
        if feature_extraction_mode:
            config.model.feature_extraction_mode = True
            feature_extraction_model = _get_arg(args, 'feature_extraction_model')
            regression_model_type = _get_arg(args, 'regression_model_type')
            extract_features = getattr(args, 'extract_features', None)  # None means use config default
            
            if not feature_extraction_model:
                raise ValueError("--feature-extraction-model is required when --feature-extraction-mode is set")
            if not regression_model_type:
                raise ValueError("--regression-model-type is required when --feature-extraction-mode is set")
            
            # Convert model name (e.g., 'dinov2_base') to pretrained path/name using model constants
            # This allows users to use consistent model names instead of hardcoded paths
            from config.model_constants import get_pretrained_weights_path
            pretrained_path_or_name = get_pretrained_weights_path(feature_extraction_model)
            config.model.feature_extraction_model_name = pretrained_path_or_name
            config.model.regression_model_type = regression_model_type
            
            # Set extract_features flag if explicitly provided
            if extract_features is not None:
                config.model.extract_features = extract_features
    
    # Apply data manipulation combo if provided
    data_manipulation_combo = _get_arg(args, 'data_manipulation_combo')
    if data_manipulation_combo:
        from utils.config.config_updater import apply_combo_to_config
        apply_combo_to_config(config, data_manipulation_combo)
    
    fresh_train = getattr(args, 'fresh_train', False)
    export_only = getattr(args, 'export_only', False)
    
    # Get regression model variant ID if in feature extraction mode
    regression_model_variant_id = None
    if feature_extraction_mode:
        regression_model_variant_id = _get_arg(args, 'regression_model_variant_id')
    
    train_and_export_pipeline(
        config=config,
        results_file=_get_arg(args, 'results_file'),
        variant_id=_get_arg(args, 'variant_id'),
        export_dir=_get_arg(args, 'export_dir'),
        fresh_train=fresh_train,
        export_only=export_only,
        regression_model_variant_id=regression_model_variant_id
    )


def _handle_export_model(args: argparse.Namespace, config: Config) -> None:
    """Handle export_model command."""
    from pipelines import export_model_pipeline
    
    export_model_pipeline(
        config=config,
        results_file=_get_arg(args, 'results_file'),
        variant_id=_get_arg(args, 'variant_id'),
        best_variant_file=_get_arg(args, 'best_variant_file'),
        export_dir=_get_arg(args, 'export_dir')
    )


def _handle_submit(args: argparse.Namespace, config: Config) -> None:
    """Handle submit command."""
    from pipelines import submit_lightweight_pipeline
    
    # Apply dataset_type if provided
    dataset_type = _get_arg(args, 'dataset_type', 'split')
    config.data.dataset_type = dataset_type
    
    submit_lightweight_pipeline(
        config=config,
        model_path=_get_arg(args, 'model_path'),
        metadata_path=_get_arg(args, 'metadata_path'),
        results_file=_get_arg(args, 'results_file'),
        model_name=_get_arg(args, 'model_name')
    )


def _handle_ensemble_from_paths(args: argparse.Namespace, config: Config) -> None:
    """Handle ensemble command with direct model paths."""
    from pipelines import ensemble_pipeline_from_paths
    import json
    from pathlib import Path
    
    model_paths_str = _get_arg(args, 'model_paths', None)
    if not model_paths_str:
        raise ValueError("--model-paths is required for ensemble from paths")
    
    # Parse model_paths (comma-separated)
    model_paths = _parse_comma_separated(model_paths_str)
    
    if not model_paths:
        raise ValueError("--model-paths cannot be empty")
    
    # Parse submission_scores if provided
    submission_scores = None
    submission_scores_str = _get_arg(args, 'submission_scores', None)
    if submission_scores_str:
        # Try to parse as JSON string first
        try:
            submission_scores = json.loads(submission_scores_str)
        except json.JSONDecodeError:
            # If not valid JSON, try as file path
            scores_path = Path(submission_scores_str)
            if scores_path.exists():
                with open(scores_path, 'r') as f:
                    submission_scores = json.load(f)
            else:
                raise ValueError(
                    f"submission_scores must be valid JSON string or path to JSON file. "
                    f"Got: {submission_scores_str}"
                )
    
    # Get score_type
    score_type = _get_arg(args, 'score_type', 'cv')
    
    # Apply dataset_type if provided
    dataset_type = _get_arg(args, 'dataset_type', 'split')
    config.data.dataset_type = dataset_type
    
    ensemble_pipeline_from_paths(
        config=config,
        model_paths=model_paths,
        method=_get_arg(args, 'method', 'weighted_average'),
        submission_scores=submission_scores,
        score_type=score_type
    )


def _handle_ensemble_from_results(args: argparse.Namespace, config: Config) -> None:
    """Handle ensemble command with results files."""
    from pipelines import ensemble_pipeline
    
    # Parse results_files if provided (comma-separated)
    results_files_str = _get_arg(args, 'results_files', None)
    results_files = _parse_comma_separated(results_files_str)
    
    # Parse fallback_paths if provided (comma-separated)
    fallback_paths_str = _get_arg(args, 'fallback_paths', None)
    fallback_paths = _parse_comma_separated(fallback_paths_str)
    
    ensemble_pipeline(
        config=config,
        results_files=results_files,
        top_n=_get_arg(args, 'top_n', 3),
        method=_get_arg(args, 'method', 'weighted_average'),
        fallback_paths=fallback_paths
    )


def _handle_ensemble(args: argparse.Namespace, config: Config) -> None:
    """Handle ensemble command - routes to appropriate handler based on arguments."""
    model_paths_str = _get_arg(args, 'model_paths', None)
    
    if model_paths_str:
        _handle_ensemble_from_paths(args, config)
    else:
        _handle_ensemble_from_results(args, config)


def _handle_regression_ensemble(args: argparse.Namespace, config: Config) -> None:
    """Handle regression_ensemble command."""
    from pipelines import regression_ensemble_pipeline
    import json
    
    ensemble_config_str = _get_arg(args, 'ensemble_config', None)
    if not ensemble_config_str:
        raise ValueError("--ensemble-config is required for regression_ensemble")
    
    # Parse JSON config
    try:
        ensemble_config = json.loads(ensemble_config_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in --ensemble-config: {e}")
    
    # Apply dataset_type if provided
    dataset_type = _get_arg(args, 'dataset_type', 'split')
    config.data.dataset_type = dataset_type
    
    regression_ensemble_pipeline(
        config=config,
        ensemble_config=ensemble_config
    )


def _handle_stacking(args: argparse.Namespace, config: Config) -> None:
    """Handle stacking command."""
    from pipelines import stacking_pipeline
    import json
    
    stacking_config_str = _get_arg(args, 'stacking_config', None)
    if not stacking_config_str:
        raise ValueError("--stacking-config is required for stacking")
    
    # Parse JSON config
    try:
        stacking_config = json.loads(stacking_config_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in --stacking-config: {e}")
    
    # Apply dataset_type if provided
    dataset_type = _get_arg(args, 'dataset_type', 'split')
    config.data.dataset_type = dataset_type
    
    stacking_pipeline(
        config=config,
        stacking_config=stacking_config
    )


def _handle_stacking_ensemble(args: argparse.Namespace, config: Config) -> None:
    """Handle stacking_ensemble command."""
    from pipelines import stacking_ensemble_pipeline
    import json
    
    stacking_ensemble_config_str = _get_arg(args, 'stacking_ensemble_config', None)
    if not stacking_ensemble_config_str:
        raise ValueError("--stacking-ensemble-config is required for stacking_ensemble")
    
    # Parse JSON config
    try:
        stacking_ensemble_config = json.loads(stacking_ensemble_config_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in --stacking-ensemble-config: {e}")
    
    # Apply dataset_type if provided
    dataset_type = _get_arg(args, 'dataset_type', 'split')
    config.data.dataset_type = dataset_type
    
    stacking_ensemble_pipeline(
        config=config,
        stacking_ensemble_config=stacking_ensemble_config
    )


def _handle_hybrid_stacking(args: argparse.Namespace, config: Config) -> None:
    """Handle hybrid_stacking command."""
    from pipelines import hybrid_stacking_pipeline
    import json
    
    hybrid_stacking_config_str = _get_arg(args, 'hybrid_stacking_config', None)
    if not hybrid_stacking_config_str:
        raise ValueError("--hybrid-stacking-config is required for hybrid_stacking")
    
    # Parse JSON config
    try:
        hybrid_stacking_config = json.loads(hybrid_stacking_config_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in --hybrid-stacking-config: {e}")
    
    # Apply dataset_type if provided
    dataset_type = _get_arg(args, 'dataset_type', 'split')
    config.data.dataset_type = dataset_type
    
    hybrid_stacking_pipeline(
        config=config,
        hybrid_stacking_config=hybrid_stacking_config
    )


def _handle_multi_variant_regression_train(args: argparse.Namespace, config: Config) -> None:
    """Handle multi_variant_regression_train command."""
    from pipelines import multi_variant_regression_training_pipeline
    
    # Apply dataset_type if provided
    dataset_type = _get_arg(args, 'dataset_type', 'split')
    config.data.dataset_type = dataset_type
    
    # Parse model IDs
    model_ids_str = _get_arg(args, 'model_ids', None)
    if not model_ids_str:
        raise ValueError("--model-ids is required for multi_variant_regression_train")
    
    # Parse model_ids as strings (not integers)
    model_ids = [model_id.strip() for model_id in model_ids_str.split(',')]
    if not model_ids:
        raise ValueError(f"Invalid model_ids format: {model_ids_str}. Expected comma-separated model_id strings.")
    
    # Get other required arguments
    feature_extraction_model = _get_arg(args, 'feature_extraction_model', None)
    if not feature_extraction_model:
        raise ValueError("--feature-extraction-model is required")
    
    regression_model_type = _get_arg(args, 'regression_model_type', None)
    if not regression_model_type:
        raise ValueError("--regression-model-type is required")
    
    extract_features = getattr(args, 'extract_features', True)
    fresh_train = getattr(args, 'fresh_train', False)
    data_manipulation_combo = _get_arg(args, 'data_manipulation_combo', None)
    
    # Run pipeline
    multi_variant_regression_training_pipeline(
        config=config,
        model_ids=model_ids,
        feature_extraction_model=feature_extraction_model,
        regression_model_type=regression_model_type,
        data_manipulation_combo=data_manipulation_combo,
        extract_features=extract_features,
        fresh_train=fresh_train
    )


# Command handler registry
_COMMAND_HANDLERS: Dict[str, Callable[[argparse.Namespace, Config], None]] = {
    Command.TRAIN.value: _handle_train,
    Command.TEST.value: _handle_test,
    Command.TRAIN_TEST.value: _handle_train_test,
    Command.DATASET_GRID_SEARCH.value: _handle_dataset_grid_search,
    Command.HYPERPARAMETER_GRID_SEARCH.value: _handle_hyperparameter_grid_search,
    Command.CLEANUP_GRID_SEARCH.value: _handle_cleanup_grid_search,
    Command.SUBMIT_BEST.value: _handle_submit_best,
    Command.TRAIN_AND_EXPORT.value: _handle_train_and_export,
    Command.EXPORT_MODEL.value: _handle_export_model,
    Command.SUBMIT.value: _handle_submit,
    Command.ENSEMBLE.value: _handle_ensemble,
    Command.REGRESSION_GRID_SEARCH.value: _handle_regression_grid_search,
    Command.REGRESSION_ENSEMBLE.value: _handle_regression_ensemble,
    Command.STACKING.value: _handle_stacking,
    Command.STACKING_ENSEMBLE.value: _handle_stacking_ensemble,
    Command.HYBRID_STACKING.value: _handle_hybrid_stacking,
    Command.MULTI_VARIANT_REGRESSION_TRAIN.value: _handle_multi_variant_regression_train
}


def route_command(command: str, args: argparse.Namespace, config: Config) -> None:
    """
    Route command to appropriate pipeline function.
    
    Implements command pattern for dispatching CLI commands to their
    corresponding pipeline implementations. All business logic is delegated
    to pipeline functions.
    
    Args:
        command: Command name. Must be a valid command string.
                Valid commands: 'train', 'test', 'train_test',
                'dataset_grid_search', 'hyperparameter_grid_search', 'cleanup_grid_search',
                'submit_best', 'train_and_export', 'export_model', 'submit'.
        args: Parsed arguments object from argparse. Used to extract optional
              parameters for pipeline functions.
        config: Configuration object. Must not be None and must have all
                required attributes configured.
        
    Returns:
        None. Pipeline functions handle their own return values and side effects.
        
    Raises:
        ValueError: If command is None, empty, or unknown.
        TypeError: If args or config have invalid types.
        RuntimeError: If pipeline execution fails (propagated from pipeline functions).
    """
    # Validate inputs
    if not command or not isinstance(command, str):
        raise ValueError(f"command must be non-empty string, got {command}")
    
    if config is None:
        raise ValueError("config cannot be None")
    
    # Validate command using enum
    try:
        command_enum = Command.from_string(command)
    except ValueError as e:
        raise ValueError(str(e))
    
    # Route to handler using dictionary lookup
    handler = _COMMAND_HANDLERS.get(command_enum.value)
    if handler is None:
        raise ValueError(
            f"Command '{command}' is valid but has no handler registered. "
            f"This is a programming error."
        )
    
    handler(args, config)

