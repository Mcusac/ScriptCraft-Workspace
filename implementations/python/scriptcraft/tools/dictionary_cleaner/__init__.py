"""
Dictionary Cleaner

This transformer standardizes and validates dictionary entries, including normalizing value types,
standardizing expected values, and ensuring consistent formatting across all dictionary fields.
"""

from .tool import DictionaryCleaner, cleaner, run_dictionary_cleaner

__version__ = "1.0.0"
__all__ = ["DictionaryCleaner", "cleaner", "run_dictionary_cleaner"]
