"""Score totals checker for validating calculated score totals against their component values."""

from scripts.common import (
    log_and_print, load_data, 
    find_first_data_file,
)
from scripts.common.core import BaseProcessor
from .utils import calculate_totals_and_compare
from typing import Any

class ScoreTotalsChecker(BaseProcessor):
    """Checker for validating score totals against their component values."""
    
    def __init__(self):
        super().__init__(
            name="Score Totals Checker",
            description="Validates score totals against their component values"
        )
    
    def validate_input(self, input_data: Any) -> bool:
        """Validate input data for the checker."""
        # For this checker, we don't use input_data directly
        # The validation is done internally using filenames
        return True
    
    def check(self, domain: str, input_path: str, output_path: str, paths: dict) -> None:
        """
        Check score totals against their component values.
        
        Args:
            domain: The domain to check (e.g., "Biomarkers", "Clinical")
            input_path: Path to the input data file
            output_path: Path to save the check results
            paths: Dictionary containing path configurations
        
        Returns:
            None
        """
        data_file = find_first_data_file(input_path)

        if not data_file:
            log_and_print(f"❌ No data file found in {input_path}")
            return

        df = load_data(data_file)
        result_df = calculate_totals_and_compare(df, domain)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        result_df.to_csv(output_path, index=False)
        log_and_print(f"✅ Totals comparison saved to: {output_path}")

# Create singleton instance
checker = ScoreTotalsChecker()

def run_score_totals_checker(domain, input_path, output_path, paths):
    """
    Entry point function for the Score Totals Checker.
    
    Args:
        domain: The domain to check
        input_path: Path to the input data file
        output_path: Path to save the check results
        paths: Dictionary containing path configurations
    
    Returns:
        None
    """
    return checker.check(domain, input_path, output_path, paths) 