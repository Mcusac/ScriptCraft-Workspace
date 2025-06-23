"""
Data Content Comparer Tool

This tool compares the content of two datasets to identify differences.
It can handle various data formats and provides detailed comparison reports.
"""

from pathlib import Path
from typing import Optional, List, Union, Dict, Any

from scriptcraft.common.core import BaseTool
from .utils import (
    load_datasets,
    compare_datasets,
    generate_report
)


class DataContentComparer(BaseTool):
    """Tool for comparing content between datasets."""
    
    def __init__(self):
        super().__init__(
            name="Data Content Comparer",
            description="Compares content between datasets and generates detailed reports."
        )
    
    def run(self,
            mode: Optional[str] = None,
            input_paths: Optional[List[Union[str, Path]]] = None,
            output_dir: Optional[Union[str, Path]] = None,
            domain: Optional[str] = None,
            output_filename: Optional[str] = None,
            **kwargs) -> None:
        """
        Run the data content comparison.
        
        Args:
            mode: Comparison mode (e.g., 'full', 'quick')
            input_paths: List containing paths to the datasets to compare
            output_dir: Directory to save comparison reports
            domain: Optional domain to filter comparison
            output_filename: Optional custom output filename
            **kwargs: Additional arguments:
                - comparison_type: Type of comparison to perform
                - output_format: Format for the output report
        """
        self.log_start()
        
        # Validate inputs
        if not input_paths or len(input_paths) < 2:
            raise ValueError("❌ Need at least two input files to compare")
        
        # Get comparison settings
        comparison_type = kwargs.get('comparison_type', 'full')
        output_format = kwargs.get('output_format', 'excel')
        
        try:
            # Load datasets
            datasets = load_datasets(input_paths)
            if not datasets:
                raise ValueError("❌ Failed to load datasets")
            
            # Compare datasets
            comparison_results = compare_datasets(
                datasets[0],
                datasets[1],
                comparison_type=comparison_type,
                domain=domain
            )
            
            # Generate report
            if output_dir:
                output_path = Path(output_dir)
            else:
                output_path = Path("output")
            
            if output_filename:
                report_path = output_path / output_filename
            else:
                report_path = output_path / f"content_comparison.{output_format}"
            
            generate_report(
                comparison_results,
                report_path,
                format=output_format
            )
            
            self.log_completion()
            
        except Exception as e:
            self.log_and_print(f"❌ Error: {str(e)}")
            raise


# Create singleton instance
tool = DataContentComparer()

def run_content_comparer(mode: Optional[str] = None, **kwargs) -> None:
    """
    Wrapper function for running the data content comparer tool.
    
    Args:
        mode: Comparison mode (e.g., 'rhq_mode', 'standard_mode')
        **kwargs: Additional arguments passed to the tool
    """
    return tool.run(mode=mode, **kwargs) 