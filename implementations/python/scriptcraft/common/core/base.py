"""
Base Classes Module

This module provides a comprehensive hierarchy of base classes for the project:

- BaseComponent: Root base class with common functionality
- BaseProcessor: Abstract base for components that process data
- BasePipelineStep: For pipeline steps
- BaseEnhancement: For data enhancements
- BaseTool: For tools

The hierarchy is designed to maximize code reuse while maintaining clear separation
of concerns and extensibility.
"""

import logging
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Callable
import pandas as pd

from ..io import ensure_output_dir
from ..logging import log_and_print
from .registry import register_step, register_tool


@dataclass
class BaseComponent(ABC):
    """Base class for all components."""
    name: str
    description: str = ""
    config: Dict[str, Any] = field(default_factory=dict)
    logger: Optional[logging.Logger] = None
    
    def __post_init__(self):
        """Initialize component."""
        if not self.logger:
            self.logger = logging.getLogger(self.name)
    
    @abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Run the component."""
        pass


@dataclass
class BaseProcessor(BaseComponent):
    """Base class for data processors."""
    input_dir: Optional[Path] = None
    output_dir: Optional[Path] = None
    
    def __post_init__(self):
        """Initialize processor."""
        super().__post_init__()
        if self.output_dir:
            ensure_output_dir(self.output_dir)
    
    def process(self, data: Any) -> Any:
        """Process the data."""
        raise NotImplementedError("Subclasses must implement process()")
    
    def run(self, data: Any) -> Any:
        """Run the processor."""
        self.logger.info(f"Running processor: {self.name}")
        try:
            result = self.process(data)
            self.logger.info(f"Processor {self.name} completed successfully")
            return result
        except Exception as e:
            self.logger.error(f"Processor {self.name} failed: {str(e)}")
            raise


@dataclass
class BasePipelineStep(BaseProcessor):
    """Base class for pipeline steps."""
    def __post_init__(self):
        """Initialize step."""
        super().__post_init__()
        register_step(self.name, self)
    
    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process the data."""
        pass


@dataclass
class BaseEnhancement(BaseProcessor):
    """Base class for enhancements."""
    def __post_init__(self):
        """Initialize enhancement."""
        super().__post_init__()
        register_step(self.name, self)
    
    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process the data."""
        pass


@dataclass
class BaseTool(BaseComponent):
    """Base class for tools."""
    def __post_init__(self):
        """Initialize tool."""
        super().__post_init__()
        register_tool(self.name, self)
    
    @abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Run the tool."""
        pass


class BaseComponent(ABC):
    """Root base class for all components."""
    
    def __init__(self, name: str, description: str):
        """
        Initialize base component.
        
        Args:
            name: Component name
            description: Component description
        """
        self.name = name
        self.description = description
    
    def log_message(self, message: str, level: str = "info") -> None:
        """
        Log a message with component name prefix.
        
        Args:
            message: Message to log
            level: Log level (info, warning, error)
        """
        prefix = f"[{self.name}] "
        log_and_print(prefix + message, level=level)
    
    def log_start(self) -> None:
        """Log component start."""
        self.log_message(f"🚀 Starting {self.name}...")
    
    def log_completion(self, output_path: Optional[Path] = None) -> None:
        """
        Log component completion.
        
        Args:
            output_path: Optional path to output file
        """
        msg = f"✅ {self.name} completed successfully"
        if output_path:
            msg += f"\n📄 Output saved to: {output_path}"
        self.log_message(msg)
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.name} ({self.description})"


