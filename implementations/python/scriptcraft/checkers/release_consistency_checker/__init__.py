"""Release consistency checker for validating data consistency between different releases."""

__version__ = "1.0.0"
__author__ = "UNT Data Team"
__description__ = "A checker that validates data consistency between different releases"

from .tool import run_release_consistency_checker, checker

__all__ = ['run_release_consistency_checker', 'checker']
