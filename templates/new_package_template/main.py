"""
Tool Template

This template demonstrates the simplified, DRY approach for ScriptCraft tools.
ALL tools inherit from BaseTool and use its standardized methods.

Key Principle: Load → Process → Save
- Use BaseTool.load_data_file() for loading
- Implement your custom logic
- Use BaseTool.save_data_file() for saving
"""

import sys
from pathlib import Path

# === Environment Detection & Import Setup ===
# Import the environment detection module (copy env.py into your tool)
from env import setup_environment, import_dual_env

# Set up environment and get imports
IS_DISTRIBUTABLE = setup_environment()

# Import with fallbacks for dual environment support
try:
    # Development imports (try first)
    from scriptcraft.common.logging import log_and_print
    from scriptcraft.common.core import BaseTool
    from scriptcraft.common.cli import parse_tool_args
except ImportError:
    # Distributable imports (fallback)
    from common.logging import log_and_print
    from common.core import BaseTool
    from common.cli import parse_tool_args

# Import utilities
from .utils import ToolNameUtils


# SIMPLIFIED ARCHITECTURE: Only BaseTool needed!
# Choose your tool pattern:

# 1. SINGLE FILE ANALYSIS (most common)
class SingleFileAnalyzer(BaseTool):
    """Tool that analyzes one file at a time."""
    
    def __init__(self):
        super().__init__(
            name="Single File Analyzer",
            description="🔍 Analyzes individual data files"
        )
    
    def run(self, input_paths, output_dir=None, **kwargs):
        """Run analysis on input files."""
        # Validate inputs using DRY method
        if not self.validate_input_files(input_paths):
            return False
        
        output_path = self.resolve_output_directory(output_dir)
        
        for input_path in input_paths:
            # Load using DRY method
            data = self.load_data_file(input_path)
            
            # Your custom analysis logic here
            results = self._analyze_data(data)
            
            # Save using DRY method  
            output_filename = self.get_output_filename(input_path, suffix="analysis")
            self.save_data_file(results, output_path / output_filename)
    
    def _analyze_data(self, data):
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
class DataComparer(BaseTool):
    """Tool that compares two datasets."""
    
    def __init__(self):
        super().__init__(
            name="Data Comparer",
            description="🔍 Compares two datasets for differences"
        )
    
    def run(self, input_paths, output_dir=None, **kwargs):
        """Compare datasets."""
        # Validate we have exactly 2 files
        if not self.validate_input_files(input_paths, required_count=2):
            return False
        
        output_path = self.resolve_output_directory(output_dir)
            
        # Load both files using DRY method
        df1 = self.load_data_file(input_paths[0])
        df2 = self.load_data_file(input_paths[1])
        
        # Use built-in comparison method
        basic_comparison = self.compare_dataframes(df1, df2)
        
        # Add your custom comparison logic
        detailed_comparison = self._detailed_compare(df1, df2)
        
        # Combine and save results
        results = {**basic_comparison, 'detailed': detailed_comparison}
        # Save as JSON or convert to DataFrame as needed
        
    def _detailed_compare(self, df1, df2):
        """Your custom comparison logic."""
        return {"custom_analysis": "results"}


# 3. DATA TRANSFORMATION (legacy transform() pattern)
class DataTransformer(BaseTool):
    """Tool that transforms data (supports legacy transform pattern)."""
    
    def __init__(self):
        super().__init__(
            name="Data Transformer", 
            description="🔄 Transforms data files"
        )
    
    def run(self, input_paths, output_dir=None, **kwargs):
        """Run transformation."""
        if not self.validate_input_files(input_paths):
            return False
        
        output_path = self.resolve_output_directory(output_dir)
        
        for input_path in input_paths:
            # Load → Process → Save pattern
            data = self.load_data_file(input_path)
            processed_data = self._process_data(data)
            
            output_filename = self.get_output_filename(input_path, suffix="processed")
            self.save_data_file(processed_data, output_path / output_filename)
    
    # Legacy support: can also be called via transform()
    def transform(self, domain, input_path, output_path, paths=None):
        """Legacy transform method for backward compatibility."""
        data = self.load_data_file(input_path)
        processed_data = self._process_data(data)
        self.save_data_file(processed_data, output_path)
    
    def _process_data(self, data):
        """Your custom processing logic."""
        # Example: basic data cleaning
        cleaned = data.copy()
        cleaned = cleaned.dropna(how='all')  # Remove empty rows
        cleaned = cleaned.drop_duplicates()   # Remove duplicates
        return cleaned


# 4. YOUR ACTUAL TOOL (replace with your implementation)
class ToolName(BaseTool):
    """Replace this with your actual tool implementation."""
    
    def __init__(self):
        super().__init__(
            name="Tool Name",
            description="🔧 Brief description of what this tool does"
        )
        self.utils = ToolNameUtils()  # Your utility class
    
    def run(self, input_paths=None, output_dir=None, mode=None, **kwargs):
        """
        Main execution method for the tool.
        
        Args:
            input_paths: List of input file paths
            output_dir: Output directory path
            mode: Operating mode (if applicable)
            **kwargs: Additional tool-specific arguments
        """
        # Use standardized error handling
        return self.run_with_error_handling(
            self._execute_tool, 
            input_paths=input_paths, 
            output_dir=output_dir, 
            mode=mode, 
            **kwargs
        )
    
    def _execute_tool(self, input_paths=None, output_dir=None, mode=None, **kwargs):
        """Internal execution logic."""
        # 1. Validate inputs using DRY method
        if not self.validate_input_files(input_paths or []):
            raise ValueError("Input validation failed")
        
        # 2. Resolve paths using DRY methods
        output_path = self.resolve_output_directory(output_dir)
        
        # 3. Process each file
        for input_path in input_paths:
            self._process_file(Path(input_path), output_path, mode, **kwargs)
    
    def _process_file(self, input_file: Path, output_dir: Path, mode, **kwargs):
        """Process a single input file."""
        self.log_message(f"🔄 Processing file: {input_file}")
        
        try:
            # Load data using DRY method
            data = self.load_data_file(input_file)
            
            # Apply your custom processing
            processed_data = self.utils.process_data(data, mode, **kwargs)
            
            # Save results using DRY method
            output_filename = self.get_output_filename(input_file, suffix="processed")
            output_path = self.save_data_file(processed_data, output_dir / output_filename)
            
            self.log_message(f"✅ Completed processing: {input_file}")
            
        except Exception as e:
            self.log_message(f"❌ Error processing {input_file}: {e}", level="error")
            raise
    

def main():
    """Main entry point for the tool."""
    # Parse command line arguments
    args = parse_tool_args("Tool Name - Brief description")
    
    # Create tool instance  
    tool = ToolName()
        
        # Run the tool
    try:
        tool.run(
            input_paths=args.input_paths,
            output_dir=getattr(args, 'output_dir', None),
            mode=getattr(args, 'mode', None),
            debug=getattr(args, 'debug', False)
        )
        
        log_and_print("🎉 Tool execution completed successfully!")
        
    except Exception as e:
        log_and_print(f"❌ Tool execution failed: {e}", level="error")
        sys.exit(1)


if __name__ == "__main__":
    main() 