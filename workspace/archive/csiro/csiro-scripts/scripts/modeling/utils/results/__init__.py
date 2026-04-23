# results package
# Results and variant utilities
#
# This package contains utilities for working with grid search results and variants:
# - best_variant: Finding and working with best variants from results
# - results: Viewing and verifying grid search results
# - variants: Variant ID and key operations


__all__ = [
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
    # Variant utilities
    'create_variant_id',
    'create_variant_key',
    'parse_variant_id',
    'is_valid_variant_id',
    'normalize_variant_id',
    'VARIANT_ID_FORMAT',
    'COMBINATION_ID_FORMAT'
]

