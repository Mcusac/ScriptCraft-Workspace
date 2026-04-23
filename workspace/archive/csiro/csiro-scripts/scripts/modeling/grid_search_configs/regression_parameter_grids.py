# regression_parameter_grids.py
# Parameter grid definitions for regression model hyperparameter grid search
#
# Parameter grids are based on:
# 1. Data-driven analysis: Analysis of top 50 performers from gridsearch_metadata.json (956 total results)
#    - Top 50 ALL have: n_estimators=50, learning_rate=0.005, min_child_samples=30
#    - Top 50 common: num_leaves=[31(15), 63(17), 127(18)], max_depth=[-1(25), 7(25)],
#      subsample=[0.8(17), 0.9(16), 1.0(17)], colsample_bytree=[0.8(18), 0.9(17), 1.0(15)]
#    - Score range: -0.054516 to 0.203698 (best: 0.203698)
# 2. Best practices: LightGBM/XGBoost/Ridge regression tuning guidelines
#    - LGBM: num_leaves should be ≤ 2^max_depth, learning_rate 0.001-0.01 for fine tuning
#    - XGBoost: Similar structure, lower learning rates may be beneficial
#    - Ridge: Logarithmic alpha search (1e-3 to 1e8), solver selection based on data
# 3. Exploration strategy: Focused exploration around top performers with wider ranges for thorough search
#
# The grid search system automatically skips variants that already exist in metadata.json,
# so these grids can include both tested and untested values without duplicate testing.

from typing import Dict, List, Any


def _get_lgbm_defaults() -> Dict[str, Any]:
    """Get default LGBM parameters."""
    return {
        'n_estimators': 300,
        'learning_rate': 0.05,
        'num_leaves': 31,
        'max_depth': -1,  # -1 means no limit
        'min_child_samples': 20,
        'subsample': 1.0,
        'colsample_bytree': 1.0,
        'random_state': 42
    }


def _get_xgboost_defaults() -> Dict[str, Any]:
    """Get default XGBoost parameters."""
    return {
        'n_estimators': 300,
        'learning_rate': 0.05,
        'max_depth': 6,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'gamma': 0,
        'reg_alpha': 0,
        'reg_lambda': 1,
        'random_state': 42
    }


def _get_ridge_defaults() -> Dict[str, Any]:
    """Get default Ridge parameters."""
    return {
        'alpha': 1.0,
        'fit_intercept': True,
        'copy_X': True,
        'max_iter': None,
        'tol': 1e-4,
        'solver': 'auto',
        'positive': False,
        'random_state': 42
    }


