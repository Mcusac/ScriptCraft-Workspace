"""
Supplement Prepper Enhancement

This enhancement merges and cleans supplement files to prepare them for splitting
and application to domain dictionaries.
"""

from pathlib import Path
from typing import List, Union, Dict
import pandas as pd

from scripts.common.core import BaseEnhancement
from scripts.common import get_project_root
from .utils import merge_and_clean_supplement


class SupplementPrepper(BaseEnhancement):
    """Enhancement for merging and cleaning supplement files."""
    
    def __init__(self):
        super().__init__(
            name="Supplement Prepper",
            description="Merges and cleans supplement files for dictionary enhancement."
        )
        self.root = get_project_root()
        
        # Default paths
        self.default_input_files = [
            self.root / "scripts/enhancements/supplement_prepper/supplements/minmaxUpdated-beginning.xlsx",
            self.root / "scripts/enhancements/supplement_prepper/supplements/minmaxUpdated-end.xlsx",
        ]
        self.default_output_path = self.root / "scripts/enhancements/supplement_splitter/supplements/merged_supplement.xlsx"
    
    def enhance(self,
                input_data: Union[pd.DataFrame, Dict[str, pd.DataFrame]] = None,
                **kwargs) -> pd.DataFrame:
        """
        Merge and clean supplement files.
        
        Args:
            input_data: Not used (files are loaded from paths)
            **kwargs: Optional parameters:
                - input_files: List of input file paths
                - output_path: Path for output file
        
        Returns:
            Merged and cleaned supplement DataFrame
        """
        self.log_start()
        
        # Get paths from kwargs or use defaults
        input_files = kwargs.get('input_files', self.default_input_files)
        output_path = Path(kwargs.get('output_path', self.default_output_path))
        
        # Validate input files
        for file_path in input_files:
            if not Path(file_path).exists():
                raise FileNotFoundError(f"Input file not found: {file_path}")
        
        # Merge and clean supplements
        merged_df = merge_and_clean_supplement(input_files)
        
        # Save output
        self.save_output(merged_df, output_path)
        self.log_completion(output_path)
        
        return merged_df


# Create singleton instance
enhancement = SupplementPrepper() 