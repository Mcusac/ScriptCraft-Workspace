"""Unit tests for the release consistency checker."""

import pytest
import pandas as pd
from pathlib import Path
from scripts.checkers.release_consistency_checker import checker
from scripts.checkers.release_consistency_checker.utils import (
    compare_datasets,
    compare_datasets_filtered,
    align_dtypes,
    analyze_column_changes
)

@pytest.fixture
def sample_old_data():
    """Create sample R5 data."""
    return pd.DataFrame({
        "Med_ID": [1, 1, 2],
        "Visit_ID": [1, 2, 1],
        "Value_A": [10, 20, 30],
        "Old_Col": [1, 2, 3]
    })

@pytest.fixture
def sample_new_data():
    """Create sample R6 data."""
    return pd.DataFrame({
        "Med_ID": [1, 1, 2],
        "Visit_ID": [1, 2, 1],
        "Value_A": [10, 25, 30],  # Changed one value
        "New_Col": [4, 5, 6]      # New column
    })

def test_checker_initialization():
    """Test checker initialization."""
    assert checker.name == "Release Consistency Checker"
    assert "releases" in checker.description.lower()

def test_compare_datasets(sample_old_data, sample_new_data, temp_output_dir):
    """Test dataset comparison functionality."""
    compare_datasets(
        sample_old_data,
        sample_new_data,
        "Test_Dataset",
        Path(temp_output_dir)
    )
    result_file = Path(temp_output_dir) / "Test_Dataset_changed_rows.csv"
    assert result_file.exists()
    
def test_align_dtypes():
    """Test dtype alignment functionality."""
    df1 = pd.DataFrame({"A": ["1", "2"], "B": [1, 2]})
    df2 = pd.DataFrame({"A": [1, 2], "B": [1, 2]})
    
    align_dtypes(df1, df2, "Test", ["-9999"])
    assert df1["A"].dtype == df2["A"].dtype

def test_invalid_domain():
    """Test checker behavior with invalid domain."""
    with pytest.raises(ValueError, match="No dataset config found"):
        checker.check("Invalid_Domain", "", "", {})