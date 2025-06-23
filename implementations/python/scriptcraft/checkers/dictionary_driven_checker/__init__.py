"""Dictionary-driven checker for validating data against defined dictionaries with plugin support."""


__version__ = "1.0.0"
__author__ = "UNT Data Team"
__description__ = "A flexible checker that validates data against dictionaries using configurable plugins"

from .tool import run_dictionary_driven_checker, checker

__all__ = ['run_dictionary_driven_checker', 'checker']