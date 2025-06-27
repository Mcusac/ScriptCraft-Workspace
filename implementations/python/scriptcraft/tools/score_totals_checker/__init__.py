"""Score totals checker for validating calculated score totals against their component values."""

__version__ = "1.0.0"
__author__ = "UNT Data Team"
__description__ = "A checker that validates calculated score totals against their component values"

from .tool import run_score_totals_checker, checker

__all__ = ['run_score_totals_checker', 'checker']
