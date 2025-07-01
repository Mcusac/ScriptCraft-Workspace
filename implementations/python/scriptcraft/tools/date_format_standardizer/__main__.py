"""Command-line entry point for the date format standardizer."""

from scriptcraft.common.cli import run_tool_from_cli
from .tool import DateFormatStandardizer

if __name__ == "__main__":
    run_tool_from_cli(
        tool_name="Date Format Standardizer",
        description="Standardizes date formats in datasets to ensure consistency",
        tool_class=DateFormatStandardizer
    ) 