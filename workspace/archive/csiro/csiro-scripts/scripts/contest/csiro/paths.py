# contest/csiro/paths.py
# CSIRO biomass competition path constants

from pathlib import Path
from contest.base import ContestPaths


class CSIROPaths(ContestPaths):
    """
    CSIRO biomass competition path constants.
    
    Defines Kaggle dataset names and local path defaults for the CSIRO competition.
    """
    
    @property
    def kaggle_input_dataset_name(self) -> str:
        """CSIRO main Kaggle input dataset name."""
        return 'csiro-biomass'
    
    @property
    def kaggle_input_models_dataset_name(self) -> str:
        """CSIRO Kaggle models dataset name."""
        return 'csiro-models'
    
    @property
    def kaggle_input_metadata_dataset_name(self) -> str:
        """CSIRO Kaggle metadata dataset name."""
        return 'csiro-metadata'
    
    @property
    def kaggle_input_scripts_dataset_name(self) -> str:
        """CSIRO Kaggle scripts dataset name."""
        return 'csiro-scripts'
    
    @property
    def kaggle_input_features_dataset_name(self) -> str:
        """CSIRO Kaggle features dataset name."""
        return 'csiro-extracted-features'
    
    @property
    def local_data_root(self) -> Path:
        """CSIRO default local data root path."""
        return Path('../csiro-biomass')


# Singleton instance for easy access
_csiro_paths_instance: CSIROPaths = None


def get_csiro_paths() -> CSIROPaths:
    """Get singleton CSIRO paths instance."""
    global _csiro_paths_instance
    if _csiro_paths_instance is None:
        _csiro_paths_instance = CSIROPaths()
    return _csiro_paths_instance
