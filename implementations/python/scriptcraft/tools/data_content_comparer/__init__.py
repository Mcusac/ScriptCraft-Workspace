"""
📊 Data Content Comparer Tool

This tool compares the content of two datasets and generates a detailed report
of their differences, including column differences, data type mismatches,
value discrepancies, and missing or extra rows.

Features:
- 📋 Column comparison and analysis
- 🔍 Data type mismatch detection
- 📊 Value discrepancy identification
- 🆔 Missing/extra row detection
- 📄 Comprehensive reporting
- 🔀 Multiple comparison modes

Author: ScriptCraft Team
"""

from .tool import DataContentComparer

# Tool metadata
__description__ = "📊 Compares datasets and generates detailed difference reports"
__tags__ = ["comparison", "analysis", "validation", "data-quality", "reporting"]
__data_types__ = ["csv", "xlsx", "xls"]
__domains__ = ["clinical", "biomarkers", "genomics", "imaging"]
__complexity__ = "moderate"
__maturity__ = "stable"
__distribution__ = "hybrid"

# Export the main tool
__all__ = ['DataContentComparer']
