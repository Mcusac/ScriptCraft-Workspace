# feature_change_checker/tool.py

"""Core implementation of the feature change checker."""

from typing import Dict, Optional, Any
from scripts.common import (
    log_and_print,
    load_data, find_matching_file,
    FILE_PATTERNS
)
from scripts.checkers.feature_change_checker.utils import (
    run_categorized_changes,
    run_between_visit_changes,
)
from scripts.common.core import BaseProcessor

class FeatureChangeChecker(BaseProcessor):
    """Checker for tracking changes in feature values between visits."""
    
    def __init__(self, feature_name: str = "CDX_Cog", categorize: bool = True):
        """
        Initialize the feature change checker.
        
        Args:
            feature_name: Name of the feature to track changes for
            categorize: Whether to categorize changes or just track differences
        """
        super().__init__(
            name="Feature Change Checker",
            description=f"Tracks changes in {feature_name} values between visits"
        )
        self.feature_name = feature_name
        self.categorize = categorize
    
    def validate_input(self, input_data: Any) -> bool:
        """Validate input data for the checker."""
        # For this checker, we don't use input_data directly
        # The validation is done internally using filenames
        return True
    
    def check(self, domain: str, input_path: str, output_path: str, paths: Dict[str, str]) -> None:
        """
        Check feature changes between visits.
        
        Args:
            domain: The domain to check (e.g., "Biomarkers", "Clinical")
            input_path: Not used directly (paths dict is used instead)
            output_path: Not used directly (paths dict is used instead)
            paths: Dictionary containing path configurations
                Required keys:
                - merged_data: Path to merged data directory
                - qc_output: Path to QC output directory
        
        Returns:
            None
            
        Raises:
            FileNotFoundError: If the data file is not found
            KeyError: If required paths are missing
            ValueError: If feature_name is not in the dataset
        """
        if not paths.get("merged_data") or not paths.get("qc_output"):
            raise KeyError("Required paths 'merged_data' and 'qc_output' must be provided")
            
        df_path = find_matching_file(paths["merged_data"], FILE_PATTERNS["clinical_final"])

        if not df_path.exists():
            raise FileNotFoundError(f"Data file not found for {domain}: {df_path}")

        df = load_data(df_path)
        
        if self.feature_name not in df.columns:
            raise ValueError(f"Feature '{self.feature_name}' not found in dataset")

        if self.categorize:
            run_categorized_changes(df, self.feature_name, paths["qc_output"])
        else:
            run_between_visit_changes(df, self.feature_name, paths["qc_output"])

# Create singleton instance with default configuration
checker = FeatureChangeChecker()

def run_feature_change_tracker(domain: str, input_path: str, output_path: str, paths: Dict[str, str]) -> None:
    """
    Entry point function for the Feature Change Checker.
    
    Args:
        domain: The domain to check
        input_path: Not used directly (paths dict is used instead)
        output_path: Not used directly (paths dict is used instead)
        paths: Dictionary containing path configurations
    
    Returns:
        None
    """
    return checker.check(domain, input_path, output_path, paths) 