"""
Dictionary tools package that consolidates all dictionary-related functionality.

This package provides a unified interface to all dictionary-related operations
across the codebase, including cleaning, validation, and checking. It serves
as a facade to the underlying components while maintaining their separation
of concerns.

Example:
    >>> from scripts.dictionary_tools import cleaner, validator, checker
    >>> 
    >>> # Clean a dictionary
    >>> cleaner.transform(domain="Clinical", 
    ...                   input_path="raw_dict.csv",
    ...                   output_path="clean_dict.csv",
    ...                   paths={})
    >>> 
    >>> # Validate data against dictionary
    >>> validator.validate(domain="Clinical",
    ...                    input_path="data.csv",
    ...                    output_path="validation_results.csv",
    ...                    paths={"dictionary": "clean_dict.csv"})
    >>> 
    >>> # Run dictionary-driven checks
    >>> checker.check(domain="Clinical",
    ...               input_path="data.csv",
    ...               output_path="check_results.csv",
    ...               paths={"dictionary": "clean_dict.csv"})
"""

from typing import Dict, Any

from scripts.transformers.dictionary_cleaner.main import DictionaryCleaner
from scripts.validators.dictionary_validator.main import DictionaryValidator
from scripts.checkers.dictionary_driven_checker.main import DictionaryDrivenChecker

# Export all dictionary-related components
__all__ = [
    'DictionaryCleaner',
    'DictionaryValidator',
    'DictionaryDrivenChecker',
    'cleaner',
    'validator',
    'checker'
]

# Create singleton instances for easy access
cleaner: DictionaryCleaner = DictionaryCleaner()
validator: DictionaryValidator = DictionaryValidator()
checker: DictionaryDrivenChecker = DictionaryDrivenChecker()

# Type hints for better IDE support
DictionaryTools = Dict[str, Any]  # Type alias for dictionary configurations 