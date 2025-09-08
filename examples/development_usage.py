#!/usr/bin/env python3
"""
Development Usage Examples

This file demonstrates the recommended approaches for using ScriptCraft
in development, following industry standards and DRY principles.
"""

import sys
from pathlib import Path

# Add the package to path (only needed for development)
sys.path.insert(0, str(Path(__file__).parent.parent / "implementations" / "python-package"))

import scriptcraft.common as cu
from scriptcraft.pipelines.git_pipelines import (
    create_pypi_test_pipeline,
    create_pypi_release_pipeline,
    create_full_git_sync_pipeline
)
from scriptcraft.tools.pypi_release_tool import PyPIReleaseTool
from scriptcraft.tools.git_workspace_tool import GitWorkspaceTool

def example_1_cli_approach():
    """
    RECOMMENDED: Use CLI commands for simple operations.
    
    In terminal:
    scriptcraft-release pypi-test
    scriptcraft-release pypi-release
    scriptcraft-release git-sync
    """
    cu.log_and_print("🎯 CLI Approach (Recommended for simple operations)")
    cu.log_and_print("Run these commands in terminal:")
    cu.log_and_print("  scriptcraft-release pypi-test")
    cu.log_and_print("  scriptcraft-release pypi-release")
    cu.log_and_print("  scriptcraft-release git-sync")
    cu.log_and_print("  scriptcraft-release full-release")
    cu.log_and_print("  scriptcraft --tool rhq_form_autofiller")
    cu.log_and_print("  scriptcraft --tool data_content_comparer")

def example_2_pipeline_approach():
    """
    RECOMMENDED: Use pipelines for complex workflows.
    
    This approach uses the consolidated pipeline system and
    follows ScriptCraft patterns.
    """
    cu.log_and_print("🎯 Pipeline Approach (Recommended for complex workflows)")
    
    # Create and run PyPI test pipeline
    cu.log_and_print("Creating PyPI test pipeline...")
    pipeline = create_pypi_test_pipeline()
    cu.log_and_print(f"Pipeline created: {pipeline.name}")
    cu.log_and_print(f"Steps: {[step.name for step in pipeline.steps]}")
    
    # You can run it with: pipeline.run()
    # cu.log_and_print("Running pipeline...")
    # pipeline.run()

def example_3_individual_tools():
    """
    RECOMMENDED: Use individual tools for specific operations.
    
    This approach gives you fine-grained control while still
    using the ScriptCraft tool system.
    """
    cu.log_and_print("🎯 Individual Tools Approach (For specific operations)")
    
    # Create and run individual tools
    cu.log_and_print("Creating PyPI release tool...")
    pypi_tool = PyPIReleaseTool()
    cu.log_and_print(f"Tool created: {pypi_tool.name}")
    
    # You can run specific operations
    # pypi_tool.run(operation="test")
    # pypi_tool.run(operation="build")
    # pypi_tool.run(operation="release")

def example_4_run_all_approach():
    """
    RECOMMENDED: Use run_all.py for complex orchestration.
    
    This mimics your distributable pattern and uses config.yaml
    as the single source of truth.
    """
    cu.log_and_print("🎯 run_all.py Approach (For complex orchestration)")
    cu.log_and_print("Run these commands in terminal:")
    cu.log_and_print("  python run_all.py --list")
    cu.log_and_print("  python run_all.py --pipeline data_quality")
    cu.log_and_print("  python run_all.py --pipeline dictionary_pipeline")
    cu.log_and_print("  python run_all.py --tool rhq_form_autofiller")
    cu.log_and_print("  python run_all.py --tool data_content_comparer")

def example_5_anti_pattern():
    """
    ANTI-PATTERN: Don't create simple scripts for everything.
    
    This breaks DRY principles and doesn't use the config system.
    """
    cu.log_and_print("❌ Anti-Pattern: Simple Scripts (Avoid)")
    cu.log_and_print("Don't create scripts like this:")
    cu.log_and_print("  # my_custom_script.py")
    cu.log_and_print("  # Hardcoded logic that duplicates functionality")
    cu.log_and_print("  # Not config-driven")
    cu.log_and_print("  # Not distributable")
    cu.log_and_print("  # Breaks DRY principles")

def main():
    """Demonstrate all approaches."""
    cu.log_and_print("🚀 ScriptCraft Development Usage Examples")
    cu.log_and_print("=" * 50)
    
    example_1_cli_approach()
    cu.log_and_print("")
    
    example_2_pipeline_approach()
    cu.log_and_print("")
    
    example_3_individual_tools()
    cu.log_and_print("")
    
    example_4_run_all_approach()
    cu.log_and_print("")
    
    example_5_anti_pattern()
    cu.log_and_print("")
    
    cu.log_and_print("🎯 RECOMMENDATION:")
    cu.log_and_print("1. Use CLI commands for simple operations")
    cu.log_and_print("2. Use run_all.py for complex workflows")
    cu.log_and_print("3. Use pipelines for multi-step processes")
    cu.log_and_print("4. Use individual tools for specific operations")
    cu.log_and_print("5. Avoid simple scripts (anti-DRY)")

if __name__ == "__main__":
    main()
