"""
Data processing patterns and utilities.

This module consolidates common data processing patterns used across tools,
including data loading, validation, transformation, and saving operations.
"""

import pandas as pd
from pathlib import Path
from typing import Union, List, Dict, Any, Optional, Callable, Tuple
from ..logging import log_and_print
from ..io import load_data, ensure_output_dir, find_latest_file, find_matching_file, FILE_PATTERNS


def setup_tool_files(paths: Dict[str, Any], domain: str, tool_name: str) -> Tuple[Optional[Path], Optional[Path]]:
    """
    Common pattern for setting up dataset and dictionary files for tools.
    
    This consolidates the duplicated pattern of:
    - Finding the latest dataset file
    - Finding dictionary file (cleaned first, fallback to release)
    - Logging file usage
    - Validating file existence
    
    Args:
        paths: Path configuration dictionary
        domain: Domain being processed
        tool_name: Name of the tool for logging
        
    Returns:
        Tuple of (dataset_file, dictionary_file) or (None, None) if files not found
    """
    # Find dataset file
    dataset_file = find_latest_file(paths["merged"])
    
    # Try cleaned dictionary first, fallback to release dictionary
    dictionary_file = find_matching_file(paths["dictionary"], FILE_PATTERNS["cleaned_dict"])
    
    if not dictionary_file:
        dictionary_file = find_matching_file(paths["dictionary"], FILE_PATTERNS["release_dict"])
        if dictionary_file:
            log_and_print("🟡 Using fallback release dictionary (cleaned version not found).")
    
    # Log start
    log_and_print(f"\n🚀 Starting {tool_name} for **{domain}**")
    
    # Validate files exist
    if not dataset_file:
        log_and_print("⚠️ No dataset file found.")
        return None, None
    if not dictionary_file:
        log_and_print("⚠️ No dictionary file found.")
        return None, None
    
    # Log file usage
    log_and_print(f"📂 Dataset in use: {dataset_file}")
    log_and_print(f"📂 Dictionary in use: {dictionary_file}")
    
    return dataset_file, dictionary_file


def load_and_validate_data(input_paths: Union[str, Path, List[Union[str, Path]]], 
                          required_columns: Optional[List[str]] = None) -> Union[pd.DataFrame, List[pd.DataFrame]]:
    """
    Load and validate data from input paths.
    
    Args:
        input_paths: Single path or list of paths to load
        required_columns: Optional list of required columns
        
    Returns:
        Loaded DataFrame(s)
    """
    if isinstance(input_paths, (str, Path)):
        input_paths = [input_paths]
    
    dataframes = []
    for path in input_paths:
        try:
            df = load_data(path)
            if df is not None:
                # Basic validation
                if required_columns:
                    missing = set(required_columns) - set(df.columns)
                    if missing:
                        log_and_print(f"⚠️ Missing required columns in {path}: {missing}")
                
                dataframes.append(df)
                log_and_print(f"✅ Loaded {path.name}: {df.shape[0]} rows, {df.shape[1]} columns")
            else:
                log_and_print(f"⚠️ Failed to load {path}")
        except Exception as e:
            log_and_print(f"❌ Error loading {path}: {e}")
    
    return dataframes[0] if len(dataframes) == 1 else dataframes


def save_data(data: pd.DataFrame, output_path: Union[str, Path], format: str = 'excel') -> Path:
    """
    Save data to output path with standard formatting.
    
    Args:
        data: DataFrame to save
        output_path: Path to save the data
        format: Output format ('excel' or 'csv')
        
    Returns:
        Path to saved file
    """
    output_path = Path(output_path)
    ensure_output_dir(output_path.parent)
    
    if format.lower() == 'excel':
        data.to_excel(output_path, index=False)
    else:
        data.to_csv(output_path, index=False)
    
    log_and_print(f"💾 Saved data to: {output_path}")
    return output_path


def standardize_tool_execution(
    tool_class,
    domain: str,
    input_path: str,
    output_path: str,
    paths: Dict[str, Any],
    **kwargs
) -> None:
    """
    Standardized tool execution pattern.
    
    This function provides a consistent execution pattern for tools
    that follow the domain/input/output/paths pattern.
    
    Args:
        tool_class: Tool class to instantiate and run
        domain: Domain to process
        input_path: Input file path
        output_path: Output file path
        paths: Path configuration dictionary
        **kwargs: Additional arguments for tool execution
    """
    try:
        # Create tool instance
        tool = tool_class()
        
        # Log start
        log_and_print(f"🚀 Starting {tool.name} for {domain}")
        log_and_print(f"📂 Input: {input_path}")
        log_and_print(f"📂 Output: {output_path}")
        
        # Execute tool
        if hasattr(tool, 'check'):
            tool.check(domain, input_path, output_path, paths, **kwargs)
        elif hasattr(tool, 'validate'):
            tool.validate(domain, input_path, output_path, paths, **kwargs)
        elif hasattr(tool, 'transform'):
            tool.transform(domain, input_path, output_path, paths, **kwargs)
        elif hasattr(tool, 'run'):
            tool.run(domain=domain, input_path=input_path, output_path=output_path, paths=paths, **kwargs)
        else:
            raise AttributeError(f"Tool {tool_class.__name__} has no recognized execution method")
        
        # Log completion
        log_and_print(f"✅ Completed {tool.name} for {domain}")
        
    except Exception as e:
        log_and_print(f"❌ Error in {tool_class.__name__} for {domain}: {e}")
        raise


def create_tool_runner(tool_class, **default_kwargs):
    """
    Create a standardized tool runner function.
    
    Args:
        tool_class: Tool class to create runner for
        **default_kwargs: Default arguments for the tool
        
    Returns:
        Function that can be used as a tool runner
    """
    def runner(domain: str, input_path: str, output_path: str, paths: dict, **kwargs):
        """Standardized tool runner function."""
        # Merge default kwargs with provided kwargs
        execution_kwargs = {**default_kwargs, **kwargs}
        standardize_tool_execution(tool_class, domain, input_path, output_path, paths, **execution_kwargs)
    
    return runner


# Convenience functions for common patterns
def load_and_process_data(
    input_paths: Union[str, Path, List[Union[str, Path]]],
    process_func: Callable,
    output_path: Union[str, Path],
    **kwargs
) -> pd.DataFrame:
    """
    Load data, apply processing function, and save result.
    
    Args:
        input_paths: Input file path(s)
        process_func: Function to process the data
        output_path: Path to save processed data
        **kwargs: Additional arguments for processing
        
    Returns:
        Processed DataFrame
    """
    processor = DataProcessor()
    data = processor.load_and_validate(input_paths)
    return processor.process_and_save(data, output_path, process_func, **kwargs)


def validate_and_transform_data(
    data: pd.DataFrame,
    validation_rules: Dict[str, Any],
    transform_func: Optional[Callable] = None,
    **kwargs
) -> pd.DataFrame:
    """
    Validate data against rules and optionally transform.
    
    Args:
        data: DataFrame to validate and transform
        validation_rules: Rules to validate against
        transform_func: Optional transformation function
        **kwargs: Additional arguments
        
    Returns:
        Validated and optionally transformed DataFrame
    """
    # Apply validation rules
    for rule_name, rule_config in validation_rules.items():
        # This is a placeholder for validation logic
        # In a real implementation, you would apply the specific rules
        pass
    
    # Apply transformation if provided
    if transform_func:
        data = transform_func(data, **kwargs)
    
    return data 