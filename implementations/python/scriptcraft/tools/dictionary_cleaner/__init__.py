"""
🧹 Dictionary Cleaner Tool

Cleans and standardizes data dictionary files by normalizing value formats,
fixing encoding issues, and ensuring consistent structure.

Features:
- 🧹 Value format cleaning and normalization
- 🔧 Encoding issue resolution
- 📋 Structure standardization
- ✨ Brace formatting fixes
- 📊 Quality validation

Author: ScriptCraft Team
"""

from .tool import DictionaryCleaner

# Tool metadata
__description__ = "🧹 Cleans and standardizes data dictionary files"
__tags__ = ["cleaning", "dictionaries", "standardization", "preprocessing", "quality"]
__data_types__ = ["csv", "xlsx", "xls"]
__domains__ = ["clinical", "biomarkers", "genomics", "imaging"]
__complexity__ = "moderate"
__maturity__ = "stable"
__distribution__ = "pipeline"

# Export the main tool
__all__ = ['DictionaryCleaner']
