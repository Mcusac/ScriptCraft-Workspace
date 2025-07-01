"""
Score Totals Checker

This checker validates that calculated totals match expected totals in datasets.
"""

from scriptcraft.common import (
    log_and_print, load_dataset_columns, load_dictionary_columns,
    create_standard_tool, create_runner_function
)
from .utils import calculate_totals_and_compare
import pandas as pd


def check_score_totals(dataset_file, dictionary_file, domain: str) -> pd.DataFrame:
    """
    Check calculated totals against expected totals.
    
    Args:
        dataset_file: Path to dataset file
        dictionary_file: Path to dictionary file
        domain: The domain to check
        
    Returns:
        DataFrame with comparison results
    """
    log_and_print(f"🔍 Checking totals in {dataset_file.name} against {dictionary_file.name}...\n")

    # Load and process data
    dataset_columns = load_dataset_columns(dataset_file)
    dictionary_columns = load_dictionary_columns(dictionary_file)
    results = calculate_totals_and_compare(dataset_columns, dictionary_columns, domain)
    
    return results


# Create tool using consolidated pattern
ScoreTotalsChecker = create_standard_tool(
    'checker',
    'Score Totals Checker',
    'Validates that calculated totals match expected totals in datasets',
    check_score_totals,
    requires_dictionary=True
)

# Create runner function
run_score_totals_checker = create_runner_function(ScoreTotalsChecker) 