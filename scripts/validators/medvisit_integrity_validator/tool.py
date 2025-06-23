"""
MedVisit Integrity Validator

This validator checks Med_ID and Visit_ID integrity between old and new datasets.
"""

import pandas as pd
from scripts.common import (
    log_and_print,
    load_datasets,
    standardize_columns,
    ensure_output_dir,
    compare_dataframes,
)
from scripts.common.core import BaseProcessor
from typing import Any


FILENAME_MAP = {
    "Biomarkers": {
        "old": "HD Release 6 Biomarkers_FINAL.csv",
        "new": "HD6 + New data_Biomarkers---MatthewReviewPending.xlsx"
    },
    # "Clinical": {
    #     "old": "HD Release 6 Clinical_FINAL.csv",
    #     "new": "HD6 + New data_Clinical---Review.xlsx"
    # },
    # Add Genomics/Imaging when ready
}


class MedVisitIntegrityValidator(BaseProcessor):
    """Validator for checking Med_ID and Visit_ID integrity between old and new datasets."""
    
    def __init__(self):
        super().__init__(
            name="MedVisit Integrity Validator",
            description="Validates the integrity of Med_ID and Visit_ID combinations between datasets"
        )
    
    def validate_input(self, input_data: Any) -> bool:
        """Validate input data for the validator."""
        # For this validator, we don't use input_data directly
        # The validation is done internally using filenames
        return True
    
    def validate(self, domain: str, input_path: str, output_path: str, paths: dict) -> None:
        """
        Validate Med_ID and Visit_ID integrity between old and new datasets.
        
        Args:
            domain: The domain to validate (e.g., "Biomarkers", "Clinical")
            input_path: Not used in this validator
            output_path: Path to save the validation results
            paths: Dictionary containing path configurations
        
        Returns:
            None
        """
        filenames = FILENAME_MAP.get(domain)
        if not filenames:
            log_and_print(f"⏩ Skipping {domain} — no file mapping found.")
            return

        df_old, df_new = load_datasets(
            old_filename=filenames["old"],
            new_filename=filenames["new"],
            data_dir=domain,
            mode="standard"
        )

        df_new = standardize_columns(df_new, {"Visit": "Visit_ID", "Med ID": "Med_ID"})
        
        # Use compare_dataframes with med_ids step to check Med/Visit ID integrity
        comparison_result = compare_dataframes(
            df_old, 
            df_new, 
            dataset_name=domain,
            steps=["med_ids"]
        )
        
        # Extract missing IDs from the comparison result
        missing_in_new, missing_in_old = comparison_result.missing_ids or (pd.DataFrame(), pd.DataFrame())

        ensure_output_dir(output_path)
        with pd.ExcelWriter(output_path) as writer:
            missing_in_new.to_excel(writer, sheet_name="Missing in New", index=False)
            missing_in_old.to_excel(writer, sheet_name="Missing in Old", index=False)

        log_and_print(f"🔍 Combos missing in new dataset: {len(missing_in_new)}")
        log_and_print(f"🔍 Combos missing in old dataset: {len(missing_in_old)}")
        log_and_print(f"✅ Comparison saved to: {output_path}")


# Create singleton instance
validator = MedVisitIntegrityValidator()

def run_medvisit_integrity_validator(domain, input_path, output_path, paths):
    """
    Entry point function for the MedVisit Integrity Validator.
    
    Args:
        domain: The domain to validate
        input_path: Not used in this validator
        output_path: Path to save validation results
        paths: Dictionary containing path configurations
    
    Returns:
        None
    """
    return validator.validate(domain, input_path, output_path, paths) 