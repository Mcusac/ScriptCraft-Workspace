# run.py
# Central script to run any logic

import os
import sys
import warnings
from pathlib import Path

# CRITICAL: Set PyTorch CUDA allocator config BEFORE importing PyTorch
# This must be done before any PyTorch imports to take effect
# expandable_segments helps reduce memory fragmentation and OOM errors
os.environ.setdefault('PYTORCH_CUDA_ALLOC_CONF', 'expandable_segments:True')

# Configure Python debugger to work with frozen modules (Python 3.11+)
# This is proper configuration, not suppression - tells debugger we understand the limitation
os.environ.setdefault('PYDEVD_DISABLE_FILE_VALIDATION', '1')

# Suppress harmless errors from stderr (protobuf/HuggingFace compatibility issues)
# MessageFactory.GetPrototype AttributeError is harmless and occurs when loading HuggingFace models
# with certain protobuf versions - it's a known compatibility issue that doesn't affect functionality
class FilteredStderr:
    """Filter stderr to suppress harmless compatibility errors."""
    def __init__(self, original_stderr):
        self.original_stderr = original_stderr
    
    def write(self, message):
        # Filter out MessageFactory.GetPrototype AttributeError messages (protobuf/HF compatibility)
        if 'MessageFactory' in message and 'GetPrototype' in message:
            return  # Suppress this harmless error
        self.original_stderr.write(message)
    
    def flush(self):
        self.original_stderr.flush()

# Replace stderr with filtered version to suppress MessageFactory errors
# Note: setup.py also filters install_requirements.sh errors, but this runs earlier in run.py
sys.stderr = FilteredStderr(sys.stderr)

# Note: Pydantic warnings are expected and intermittent - they come from dependencies
# (likely HuggingFace transformers) and are harmless. We keep the filter minimal
# to avoid hiding vital warnings from our own code.
# Filter UnsupportedFieldAttributeWarning from pydantic (comes from dependency usage of Field())
# This warning occurs when dependencies use Field() with attributes that don't apply in their context
warnings.filterwarnings('ignore', category=UserWarning, module='pydantic._internal._generate_schema')
# Also catch by message pattern in case it's emitted differently
warnings.filterwarnings('ignore', message='.*UnsupportedFieldAttributeWarning.*')
warnings.filterwarnings('ignore', message='.*repr.*attribute.*Field.*function.*')
warnings.filterwarnings('ignore', message='.*frozen.*attribute.*Field.*function.*')

import argparse
import logging

# Add scripts directory to path for direct execution
scripts_dir = Path(__file__).parent
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

# Import system utilities (suppresses Kaggle install_requirements.sh error at module import time)
from utils.system import setup_logging, set_seed
from utils.config import update_config_from_args
from config.config import default_config

logger = logging.getLogger(__name__)


def add_common_arguments(parser: argparse.ArgumentParser) -> None:
    """Add common arguments to a parser"""
    parser.add_argument('--data-root', type=str, help='Data root directory')
    parser.add_argument('--model', type=str, help='Timm model name (e.g., efficientnet_b0)')
    parser.add_argument('--preprocessing', type=str, default='', help='Comma-separated preprocessing list (e.g., "resize,normalize")')
    parser.add_argument('--data-augmentation', type=str, default='', help='Comma-separated augmentation list (e.g., "geometric_transformations,color_jittering")')
    parser.add_argument('--log-file', type=str, help='Optional log file path for output (uses existing logging infrastructure)')


