"""
Date Format Standardizer

This transformer standardizes date formats across all date columns in datasets.
"""

from scripts.common import (
    log_and_print, standardize_dates_in_dataframe,
    ensure_output_dir,
    find_first_data_file, load_data,
)
from scripts.common.core import BaseProcessor
from typing import Any


class DateFormatStandardizer(BaseProcessor):
    """Transformer for standardizing date formats in datasets."""
    
    def __init__(self):
        super().__init__(
            name="Date Format Standardizer",
            description="Standardizes date formats in datasets to ensure consistency"
        )
    
    def validate_input(self, input_data: Any) -> bool:
        """Validate input data for the transformer."""
        # For this transformer, we don't use input_data directly
        # The validation is done internally using filenames
        return True
    
    def transform(self, domain: str, input_path: str, output_path: str, paths: dict) -> None:
        """
        Transform date formats in the dataset to a standard format.
        
        Args:
            domain: The domain to process (e.g., "Biomarkers", "Clinical")
            input_path: Path to the input data file
            output_path: Path to save the transformed data
            paths: Dictionary containing path configurations
        
        Returns:
            None
        """
        try:
            dataset_file = find_first_data_file(input_path)
            if not dataset_file:
                log_and_print(f"❌ No input file found for {domain}")
                return
                
            df = load_data(dataset_file)
            cleaned = standardize_dates_in_dataframe(df)

            ensure_output_dir(output_path)
            cleaned.to_csv(output_path, index=False)

            log_and_print(f"✅ Standardized dates saved to: {output_path}")
        except Exception as e:
            log_and_print(f"❌ Error processing {domain}: {e}")


# Create singleton instance
transformer = DateFormatStandardizer()

def run_date_format_standardizer(domain, input_path, output_path, paths):
    """
    Entry point function for the Date Format Standardizer.
    
    Args:
        domain: The domain to process
        input_path: Path to the input data file
        output_path: Path to save the transformed data
        paths: Dictionary containing path configurations
    
    Returns:
        None
    """
    return transformer.transform(domain, input_path, output_path, paths) 