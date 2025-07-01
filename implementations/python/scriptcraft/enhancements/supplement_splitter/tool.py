"""
Supplement Splitter Enhancement

This enhancement splits a merged supplement file into domain-specific supplements
based on cleaned dictionary files.
"""

from pathlib import Path
from typing import Dict, Union
import pandas as pd

from scriptcraft.common.core import BaseTool
from scriptcraft.common import (
    get_project_root,
    get_domain_paths,
    find_matching_file,
    FILE_PATTERNS,
    load_data
)
from .utils import split_supplement_into_domains


class SupplementSplitter(BaseTool):
    """Enhancement for splitting supplements into domain-specific files."""
    
    def __init__(self):
        super().__init__(
            name="Supplement Splitter",
            description="Splits merged supplement into domain-specific supplements."
        )
        self.root = get_project_root()
        
        # Default paths
        self.default_supplement_path = self.root / "scripts/enhancements/supplement_splitter/supplements/merged_supplement.xlsx"
        self.default_output_dir = self.root / "scripts/enhancements/dictionary_supplementer/supplements"
    
    def enhance(self,
                input_data: Union[pd.DataFrame, Dict[str, pd.DataFrame]] = None,
                **kwargs) -> Dict[str, pd.DataFrame]:
        """
        Split supplement into domain-specific files.
        
        Args:
            input_data: Optional pre-loaded supplement DataFrame
            **kwargs: Optional parameters:
                - supplement_path: Path to merged supplement file
                - output_dir: Directory for domain-specific outputs
                - domains: List of specific domains to process (default: all)
        
        Returns:
            Dict mapping domain names to their supplement DataFrames
        """
        self.log_start()
        
        # Get paths from kwargs or use defaults
        supplement_path = Path(kwargs.get('supplement_path', self.default_supplement_path))
        output_dir = Path(kwargs.get('output_dir', self.default_output_dir))
        specific_domains = kwargs.get('domains', None)
        
        # Load supplement if not provided
        if input_data is None:
            if not supplement_path.exists():
                raise FileNotFoundError(f"Supplement file not found: {supplement_path}")
            input_data = load_data(supplement_path)
        
        if not self.validate_input(input_data):
            raise ValueError("Invalid or empty supplement data")
        
        # Get cleaned dictionary paths for each domain
        domain_paths = get_domain_paths(self.root)
        cleaned_dicts = {}
        
        for domain, paths in domain_paths.items():
            if specific_domains and domain not in specific_domains:
                continue
                
            dict_path = find_matching_file(paths["dictionary"], FILE_PATTERNS["cleaned_dict"])
            if dict_path:
                cleaned_dicts[domain] = dict_path
            else:
                self.log_and_print(f"⚠️ No cleaned dictionary found for {domain}. It will be skipped.", level="warning")
        
        if not cleaned_dicts:
            raise ValueError("No valid cleaned dictionaries found")
        
        # Split supplements
        domain_supplements = split_supplement_into_domains(cleaned_dicts, input_data, output_dir)
        
        # Save each domain supplement
        for domain, df in domain_supplements.items():
            output_path = output_dir / f"{domain}_supplement.xlsx"
            self.save_output(df, output_path)
        
        self.log_completion()
        return domain_supplements


# Create singleton instance
enhancement = SupplementSplitter() 