def main() -> None:
    # CLI description (contest-agnostic, defaults to CSIRO)
    parser = argparse.ArgumentParser(description='ML Competition Framework - Biomass Prediction')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Train command
    train_parser = subparsers.add_parser('train', help='Train model')
    add_common_arguments(train_parser)
    train_parser.add_argument('--batch-size', type=int, help='Batch size')
    train_parser.add_argument('--lr', type=float, help='Learning rate')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test model')
    test_parser.add_argument('--model-path', type=str, help='Model checkpoint path (if not provided, uses best fold)')
    test_parser.add_argument('--data-root', type=str, help='Data root directory')
    
    # Train and test command
    train_test_parser = subparsers.add_parser('train_test', help='Train and test')
    add_common_arguments(train_test_parser)
    
    # Grid search command
    grid_search_parser = subparsers.add_parser('grid_search', help='Run hyperparameter grid search')
    grid_search_parser.add_argument('--search-type', choices=['quick', 'in_depth'], default='quick', help='Grid search type')
    add_common_arguments(grid_search_parser)
    
    # Dataset grid search command
    dataset_grid_search_parser = subparsers.add_parser('dataset_grid_search', help='Run dataset grid search (preprocessing/augmentation combinations)')
    add_common_arguments(dataset_grid_search_parser)
    dataset_grid_search_parser.add_argument('--dataset-type', type=str, choices=['full', 'split'], default='split', help='Dataset type: left/right split (default: split, standard approach) or full image (explicit override)')
    dataset_grid_search_parser.add_argument('--max-augmentation', action='store_true', default=False, help='Quick test mode: test only the maximally augmented variant (all preprocessing + all augmentation) instead of full grid search')
    
    # Hyperparameter grid search command
    hyperparameter_grid_search_parser = subparsers.add_parser('hyperparameter_grid_search', help='Run hyperparameter grid search using fixed dataset config from saved model')
    hyperparameter_grid_search_parser.add_argument('--search-type', choices=['defaults', 'quick', 'in_depth', 'thorough', 'focused_in_depth', 'focused_thorough'], default='thorough', help='Grid search type (default: thorough). "defaults" tests baseline, focused_* types require --previous-results-file')
    hyperparameter_grid_search_parser.add_argument('--dataset-type', type=str, choices=['full', 'split'], default='split', help='Dataset type: left/right split (default: split, standard approach) or full image (explicit override)')
    hyperparameter_grid_search_parser.add_argument('--metadata-path', type=str, help='Optional path to model_metadata.json (auto-detects if not provided)')
    hyperparameter_grid_search_parser.add_argument('--results-file', type=str, help='Optional path to results.json from dataset grid search (fallback for metadata)')
    hyperparameter_grid_search_parser.add_argument('--previous-results-file', type=str, help='Optional path to previous hyperparameter grid search results.json (required for focused_* search types)')
    add_common_arguments(hyperparameter_grid_search_parser)
    
    # Regression grid search command
    regression_grid_search_parser = subparsers.add_parser('regression_grid_search', help='Run regression model hyperparameter grid search using pre-extracted features')
    regression_grid_search_parser.add_argument('--feature-filename', type=str, required=True, help='Feature filename (e.g., "variant_0100_features.npz")')
    regression_grid_search_parser.add_argument('--regression-model-type', type=str, choices=['lgbm', 'xgboost', 'ridge'], default='lgbm', help='Type of regression model (default: lgbm)')
    regression_grid_search_parser.add_argument('--search-type', choices=['defaults', 'quick', 'in_depth', 'thorough'], default='quick', help='Grid search type (default: quick)')
    add_common_arguments(regression_grid_search_parser)
    
    # Cleanup grid search checkpoints command
    cleanup_parser = subparsers.add_parser('cleanup_grid_search', help='Retroactively clean up grid search checkpoints')
    cleanup_parser.add_argument('--model-dir', type=str, help='Model directory (default: from config)')
    cleanup_parser.add_argument('--results-file', type=str, help='Results JSON file path (default: output/dataset_grid_search/gridsearch_results.json)')
    cleanup_parser.add_argument('--keep-top', type=int, default=20, help='Number of top variants to keep (default: 20)')
    
    # Submit best variant command
    submit_best_parser = subparsers.add_parser('submit_best', help='Generate submission using best variant from dataset grid search')
    add_common_arguments(submit_best_parser)
    submit_best_parser.add_argument('--variant-id', type=str, help='Optional variant ID to use instead of best (e.g., variant_0067)')
    submit_best_parser.add_argument('--results-file', type=str, help='Path to results.json file (default: output/dataset_grid_search/gridsearch_results.json)')
    
    # Train and export command (Pipeline C)
    train_and_export_parser = subparsers.add_parser('train_and_export', help='Train model and export for submission (Pipeline C)')
    add_common_arguments(train_and_export_parser)
    train_and_export_parser.add_argument('--results-file', type=str, help='Optional path to grid search results.json to use best variant')
    train_and_export_parser.add_argument('--variant-id', type=str, help='Optional variant ID to use instead of best (e.g., variant_0001). If not provided, uses variant with highest CV score.')
    train_and_export_parser.add_argument('--export-dir', type=str, help='Export directory (default: uses get_best_model_path())')
    train_and_export_parser.add_argument('--dataset-type', type=str, choices=['full', 'split'], default='split', help='Dataset type: left/right split (default: split, standard approach) or full image (explicit override)')
    train_and_export_parser.add_argument('--fresh-train', action='store_true', default=False, help='Delete directory if all folds complete and start fresh training. If False, preserve directory to allow resume from checkpoints.')
    train_and_export_parser.add_argument('--export-only', action='store_true', default=False, help='Skip training entirely and just export existing model. If False, perform training (either fresh or resume based on --fresh-train).')
    # Feature extraction mode arguments
    train_and_export_parser.add_argument('--feature-extraction-mode', action='store_true', default=False, help='Enable feature extraction mode: extract features from images, then train regression model on features')
    train_and_export_parser.add_argument('--feature-extraction-model', type=str, help='Model name for feature extraction (e.g., facebook/dinov2-large). Required if --feature-extraction-mode is set.')
    train_and_export_parser.add_argument('--regression-model-type', type=str, choices=['lgbm', 'xgboost', 'ridge'], help='Regression model type for feature extraction mode. Required if --feature-extraction-mode is set.')
    train_and_export_parser.add_argument('--regression-model-variant-id', type=str, help='Regression model variant ID to use instead of best (e.g., variant_0001). If not provided, uses variant with highest CV score.')
    train_and_export_parser.add_argument('--extract-features', action='store_true', default=None, help='Extract features from scratch (overrides config). If not set, uses config value (default: True). Use --no-extract-features to load from cache.')
    train_and_export_parser.add_argument('--data-manipulation-combo', type=str, help='Data manipulation combo ID (e.g., "combo_00", "combo_63"). Loads preprocessing/augmentation from metadata and applies to config.')
    train_and_export_parser.add_argument('--no-extract-features', dest='extract_features', action='store_false', help='Load features from cache instead of extracting (requires --extract-features=False or config.extract_features=False)')
    
    # Export model command (utility)
    export_model_parser = subparsers.add_parser('export_model', help='Export existing trained model for submission')
    add_common_arguments(export_model_parser)
    export_model_parser.add_argument('--results-file', type=str, help='Optional path to grid search results.json')
    export_model_parser.add_argument('--variant-id', type=str, help='Optional variant ID to export (instead of best)')
    export_model_parser.add_argument('--best-variant-file', type=str, help='Optional path to best_dataset_variant.json')
    export_model_parser.add_argument('--export-dir', type=str, help='Export directory (default: uses get_best_model_path())')
    
    # Ensemble command
    ensemble_parser = subparsers.add_parser('ensemble', help='Generate submission using ensemble of top N models from grid search results')
    add_common_arguments(ensemble_parser)
    ensemble_parser.add_argument('--model-paths', type=str, help='Comma-separated list of model base paths (directories containing best_model.pth and model_metadata.json). If provided, uses direct paths instead of grid search results.')
    ensemble_parser.add_argument('--results-files', type=str, help='Comma-separated list of results file paths (optional, auto-detects if not provided). Ignored if --model-paths is provided.')
    ensemble_parser.add_argument('--top-n', type=int, default=3, help='Number of top models to ensemble (default: 3). Ignored if --model-paths is provided.')
    ensemble_parser.add_argument('--method', choices=['simple_average', 'weighted_average', 'ranked_average', 'percentile_average'], default='weighted_average', help='Ensembling method (default: weighted_average)')
    ensemble_parser.add_argument('--fallback-paths', type=str, help='Comma-separated list of additional paths to search for results files. Ignored if --model-paths is provided.')
    ensemble_parser.add_argument('--submission-scores', type=str, help='JSON file path or inline JSON string with model_path -> submission_score mapping. Example: \'{"path1": 0.5, "path2": 0.4}\' or path to JSON file.')
    ensemble_parser.add_argument('--score-type', choices=['cv', 'submission', 'combined'], default='cv', help='Which scores to use for weighting: cv (default), submission, or combined (weighted average of cv and submission)')
    ensemble_parser.add_argument('--dataset-type', type=str, choices=['full', 'split'], default='split', help='Dataset type: left/right split (default: split, standard approach) or full image (explicit override)')
    
    # Regression ensemble command
    regression_ensemble_parser = subparsers.add_parser('regression_ensemble', help='Generate submission using ensemble of regression models (LGBM, XGBoost, Ridge)')
    add_common_arguments(regression_ensemble_parser)
    regression_ensemble_parser.add_argument('--ensemble-config', type=str, required=True, help='JSON string with ensemble configuration: {"model_types": [...], "model_indices": {...}, "method": "...", "score_type": "..."}')
    regression_ensemble_parser.add_argument('--dataset-type', type=str, choices=['full', 'split'], default='split', help='Dataset type: left/right split (default: split, standard approach) or full image (explicit override)')
    
    # Stacking command
    stacking_parser = subparsers.add_parser('stacking', help='Generate submission using stacking ensemble with Ridge meta-model')
    add_common_arguments(stacking_parser)
    stacking_parser.add_argument('--stacking-config', type=str, required=True, help='JSON string with stacking configuration: {"model_types": [...], "model_versions": {...}, "meta_model_alpha": 10.0, "n_folds": 5}')
    stacking_parser.add_argument('--dataset-type', type=str, choices=['full', 'split'], default='split', help='Dataset type: left/right split (default: split, standard approach) or full image (explicit override)')
    
    # Stacking ensemble command
    stacking_ensemble_parser = subparsers.add_parser('stacking_ensemble', help='Generate submission using stacking with ensemble base models')
    add_common_arguments(stacking_ensemble_parser)
    stacking_ensemble_parser.add_argument('--stacking-ensemble-config', type=str, required=True, help='JSON string with stacking ensemble configuration: {"model_types": [...], "ensemble_configs": {...}, "meta_model_alpha": 10.0, "n_folds": 5}')
    stacking_ensemble_parser.add_argument('--dataset-type', type=str, choices=['full', 'split'], default='split', help='Dataset type: left/right split (default: split, standard approach) or full image (explicit override)')
    
    # Hybrid stacking command
    hybrid_stacking_parser = subparsers.add_parser('hybrid_stacking', help='Generate submission using hybrid stacking (regression + end-to-end ensembles)')
    add_common_arguments(hybrid_stacking_parser)
    hybrid_stacking_parser.add_argument('--hybrid-stacking-config', type=str, required=True, help='JSON string with hybrid stacking configuration: {"regression_ensembles": {...}, "end_to_end_ensembles": {...}, "meta_model_alpha": 10.0, "n_folds": 5}')
    hybrid_stacking_parser.add_argument('--dataset-type', type=str, choices=['full', 'split'], default='split', help='Dataset type: left/right split (default: split, standard approach) or full image (explicit override)')
    
    # Multi-variant regression training command
    multi_variant_regression_train_parser = subparsers.add_parser('multi_variant_regression_train', help='Train and export multiple regression models, one per model_id')
    add_common_arguments(multi_variant_regression_train_parser)
    multi_variant_regression_train_parser.add_argument('--feature-extraction-model', type=str, required=True, help='Model for feature extraction (e.g., dinov2_base)')
    multi_variant_regression_train_parser.add_argument('--regression-model-type', type=str, required=True, choices=['lgbm', 'xgboost', 'ridge'], help='Regression model type')
    multi_variant_regression_train_parser.add_argument('--model-ids', type=str, required=True, help='Comma-separated list of model_id strings from gridsearch_metadata.json (e.g., "080,083,086,116,119")')
    multi_variant_regression_train_parser.add_argument('--extract-features', action='store_true', default=None, help='Extract features from scratch (overrides config). If not set, uses config value (default: True). Use --no-extract-features to load from cache.')
    multi_variant_regression_train_parser.add_argument('--no-extract-features', dest='extract_features', action='store_false', help='Load features from cache instead of extracting')
    multi_variant_regression_train_parser.add_argument('--data-manipulation-combo', type=str, help='Data manipulation combo ID (e.g., "combo_00", "combo_63"). Loads preprocessing/augmentation from metadata and applies to config.')
    multi_variant_regression_train_parser.add_argument('--fresh-train', action='store_true', help='Start fresh training (delete existing directories)')
    multi_variant_regression_train_parser.add_argument('--dataset-type', type=str, choices=['full', 'split'], default='split', help='Dataset type: left/right split (default: split, standard approach) or full image (explicit override)')
    
    # Submit command (Pipeline A - lightweight)
    submit_parser = subparsers.add_parser('submit', help='Generate submission from uploaded model (Pipeline A - offline)')
    add_common_arguments(submit_parser)
    submit_parser.add_argument('--model-path', type=str, help='Optional explicit model checkpoint path')
    submit_parser.add_argument('--metadata-path', type=str, help='Optional explicit model_metadata.json path')
    submit_parser.add_argument('--results-file', type=str, help='Optional results.json path (fallback if metadata not found)')
    submit_parser.add_argument('--model-name', type=str, help='Model name for model-specific folder structure (e.g., dinov2, timm_efficientnet_b3). Used to locate checkpoints in csiro-models/pytorch/{model-name}/')
    submit_parser.add_argument('--dataset-type', type=str, choices=['full', 'split'], default='split', help='Dataset type: left/right split (default: split, standard approach) or full image (explicit override)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Setup logging (use log file if provided)
    log_file = getattr(args, 'log_file', None)
    setup_logging(log_file=log_file)
    logger.info(f"Running command: {args.command}")
    if log_file:
        logger.info(f"Logging output to: {log_file}")
    
    # Setup seed
    set_seed(default_config.seed)
    
    # Create config
    config = default_config
    
    # Update config from args using utility function
    update_config_from_args(
        config=config,
        data_root=getattr(args, 'data_root', None),
        model_name=getattr(args, 'model_name', None),
        preprocessing=getattr(args, 'preprocessing', None),
        data_augmentation=getattr(args, 'data_augmentation', None),
        batch_size=getattr(args, 'batch_size', None),
        learning_rate=getattr(args, 'lr', None),
        setup_kaggle_paths=True
    )
    
    # Route command to appropriate pipeline
    from cli.command_router import route_command
    route_command(args.command, args, config)


if __name__ == '__main__':
    main()
