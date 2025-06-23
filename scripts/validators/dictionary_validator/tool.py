"""
Dictionary Validator

This validator checks consistency between dataset columns and dictionary columns.
"""

from scripts.common import (
    log_and_print, find_matching_file,
    load_dataset_columns, load_dictionary_columns,
    find_latest_file,
    FILE_PATTERNS,
)
from scripts.common.core import BaseProcessor
from .utils import compare_columns
from typing import Any


class DictionaryValidator(BaseProcessor):
    """Validator for checking consistency between dataset columns and dictionary columns."""
    
    def __init__(self):
        super().__init__(
            name="Dictionary Validator",
            description="Validates consistency between dataset columns and dictionary columns"
        )
    
    def validate_input(self, input_data: Any) -> bool:
        """Validate input data for the validator."""
        # For this validator, we don't use input_data directly
        # The validation is done internally using filenames
        return True
    
    def validate(self, domain: str, input_path: str, output_path: str, paths: dict) -> None:
        """
        Validate dataset columns against dictionary columns.
        
        Args:
            domain: The domain to validate (e.g., "Biomarkers", "Clinical")
            input_path: Not used directly (paths dict is used instead)
            output_path: Not used (results are logged)
            paths: Dictionary containing path configurations
        
        Returns:
            None
        """
        # dataset_file = find_matching_file(paths["old_data"], FILE_PATTERNS["final_csv"])
        dataset_file = find_latest_file(paths["merged"])

        # Try cleaned dictionary first
        dictionary_file = find_matching_file(paths["dictionary"], FILE_PATTERNS["cleaned_dict"])

        # Fallback to release dictionary if cleaned doesn't exist
        if not dictionary_file:
            dictionary_file = find_matching_file(paths["dictionary"], FILE_PATTERNS["release_dict"])
            if dictionary_file:
                log_and_print("🟡 Using fallback release dictionary (cleaned version not found).")

        log_and_print(f"\n🚀 Starting validation for **{domain}**")

        if not dataset_file:
            log_and_print("⚠️ No dataset file found.")
            return
        if not dictionary_file:
            log_and_print("⚠️ No dictionary file found.")
            return

        log_and_print(f"📂 Dataset in use: {dataset_file}")
        log_and_print(f"📂 Dictionary in use: {dictionary_file}")
        log_and_print(f"🔍 Validating {dataset_file.name} against {dictionary_file.name}...\n")

        dataset_columns = load_dataset_columns(dataset_file)
        dictionary_columns = load_dictionary_columns(dictionary_file)

        comparison = compare_columns(dataset_columns, dictionary_columns)

        log_and_print(f"✅ Columns in both: {len(comparison['in_both'])}")
        log_and_print(f"❌ Only in dataset ({len(comparison['only_in_dataset'])}): {comparison['only_in_dataset']}")
        log_and_print(f"❌ Only in dictionary ({len(comparison['only_in_dictionary'])}): {comparison['only_in_dictionary']}")
        log_and_print(f"🔄 Case mismatches ({len(comparison['case_mismatches'])}): {comparison['case_mismatches']}\n")


# Create singleton instance
validator = DictionaryValidator()

def run_dictionary_validator(domain, input_path, output_path, paths):
    """
    Entry point function for the Dictionary Validator.
    
    Args:
        domain: The domain to validate
        input_path: Not used directly (paths dict is used instead)
        output_path: Not used (results are logged)
        paths: Dictionary containing path configurations
    
    Returns:
        None
    """
    return validator.validate(domain, input_path, output_path, paths) 