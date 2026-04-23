# modeling package
# Model-related utilities
#
# This package contains utilities for model management organized into subpackages:
# - export/: Model export operations and metadata management
# - finding/: Model checkpoint finding utilities
# - results/: Results and variant utilities
# - ensemble_diagnostics/: Ensemble analysis utilities
#
# Subpackages:
# - export: Export operations, metadata builder/loader, scenario handlers
# - finding: Model finder functions and location strategies
# - results: Best variant utilities, results viewing, variant ID operations
# - ensemble_diagnostics: Ensemble weighting and diagnostics
#
# Cross-package dependencies:
# - Imports from training package for fold operations
# - Imports from system package for file/path operations
# These are acceptable as modeling operations build on training results.

from modeling.utils.export import (
    handle_just_trained_model,
    handle_best_variant_file,
    handle_results_file,
    handle_auto_detect,
    export_from_training_dir,
    export_from_grid_search,
    export_from_single_checkpoint,
    copy_model_checkpoint,
    write_metadata_file,
    copy_results_file,
    MetadataBuilder,
    prepare_model_metadata_dict,
    load_model_metadata,
    save_submission_file,
    process_batch_for_model,
    extract_batch_data,
)

from modeling.utils.results import (
    create_variant_id,
    create_variant_key,
    parse_variant_id,
    is_valid_variant_id,
    normalize_variant_id,
    VARIANT_ID_FORMAT,
    COMBINATION_ID_FORMAT,
    load_results_json,
    find_best_variant,
    find_variant_by_id,
    get_variant_best_fold,
    get_best_variant_info,
    get_regression_variant_info,
    view_grid_search_results,
    verify_submission_file,
    get_top_n_results,
    create_grid_search_result_dict,
    create_grid_search_error_result_dict,
    get_next_variant_index,
    update_best_score,
)

from modeling.utils.finding import CSIROModelsStrategy

from modeling.utils.ensemble_diagnostics import (
    load_cv_scores_from_paths,
    compare_cv_submission_scores,
    get_method_weights,
    analyze_ensemble_weights,
    print_diagnostic_summary,
)

__all__ = [
    # Export handlers
    'handle_just_trained_model',
    'handle_best_variant_file',
    'handle_results_file',
    'handle_auto_detect',
    # Model export utilities
    'export_from_training_dir',
    'export_from_grid_search',
    'export_from_single_checkpoint',
    'copy_model_checkpoint',
    'write_metadata_file',
    'copy_results_file',
    # Metadata builder
    'MetadataBuilder',
    'prepare_model_metadata_dict',
    # Variant utilities
    'create_variant_id',
    'create_variant_key',
    'parse_variant_id',
    'is_valid_variant_id',
    'normalize_variant_id',
    'VARIANT_ID_FORMAT',
    'COMBINATION_ID_FORMAT',
    # Best variant utilities
    'load_results_json',
    'find_best_variant',
    'find_variant_by_id',
    'get_variant_best_fold',
    'get_best_variant_info',
    'get_regression_variant_info',
    # Results utilities
    'view_grid_search_results',
    'verify_submission_file',
    'get_top_n_results',
    'create_grid_search_result_dict',
    'create_grid_search_error_result_dict',
    'get_next_variant_index',
    'update_best_score',
    # Model finding utilities
    'CSIROModelsStrategy',
    # Metadata loader
    'load_model_metadata',
    # Submission utilities
    'save_submission_file',
    # Batch processing
    'process_batch_for_model',
    'extract_batch_data',
    # Ensemble diagnostics
    'load_cv_scores_from_paths',
    'compare_cv_submission_scores',
    'get_method_weights',
    'analyze_ensemble_weights',
    'print_diagnostic_summary'
]

