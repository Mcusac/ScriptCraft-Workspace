# hyperparameter_base.py
# Base class for hyperparameter grid searches
#
# Provides common infrastructure for hyperparameter-specific grid search logic.
# This is an intermediate abstract class that can be used to share common
# hyperparameter-related functionality between end-to-end and regression head searches.

from abc import ABC
from typing import Dict, List, Any, Tuple
from itertools import product

import logging
from config.config import Config
from ...base import GridSearchBase

logger = logging.getLogger(__name__)


class HyperparameterGridSearchBase(GridSearchBase, ABC):
    """
    Base class for hyperparameter grid searches.
    
    Provides common infrastructure for hyperparameter-specific logic:
    - Parameter grid management
    - Combination generation
    - Hyperparameter application
    
    Subclasses should implement:
    - `_get_grid_search_type()`: Return grid search type identifier
    - `_get_results_filename()`: Return results filename
    - `_generate_variant_grid()`: Generate the grid of variants
    - `_create_variant_key()`: Create unique key for variant tracking
    - `_run_variant()`: Execute a single variant
    """
    
    def __init__(self, config: Config):
        """
        Initialize hyperparameter grid search base.
        
        Args:
            config: Configuration object with grid_search settings.
        """
        super().__init__(config)
        self.param_grid: Dict[str, List[Any]] = {}
        self.param_names: List[str] = []
        self.all_combinations: List[tuple] = []
    
    def setup_parameter_grid(self, param_grid: Dict[str, List[Any]]) -> Tuple[Dict[str, List[Any]], List[tuple]]:
        """
        Setup hyperparameter grid and generate all combinations.
        
        Args:
            param_grid: Parameter grid dictionary mapping parameter names to value lists.
        
        Returns:
            Tuple of (param_grid, all_combinations).
        """
        self.param_grid = param_grid
        self.param_names = list(param_grid.keys())
        param_values = list(param_grid.values())
        self.all_combinations = list(product(*param_values))
        
        logger.info(f"Total hyperparameter combinations: {len(self.all_combinations):,}")
        
        return self.param_grid, self.all_combinations
    
    def _generate_variant_grid(self) -> List[tuple]:
        """
        Generate the grid of hyperparameter combinations.
        
        Returns:
            List of hyperparameter combination tuples.
        """
        if not self.all_combinations:
            raise ValueError("Parameter grid not set. Call setup_parameter_grid() first.")
        return self.all_combinations
    
    def _create_variant_key_from_hyperparameters(self, variant: tuple) -> Tuple[Tuple[str, Any], ...]:
        """
        Create hyperparameter key from variant tuple.
        
        This is a helper method that converts a variant tuple to a sorted
        tuple of (key, value) pairs for use in variant keys.
        
        Args:
            variant: Hyperparameter combination tuple.
        
        Returns:
            Sorted tuple of (key, value) pairs from hyperparameters.
        """
        if not self.param_names:
            raise ValueError("Parameter names not set. Call setup_parameter_grid() first.")
        
        hyperparameters = dict(zip(self.param_names, variant))
        return tuple(sorted(hyperparameters.items()))
