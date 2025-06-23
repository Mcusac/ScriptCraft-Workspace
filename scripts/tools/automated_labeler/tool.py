"""
Automated Labeler Tool

This tool automatically labels data based on predefined rules and patterns.
It supports various labeling strategies and can handle different data formats.
"""

from pathlib import Path
from typing import Optional, List, Union, Dict, Any

from scripts.common.core import BaseTool
from .utils import (
    load_data,
    apply_labeling_rules,
    save_labeled_data
)


class AutomatedLabeler(BaseTool):
    """Tool for automated data labeling."""
    
    def __init__(self):
        super().__init__(
            name="Automated Labeler",
            description="Automatically labels data based on predefined rules and patterns."
        )
    
    def run(self,
            mode: Optional[str] = None,
            input_paths: Optional[List[Union[str, Path]]] = None,
            output_dir: Optional[Union[str, Path]] = None,
            domain: Optional[str] = None,
            output_filename: Optional[str] = None,
            **kwargs) -> None:
        """
        Run the automated labeling process.
        
        Args:
            mode: Labeling mode (e.g., 'standard', 'custom')
            input_paths: List containing paths to the data files to label
            output_dir: Directory to save labeled data
            domain: Optional domain to filter labeling
            output_filename: Optional custom output filename
            **kwargs: Additional arguments:
                - labeling_rules: Custom labeling rules to apply
                - output_format: Format for the output data
        """
        self.log_start()
        
        # Validate inputs
        if not input_paths:
            raise ValueError("❌ No input files provided")
        
        # Get labeling settings
        labeling_rules = kwargs.get('labeling_rules', {})
        output_format = kwargs.get('output_format', 'excel')
        
        try:
            # Load data
            data = load_data(input_paths[0])
            if data is None:
                raise ValueError("❌ Failed to load data")
            
            # Apply labeling rules
            labeled_data = apply_labeling_rules(
                data,
                rules=labeling_rules,
                domain=domain
            )
            
            # Save labeled data
            if output_dir:
                output_path = Path(output_dir)
            else:
                output_path = Path("output")
            
            if output_filename:
                output_file = output_path / output_filename
            else:
                output_file = output_path / f"labeled_data.{output_format}"
            
            save_labeled_data(
                labeled_data,
                output_file,
                format=output_format
            )
            
            self.log_completion()
            
        except Exception as e:
            self.log_and_print(f"❌ Error: {str(e)}")
            raise


# Create singleton instance
tool = AutomatedLabeler() 