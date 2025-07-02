"""
Data loading operations for various file formats.
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Union, List, Dict, Any
import json
import yaml

def load_data(
    file_path: Union[str, Path],
    encoding: Optional[str] = None,
    **kwargs: Any
) -> pd.DataFrame:
    """Load data from a file into a DataFrame.
    
    Args:
        file_path: Path to the data file
        encoding: File encoding to use
        **kwargs: Additional arguments for pd.read_csv
    
    Returns:
        Loaded DataFrame
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if file_path.suffix.lower() == '.csv':
        return pd.read_csv(file_path, encoding=encoding, **kwargs)
    elif file_path.suffix.lower() in ['.xlsx', '.xls']:
        return pd.read_excel(file_path, **kwargs)
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")

def load_datasets_as_dict(
    file_paths: List[Union[str, Path]],
    encoding: Optional[str] = None,
    **kwargs: Any
) -> Dict[str, pd.DataFrame]:
    """Load multiple datasets from files.
    
    Args:
        file_paths: List of paths to data files
        encoding: File encoding to use
        **kwargs: Additional arguments for load_data
    
    Returns:
        Dictionary mapping file names to DataFrames
    """
    return {
        Path(fp).stem: load_data(fp, encoding, **kwargs)
        for fp in file_paths
    }

def load_dataset_columns(
    file_path: Union[str, Path],
    columns: List[str],
    encoding: Optional[str] = None,
    **kwargs: Any
) -> pd.DataFrame:
    """Load specific columns from a dataset.
    
    Args:
        file_path: Path to the data file
        columns: List of column names to load
        encoding: File encoding to use
        **kwargs: Additional arguments for load_data
    
    Returns:
        DataFrame with specified columns
    """
    return load_data(file_path, encoding, usecols=columns, **kwargs)

def load_dictionary_columns(
    file_path: Union[str, Path],
    encoding: Optional[str] = None,
    **kwargs: Any
) -> pd.DataFrame:
    """Load dictionary columns from a file.
    
    Args:
        file_path: Path to the dictionary file
        encoding: File encoding to use
        **kwargs: Additional arguments for load_data
    
    Returns:
        DataFrame with dictionary columns
    """
    return load_data(file_path, encoding, **kwargs)

def load_comparison_datasets(
    file_paths: List[Union[str, Path]],
    encoding: Optional[str] = None,
    **kwargs: Any
) -> Dict[str, pd.DataFrame]:
    """Load datasets for comparison.
    
    Args:
        file_paths: List of paths to data files
        encoding: File encoding to use
        **kwargs: Additional arguments for load_data
    
    Returns:
        Dictionary mapping file names to DataFrames
    """
    return load_datasets_as_dict(file_paths, encoding, **kwargs)

def load_json(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Load data from a JSON file.
    
    Args:
        file_path: Path to the JSON file
    
    Returns:
        Loaded JSON data
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
        if isinstance(data, dict):
            return data
        else:
            return {"data": data}

def load_yaml(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Load data from a YAML file.
    
    Args:
        file_path: Path to the YAML file
    
    Returns:
        Loaded YAML data
    """
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
        if isinstance(data, dict):
            return data
        else:
            return {"data": data} 