"""
Base Classes Module

Provides a SINGLE, DRY base class for ALL tools.
Every tool follows the same pattern: Input → Process → Output + Logs

No artificial distinctions. No organizational cruft. Just functionality.
"""

import logging
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Callable
import pandas as pd

from ..io import ensure_output_dir
from ..logging import log_and_print


class BaseTool(ABC):
    """
    Universal base class for ALL tools.
    
    Handles the complete pattern: Input → Process → Output + Logs
    No artificial distinctions between "processors", "analyzers", "comparers".
    """
    
    def __init__(self, name: str, description: str, supported_formats: Optional[List[str]] = None):
        """
        Initialize tool.
        
        Args:
            name: Tool name
            description: Tool description  
            supported_formats: List of supported file formats (e.g., ['.csv', '.xlsx'])
        """
        self.name = name
        self.description = description
        self.logger = logging.getLogger(name)
        self.supported_formats = supported_formats or ['.csv', '.xlsx', '.xls']
    
    # ===== LOGGING (DRY) =====
    
    def log_message(self, message: str, level: str = "info") -> None:
        """Log a message with emoji formatting."""
        log_and_print(message, level=level)
    
    def log_start(self) -> None:
        """Log tool start."""
        self.log_message(f"🚀 Starting {self.name}...")
    
    def log_completion(self, output_path: Optional[Path] = None) -> None:
        """Log successful completion."""
        if output_path:
            self.log_message(f"✅ {self.name} completed successfully: {output_path}")
        else:
            self.log_message(f"✅ {self.name} completed successfully")
    
    def log_error(self, error: Union[str, Exception]) -> None:
        """Log an error."""
        error_msg = str(error)
        self.log_message(f"❌ {self.name} error: {error_msg}", level="error")
    
    # ===== ENVIRONMENT DETECTION (DRY) =====
    
    @staticmethod
    def is_distributable_environment() -> bool:
        """Detect if we're running in a distributable environment."""
        current_dir = Path.cwd()
        return (current_dir.name == 'scripts' or 
                'distributable' in str(current_dir).lower())
    
    def resolve_input_directory(self, input_dir: Optional[Union[str, Path]] = None, 
                               config: Optional[Any] = None) -> Path:
        """Resolve input directory path for both environments."""
        if input_dir:
            return Path(input_dir)
        
        if config and hasattr(config, 'paths') and hasattr(config.paths, 'input_dir'):
            return Path(config.paths.input_dir)
        
        # Environment-based defaults
        if self.is_distributable_environment():
            current_dir = Path.cwd()
            if current_dir.name == 'scripts':
                return current_dir.parent / "input"
            else:
                return current_dir / "input"
        else:
            return Path("input")
    
    def resolve_output_directory(self, output_dir: Optional[Union[str, Path]] = None) -> Path:
        """Resolve output directory path for both environments."""
        if output_dir:
            output_path = Path(output_dir)
        elif self.is_distributable_environment():
            current_dir = Path.cwd()
            if current_dir.name == 'scripts':
                output_path = current_dir.parent / "output"
            else:
                output_path = current_dir / "output"
        else:
            output_path = Path("output")
        
        ensure_output_dir(output_path)
        return output_path
    
    # ===== FILE OPERATIONS (DRY) =====
    
    def validate_input_files(self, input_paths: List[Union[str, Path]], 
                            required_count: Optional[int] = None) -> bool:
        """Validate input files with standard checks."""
        if not input_paths:
            self.log_error("No input paths provided")
            return False
        
        if required_count and len(input_paths) < required_count:
            self.log_error(f"Need at least {required_count} input files, got {len(input_paths)}")
            return False
            
        for path in input_paths:
            path = Path(path)
            if not path.exists():
                self.log_error(f"Input file not found: {path}")
                return False
            
            if path.suffix.lower() not in [ext.lower() for ext in self.supported_formats]:
                self.log_error(f"Unsupported file type: {path.suffix}. Supported: {self.supported_formats}")
                return False
        
        return True
    
    def load_data_file(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """Universal data file loader with format detection."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {file_path}")
        
        if file_path.suffix.lower() not in [ext.lower() for ext in self.supported_formats]:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
        
        try:
            if file_path.suffix.lower() == '.csv':
                df = pd.read_csv(file_path)
            elif file_path.suffix.lower() in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_path.suffix}")
            
            self.log_message(f"📂 Loaded {file_path.name}: {df.shape[0]} rows, {df.shape[1]} columns")
            return df
            
        except Exception as e:
            self.log_error(f"Failed to load {file_path}: {e}")
            raise
    
    def save_data_file(self, data: pd.DataFrame, output_path: Union[str, Path], 
                      include_index: bool = False) -> Path:
        """Universal data file saver with format detection."""
        output_path = Path(output_path)
        ensure_output_dir(output_path.parent)
        
        try:
            if output_path.suffix.lower() == '.csv':
                data.to_csv(output_path, index=include_index)
            elif output_path.suffix.lower() in ['.xlsx', '.xls']:
                data.to_excel(output_path, index=include_index)
            else:
                # Default to CSV
                output_path = output_path.with_suffix('.csv')
                data.to_csv(output_path, index=include_index)
            
            self.log_message(f"💾 Saved to: {output_path}")
            self.log_message(f"📊 Output shape: {data.shape[0]} rows, {data.shape[1]} columns")
            return output_path
            
        except Exception as e:
            self.log_error(f"Failed to save {output_path}: {e}")
            raise
    
    def get_output_filename(self, input_path: Union[str, Path], 
                           suffix: Optional[str] = None,
                           extension: str = '.csv') -> str:
        """Generate output filename with standardized naming."""
        input_path = Path(input_path)
        base_name = input_path.stem
        
        if suffix:
            base_name = f"{base_name}_{suffix}"
        
        return f"{base_name}{extension}"
    
    # ===== EXECUTION PATTERNS (DRY) =====
    
    def run_with_error_handling(self, func: Callable, *args, **kwargs) -> Any:
        """Execute a function with standardized logging and error handling."""
        self.log_start()
        try:
            result = func(*args, **kwargs)
            self.log_completion()
            return result
        except Exception as e:
            self.log_error(f"Execution failed: {e}")
            raise
    
    # ===== COMMON ANALYSIS PATTERNS (DRY) =====
    
    def compare_dataframes(self, df1: pd.DataFrame, df2: pd.DataFrame, 
                          compare_columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """Standard DataFrame comparison for all comparison tools."""
        comparison = {
            'shape_comparison': {
                'df1_shape': df1.shape,
                'df2_shape': df2.shape,
                'shape_match': df1.shape == df2.shape
            },
            'column_comparison': {
                'df1_columns': list(df1.columns),
                'df2_columns': list(df2.columns),
                'common_columns': list(set(df1.columns) & set(df2.columns)),
                'df1_only': list(set(df1.columns) - set(df2.columns)),
                'df2_only': list(set(df2.columns) - set(df1.columns))
            }
        }
        
        self.log_message(f"📊 Comparison: DF1 {df1.shape} vs DF2 {df2.shape}")
        if not comparison['shape_comparison']['shape_match']:
            self.log_message(f"⚠️ Shape mismatch detected")
        
        return comparison
    
    # ===== LEGACY SUPPORT METHODS =====
    
    def validate_input(self, input_data: Any) -> bool:
        """Legacy validation method for backward compatibility."""
        return True
    
    def process(self, data: Any) -> Any:
        """Legacy process method for backward compatibility."""
        return data
    
    def transform(self, domain: str, input_path: Union[str, Path], 
                 output_path: Union[str, Path], paths: Optional[Dict[str, Any]] = None) -> None:
        """Legacy transform method for backward compatibility."""
        try:
            # Load → Process → Save pattern
            data = self.load_data_file(input_path)
            processed_data = self.process(data)
            self.save_data_file(processed_data, output_path)
            
        except Exception as e:
            self.log_error(f"Transform failed for domain {domain}: {e}")
            raise
    
    # ===== ABSTRACT METHOD FOR TOOL-SPECIFIC LOGIC =====
    
    @abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> Any:
        """
        Run the tool. Implement your specific logic here.
        Use the DRY methods above for common operations.
        """
        pass
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.name}: {self.description}"


# ===== LEGACY ALIASES FOR BACKWARD COMPATIBILITY =====
# These maintain compatibility during migration period

BaseComponent = BaseTool
BaseProcessor = BaseTool
BasePipelineStep = BaseTool
BaseEnhancement = BaseTool
DataAnalysisTool = BaseTool
DataComparisonTool = BaseTool
DataProcessorTool = BaseTool


# ===== UTILITY CLASSES (NOT BASE CLASSES) =====

class BaseMainRunner:
    """Utility class for standardized tool execution patterns."""
    
    @staticmethod
    def setup_environment() -> None:
        """Setup execution environment."""
        pass
    
    @staticmethod
    def import_tool(tool_name: str) -> Any:
        """Import a tool class dynamically."""
        try:
            module = __import__(f"scriptcraft.tools.{tool_name}.tool", fromlist=[tool_name])
            return getattr(module, tool_name.title().replace('_', ''))
        except (ImportError, AttributeError) as e:
            raise ImportError(f"Could not import tool {tool_name}: {e}")
    
    @classmethod
    def run(cls, tool_name: str, parse_args_func: Optional[Callable] = None) -> None:
        """Standard main runner for tools."""
        cls.setup_environment()
        
        try:
            tool_class = cls.import_tool(tool_name)
            tool = tool_class()
            
            if parse_args_func:
                args = parse_args_func()
                tool.run(**vars(args))
            else:
                tool.run()
                
        except Exception as e:
            log_and_print(f"❌ Tool execution failed: {e}", level="error")
            sys.exit(1) 