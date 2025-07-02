"""
Tool Template - ScriptCraft v2.0.0 Standardized Pattern

This template demonstrates the NEW, DRY approach for ScriptCraft tools.
ALL tools inherit from BaseTool and use its standardized methods.

Key Principle: Load → Process → Save
- Use BaseTool.load_data_file() for loading
- Implement your custom logic
- Use BaseTool.save_data_file() for saving

NEW: Automatic configuration loading, standardized CLI, and simplified main functions!
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# === Environment Detection & Import Setup ===
# Import the environment detection module (copy env.py into your tool)
from .env import setup_environment

# Set up environment and get imports
IS_DISTRIBUTABLE = setup_environment()

# Import with fallbacks for dual environment support
if IS_DISTRIBUTABLE:
    # Distributable imports
    import common as cu
else:
    # Development imports
    import scriptcraft.common as cu

# Import utilities (same in both environments since it's local)
try:
    from .utils import ToolNameUtils
except ImportError:
    # If utils import fails, try current directory
    from .utils import ToolNameUtils


# ===== SIMPLIFIED ARCHITECTURE: Only BaseTool needed! =====

# 1. SINGLE FILE ANALYSIS (most common pattern)
class SingleFileAnalyzer(cu.BaseTool):
    """Tool that analyzes one file at a time."""
    
    def __init__(self):
        super().__init__(
            name="Single File Analyzer",
            description="🔍 Analyzes individual data files",
            tool_name="single_file_analyzer"  # For config access
        )
    
    def run(self, input_paths: Optional[List[Union[str, Path]]] = None,
            output_dir: Optional[Union[str, Path]] = None,
            domain: Optional[str] = None,
            output_filename: Optional[str] = None,
            **kwargs) -> None:
        """Run analysis on input files."""
        self.log_start()
        
        try:
            # Validate inputs using DRY method
            if not self.validate_input_files(input_paths or []):
                raise ValueError("❌ No input files provided")
            
            # Resolve output directory using DRY method
            output_path = self.resolve_output_directory(output_dir or self.default_output_dir)
            
            # Process each input file
            for input_path in input_paths:
                cu.log_and_print(f"🔍 Processing: {input_path}")
                
                # Load data using DRY method
                data = self.load_data_file(input_path)
                
                # Your custom analysis logic here
                results = self._analyze_data(data, domain)
                
                # Generate output filename using DRY method
                if not output_filename:
                    output_filename = self.get_output_filename(
                        input_path, 
                        suffix="analysis"
                    )
                
                # Save using DRY method  
                output_file = output_path / output_filename
                self.save_data_file(results, output_file, include_index=False)
                
                cu.log_and_print(f"✅ Analysis completed: {output_file}")
            
            self.log_completion()
            
        except Exception as e:
            self.log_error(f"Analysis failed: {e}")
            raise
    
    def _analyze_data(self, data: Any, domain: Optional[str] = None) -> Any:
        """Your custom analysis logic."""
        # Example: basic data profiling
        import pandas as pd
        
        profile = pd.DataFrame({
            'column': data.columns,
            'dtype': data.dtypes,
            'non_null_count': data.count(),
            'null_percentage': (data.isnull().sum() / len(data) * 100).round(2)
        })
        
        return profile


# 2. DATA COMPARISON (for comparing datasets)
class DataComparer(cu.BaseTool):
    """Tool that compares two datasets."""
    
    def __init__(self):
        super().__init__(
            name="Data Comparer",
            description="🔍 Compares two datasets for differences",
            tool_name="data_comparer"
        )
    
    def run(self, input_paths: Optional[List[Union[str, Path]]] = None,
            output_dir: Optional[Union[str, Path]] = None,
            domain: Optional[str] = None,
            output_filename: Optional[str] = None,
            **kwargs) -> None:
        """Compare datasets."""
        self.log_start()
        
        try:
            # Validate we have exactly 2 files
            if not self.validate_input_files(input_paths or [], required_count=2):
                raise ValueError("❌ Need exactly 2 input files to compare")
            
            # Resolve output directory using DRY method
            output_path = self.resolve_output_directory(output_dir or self.default_output_dir)
                
            # Load both files using DRY method
            cu.log_and_print("📂 Loading datasets...")
            df1 = self.load_data_file(input_paths[0])
            df2 = self.load_data_file(input_paths[1])
            
            # Use built-in comparison method
            basic_comparison = self.compare_dataframes(df1, df2)
            
            # Add your custom comparison logic
            detailed_comparison = self._detailed_compare(df1, df2, domain)
            
            # Combine results
            comparison_results = {
                **basic_comparison,
                'detailed_analysis': detailed_comparison
            }
            
            # Generate output filename using DRY method
            if not output_filename:
                output_filename = self.get_output_filename(
                    input_paths[0], 
                    suffix=f"vs_{Path(input_paths[1]).stem}_comparison"
                )
            
            # Save results (convert to DataFrame or save as needed)
            output_file = output_path / output_filename
            # self.save_data_file(comparison_results, output_file)
            
            self.log_completion(output_file)
            
        except Exception as e:
            self.log_error(f"Comparison failed: {e}")
            raise
        
    def _detailed_compare(self, df1: Any, df2: Any, domain: Optional[str] = None) -> Dict[str, Any]:
        """Your custom comparison logic."""
        return {"custom_analysis": "results"}


# 3. DATA TRANSFORMATION (legacy transform() pattern)
class DataTransformer(cu.BaseTool):
    """Tool that transforms data (supports legacy transform pattern)."""
    
    def __init__(self):
        super().__init__(
            name="Data Transformer", 
            description="🔄 Transforms data files",
            tool_name="data_transformer"
        )
    
    def run(self, input_paths: Optional[List[Union[str, Path]]] = None,
            output_dir: Optional[Union[str, Path]] = None,
            domain: Optional[str] = None,
            output_filename: Optional[str] = None,
            **kwargs) -> None:
        """Run transformation."""
        self.log_start()
        
        try:
            if not self.validate_input_files(input_paths or []):
                raise ValueError("❌ No input files provided")
            
            output_path = self.resolve_output_directory(output_dir or self.default_output_dir)
            
            for input_path in input_paths:
                cu.log_and_print(f"🔄 Processing: {input_path}")
                
                # Load → Process → Save pattern
                data = self.load_data_file(input_path)
                processed_data = self._process_data(data, domain)
                
                # Generate output filename using DRY method
                if not output_filename:
                    output_filename = self.get_output_filename(
                        input_path, 
                        suffix="processed"
                    )
                
                output_file = output_path / output_filename
                self.save_data_file(processed_data, output_file, include_index=False)
                
                cu.log_and_print(f"✅ Transformation completed: {output_file}")
            
            self.log_completion()
            
        except Exception as e:
            self.log_error(f"Transformation failed: {e}")
            raise
    
    # Legacy support: can also be called via transform()
    def transform(self, domain: str, input_path: Union[str, Path], 
                 output_path: Union[str, Path], paths: Optional[Dict[str, Any]] = None) -> None:
        """Legacy transform method for backward compatibility."""
        data = self.load_data_file(input_path)
        processed_data = self._process_data(data, domain)
        self.save_data_file(processed_data, output_path)
    
    def _process_data(self, data: Any, domain: Optional[str] = None) -> Any:
        """Your custom processing logic."""
        # Example: basic data cleaning
        cleaned = data.copy()
        cleaned = cleaned.dropna(how='all')  # Remove empty rows
        cleaned = cleaned.drop_duplicates()   # Remove duplicates
        return cleaned


# 4. YOUR ACTUAL TOOL (replace with your implementation)
class ToolName(cu.BaseTool):
    """Replace this with your actual tool implementation."""
    
    def __init__(self):
        super().__init__(
            name="Tool Name",
            description="🔧 Brief description of what this tool does",
            tool_name="tool_name",  # For config access
            requires_dictionary=False  # Set to True if tool needs dictionary
        )
        self.utils = ToolNameUtils()  # Your utility class
    
    def run(self, input_paths: Optional[List[Union[str, Path]]] = None,
            output_dir: Optional[Union[str, Path]] = None,
            domain: Optional[str] = None,
            output_filename: Optional[str] = None,
            mode: Optional[str] = None,
            **kwargs) -> None:
        """
        Main execution method for the tool.
        
        Args:
            input_paths: List of input file paths
            output_dir: Output directory path
            domain: Domain name (e.g., Clinical, Biomarkers)
            output_filename: Custom output filename
            mode: Operating mode (if applicable)
            **kwargs: Additional tool-specific arguments
        """
        self.log_start()
        
        try:
            # 1. Validate inputs using DRY method
            if not self.validate_input_files(input_paths or []):
                raise ValueError("❌ No input files provided")
            
            # 2. Resolve paths using DRY methods
            output_path = self.resolve_output_directory(output_dir or self.default_output_dir)
            
            # 3. Process each file
            for input_path in input_paths:
                self._process_file(Path(input_path), output_path, domain, mode, output_filename, **kwargs)
            
            self.log_completion()
            
        except Exception as e:
            self.log_error(f"Tool execution failed: {e}")
            raise
    
    def _process_file(self, input_file: Path, output_dir: Path, domain: Optional[str], 
                     mode: Optional[str], output_filename: Optional[str], **kwargs) -> None:
        """Process a single input file."""
        cu.log_and_print(f"🔄 Processing file: {input_file}")
        
        try:
            # Load data using DRY method
            data = self.load_data_file(input_file)
            
            # Apply your custom processing
            processed_data = self.utils.process_data(data, domain, mode, **kwargs)
            
            # Generate output filename using DRY method
            if not output_filename:
                output_filename = self.get_output_filename(
                    input_file, 
                    suffix="processed"
                )
            
            # Save results using DRY method
            output_file = output_dir / output_filename
            self.save_data_file(processed_data, output_file, include_index=False)
            
            cu.log_and_print(f"✅ Completed processing: {input_file}")
            
        except Exception as e:
            self.log_error(f"Error processing {input_file}: {e}")
            raise


# ===== SIMPLIFIED MAIN FUNCTION =====
# NEW: Use the standardized main function pattern!

def main():
    """Main entry point for the tool."""
    # NEW: Use the standardized argument parsing
    args = cu.parse_tool_args("Tool Name - Brief description")
    
    # Create tool instance  
    tool = ToolName()
    
    # Run the tool with standardized error handling
    tool.run(
        input_paths=args.input_paths,
        output_dir=args.output_dir,
        domain=args.domain,
        output_filename=args.output_filename,
        mode=args.mode
    )


# ===== ALTERNATIVE: Use the factory function for even simpler main =====
# Uncomment the line below to use the automatic main function factory:
# main = cu.create_standard_main_function(ToolName, "tool_name", "Tool Name - Brief description")


if __name__ == "__main__":
    main() 