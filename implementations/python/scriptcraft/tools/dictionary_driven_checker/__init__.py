"""
🔍 Dictionary-Driven Checker Tool

A flexible checker that validates data against dictionaries using configurable plugins.
Supports multiple validation types and provides detailed reporting.

Features:
- 🔌 Plugin-based validation system
- 📊 Multiple data type support (numeric, text, date)
- 🎯 Dictionary-driven validation rules
- 📋 Comprehensive error reporting
- ⚙️ Configurable validation options
- 🔍 Outlier detection

Author: ScriptCraft Team
"""

from .tool import DictionaryDrivenChecker

# Tool metadata
__description__ = "🔍 Validates data against dictionaries using configurable plugins"
__tags__ = ["validation", "dictionaries", "quality-control", "plugins", "checking"]
__data_types__ = ["csv", "xlsx", "xls"]
__domains__ = ["clinical", "biomarkers", "genomics", "imaging"]
__complexity__ = "complex"
__maturity__ = "stable"
__distribution__ = "hybrid"

# Export the main tool
__all__ = ['DictionaryDrivenChecker']