# dictionary_driven_checker/tool.py

"""Dictionary-driven checker using the new pipeline architecture.

This module provides the main functionality for dictionary-based validation,
supporting both basic dictionary validation and plugin-based special validators.
"""

import sys
from pathlib import Path
import pandas as pd
from typing import Optional, Dict, Any
from scriptcraft.common import (
    load_config, setup_logging, log_and_print,
    OutlierMethod, normalize_column_names
)
from .utils import run_dictionary_checker
from scriptcraft.common.plugins import registry
from scriptcraft.common.core import BaseTool

def initialize_plugins(config: Dict[str, Any]) -> None:
    """Initialize plugin system with configuration."""
    # Register any additional plugins from config
    plugin_settings = config.get('plugins', {})
    validators = registry.get_all_plugins('validator')
    for plugin_type, settings in plugin_settings.items():
        if plugin_type in validators:
            validator = validators[plugin_type]
            for key, value in settings.items():
                setattr(validator, key, value)

class DictionaryDrivenChecker(BaseTool):
    """Checker for validating data against a data dictionary using plugins."""
    
    def __init__(self):
        super().__init__(
            name="Dictionary Driven Checker",
            description="Validates data against a data dictionary using configurable plugins"
        )
        self.config = load_config()
        initialize_plugins(self.config)
    
    def validate_input(self, input_data: Any) -> bool:
        """Validate input data for the checker."""
        # For this checker, we don't use input_data directly
        # The validation is done internally using filenames
        return True
    
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Process method for BaseProcessor compatibility.
        
        Args:
            data: Input DataFrame to validate
            
        Returns:
            pd.DataFrame: Validation results
        """
        # This is a validation tool, not a data transformer
        # Return the original data unchanged
        return data
    
    def run(self, *args, **kwargs):
        """
        Run method for BaseComponent compatibility.
        
        This method satisfies the abstract method requirement.
        For this tool, the primary interface is through check() method.
        """
        self.log_message("🔍 Dictionary Driven Checker run method called")
        return True
    
    def check(self, domain: str, input_path: str, output_path: str, paths: dict) -> None:
        """
        Check data against dictionary using plugins.
        
        Args:
            domain: The domain to check (e.g., "Biomarkers", "Clinical")
            input_path: Path to the input data file
            output_path: Path to save validation results
            paths: Dictionary containing path configurations
        
        Returns:
            None
        
        Raises:
            FileNotFoundError: If dictionary file is not found
            pd.errors.EmptyDataError: If input file is empty
            ValueError: If required columns are missing
        """
        try:
            # Load and normalize data
            log_and_print(f"\n📂 Loading {domain} dataset and dictionary...")
            
            # Read input data
            input_path = Path(input_path)
            df = pd.read_excel(input_path) if str(input_path).endswith('.xlsx') else pd.read_csv(input_path)
            
            # Read dictionary for this domain
            dict_path = input_path.parent / f"{domain}_dictionary.csv"
            if not dict_path.exists():
                raise FileNotFoundError(f"Dictionary not found: {dict_path}")
                
            dict_df = pd.read_excel(dict_path) if str(dict_path).endswith('.xlsx') else pd.read_csv(dict_path)
            
            # Normalize column names
            df.columns = normalize_column_names(df.columns)
            dict_df.columns = normalize_column_names(dict_df.columns)
            
            # Get outlier detection method from config
            outlier_method = OutlierMethod[
                self.config.get('outlier_detection', 'IQR').upper()
            ]
            
            # Run validation with plugins
            output_path = Path(output_path)
            run_dictionary_checker(
                df=df,
                dict_df=dict_df,
                domain=domain,
                output_path=output_path,
                outlier_method=outlier_method
            )
            
        except Exception as e:
            log_and_print(f"❌ Error in dictionary validation: {str(e)}")
            raise

# Create singleton instance
checker = DictionaryDrivenChecker()

def run_dictionary_driven_checker(domain: str, input_path: str, output_path: str, paths: dict) -> None:
    """
    Entry point function for the Dictionary Driven Checker.
    
    Args:
        domain: The domain to check
        input_path: Path to the input data file
        output_path: Path to save validation results
        paths: Dictionary containing path configurations
    
    Returns:
        None
    """
    return checker.check(domain, input_path, output_path, paths)