def get_regression_parameter_grid(
    model_type: str,
    search_type: str = "quick"
) -> Dict[str, List[Any]]:
    """
    Get parameter grid for regression model grid search.
    
    Uses dict merge to build grids: base defaults + varied parameters.
    Only varied parameters need to be specified for each search type.
    All search types include all model-specific parameters. For parameters not being varied,
    a single default value is used to ensure consistent result structure.
    
    Args:
        model_type: Type of regression model ('lgbm', 'xgboost', 'ridge')
        search_type: Type of grid search ('defaults', 'quick', 'in_depth', 'thorough')
            - 'defaults': Single combination with all default hyperparameters (baseline)
            - 'quick': Small grid (varies key hyperparameters)
            - 'in_depth': Medium grid (varies more hyperparameters)
            - 'thorough': Comprehensive grid (varies all hyperparameters)
    
    Returns:
        Dictionary mapping hyperparameter names to lists of values to try.
        All model-specific parameters are always included.
    
    Raises:
        ValueError: If model_type or search_type is invalid.
    """
    if model_type == 'lgbm':
        defaults = _get_lgbm_defaults()
    elif model_type == 'xgboost' or model_type == 'xgb':
        defaults = _get_xgboost_defaults()
    elif model_type == 'ridge':
        defaults = _get_ridge_defaults()
    else:
        raise ValueError(
            f"Invalid model_type: {model_type}. "
            "Must be one of: 'lgbm', 'xgboost', 'ridge'"
        )
    
    # Base grid: all parameters with single default value
    base_grid = {param: [value] for param, value in defaults.items()}
    
    if search_type == 'defaults':
        # Return base grid as-is (single combination)
        return base_grid
    
    elif search_type == 'quick':
        if model_type == 'lgbm':
            # Analysis-based: Top 50 ALL have n_estimators=50, learning_rate=0.005, min_child_samples=30
            # Top 50 common values: num_leaves=[31,63,127], max_depth=[-1,7], 
            #   subsample=[0.8,0.9,1.0], colsample_bytree=[0.8,0.9,1.0]
            # Strategy: Include all top performer values + small exploration (±10%)
            varied = {
                # ANALYSIS-BASED: Top performer values (all top 50)
                'n_estimators': [45, 50, 55],  # Top: 50 (all 50) + explore ±10%
                'learning_rate': [0.0045, 0.005, 0.0055],  # Top: 0.005 (all 50) + explore ±10%
                'num_leaves': [31, 63, 127],  # Top 50: 31(15), 63(17), 127(18) - all common
                'max_depth': [-1, 7],  # Top 50: -1(25), 7(25) - equally common
                'min_child_samples': [25, 30, 35],  # Top: 30 (all 50) + explore ±17%
                'subsample': [0.8, 0.9, 1.0],  # Top 50: 0.8(17), 0.9(16), 1.0(17) - all common
                'colsample_bytree': [0.8, 0.9, 1.0],  # Top 50: 0.8(18), 0.9(17), 1.0(15) - all common
            }
        elif model_type == 'xgboost' or model_type == 'xgb':
            # Best practices: XGBoost similar to LGBM but may benefit from lower learning rates
            # Multi-output regression considerations: use one_output_per_tree or multi_output_tree strategies
            varied = {
                'n_estimators': [100, 300, 500],  # Best practice: 100-1000
                'learning_rate': [0.005, 0.01, 0.05, 0.1],  # Include lower LR (0.005) based on LGBM findings
                'max_depth': [4, 6, 8],  # Best practice: 4-8 for regression
            }
        else:  # ridge
            # Best practices: Ridge regression alpha tuning on logarithmic scale
            varied = {
                'alpha': [1e-3, 1e-2, 1e-1, 1.0, 10.0, 100, 1e3, 1e4],  # Logarithmic scale: 1e-3 to 1e4
                'solver': ['auto', 'svd', 'lsqr'],  # Common solvers for medium datasets
            }
        return {**base_grid, **varied}
    
    elif search_type == 'in_depth':
        if model_type == 'lgbm':
            # Analysis-based: Top 50 values + wider exploration (±30-50%) + best practice ranges
            # Includes all top performer values plus exploration to find optimal combinations
            varied = {
                # ANALYSIS-BASED: Top performer (50) + wider exploration + best practices
                'n_estimators': [50, 100, 200, 300, 500],  # Top: 50 + explore 2x-10x range
                # ANALYSIS-BASED: Top performer (0.005) + wider range + best practices
                'learning_rate': [0.003, 0.004, 0.005, 0.006, 0.01, 0.03],  # Top: 0.005 + explore ±40% + higher
                # ANALYSIS-BASED: Top performers (31,63,127) + exploration
                'num_leaves': [31, 63, 127, 255],  # Top: 31/63/127 + higher exploration (best practice: ≤2^max_depth)
                # ANALYSIS-BASED: Top performers (-1, 7) + exploration
                'max_depth': [-1, 5, 7, 10],  # Top: -1, 7 + exploration (best practice: 15-100 range)
                # ANALYSIS-BASED: Top performer (30) + wider range
                'min_child_samples': [20, 30, 40, 50],  # Top: 30 + exploration (best practice: hundreds for large datasets)
                # ANALYSIS-BASED: Top performers (0.8,0.9,1.0) + lower exploration
                'subsample': [0.7, 0.8, 0.9, 1.0],  # Top: 0.8/0.9/1.0 + lower exploration
                # ANALYSIS-BASED: Top performers (0.8,0.9,1.0) + exploration
                'colsample_bytree': [0.7, 0.8, 0.9, 1.0],  # Top: 0.8/0.9/1.0 + exploration
            }
        elif model_type == 'xgboost' or model_type == 'xgb':
            # Best practices: XGBoost tuning with multi-output regression considerations
            varied = {
                'n_estimators': [100, 200, 300, 500, 1000],  # Best practice: 100-1000
                'learning_rate': [0.005, 0.01, 0.03, 0.05, 0.1],  # Include lower LR (0.005) based on LGBM findings
                'max_depth': [4, 5, 6, 7, 8],  # Best practice: 4-8 for regression
                'subsample': [0.7, 0.8, 0.9, 1.0],  # Best practice: 0.6-1.0
                'colsample_bytree': [0.7, 0.8, 0.9, 1.0],  # Best practice: 0.6-1.0
                'gamma': [0, 0.1, 0.5],  # Best practice: 0-1.0 for complexity control
                'reg_alpha': [0, 0.1, 1.0],  # L1 regularization
                'reg_lambda': [0.5, 1.0, 2.0],  # L2 regularization (default 1.0)
            }
        else:  # ridge
            # Best practices: Ridge regression comprehensive tuning
            varied = {
                'alpha': [1e-3, 1e-2, 1e-1, 1.0, 10.0, 100, 1e3, 1e4, 1e5],  # Logarithmic scale: 1e-3 to 1e5
                'solver': ['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg'],  # Best practice: multiple solvers
                'fit_intercept': [True, False],  # Best practice: test both
                'positive': [False, True],  # Constrain coefficients to be positive
            }
        return {**base_grid, **varied}
    
    elif search_type == 'thorough':
        if model_type == 'lgbm':
            # Comprehensive grid: Top performer values + wide exploration (±50-100%) + best practice full ranges
            # Explores edge cases and unexplored regions while ensuring top performers are included
            varied = {
                # ANALYSIS-BASED: Top performer (50) + comprehensive range (explore 1x-40x)
                'n_estimators': [50, 100, 200, 300, 500, 1000, 2000],  # Top: 50 + full best practice range
                # ANALYSIS-BASED: Top performer (0.005) + comprehensive range (explore ±60% + higher)
                'learning_rate': [0.003, 0.004, 0.005, 0.006, 0.007, 0.01, 0.03, 0.05, 0.1],  # Top: 0.005 + wide exploration
                # ANALYSIS-BASED: Top performers (31,63,127) + comprehensive range
                'num_leaves': [15, 31, 63, 127, 255],  # Top: 31/63/127 + full exploration (best practice: 10-100, ≤2^max_depth)
                # ANALYSIS-BASED: Top performers (-1, 7) + comprehensive range
                'max_depth': [-1, 3, 5, 7, 10, 15],  # Top: -1, 7 + full exploration (best practice: 15-100)
                # ANALYSIS-BASED: Top performer (30) + comprehensive range
                'min_child_samples': [5, 10, 20, 30, 40, 50],  # Top: 30 + full exploration (best practice: hundreds for large datasets)
                # ANALYSIS-BASED: Top performers (0.8,0.9,1.0) + comprehensive range
                'subsample': [0.6, 0.7, 0.8, 0.9, 1.0],  # Top: 0.8/0.9/1.0 + full exploration
                # ANALYSIS-BASED: Top performers (0.8,0.9,1.0) + comprehensive range
                'colsample_bytree': [0.6, 0.7, 0.8, 0.9, 1.0],  # Top: 0.8/0.9/1.0 + full exploration
            }
        elif model_type == 'xgboost' or model_type == 'xgb':
            # Best practices: Comprehensive XGBoost tuning for multi-output regression
            varied = {
                'n_estimators': [100, 200, 300, 500, 1000, 2000],  # Best practice: 100-2000
                'learning_rate': [0.005, 0.01, 0.03, 0.05, 0.1, 0.2],  # Include lower LR (0.005) based on LGBM findings
                'max_depth': [3, 4, 5, 6, 7, 8, 10],  # Best practice: 3-10 for regression
                'subsample': [0.6, 0.7, 0.8, 0.9, 1.0],  # Best practice: 0.6-1.0
                'colsample_bytree': [0.6, 0.7, 0.8, 0.9, 1.0],  # Best practice: 0.6-1.0
                'gamma': [0, 0.1, 0.5, 1.0],  # Best practice: 0-1.0 for complexity control
                'reg_alpha': [0, 0.01, 0.1, 1.0, 10.0],  # L1 regularization: wider range
                'reg_lambda': [0.5, 1.0, 2.0, 5.0],  # L2 regularization: wider range
            }
        else:  # ridge
            # Best practices: Ridge regression comprehensive tuning with full alpha range
            varied = {
                'alpha': [1e-3, 1e-2, 1e-1, 1.0, 10.0, 100, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8],  # Full logarithmic range
                'solver': ['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag', 'saga'],  # All available solvers
                'fit_intercept': [True, False],  # Best practice: test both
                'positive': [False, True],  # Constrain coefficients to be positive
            }
        return {**base_grid, **varied}
    
    else:
        raise ValueError(
            f"Unknown search_type: {search_type}. "
            f"Must be 'defaults', 'quick', 'in_depth', or 'thorough'"
        )

