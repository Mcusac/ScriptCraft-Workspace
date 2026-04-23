# grid_search_class.py
# HyperparameterGridSearch class extending GridSearchBase

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from itertools import product

from config.config import Config
from ...base import GridSearchBase
from ...utils.constants import (
    GRID_SEARCH_TYPE_HYPERPARAMETER,
    RESULTS_FILE_GRIDSEARCH
)
from ...utils.helpers import (
    create_variant_key,
    create_variant_key_from_result
)
from modeling.grid_search_configs import get_parameter_grid, get_focused_parameter_grid
from .execution import execute_single_combination
from .setup import _load_dataset_configuration

logger = logging.getLogger(__name__)


class HyperparameterGridSearch(GridSearchBase):
    """
    Hyperparameter grid search implementation using GridSearchBase.
    
    Tests hyperparameter combinations with fixed dataset configuration.
    """
    
    def __init__(
        self,
        config: Config,
        search_type: str,
        metadata_path: Optional[str] = None,
        results_file: Optional[str] = None,
        previous_results_file: Optional[str] = None
    ):
        """
        Initialize hyperparameter grid search.
        
        Args:
            config: Configuration object.
            search_type: Type of grid search.
            metadata_path: Optional path to model_metadata.json.
            results_file: Optional path to results.json from dataset grid search.
            previous_results_file: Optional path to previous hyperparameter grid search results.json.
        """
        super().__init__(config)
        self.search_type = search_type
        self.metadata_path = metadata_path
        self.results_file = results_file
        self.previous_results_file = previous_results_file
        self.preprocessing_list: List[str] = []
        self.augmentation_list: List[str] = []
        self.metadata_dict: Dict[str, Any] = {}
        self.param_grid: Dict[str, List[Any]] = {}
        self.all_combinations: List[tuple] = []
    
    def _get_grid_search_type(self) -> str:
        """Return grid search type identifier."""
        return GRID_SEARCH_TYPE_HYPERPARAMETER
    
    def _get_results_filename(self) -> str:
        """Return results filename."""
        return RESULTS_FILE_GRIDSEARCH
    
    def setup_metadata(self) -> Tuple[Dict[str, Any], List[str], List[str]]:
        """
        Load dataset configuration from metadata.
        
        Returns:
            Tuple of (metadata_dict, preprocessing_list, augmentation_list).
        """
        self.metadata_dict, self.preprocessing_list, self.augmentation_list = _load_dataset_configuration(
            self.metadata_path, self.results_file, self.config
        )
        return self.metadata_dict, self.preprocessing_list, self.augmentation_list
    
    def setup_parameter_grid(self) -> Tuple[Dict[str, List[Any]], List[tuple]]:
        """
        Setup hyperparameter grid based on search type.
        
        Returns:
            Tuple of (param_grid, all_combinations).
        """
        # Get hyperparameter grid
        if self.search_type in ['focused_in_depth', 'focused_thorough']:
            if not self.previous_results_file:
                raise ValueError(
                    f"search_type '{self.search_type}' requires previous_results_file parameter."
                )
            self.param_grid = get_focused_parameter_grid(
                self.search_type, self.previous_results_file
            )
        else:
            self.param_grid = get_parameter_grid(self.search_type)
        
        # Generate all combinations
        param_values = list(self.param_grid.values())
        self.all_combinations = list(product(*param_values))
        
        logger.info(f"Total hyperparameter combinations: {len(self.all_combinations):,}")
        
        return self.param_grid, self.all_combinations
    
    def _generate_variant_grid(self) -> List[tuple]:
        """Generate the grid of hyperparameter combinations."""
        if not self.all_combinations:
            self.setup_parameter_grid()
        return self.all_combinations
    
    def _create_variant_key(self, variant: tuple) -> Tuple:
        """
        Create variant key from hyperparameter combination.
        
        Args:
            variant: Hyperparameter combination tuple.
        
        Returns:
            Variant key tuple.
        """
        param_names = list(self.param_grid.keys())
        hyperparameters = dict(zip(param_names, variant))
        return create_variant_key(
            config=self.config,
            preprocessing_list=self.preprocessing_list,
            augmentation_list=self.augmentation_list,
            hyperparameters=hyperparameters
        )
    
    def _create_variant_key_from_result(self, result: Dict[str, Any]) -> Optional[Tuple]:
        """
        Create variant key from result dictionary.
        
        Args:
            result: Result dictionary from JSON file.
        
        Returns:
            Variant key tuple or None if result is invalid.
        """
        return create_variant_key_from_result(result, config=self.config)
    
    def _run_variant(
        self,
        variant: tuple,
        variant_index: int,
        total_variants: int,
        actual_variant_num: Optional[int] = None,
        total_to_test: Optional[int] = None
    ) -> Tuple[Optional[float], Optional[List[float]], Dict[str, Any], Path]:
        """
        Run a single hyperparameter combination.
        
        Args:
            variant: Hyperparameter combination tuple.
            variant_index: Index of variant in grid.
            total_variants: Total number of variants.
        
        Returns:
            Tuple of (cv_score, fold_scores, result_dict, variant_model_dir).
            Note: For hyperparameter searches, result_dict contains the full result,
            and variant_model_dir is extracted from the result.
        """
        param_names = list(self.param_grid.keys())
        result, was_skipped = execute_single_combination(
            idx=variant_index - self.starting_index,  # Convert to 0-based index within this grid
            starting_index=self.starting_index,
            combination=variant,
            param_names=param_names,
            total_combinations=total_variants,
            config=self.config,
            preprocessing_list=self.preprocessing_list,
            augmentation_list=self.augmentation_list,
            base_model_dir=self.base_model_dir,
            results_file_path=self.results_file,
            keep_top_n=self.config.grid_search.keep_top_variants
        )
        
        if result is None:
            return None, None, {}, Path()
        
        # Extract variant_model_dir from result (stored in execution)
        from ...utils.constants import MODEL_DIR_HYPERPARAMETER_GRID_SEARCH
        from modeling.utils import COMBINATION_ID_FORMAT
        combo_id = result.get('variant_id', COMBINATION_ID_FORMAT.format(index=variant_index))
        variant_model_dir = self.base_model_dir / MODEL_DIR_HYPERPARAMETER_GRID_SEARCH / combo_id
        
        cv_score = result.get('cv_score')
        fold_scores = result.get('fold_scores')
        
        return cv_score, fold_scores, result, variant_model_dir
