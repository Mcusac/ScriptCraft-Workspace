"""
Dictionary Validator

This validator checks consistency between dataset columns and dictionary columns.
"""

from scriptcraft.common import (
    log_and_print, load_dataset_columns, load_dictionary_columns,
    create_standard_tool, create_runner_function
)
from .utils import compare_columns


def validate_dictionary_columns(domain: str, dataset_file, dictionary_file, output_path: str, paths: dict) -> None:
    """
    Validate dataset columns against dictionary columns.
    
    Args:
        domain: The domain to validate
        dataset_file: Path to dataset file
        dictionary_file: Path to dictionary file
        output_path: Not used (results are logged)
        paths: Dictionary containing path configurations
    
    Returns:
        None
    """
    log_and_print(f"🔍 Validating {dataset_file.name} against {dictionary_file.name}...\n")

    # Load and compare columns
    dataset_columns = load_dataset_columns(dataset_file)
    dictionary_columns = load_dictionary_columns(dictionary_file)
    comparison = compare_columns(dataset_columns, dictionary_columns)

    # Log results
    log_and_print(f"✅ Columns in both: {len(comparison['in_both'])}")
    log_and_print(f"❌ Only in dataset ({len(comparison['only_in_dataset'])}): {comparison['only_in_dataset']}")
    log_and_print(f"❌ Only in dictionary ({len(comparison['only_in_dictionary'])}): {comparison['only_in_dictionary']}")
    log_and_print(f"🔄 Case mismatches ({len(comparison['case_mismatches'])}): {comparison['case_mismatches']}\n")


# Create tool using consolidated pattern
DictionaryValidator = create_standard_tool(
    'validation',
    'Dictionary Validator',
    'Validates consistency between dataset columns and dictionary columns',
    validate_dictionary_columns,
    requires_dictionary=True
)

# Create runner function
run_dictionary_validator = create_runner_function(DictionaryValidator) 