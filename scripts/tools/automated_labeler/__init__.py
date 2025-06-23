"""
Automated Labeler Tool

Loads an input Excel file and a Word DOCX template, then populates labels
based on ID columns.
"""

from .tool import AutomatedLabeler, tool

__version__ = "1.0.0"
__all__ = ["AutomatedLabeler", "tool"]
