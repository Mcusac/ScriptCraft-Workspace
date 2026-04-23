# notebook package
# Notebook utilities for notebook cells: command builders, handlers, descriptions.
# See NOTEBOOK_GUIDE.md for usage.

from .core import (
    calculate_total_combinations,
    print_gpu_memory_status,
    run_notebook_cell,
    print_config_section,
    handle_command_result,
    execute_submission_pipeline,
)
from .commands.grid_search import (
    build_hyperparameter_grid_search_command,
    build_dataset_grid_search_command,
    build_regression_grid_search_command,
)
from .commands.ensemble import build_ensemble_command
from .commands.regression_ensemble import build_regression_ensemble_command
from .commands.stacking import (
    build_stacking_command,
    build_stacking_ensemble_command,
    build_hybrid_stacking_command,
)
from .commands.submission import (
    build_end_to_end_submission_command,
    build_regression_submission_command,
    detect_submission_model_path,
)
from .commands.train_export import (
    build_train_and_export_command,
    build_feature_extraction_train_command,
    build_multi_variant_regression_train_command,
)
from .descriptions.grid_search import (
    build_hyperparameter_grid_search_description,
    build_dataset_grid_search_description,
    build_regression_grid_search_description,
)
from .descriptions.ensemble import build_ensemble_description
from .descriptions.regression_ensemble import build_regression_ensemble_description
from .descriptions.stacking import (
    build_stacking_description,
    build_stacking_ensemble_description,
    build_hybrid_stacking_description,
)
from .handlers.grid_search import (
    handle_hyperparameter_grid_search_result,
    handle_dataset_grid_search_result,
    handle_regression_grid_search_result,
)
from .handlers.train_export import verify_export_output
from .handlers.ensemble import handle_ensemble_result
from .handlers.regression_ensemble import handle_regression_ensemble_result
from .handlers.stacking import (
    handle_stacking_result,
    handle_stacking_ensemble_result,
    handle_hybrid_stacking_result,
)
from .grid_search.utils import calculate_focused_grid_size, auto_detect_grid_search_results
from .train_export import detect_train_export_mode

__all__ = [
    # Core
    'calculate_total_combinations',
    'print_gpu_memory_status',
    'run_notebook_cell',
    'print_config_section',
    'handle_command_result',
    'execute_submission_pipeline',
    # Commands
    'build_hyperparameter_grid_search_command',
    'build_dataset_grid_search_command',
    'build_regression_grid_search_command',
    'build_ensemble_command',
    'build_regression_ensemble_command',
    'build_stacking_command',
    'build_stacking_ensemble_command',
    'build_hybrid_stacking_command',
    'build_end_to_end_submission_command',
    'build_regression_submission_command',
    'detect_submission_model_path',
    'build_train_and_export_command',
    'build_feature_extraction_train_command',
    'build_multi_variant_regression_train_command',
    # Descriptions
    'build_hyperparameter_grid_search_description',
    'build_dataset_grid_search_description',
    'build_regression_grid_search_description',
    'build_ensemble_description',
    'build_regression_ensemble_description',
    'build_stacking_description',
    'build_stacking_ensemble_description',
    'build_hybrid_stacking_description',
    # Handlers
    'handle_hyperparameter_grid_search_result',
    'handle_dataset_grid_search_result',
    'handle_regression_grid_search_result',
    'verify_export_output',
    'handle_ensemble_result',
    'handle_regression_ensemble_result',
    'handle_stacking_result',
    'handle_stacking_ensemble_result',
    'handle_hybrid_stacking_result',
    # Grid search utilities
    'calculate_focused_grid_size',
    'auto_detect_grid_search_results',
    # Train/export
    'detect_train_export_mode'
]
