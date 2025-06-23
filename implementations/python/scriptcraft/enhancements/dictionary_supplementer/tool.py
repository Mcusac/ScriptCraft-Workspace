"""
Dictionary Supplementer Enhancement

This enhancement applies domain-specific supplements to cleaned dictionary files,
enhancing them with additional data and validations.
"""

from pathlib import Path
from typing import Dict, Union
import pandas as pd

from scriptcraft.common.core import BaseEnhancement
from scriptcraft.common import (
    find_matching_file,
    load_data,
    FILE_PATTERNS,
    get_project_root,
    get_domain_paths
)
from .utils import supplement_dictionary


class DictionarySupplementer(BaseEnhancement):
    """Enhancement for supplementing dictionaries with additional data."""
    
    def __init__(self):
        super().__init__(
            name="Dictionary Supplementer",
            description="Enhances cleaned dictionaries with domain-specific supplements."
        )
        self.root = get_project_root()
        self.supplement_dir = self.root / "scripts/enhancements/dictionary_supplementer/supplements"
    
    def enhance(self,
                input_data: Union[pd.DataFrame, Dict[str, pd.DataFrame]] = None,
                **kwargs) -> Dict[str, pd.DataFrame]:
        """
        Apply supplements to dictionaries.
        
        Args:
            input_data: Optional pre-loaded dictionary data
            **kwargs: Optional parameters:
                - domains: List of specific domains to process (default: all)
                - update_existing: Whether to update existing values (default: True)
                - input_dir: Directory containing cleaned dictionaries
                - output_dir: Directory for supplemented outputs
        
        Returns:
            Dict mapping domain names to their supplemented dictionary DataFrames
        """
        self.log_start()
        
        # Get parameters
        specific_domains = kwargs.get('domains')
        update_existing = kwargs.get('update_existing', True)
        input_dir = kwargs.get('input_dir')
        output_dir = kwargs.get('output_dir')
        
        # Get domain paths
        domain_paths = get_domain_paths(self.root)
        if specific_domains:
            domain_paths = {k: v for k, v in domain_paths.items() if k in specific_domains}
        
        if not domain_paths:
            raise ValueError("No valid domains found to process")
        
        # Process each domain
        results = {}
        for domain, paths in domain_paths.items():
            try:
                # Get dictionary path
                dict_path = None
                if input_dir:
                    dict_path = find_matching_file(Path(input_dir), FILE_PATTERNS["cleaned_dict"])
                if not dict_path:
                    dict_path = find_matching_file(paths["dictionary"], FILE_PATTERNS["cleaned_dict"])
                
                if not dict_path:
                    self.log_and_print(f"⚠️ No cleaned dictionary found for {domain}. Skipping...", level="warning")
                    continue
                
                # Get supplement path
                supplement_path = self.supplement_dir / f"{domain}_supplement.xlsx"
                if not supplement_path.exists():
                    self.log_and_print(f"⚠️ No supplement found for {domain}. Skipping...", level="warning")
                    continue
                
                # Load data
                dictionary_df = load_data(dict_path)
                supplement_df = load_data(supplement_path)
                
                # Apply supplement
                supplemented_df = supplement_dictionary(
                    dictionary_df,
                    supplement_df,
                    update_existing=update_existing
                )
                
                # Save output
                if output_dir:
                    output_path = Path(output_dir) / f"{domain}_supplemented_dictionary.xlsx"
                else:
                    output_path = dict_path.parent / dict_path.name.replace("_cleaned", "_supplemented")
                
                self.save_output(supplemented_df, output_path)
                results[domain] = supplemented_df
                
            except Exception as e:
                self.log_and_print(f"❌ Error processing {domain}: {str(e)}", level="error")
        
        if not results:
            raise ValueError("No dictionaries were successfully supplemented")
        
        self.log_completion()
        return results


# Create singleton instance
enhancement = DictionarySupplementer() 