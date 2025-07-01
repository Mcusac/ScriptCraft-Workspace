"""
Date Format Standardizer

This transformer standardizes date formats across all date columns in datasets.
"""

import argparse
from pathlib import Path
from typing import List, Optional, Union

from scriptcraft.common import (
    log_and_print, standardize_dates_in_dataframe,
    create_standard_tool, create_runner_function
)
from scriptcraft.common.core import BaseTool
from scriptcraft.common.data.processor import DataProcessor
import pandas as pd


def transform_date_formats(df, domain: str) -> pd.DataFrame:
    """
    Transform date formats in the dataset to a standard format.
    
    Args:
        df: DataFrame to transform
        domain: The domain being processed
        
    Returns:
        Transformed DataFrame
    """
    log_and_print(f"🔄 Standardizing date formats for {domain}...")
    return standardize_dates_in_dataframe(df)


class DateFormatStandardizer(BaseTool):
    """Tool for standardizing date formats in datasets."""
    
    def __init__(self):
        super().__init__(
            name="Date Format Standardizer",
            description="Standardizes date formats in datasets to ensure consistency"
        )
        self.processor = DataProcessor()
    
    @classmethod
    def add_cli_arguments(cls, parser: argparse.ArgumentParser) -> None:
        """Add tool-specific CLI arguments."""
        parser.add_argument(
            '--input_paths', 
            nargs='+', 
            type=str,
            help='Input file paths to process'
        )
        parser.add_argument(
            '--domain',
            type=str,
            help='Domain name (e.g., Clinical, Biomarkers)'
        )
        parser.add_argument(
            '--output_filename',
            type=str,
            default='date_format_standardized.csv',
            help='Output filename (default: date_format_standardized.csv)'
        )
    
    def run(self, 
            input_paths: Optional[List[Union[str, Path]]] = None,
            output_dir: Optional[Union[str, Path]] = None,
            domain: Optional[str] = None,
            output_filename: Optional[str] = None,
            **kwargs) -> bool:
        """
        Run the date format standardizer.
        
        Args:
            input_paths: List of input file paths
            output_dir: Output directory
            domain: Domain name
            output_filename: Output filename
            **kwargs: Additional arguments
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Use the consolidated data processing pattern
            return self.processor.process_files(
                input_paths=input_paths,
                output_dir=output_dir,
                process_func=transform_date_formats,
                output_filename=output_filename or 'date_format_standardized.csv',
                domain=domain,
                **kwargs
            )
        except Exception as e:
            self.log_error(f"Date format standardization failed: {e}")
            return False


# Legacy support - keep the old pattern for backward compatibility
DateFormatStandardizerLegacy = create_standard_tool(
    'transformation',
    'Date Format Standardizer',
    'Standardizes date formats in datasets to ensure consistency',
    transform_date_formats
)

# Create runner function for legacy pipeline support
run_date_format_standardizer = create_runner_function(DateFormatStandardizerLegacy) 