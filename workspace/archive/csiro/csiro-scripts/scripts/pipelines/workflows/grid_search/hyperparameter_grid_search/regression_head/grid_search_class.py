# grid_search_class.py
# RegressionGridSearch class extending GridSearchBase


import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
import numpy as np

from config.config import Config
from ...base import GridSearchBase
from ...utils.helpers import create_regression_variant_key_from_result
from modeling.utils import get_top_n_results
from modeling.utils.metadata.regression_metadata import get_writable_metadata_dir
from utils.system.io import load_json_file

logger = logging.getLogger(__name__)


class RegressionGridSearch(GridSearchBase):
    """
    Regression grid search implementation using GridSearchBase.
    
    Tests regression model hyperparameter combinations with pre-extracted features.
    """
    
    def __init__(
        self,
        config: Config,
        regression_model_type: str
    ):
        """
        Initialize regression grid search.
        
        Args:
            config: Configuration object.
            regression_model_type: Type of regression model ('lgbm', 'xgboost', 'ridge').
        """
        super().__init__(config)
        self.regression_model_type = regression_model_type
        # Feature data will be set by setup_features() before running
        self.all_features = None
        self.all_targets = None
        self.fold_assignments = None
        self.feature_filename = None
        self.param_names = []
        self.param_grid = {}
    
    def _get_grid_search_type(self) -> str:
        """Return grid search type identifier."""
        return 'regression_grid_search'
    
    def _get_results_filename(self) -> str:
        """Return results filename."""
        return 'gridsearch_results.json'
    
    def _create_grid_search_dir(self) -> Path:
        """
        Create grid search output directory.
        
        Regression uses subdirectory based on model type.
        """
        grid_search_dir = Path(self.config.paths.output_dir) / 'regression_grid_search' / self.regression_model_type
        from utils.system import ensure_dir
        ensure_dir(grid_search_dir)
        return grid_search_dir
    
    def _generate_variant_grid(self) -> List[tuple]:
        """Generate the grid of hyperparameter combinations."""
        # This is set up by setup_parameter_grid in the pipeline
        return []
    
    def setup_features(
        self,
        all_features,
        all_targets,
        fold_assignments,
        feature_filename: str,
        param_names: List[str],
        param_grid: Dict[str, List[Any]]
    ):
        """
        Setup feature data for regression grid search.
        
        Args:
            all_features: All features array.
            all_targets: All targets array.
            fold_assignments: Fold assignments array.
            feature_filename: Feature filename.
            param_names: List of parameter names.
            param_grid: Parameter grid dictionary.
        """
        self.all_features = all_features
        self.all_targets = all_targets
        self.fold_assignments = fold_assignments
        self.feature_filename = feature_filename
        self.param_names = param_names
        self.param_grid = param_grid
    
    def _create_variant_key(self, variant: tuple) -> Tuple:
        """
        Create variant key from hyperparameter combination.
        
        Args:
            variant: Hyperparameter combination tuple.
        
        Returns:
            Variant key tuple (feature_filename, hyperparams_key).
        """
        if self.feature_filename is None:
            raise ValueError("Feature data not set. Call setup_features() first.")
        
        hyperparameters = dict(zip(self.param_names, variant))
        hyperparams_key = tuple(sorted(hyperparameters.items()))
        return (self.feature_filename, hyperparams_key)
    
    def _create_variant_key_from_result(self, result: Dict[str, Any]) -> Optional[Tuple]:
        """
        Create variant key from result dictionary.
        
        Args:
            result: Result dictionary from JSON file.
        
        Returns:
            Variant key tuple or None if result is invalid.
        """
        return create_regression_variant_key_from_result(result)
    
    def save_variant_result(self, result: Dict[str, Any]) -> None:
        """
        Override base class to skip saving to results file.
        
        Regression grid search uses metadata files instead of results file.
        Metadata saving is handled in execution.py.
        
        Args:
            result: Variant result dictionary.
        """
        # Metadata files are saved in execution.py, so we don't need to save to results file
        variant_id = result.get('variant_id', result.get('combination_id', 'unknown'))
        variant_index = result.get('variant_index', result.get('combination_index', 'unknown'))
        logger.debug(f"Result for variant {variant_id} (index {variant_index}) saved to metadata files")
    
    def load_completed_variants(self, keep_top_n: int) -> Tuple[Set[Any], Set[Any], List[Dict[str, Any]], int]:
        """
        Load completed variants from gridsearch_metadata.json.
        
        Overrides base class to use metadata files instead of results file.
        Loads from working directory (fresh copy from input).
        
        Args:
            keep_top_n: Number of top variants to keep in memory.
            
        Returns:
            Tuple of (completed_variants_set, skipped_variants_set, top_variants_list, starting_index).
        """
        completed_variants = set()
        skipped_variants = set()
        top_variants = []
        
        if self.feature_filename is None:
            logger.warning("Feature filename not set. Cannot load completed variants.")
            self.completed_variants = completed_variants
            self.skipped_variants = skipped_variants
            self.top_variants = top_variants
            self.starting_index = 0
            return completed_variants, skipped_variants, top_variants, 0
        
        # Load gridsearch_metadata.json from working directory (fresh copy from input)
        working_dir = get_writable_metadata_dir() / self.regression_model_type
        gridsearch_file = working_dir / 'gridsearch_metadata.json'
        metadata_file = working_dir / 'metadata.json'
        
        if not gridsearch_file.exists():
            logger.info(f"Gridsearch metadata file not found: {gridsearch_file}")
            self.completed_variants = completed_variants
            self.skipped_variants = skipped_variants
            self.top_variants = top_variants
            self.starting_index = 0
            return completed_variants, skipped_variants, top_variants, 0
        
        logger.info(f"Loading completed variant keys from {gridsearch_file}")
        
        # Load gridsearch results from working directory (fresh copy from input)
        all_gridsearch_results = load_json_file(
            gridsearch_file, expected_type=list, file_type="Regression gridsearch metadata JSON"
        )
        
        # Filter by feature_filename
        gridsearch_results = [
            r for r in all_gridsearch_results
            if r.get('feature_filename') == self.feature_filename
        ]
        
        # Load metadata.json for hyperparameters lookup
        variant_id_to_hyperparams = {}
        if metadata_file.exists():
            variants = load_json_file(
                metadata_file, expected_type=list, file_type="Regression metadata JSON"
            )
            for variant in variants:
                variant_id = variant.get('variant_id')
                hyperparams = variant.get('hyperparameters')
                if variant_id and hyperparams:
                    variant_id_to_hyperparams[variant_id] = hyperparams
        
        # Process gridsearch results
        successful_count = 0
        for result in gridsearch_results:
            # Only process entries with cv_score (completed successfully)
            if result.get('cv_score') is None:
                continue
            
            # Look up hyperparameters from metadata.json using variant_id
            variant_id = result.get('variant_id')
            if variant_id not in variant_id_to_hyperparams:
                logger.warning(f"Hyperparameters not found for variant_id {variant_id}, skipping")
                continue
            
            # Create result-like dict with hyperparameters for variant key creation
            enriched_result = {
                'hyperparameters': variant_id_to_hyperparams[variant_id],
                'feature_filename': result.get('feature_filename'),
                'cv_score': result.get('cv_score'),
                'fold_scores': result.get('fold_scores', [])
            }
            
            # Create variant key
            variant_key = self._create_variant_key_from_result(enriched_result)
            if variant_key is not None:
                completed_variants.add(variant_key)
                successful_count += 1
                top_variants.append(enriched_result)
        
        # Sort by score and keep only top N
        top_variants = get_top_n_results(top_variants, keep_top_n, metric_key='cv_score')
        
        # Calculate starting_index from metadata.json (source of truth)
        starting_index = 0
        if metadata_file.exists():
            variants = load_json_file(
                metadata_file, expected_type=list, file_type="Regression metadata JSON"
            )
            if variants:
                max_metadata_index = max(
                    (v.get('variant_index', -1) for v in variants if v.get('variant_index') is not None),
                    default=-1
                )
                starting_index = max_metadata_index + 1
        
        logger.info(f"Found {successful_count} successfully completed variants for {self.feature_filename}")
        logger.info(f"Tracking top {len(top_variants)} variant metadata in memory")
        logger.info(f"Starting variant_index from {starting_index} (ensuring sequential numbering)")
        
        # Store in instance variables
        self.completed_variants = completed_variants
        self.skipped_variants = skipped_variants
        self.top_variants = top_variants
        self.starting_index = starting_index
        
        return completed_variants, skipped_variants, top_variants, starting_index
    
    def _run_variant(
        self,
        variant: tuple,
        variant_index: int,
        total_variants: int,
        actual_variant_num: Optional[int] = None,
        total_to_test: Optional[int] = None
    ) -> Tuple[Optional[float], Optional[List[float]], Dict[str, Any], Path]:
        """
        Run a single regression combination.
        
        Args:
            variant: Hyperparameter combination tuple.
            variant_index: Index of variant in grid.
            total_variants: Total number of variants in grid.
            actual_variant_num: Optional actual variant number being tested (1-based, excludes skipped).
            total_to_test: Optional total number of variants actually being tested (excludes skipped).
        
        Returns:
            Tuple of (cv_score, fold_scores, result_dict, variant_model_dir).
            Note: Regression doesn't use model directories, so variant_model_dir is empty Path.
        """
        if self.all_features is None:
            raise ValueError("Feature data not set. Call setup_features() first.")
        
        from .execution import execute_single_regression_combination
        
        # Use actual variant number and total to test for logging if provided
        # Otherwise fall back to grid position
        if actual_variant_num is not None and total_to_test is not None:
            # Use actual counts (excludes skipped variants)
            idx = actual_variant_num - 1  # Convert to 0-based for internal use
            total_combinations = total_to_test
        else:
            # Fallback: calculate grid position idx for logging
            idx = 0
            try:
                from itertools import product
                if hasattr(self, 'param_grid') and self.param_grid:
                    param_values = list(self.param_grid.values())
                    all_combinations = list(product(*param_values))
                    if variant in all_combinations:
                        idx = all_combinations.index(variant)
            except (ValueError, AttributeError, TypeError):
                # Fallback: use 0 if we can't determine grid position
                pass
            total_combinations = total_variants
        
        # Execute the combination
        result, was_skipped = execute_single_regression_combination(
            idx=idx,
            variant_index=variant_index,  # Use pre-calculated variant_index from base class
            combination=variant,
            param_names=self.param_names,
            total_combinations=total_combinations,  # Use actual total to test if available
            config=self.config,
            all_features=self.all_features,
            all_targets=self.all_targets,
            fold_assignments=self.fold_assignments,
            feature_filename=self.feature_filename,
            regression_model_type=self.regression_model_type
        )
        
        if result is None:
            return None, None, {}, Path()
        
        cv_score = result.get('cv_score')
        fold_scores = result.get('fold_scores')
        
        # Regression doesn't use model directories
        variant_model_dir = Path()
        
        return cv_score, fold_scores, result, variant_model_dir