class BaseProcessor(BaseComponent):
    """Base class for components that process data."""
    
    @abstractmethod
    def validate_input(self, input_data: Any) -> bool:
        """
        Validate input data.
        
        Args:
            input_data: Data to validate
        
        Returns:
            bool: True if valid, False otherwise
        """
        pass
    
    def save_output(self,
                   data: pd.DataFrame,
                   output_path: Path,
                   index: bool = False) -> None:
        """
        Save processed data to file.
        
        Args:
            data: Data to save
            output_path: Path to save to
            index: Whether to include index
        """
        ensure_output_dir(output_path.parent)
        
        if output_path.suffix.lower() == '.csv':
            data.to_csv(output_path, index=index)
        else:
            data.to_excel(output_path, index=index)
        
        self.log_message(f"✅ Data saved to: {output_path}")
        self.log_message(f"📊 Output shape: {data.shape}")


class BasePipelineStep(BaseProcessor):
    """Base class for pipeline steps."""
    
    def __init__(self,
                 name: str,
                 description: str,
                 input_key: str = "raw_data",
                 run_mode: str = "domain",
                 tags: List[str] = None,
                 check_exists: bool = True):
        """
        Initialize pipeline step.
        
        Args:
            name: Step name
            description: Step description
            input_key: Key for input data in paths dict
            run_mode: Step run mode
            tags: Step tags
            check_exists: Whether to check file existence
        """
        super().__init__(name=name, description=description)
        self.input_key = input_key
        self.run_mode = run_mode
        self.tags = tags or []
        self.check_exists = check_exists
        
        # Auto-register step
        register_step(
            name=name,
            tags=self.tags,
            input_key=input_key,
            run_mode=run_mode,
            check_exists=check_exists
        )(self.run)
    
    @abstractmethod
    def process(self,
                input_path: Path,
                output_path: Path,
                domain: Optional[str] = None,
                **kwargs) -> bool:
        """
        Process step data.
        
        Args:
            input_path: Path to input data
            output_path: Path for output
            domain: Optional domain context
            **kwargs: Additional parameters
        
        Returns:
            bool: Success status
        """
        pass
    
    def run(self,
            domain: Optional[str] = None,
            input_path: Optional[Path] = None,
            output_path: Optional[Path] = None,
            paths: Optional[Dict[str, Path]] = None,
            **kwargs) -> bool:
        """
        Run the pipeline step.
        
        Args:
            domain: Optional domain context
            input_path: Path to input data
            output_path: Path for output
            paths: Dictionary of paths
            **kwargs: Additional parameters
        
        Returns:
            bool: Success status
        """
        try:
            # Input validation
            if input_path is None and paths:
                input_path = paths.get(self.input_key)
            if input_path is None:
                self.log_message(f"❌ No input path provided", level="error")
                return False
            
            if not self.validate_input(input_path):
                self.log_message(f"❌ Input validation failed", level="error")
                return False
            
            # Process data
            success = self.process(
                input_path=input_path,
                output_path=output_path or (paths and paths.get("qc_output")),
                domain=domain,
                **kwargs
            )
            
            if success:
                self.log_completion()
            else:
                self.log_message("❌ Processing failed", level="error")
            
            return success
            
        except Exception as e:
            self.log_message(f"❌ Error: {str(e)}", level="error")
            return False


class BaseEnhancement(BaseProcessor):
    """Base class for data enhancements."""
    
    @abstractmethod
    def enhance(self,
                input_data: Union[pd.DataFrame, Dict[str, pd.DataFrame]],
                **kwargs) -> pd.DataFrame:
        """
        Apply enhancement to input data.
        
        Args:
            input_data: Data to enhance
            **kwargs: Enhancement parameters
        
        Returns:
            Enhanced DataFrame
        """
        pass
    
    def validate_input(self, input_data: Union[pd.DataFrame, Dict[str, pd.DataFrame]]) -> bool:
        """
        Validate enhancement input.
        
        Args:
            input_data: Data to validate
        
        Returns:
            bool: True if valid, False otherwise
        """
        if isinstance(input_data, pd.DataFrame):
            return not input_data.empty
        elif isinstance(input_data, dict):
            return all(isinstance(df, pd.DataFrame) and not df.empty 
                      for df in input_data.values())
        return False


