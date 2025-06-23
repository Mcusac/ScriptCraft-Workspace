"""
Data Content Comparer Tool

This tool compares the content of two datasets and generates a detailed report
of their differences, including:
- Column differences
- Data type mismatches
- Value discrepancies
- Missing or extra rows

Usage:
    # As a package:
    from scripts.tools.data_content_comparer import DataContentComparer
    comparer = DataContentComparer()
    comparer.run(input_paths=['old.csv', 'new.csv'])
    
    # As a script:
    python -m scripts.tools.data_content_comparer old.csv new.csv
"""

from .tool import DataContentComparer

__all__ = ['DataContentComparer']
