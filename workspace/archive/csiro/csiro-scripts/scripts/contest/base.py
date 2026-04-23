# contest/base.py
# Abstract base classes for contest-specific implementations

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union
from pathlib import Path
import numpy as np
import pandas as pd


class ContestConfig(ABC):
    """
    Abstract base class for contest-specific configuration.
    
    Defines target names, weights, and derived target computation logic.
    Each contest should implement this interface with its specific values.
    """
    
    @property
    @abstractmethod
    def target_weights(self) -> Dict[str, float]:
        """Return dictionary mapping target names to their weights for evaluation."""
        pass
    
    @property
    @abstractmethod
    def target_order(self) -> List[str]:
        """Return ordered list of all target names (must match target_weights keys)."""
        pass
    
    @property
    @abstractmethod
    def primary_targets(self) -> List[str]:
        """Return list of primary target names (model outputs)."""
        pass
    
    @property
    @abstractmethod
    def derived_targets(self) -> List[str]:
        """Return list of derived target names (computed from primary targets)."""
        pass
    
    @property
    @abstractmethod
    def all_targets(self) -> List[str]:
        """Return list of all target names (primary + derived)."""
        pass
    
    @property
    @abstractmethod
    def num_primary_targets(self) -> int:
        """Return number of primary targets (model output size)."""
        pass
    
    @property
    @abstractmethod
    def num_total_targets(self) -> int:
        """Return total number of targets (primary + derived)."""
        pass
    
    @property
    @abstractmethod
    def constraint_matrix(self) -> Optional[np.ndarray]:
        """
        Return constraint matrix for post-processing, or None if no constraints.
        
        Matrix should define constraints C @ Y = 0 where:
        - C is the constraint matrix (shape: (num_constraints, num_total_targets))
        - Y is the target values vector (shape: (num_total_targets,))
        
        Returns:
            Constraint matrix as numpy array, or None if no constraints.
        """
        pass
    
    @abstractmethod
    def compute_derived_target_values(self, *args) -> Dict[str, float]:
        """
        Compute derived target values from primary target values.
        
        Args:
            *args: Primary target values (contest-specific number and order)
            
        Returns:
            Dictionary mapping all target names to their values.
        """
        pass


class ContestDataSchema(ABC):
    """
    Abstract base class for contest-specific data schema definitions.
    
    Defines CSV column names, sample ID format, and data structure assumptions.
    """
    
    @property
    @abstractmethod
    def train_csv_columns(self) -> List[str]:
        """Return list of expected columns in train.csv."""
        pass
    
    @property
    @abstractmethod
    def test_csv_columns(self) -> List[str]:
        """Return list of expected columns in test.csv."""
        pass
    
    @property
    @abstractmethod
    def metadata_columns(self) -> List[str]:
        """Return list of metadata column names (non-target columns)."""
        pass
    
    @property
    @abstractmethod
    def image_path_column(self) -> str:
        """Return name of the column containing image paths."""
        pass
    
    @property
    @abstractmethod
    def target_name_column(self) -> str:
        """Return name of the column containing target names."""
        pass
    
    @property
    @abstractmethod
    def target_value_column(self) -> str:
        """Return name of the column containing target values."""
        pass
    
    @property
    @abstractmethod
    def sample_id_column(self) -> str:
        """Return name of the column containing sample IDs."""
        pass
    
    @abstractmethod
    def parse_sample_id(self, sample_id: str) -> Dict[str, str]:
        """
        Parse sample ID into components.
        
        Args:
            sample_id: Sample ID string
            
        Returns:
            Dictionary with parsed components (e.g., {'image_id': '...', 'target_name': '...'})
        """
        pass
    
    @abstractmethod
    def format_sample_id(self, image_id: str, target_name: str) -> str:
        """
        Format sample ID from components.
        
        Args:
            image_id: Image identifier
            target_name: Target name
            
        Returns:
            Formatted sample ID string
        """
        pass
    
    @property
    @abstractmethod
    def rows_per_image_in_test(self) -> int:
        """
        Return number of rows per image in test.csv.
        
        Some competitions have one row per image, others have one row per (image, target) pair.
        """
        pass


class ContestPostProcessor(ABC):
    """
    Abstract base class for contest-specific post-processing.
    
    Defines how predictions should be post-processed to enforce constraints
    or apply contest-specific corrections.
    """
    
    @abstractmethod
    def post_process(
        self,
        predictions: Union[pd.DataFrame, np.ndarray],
        target_cols: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Post-process predictions to enforce constraints or apply corrections.
        
        Args:
            predictions: Predictions to post-process. Can be DataFrame or numpy array.
            target_cols: Optional list of target column names in order.
            
        Returns:
            DataFrame with post-processed predictions.
        """
        pass


class ContestPaths(ABC):
    """
    Abstract base class for contest-specific path constants.
    
    Defines Kaggle dataset names and local path defaults for the contest.
    """
    
    @property
    @abstractmethod
    def kaggle_input_dataset_name(self) -> str:
        """Return name of the main Kaggle input dataset (e.g., 'csiro-biomass')."""
        pass
    
    @property
    @abstractmethod
    def kaggle_input_models_dataset_name(self) -> str:
        """Return name of the Kaggle models dataset (e.g., 'csiro-models')."""
        pass
    
    @property
    @abstractmethod
    def kaggle_input_metadata_dataset_name(self) -> str:
        """Return name of the Kaggle metadata dataset (e.g., 'csiro-metadata')."""
        pass
    
    @property
    @abstractmethod
    def kaggle_input_scripts_dataset_name(self) -> str:
        """Return name of the Kaggle scripts dataset (e.g., 'csiro-scripts')."""
        pass
    
    @property
    @abstractmethod
    def kaggle_input_features_dataset_name(self) -> str:
        """Return name of the Kaggle features dataset (e.g., 'csiro-extracted-features')."""
        pass
    
    @property
    @abstractmethod
    def local_data_root(self) -> Path:
        """Return default local data root path (relative to scripts directory)."""
        pass
    
    def get_kaggle_input_path(self, base: Path) -> Path:
        """Get Kaggle input path for main dataset."""
        return base / self.kaggle_input_dataset_name
    
    def get_kaggle_input_models_path(self, base: Path) -> Path:
        """Get Kaggle input path for models dataset."""
        return base / self.kaggle_input_models_dataset_name
    
    def get_kaggle_input_metadata_path(self, base: Path) -> Path:
        """Get Kaggle input path for metadata dataset."""
        return base / self.kaggle_input_metadata_dataset_name
    
    def get_kaggle_input_scripts_path(self, base: Path) -> Path:
        """Get Kaggle input path for scripts dataset."""
        return base / self.kaggle_input_scripts_dataset_name
    
    def get_kaggle_input_features_path(self, base: Path) -> Path:
        """Get Kaggle input path for features dataset."""
        return base / self.kaggle_input_features_dataset_name
