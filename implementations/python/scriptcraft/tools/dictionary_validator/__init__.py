"""
Dictionary Validator

This validator checks consistency between dataset columns and dictionary columns.
"""

from .tool import DictionaryValidator, validator, run_dictionary_validator

__version__ = "1.0.0"
__all__ = ["DictionaryValidator", "validator", "run_dictionary_validator"]
