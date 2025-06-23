"""
Utility functions for dataset comparison.
"""

import pandas as pd
from typing import Dict, List, Set, Tuple, Optional
from .comparison_core import DataFrameComparer, ComparisonResult

def compare_dataframes(
    old_df: pd.DataFrame,
    new_df: pd.DataFrame,
    key_columns: List[str],
    compare_columns: Optional[List[str]] = None
) -> ComparisonResult:
    """Compare two DataFrames and return the differences.
    
    Args:
        old_df: Old version of the DataFrame
        new_df: New version of the DataFrame
        key_columns: Columns that uniquely identify rows
        compare_columns: Columns to compare (defaults to all non-key columns)
    
    Returns:
        ComparisonResult containing all changes
    """
    comparer = DataFrameComparer(old_df, new_df, key_columns, compare_columns)
    return comparer.compare()

def get_common_columns(
    df1: pd.DataFrame,
    df2: pd.DataFrame
) -> List[str]:
    """Get columns common to both DataFrames.
    
    Args:
        df1: First DataFrame
        df2: Second DataFrame
    
    Returns:
        List of common column names
    """
    return list(set(df1.columns) & set(df2.columns))

def compare_column_dtypes(
    df1: pd.DataFrame,
    df2: pd.DataFrame
) -> Dict[str, Tuple[str, str]]:
    """Compare data types of columns between DataFrames.
    
    Args:
        df1: First DataFrame
        df2: Second DataFrame
    
    Returns:
        Dictionary mapping column names to tuples of (df1_dtype, df2_dtype)
    """
    common_cols = get_common_columns(df1, df2)
    return {
        col: (str(df1[col].dtype), str(df2[col].dtype))
        for col in common_cols
        if df1[col].dtype != df2[col].dtype
    }

def find_duplicate_rows(
    df: pd.DataFrame,
    key_columns: List[str]
) -> pd.DataFrame:
    """Find duplicate rows based on key columns.
    
    Args:
        df: DataFrame to check
        key_columns: Columns that should be unique
    
    Returns:
        DataFrame containing duplicate rows
    """
    duplicates = df[df.duplicated(subset=key_columns, keep=False)]
    return duplicates.sort_values(key_columns)

def drop_empty_columns(
    df: pd.DataFrame,
    threshold: float = 0.95
) -> pd.DataFrame:
    """Drop columns that are mostly empty.
    
    Args:
        df: DataFrame to process
        threshold: Minimum fraction of non-null values required
    
    Returns:
        DataFrame with empty columns removed
    """
    null_fractions = df.isnull().mean()
    return df.loc[:, null_fractions < (1 - threshold)] 