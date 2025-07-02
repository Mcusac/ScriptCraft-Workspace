"""
📅 Date Format Standardizer Tool

Standardizes date formats across datasets to ensure consistency and compatibility.
Supports multiple input formats and provides flexible output formatting options.

Features:
- 📅 Multi-format date parsing
- 🔄 Format standardization
- 📊 Batch processing support
- ⚠️ Invalid date detection
- 📋 Format validation
- 🎯 Healthcare date patterns

Author: ScriptCraft Team
"""

from .main import DateFormatStandardizer

# Tool metadata
__description__ = "📅 Standardizes date formats across datasets for consistency"
__tags__ = ["dates", "formatting", "standardization", "validation", "processing"]
__data_types__ = ["csv", "xlsx", "xls"]
__domains__ = ["clinical", "biomarkers", "genomics", "imaging"]
__complexity__ = "simple"
__maturity__ = "stable"
__distribution__ = "pipeline"
