# grid_search_class.py
# DatasetGridSearch class extending GridSearchBase

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

from utils.data import get_dataset_variant_grid
from ..base import GridSearchBase
from ..utils.constants import (
    GRID_SEARCH_TYPE_DATASET,
    RESULTS_FILE_GRIDSEARCH
)
from ..utils.helpers import (
    create_variant_key,
    create_variant_key_from_result
)
from ..utils.hyperparameters import get_default_hyperparameters
from .execution import run_single_variant

logger = logging.getLogger(__name__)


class DatasetGridSearch(GridSearchBase):
    """
    Dataset grid search implementation using GridSearchBase.
    
    Tests all combinations of optional preprocessing and augmentation methods.
    """
    
    def _get_grid_search_type(self) -> str:
        """Return grid search type identifier."""
        return GRID_SEARCH_TYPE_DATASET
    
    def _get_results_filename(self) -> str:
        """Return results filename."""
        return RESULTS_FILE_GRIDSEARCH
    
    def _generate_variant_grid(self) -> List[Tuple[List[str], List[str]]]:
        """Generate the grid of preprocessing/augmentation variants."""
        return get_dataset_variant_grid()
    
    def _create_variant_key(self, variant: Tuple[List[str], List[str]]) -> Tuple:
        """
        Create variant key from preprocessing/augmentation variant.
        
        Args:
            variant: Tuple of (preprocessing_list, augmentation_list).
        
        Returns:
            Variant key tuple.
        """
        preprocessing_list, augmentation_list = variant
        default_hyperparameters = get_default_hyperparameters()
        return create_variant_key(
            config=self.config,
            preprocessing_list=preprocessing_list,
            augmentation_list=augmentation_list,
            hyperparameters=default_hyperparameters
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
        variant: Tuple[List[str], List[str]],
        variant_index: int,
        total_variants: int,
        actual_variant_num: Optional[int] = None,
        total_to_test: Optional[int] = None
    ) -> Tuple[Optional[float], Optional[List[float]], Dict[str, Any], Path]:
        """
        Run a single dataset variant.
        
        Args:
            variant: Tuple of (preprocessing_list, augmentation_list).
            variant_index: Index of variant in grid.
            total_variants: Total number of variants.
        
        Returns:
            Tuple of (cv_score, fold_scores, result_dict, variant_model_dir).
        """
        preprocessing_list, augmentation_list = variant
        
        # Run the variant using existing execution function
        cv_score, fold_scores, result, variant_model_dir = run_single_variant(
            variant=(preprocessing_list, augmentation_list),
            variant_index=variant_index,
            total_variants=total_variants,
            config=self.config,
            train_csv_path=self.get_train_csv_path(),
            base_model_dir=self.base_model_dir,
            device=self.device,
            results_file=self.results_file,
        )
        
        return cv_score, fold_scores, result, variant_model_dir
