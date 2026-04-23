# contest/csiro/data_schema.py
# CSIRO biomass competition data schema

from typing import Dict, List
from contest.base import ContestDataSchema


class CSIRODataSchema(ContestDataSchema):
    """
    CSIRO biomass competition data schema.
    
    Defines CSV column names, sample ID format, and data structure for
    the CSIRO biomass prediction competition.
    """
    
    @property
    def train_csv_columns(self) -> List[str]:
        """CSIRO train.csv expected columns."""
        return [
            'sample_id',
            'image_path',
            'Sampling_Date',
            'State',
            'Species',
            'Pre_GSHH_NDVI',
            'Height_Ave_cm',
            'target_name',
            'target'
        ]
    
    @property
    def test_csv_columns(self) -> List[str]:
        """CSIRO test.csv expected columns."""
        return [
            'sample_id',
            'image_path',
            'target_name'
        ]
    
    @property
    def metadata_columns(self) -> List[str]:
        """CSIRO metadata columns (non-target columns)."""
        return [
            'image_id',
            'image_path',
            'Sampling_Date',
            'State',
            'Species',
            'Pre_GSHH_NDVI',
            'Height_Ave_cm'
        ]
    
    @property
    def image_path_column(self) -> str:
        """CSIRO image path column name."""
        return 'image_path'
    
    @property
    def target_name_column(self) -> str:
        """CSIRO target name column name."""
        return 'target_name'
    
    @property
    def target_value_column(self) -> str:
        """CSIRO target value column name."""
        return 'target'
    
    @property
    def sample_id_column(self) -> str:
        """CSIRO sample ID column name."""
        return 'sample_id'
    
    def parse_sample_id(self, sample_id: str) -> Dict[str, str]:
        """
        Parse CSIRO sample ID format: {image_id}__{target_name}
        
        Args:
            sample_id: Sample ID string (e.g., 'ID1001187975__Dry_Green_g')
            
        Returns:
            Dictionary with 'image_id' and 'target_name' keys
        """
        parts = sample_id.split('__', 1)
        if len(parts) != 2:
            raise ValueError(f"Invalid CSIRO sample_id format: {sample_id}. Expected: {{image_id}}__{{target_name}}")
        return {
            'image_id': parts[0],
            'target_name': parts[1]
        }
    
    def format_sample_id(self, image_id: str, target_name: str) -> str:
        """
        Format CSIRO sample ID: {image_id}__{target_name}
        
        Args:
            image_id: Image identifier (e.g., 'ID1001187975')
            target_name: Target name (e.g., 'Dry_Green_g')
            
        Returns:
            Formatted sample ID (e.g., 'ID1001187975__Dry_Green_g')
        """
        return f"{image_id}__{target_name}"
    
    @property
    def rows_per_image_in_test(self) -> int:
        """
        CSIRO test.csv has 5 rows per image (one per target).
        
        Returns:
            5 (number of targets per image in test.csv)
        """
        return 5


# Singleton instance for easy access
_csiro_data_schema_instance: CSIRODataSchema = None


def get_csiro_data_schema() -> CSIRODataSchema:
    """Get singleton CSIRO data schema instance."""
    global _csiro_data_schema_instance
    if _csiro_data_schema_instance is None:
        _csiro_data_schema_instance = CSIRODataSchema()
    return _csiro_data_schema_instance
