#!/usr/bin/env python3
"""
Simple test runner for ScriptCraft workspace.

This script provides easy access to run tests from the workspace root.
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Run tests with proper configuration."""
    # Get the workspace root
    workspace_root = Path(__file__).parent.parent
    tests_dir = workspace_root / "tests"
    
    # Change to workspace root
    original_cwd = Path.cwd()
    os.chdir(workspace_root)
    
    try:
        # Run pytest with the tests directory
        cmd = [
            sys.executable, "-m", "pytest",
            str(tests_dir),
            "--tb=short",
            "--verbose"
        ]
        
        # Add coverage if available
        try:
            import pytest_cov
            cmd.extend([
                "--cov=implementations/python-package/scriptcraft",
                "--cov-report=term-missing",
                "--cov-report=html:htmlcov"
            ])
        except ImportError:
            print("⚠️ pytest-cov not available, running without coverage")
        
        # Run the tests
        result = subprocess.run(cmd)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
        else:
            print("❌ Some tests failed!")
            sys.exit(result.returncode)
            
    finally:
        # Restore original directory
        os.chdir(original_cwd)

if __name__ == "__main__":
    import os
    main() 