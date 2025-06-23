"""
[Tool Name] Utilities

This module contains utility functions specific to the [Tool Name] tool.
These functions are tool-specific and not general enough to be placed in scripts.common.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import pandas as pd


class ToolNameUtils:
    """Utility class for [Tool Name] specific operations."""
    
    def __init__(self):
        """Initialize the utility class."""
        pass
    
    def validate_input_file(self, input_file: Path) -> bool:
        """
        Validate input data/files for tool-specific requirements.
        
        Args:
            input_file: Path to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Basic file existence check
        if not input_file.exists():
            print(f"❌ Input file does not exist: {input_file}")
            return False
            
        if not input_file.is_file():
            print(f"❌ Path is not a file: {input_file}")
            return False
        
        # Check file extension
        allowed_extensions = ['.xlsx', '.csv', '.json', '.txt', '.xls']
        if input_file.suffix.lower() not in allowed_extensions:
            print(f"❌ Unsupported file type: {input_file.suffix}")
            return False
            
        # Check file size (example: max 100MB)
        max_size = 100 * 1024 * 1024  # 100MB
        if input_file.stat().st_size > max_size:
            print(f"❌ File too large: {input_file.stat().st_size} bytes")
            return False
        
        # ADD TOOL-SPECIFIC VALIDATION HERE
        # Example: Check if Excel file has required sheets
        # if input_file.suffix.lower() in ['.xlsx', '.xls']:
        #     return self._validate_excel_structure(input_file)
        
        return True
    
    def process_data(self, data: Any, mode: Optional[str], **kwargs) -> Any:
        """
        Process the loaded data with tool-specific logic.
        
        Args:
            data: Loaded input data (DataFrame, dict, etc.)
            mode: Operating mode
            **kwargs: Additional processing arguments
            
        Returns:
            Processed data
        """
        # IMPLEMENT YOUR DATA PROCESSING LOGIC HERE
        
        print("🔧 Applying tool-specific data transformations...")
        
        # Apply mode-specific processing
        if mode == "advanced":
            return self._advanced_processing(data, **kwargs)
        elif mode == "basic":
            return self._basic_processing(data, **kwargs)
        else:
            # Default processing
            return self._default_processing(data, **kwargs)
    
    def _basic_processing(self, data: Any, **kwargs) -> Any:
        """
        Basic processing mode.
        
        Args:
            data: Input data
            **kwargs: Additional arguments
            
        Returns:
            Processed data
        """
        # IMPLEMENT BASIC PROCESSING LOGIC HERE
        
        # Example for pandas DataFrame
        if isinstance(data, pd.DataFrame):
            # Basic cleanup
            processed = data.copy()
            # Remove empty rows
            processed = processed.dropna(how='all')
            # Remove duplicate rows
            processed = processed.drop_duplicates()
            return processed
        
        # For other data types, return as-is for now
        return data
    
    def _advanced_processing(self, data: Any, **kwargs) -> Any:
        """
        Advanced processing mode.
        
        Args:
            data: Input data
            **kwargs: Additional arguments
            
        Returns:
            Processed data
        """
        # IMPLEMENT ADVANCED PROCESSING LOGIC HERE
        
        # Example for pandas DataFrame
        if isinstance(data, pd.DataFrame):
            # Advanced cleanup and processing
            processed = data.copy()
            
            # Apply advanced transformations
            # processed = self._apply_advanced_transformations(processed, **kwargs)
            
            # Add computed columns
            # processed = self._add_computed_columns(processed, **kwargs)
            
            return processed
        
        # For other data types, apply advanced logic as needed
        return data
    
    def _default_processing(self, data: Any, **kwargs) -> Any:
        """
        Default processing mode.
        
        Args:
            data: Input data
            **kwargs: Additional arguments
            
        Returns:
            Processed data
        """
        # IMPLEMENT DEFAULT PROCESSING LOGIC HERE
        
        # For now, just return the data as-is
        return data
    
    def save_results(self, data: Any, output_file: Path) -> None:
        """
        Save processed results to file with tool-specific formatting.
        
        Args:
            data: Processed data to save
            output_file: Output file path
        """
        # Create output directory if it doesn't exist
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Save based on file extension
        if output_file.suffix.lower() == '.json':
            self._save_as_json(data, output_file)
        elif output_file.suffix.lower() == '.csv':
            self._save_as_csv(data, output_file)
        elif output_file.suffix.lower() in ['.xlsx', '.xls']:
            self._save_as_excel(data, output_file)
        else:
            # Default to text format
            self._save_as_text(data, output_file)
    
    def _save_as_json(self, data: Any, output_file: Path) -> None:
        """Save data as JSON file."""
        try:
            # Convert pandas DataFrame to dict if needed
            if isinstance(data, pd.DataFrame):
                data_dict = data.to_dict(orient='records')
            else:
                data_dict = data
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data_dict, f, indent=2, ensure_ascii=False, default=str)
                
        except Exception as e:
            raise ValueError(f"Failed to save as JSON: {e}")
    
    def _save_as_csv(self, data: Any, output_file: Path) -> None:
        """Save data as CSV file."""
        try:
            if isinstance(data, pd.DataFrame):
                data.to_csv(output_file, index=False, encoding='utf-8')
            else:
                # Convert to DataFrame if possible
                df = pd.DataFrame(data) if isinstance(data, (list, dict)) else pd.DataFrame([data])
                df.to_csv(output_file, index=False, encoding='utf-8')
                
        except Exception as e:
            raise ValueError(f"Failed to save as CSV: {e}")
    
    def _save_as_excel(self, data: Any, output_file: Path) -> None:
        """Save data as Excel file."""
        try:
            if isinstance(data, pd.DataFrame):
                data.to_excel(output_file, index=False)
            else:
                # Convert to DataFrame if possible
                df = pd.DataFrame(data) if isinstance(data, (list, dict)) else pd.DataFrame([data])
                df.to_excel(output_file, index=False)
                
        except Exception as e:
            raise ValueError(f"Failed to save as Excel: {e}")
    
    def _save_as_text(self, data: Any, output_file: Path) -> None:
        """Save data as text file."""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                if isinstance(data, str):
                    f.write(data)
                elif isinstance(data, pd.DataFrame):
                    f.write(data.to_string())
                else:
                    f.write(str(data))
                    
        except Exception as e:
            raise ValueError(f"Failed to save as text: {e}")
    
    # ADD MORE TOOL-SPECIFIC UTILITY METHODS HERE
    
    def _validate_excel_structure(self, input_file: Path) -> bool:
        """
        Validate Excel file structure for tool-specific requirements.
        
        Args:
            input_file: Path to Excel file
            
        Returns:
            True if valid structure, False otherwise
        """
        try:
            # Example validation
            # xl_file = pd.ExcelFile(input_file)
            # required_sheets = ['Sheet1', 'Data']
            # if not all(sheet in xl_file.sheet_names for sheet in required_sheets):
            #     print(f"❌ Missing required sheets in {input_file}")
            #     return False
            
            return True
        except Exception as e:
            print(f"❌ Error validating Excel structure: {e}")
            return False
    
    def format_output_filename(self, base_name: str, mode: Optional[str] = None, **kwargs) -> str:
        """
        Generate standardized output filename.
        
        Args:
            base_name: Base filename
            mode: Processing mode
            **kwargs: Additional formatting parameters
            
        Returns:
            Formatted filename
        """
        # Remove extension from base name
        base = Path(base_name).stem
        
        # Add mode suffix if provided
        if mode:
            base = f"{base}_{mode}"
        
        # Add timestamp if requested
        if kwargs.get('add_timestamp', False):
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base = f"{base}_{timestamp}"
        
        # Add custom suffix if provided
        if 'suffix' in kwargs:
            base = f"{base}_{kwargs['suffix']}"
        
        # Get original extension or use default
        original_ext = Path(base_name).suffix
        ext = kwargs.get('extension', original_ext or '.csv')
        
        return f"{base}{ext}" 