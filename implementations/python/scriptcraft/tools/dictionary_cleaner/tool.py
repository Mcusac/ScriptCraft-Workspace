"""
Dictionary Cleaner

This transformer standardizes and validates dictionary entries, including normalizing value types,
standardizing expected values, and ensuring consistent formatting across all dictionary fields.
"""

from pathlib import Path
from typing import Optional, Dict, Any
import pandas as pd
from scriptcraft.common.core import BaseTool
from scriptcraft.common.logging import log_and_print


# Standard mappings for value types
VALUE_TYPE_MAP = {
    "numeric": "numeric",
    "number": "numeric",
    "float": "numeric",
    "int": "numeric",
    "integer": "numeric",
    "categorical": "categorical",
    "category": "categorical",
    "text": "text",
    "string": "text",
    "date": "date",
    "datetime": "date",
    "timestamp": "date"
}


class DictionaryCleaner(BaseTool):
    """Transformer for cleaning and standardizing data dictionary entries."""
    
    def __init__(self):
        super().__init__(
            name="Dictionary Cleaner",
            description="Cleans and standardizes data dictionary entries including value types and expected values",
            supported_formats=['.csv', '.xlsx', '.xls']
        )
    
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Process dictionary DataFrame by cleaning and standardizing entries.
        
        Args:
            data: Input dictionary DataFrame
            
        Returns:
            pd.DataFrame: Cleaned dictionary
        """
        return self._clean_dictionary(data)
    
    def run(self, *args, **kwargs):
        """Run method for BaseTool compatibility."""
        # This tool uses the legacy transform/process pattern
        # The run method is provided for BaseTool compatibility
        pass
    
    def transform(self, domain: str, input_path: str, output_path: str, paths: dict) -> None:
        """
        Transform dictionary entries by cleaning and standardizing them.
        Uses the base class implementation with custom processing.
        
        Args:
            domain: The domain to process (e.g., "Biomarkers", "Clinical")
            input_path: Path to the input dictionary file
            output_path: Path to save the cleaned dictionary
            paths: Dictionary containing path configurations
        """
        try:
            input_path = Path(input_path)
            output_path = Path(output_path)
            
            if not input_path.exists():
                self.log_message(f"⚠️ Dictionary file not found: {input_path}")
                return

            # Use base class transform method
            super().transform(domain, input_path, output_path, paths)
            
            self.log_message(f"✅ Cleaned dictionary saved to: {output_path}")
            
        except Exception as e:
            self.log_error(f"Error cleaning dictionary: {e}")
            raise
    
    def _clean_dictionary(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize dictionary entries.
        
        Args:
            df: Input dictionary DataFrame
        
        Returns:
            pd.DataFrame: Cleaned dictionary
        """
        # Clean column names
        df.columns = [col.strip() for col in df.columns]
        
        # Clean and standardize each column
        for col in ["Main Variable", "Value Type", "Expected Values"]:
            if col in df.columns:
                df[col] = df[col].astype(str).apply(lambda x: x.strip())
        
        # Standardize value types
        if "Value Type" in df.columns:
            df["Value Type"] = df["Value Type"].str.lower().map(VALUE_TYPE_MAP).fillna("text")
        
        # Handle expected values based on type
        if "Expected Values" in df.columns:
            df["Expected Values"] = df.apply(self._clean_expected_values, axis=1)
        
        return df
    
    def _clean_expected_values(self, row: pd.Series) -> str:
        """
        Clean and standardize expected values based on value type.
        
        Args:
            row: Dictionary row with Value Type and Expected Values
        
        Returns:
            str: Cleaned expected values
        """
        if pd.isna(row["Expected Values"]):
            return row["Expected Values"]
        
        val_type = row["Value Type"]
        values = str(row["Expected Values"]).strip()
        
        if val_type == "numeric":
            # Standardize numeric ranges
            if "-" in values:
                try:
                    min_val, max_val = map(float, values.split("-"))
                    return f"{min_val}-{max_val}"
                except:
                    return values
            return values
            
        elif val_type == "categorical":
            # Standardize categorical lists
            items = [v.strip() for v in values.split(",")]
            return ", ".join(sorted(set(items)))
            
        elif val_type == "date":
            # Standardize date formats
            if "-" in values:
                try:
                    start, end = map(str.strip, values.split("-"))
                    return f"{start} - {end}"
                except:
                    return values
            return values
            
        return values


# Create singleton instance
cleaner = DictionaryCleaner()

def run_dictionary_cleaner(domain: str, input_path: str, output_path: str, paths: Dict[str, Any]) -> None:
    """
    Entry point function for the Dictionary Cleaner.
    
    Args:
        domain: The domain to process
        input_path: Path to the input dictionary file
        output_path: Path to save the cleaned dictionary
        paths: Dictionary containing path configurations
    
    Returns:
        None
    """
    return cleaner.transform(domain, input_path, output_path, paths) 