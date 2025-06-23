"""Core implementation of the release consistency checker."""

from pathlib import Path
import traceback
from typing import Dict, Optional, Any

import scripts.common as cu
from scripts.common.core import BaseProcessor
from .utils import monitor_changes, DATASETS

class ReleaseConsistencyChecker(BaseProcessor):
    """Checker for validating consistency between different data releases."""
    
    def __init__(self):
        """Initialize the release consistency checker."""
        super().__init__(
            name="Release Consistency Checker",
            description="Validates consistency between different data releases"
        )
    
    def validate_input(self, input_data: Any) -> bool:
        """Validate input data for the checker."""
        # For this checker, we don't use input_data directly
        # The validation is done internally using filenames
        return True
    
    def check(self, domain: str, input_path: str, output_path: str, paths: Dict[str, str]) -> None:
        """
        Check consistency between data releases.
        
        Args:
            domain: The domain to check (e.g., "Biomarkers", "Clinical")
            input_path: Not used directly (dataset config is used instead)
            output_path: Not used directly (dataset config is used instead)
            paths: Dictionary containing path configurations
        
        Returns:
            None
            
        Raises:
            ValueError: If no dataset configuration is found for the domain
            FileNotFoundError: If required data files are not found
        """
        dataset_config = next((d for d in DATASETS if d["dataset_name"] == domain), None)
        if not dataset_config:
            raise ValueError(f"No dataset config found for {domain}")

        base_path = Path("domains")
        dataset_config["data_dir"] = str(base_path / domain)
        
        resolved_path = Path(dataset_config["data_dir"])
        cu.log_and_print(f"🔍 Looking for data in: {resolved_path}")

        try:
            monitor_changes(**dataset_config)
        except Exception as e:
            cu.log_and_print(f"❌ Error while processing {domain}: {e}")
            cu.log_and_print(traceback.format_exc())
            raise
    
    def check_manual(
        self,
        r5_filename: str,
        r6_filename: str,
        debug: bool = False,
        mode: str = "old_only"
    ) -> None:
        """
        Run manual check between two specific files.
        
        Args:
            r5_filename: Path to R5 file
            r6_filename: Path to R6 file
            debug: Enable debug mode for dtype checks
            mode: Comparison mode ('old_only' or 'standard')
        
        Returns:
            None
            
        Raises:
            FileNotFoundError: If either input file is not found
            ValueError: If files have incompatible formats
        """
        monitor_changes(
            dataset_name="Manual_Run",
            r5_filename=r5_filename,
            r6_filename=r6_filename,
            data_dir=".",  # Assume flat input folder
            debug=debug,
            mode=mode
        )

# Create singleton instance
checker = ReleaseConsistencyChecker()

def run_release_consistency_checker(
    domain: str,
    input_path: str,
    output_path: str,
    paths: Dict[str, str]
) -> None:
    """
    Entry point function for the Release Consistency Checker.
    
    Args:
        domain: The domain to check
        input_path: Not used directly (dataset config is used instead)
        output_path: Not used directly (dataset config is used instead)
        paths: Dictionary containing path configurations
    
    Returns:
        None
    """
    return checker.check(domain, input_path, output_path, paths)