class BaseTool(BaseComponent):
    """Base class for tools."""
    
    @staticmethod
    def is_distributable_environment() -> bool:
        """
        Detect if we're running in a distributable environment.
        DRY method for environment detection across all tools.
        
        Returns:
            bool: True if in distributable environment, False if in development
        """
        current_dir = Path.cwd()
        return (current_dir.name == 'scripts' or 
                'distributable' in str(current_dir).lower())
    
    def resolve_input_directory(self, **kwargs) -> Path:
        """
        Resolve input directory path for both development and distributable environments.
        This is the DRY method all tools should use for input directory resolution.
        
        Args:
            **kwargs: Additional arguments that may contain:
                - input_dir: Explicit input directory path
                - config: Configuration object
                
        Returns:
            Path: Resolved input directory path
        """
        # Priority: kwargs input_dir -> config paths -> environment-based defaults
        if 'input_dir' in kwargs:
            return Path(kwargs['input_dir'])
        
        # Extract config from kwargs if provided
        config = kwargs.get('config')
        if config and hasattr(config, 'paths') and hasattr(config.paths, 'input_dir'):
            return Path(config.paths.input_dir)
        
        # Environment-based path resolution using DRY method
        if self.is_distributable_environment():
            current_dir = Path.cwd()
            # If running from scripts/ subdirectory, input is at parent level
            if current_dir.name == 'scripts':
                return current_dir.parent / "input"
            # Otherwise, input is at current level
            else:
                return current_dir / "input"
        else:
            # In development: input is relative to working directory
            return Path("input")
    
    def validate_inputs(self, input_paths: List[Union[str, Path]]) -> bool:
        """
        Validate tool input paths.
        
        Args:
            input_paths: Paths to validate
        
        Returns:
            bool: True if all valid, False otherwise
        """
        if not input_paths:
            self.log_message("❌ No input paths provided", level="error")
            return False
            
        for path in input_paths:
            path = Path(path)
            if not path.exists():
                self.log_message(f"❌ Input file not found: {path}", level="error")
                return False
        return True
    
    @abstractmethod
    def run(self,
            mode: Optional[str] = None,
            input_paths: Optional[List[Union[str, Path]]] = None,
            output_dir: Optional[Union[str, Path]] = None,
            domain: Optional[str] = None,
            output_filename: Optional[str] = None,
            **kwargs) -> None:
        """
        Run the tool.
        
        Args:
            mode: Operating mode
            input_paths: Input file paths
            output_dir: Output directory
            domain: Domain context
            output_filename: Output filename
            **kwargs: Tool parameters
        """
        pass 


class BaseMainRunner:
    """Base class for main script runners."""
    
    @staticmethod
    def setup_environment() -> None:
        """Set up the Python path for both dev and distributable environments."""
        if __package__ is None:
            # Running as script, add parent to path
            file = Path(__file__).resolve()
            parent = file.parent.parent.parent
            sys.path.append(str(parent))
    
    @staticmethod
    def import_tool(tool_name: str) -> Any:
        """Import the tool module in either environment."""
        try:
            # Try development path first
            tool_module = __import__(f'scripts.tools.{tool_name}', fromlist=['tool'])
            return getattr(tool_module, 'tool')
        except ImportError:
            try:
                # Fallback for distributable environment  
                tool_module = __import__('tool', fromlist=['tool'])
                return getattr(tool_module, 'tool')
            except ImportError as e:
                raise ImportError(f"Could not import tool {tool_name}: {e}")
    
    @classmethod
    def run(cls, tool_name: str, parse_args_func: Optional[Callable] = None) -> None:
        """
        Run the tool with proper environment setup.
        
        Args:
            tool_name: Name of the tool to run
            parse_args_func: Optional function to parse command line args
        """
        cls.setup_environment()
        tool = cls.import_tool(tool_name)
        
        if parse_args_func:
            args = parse_args_func()
            tool.run_from_cli(args)
        else:
            tool.run() 