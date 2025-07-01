"""
📅 Date Format Standardizer Tool

Standardizes date formats across datasets by detecting and converting various
date representations to consistent formats.

Features:
- 🔍 Automatic date column detection
- 📅 Multiple input format recognition
- 🎯 Configurable output formats
- ⚡ Batch processing support
- 📊 Format validation and reporting

Author: ScriptCraft Team
"""

from .tool import DateFormatStandardizer

# Tool metadata
__description__ = "📅 Standardizes date formats across datasets"
__tags__ = ["dates", "standardization", "formatting", "validation", "cleaning"]
__data_types__ = ["csv", "xlsx", "xls"]
__domains__ = ["clinical", "biomarkers", "genomics", "imaging"]
__complexity__ = "simple"
__maturity__ = "stable"
__distribution__ = "pipeline"

# Export the main tool
__all__ = ['DateFormatStandardizer']
