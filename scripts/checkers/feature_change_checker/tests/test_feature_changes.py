"""Tests for the feature change checker."""

import pytest
import pandas as pd
from pathlib import Path
from scripts.checkers.feature_change_checker.tool import FeatureChangeChecker

@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return pd.DataFrame({
        "Med_ID": [1, 1, 2, 2],
        "Visit_ID": [1, 2, 1, 2],
        "CDX_Cog": [0, 1, 1, 2]
    })

@pytest.fixture
def temp_output_dir(tmp_path):
    """Create temporary output directory."""
    return tmp_path / "output"

def test_checker_initialization():
    """Test checker initialization with custom parameters."""
    checker = FeatureChangeChecker(feature_name="Test_Feature", categorize=False)
    assert checker.feature_name == "Test_Feature"
    assert not checker.categorize

def test_checker_missing_feature():
    """Test checker behavior with missing feature."""
    checker = FeatureChangeChecker(feature_name="NonExistent")
    with pytest.raises(ValueError, match="Feature 'NonExistent' not found in dataset"):
        checker.check("Clinical", "", "", {
            "merged_data": "path",
            "qc_output": "path"
        })

def test_checker_missing_paths():
    """Test checker behavior with missing paths."""
    checker = FeatureChangeChecker()
    with pytest.raises(KeyError, match="Required paths.*must be provided"):
        checker.check("Clinical", "", "", {})