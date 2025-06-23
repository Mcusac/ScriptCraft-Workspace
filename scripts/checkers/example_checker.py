"""
Example checker demonstrating the new pipeline step architecture.
"""

from pathlib import Path
import pandas as pd
from typing import Optional, Dict
from scripts.common.core import BasePipelineStep

class ExampleChecker(BasePipelineStep):
    """Example checker that demonstrates the pipeline step architecture."""
    
    def __init__(self):
        super().__init__(
            name="Example Checker",
            input_key="raw_data",
            run_mode="domain",
            tags=["example", "checker", "validation"],
            check_exists=True
        )
        
    def validate_input(self, input_path: Path) -> bool:
        """Validate input data format and required columns."""
        try:
            if not input_path.exists():
                return False
                
            df = pd.read_csv(input_path)
            required_columns = ["Med_ID", "Visit_ID"]
            
            return all(col in df.columns for col in required_columns)
            
        except Exception as e:
            self.log_error(f"Validation error: {str(e)}")
            return False
    
    def process(self,
                input_path: Path,
                output_path: Path,
                domain: Optional[str] = None,
                **kwargs) -> bool:
        """Process the data and perform checks."""
        try:
            # Read input data
            df = pd.read_csv(input_path)
            
            # Perform example checks
            results = []
            
            # Check 1: Missing values
            missing_counts = df.isnull().sum()
            for col, count in missing_counts.items():
                if count > 0:
                    results.append({
                        "check_type": "missing_values",
                        "column": col,
                        "count": count,
                        "percentage": (count / len(df)) * 100
                    })
            
            # Check 2: Duplicate records
            duplicates = df.duplicated().sum()
            if duplicates > 0:
                results.append({
                    "check_type": "duplicates",
                    "count": duplicates,
                    "percentage": (duplicates / len(df)) * 100
                })
            
            # Save results
            results_df = pd.DataFrame(results)
            results_df.to_csv(output_path, index=False)
            
            return True
            
        except Exception as e:
            self.log_error(f"Processing error: {str(e)}")
            return False
    
    def log_error(self, message: str):
        """Helper method for consistent error logging."""
        print(f"❌ {self.name}: {message}")

# Register the checker
checker = ExampleChecker() 