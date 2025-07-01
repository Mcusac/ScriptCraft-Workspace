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
        
        # Validate inputs using base class method
        if not self.validate_input_files(input_paths or [], self.supported_formats):
            raise ValueError("❌ Input validation failed")
        
        if len(input_paths) < 2:
            self.log_error("Need at least two input files to compare")
            raise ValueError("❌ Need at least two input files to compare")
        
        # Get comparison settings
        comparison_type = kwargs.get('comparison_type', 'full')
        output_format = kwargs.get('output_format', 'excel')
        
        try:
            # Load datasets using base class method
            df1 = self.load_data_file(input_paths[0])
            df2 = self.load_data_file(input_paths[1])
            
            # Use base class comparison method for basic analysis
            basic_comparison = self.compare_dataframes(df1, df2)
            
            # Perform detailed comparison using tool-specific logic
            detailed_comparison = compare_datasets(
                df1,
                df2,
                comparison_type=comparison_type,
                domain=domain
            )
            
            # Combine results
            comparison_results = {
                **basic_comparison,
                'detailed_analysis': detailed_comparison
            }
            
            # Resolve output directory using base class method
            output_path = self.resolve_output_directory(output_dir)
            
            # Generate output filename using base class method
            if not output_filename:
                output_filename = self.get_output_filename(
                    input_paths[0], 
                    suffix=f"vs_{Path(input_paths[1]).stem}_comparison"
                )
                # Override extension for report format
                output_filename = output_filename.replace('.csv', f'.{output_format}')
            
            report_path = output_path / output_filename
            
            # Generate report
            generate_report(
                comparison_results,
                report_path,
                format=output_format
            )
            
            self.log_completion(report_path)
            
        except Exception as e:
            self.log_error(f"Comparison failed: {e}")
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