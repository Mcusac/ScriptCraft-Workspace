"""
📋 Dictionary-Driven Checker Tool

Validates datasets against data dictionaries to ensure compliance and accuracy.
Uses dictionary definitions to check data types, ranges, and value constraints.

Features:
- 📋 Dictionary-based validation
- 🔍 Data type checking
- 📊 Range and constraint validation
- ⚠️ Compliance reporting
- 🎯 Healthcare data patterns
- 📈 Quality metrics

Author: ScriptCraft Team
"""

from .main import DictionaryDrivenChecker

# Tool metadata
__description__ = "📋 Validates datasets against data dictionaries for compliance"
__tags__ = ["validation", "dictionaries", "compliance", "quality-control", "checking"]
__data_types__ = ["csv", "xlsx", "xls"]
__domains__ = ["clinical", "biomarkers", "genomics", "imaging"]
__complexity__ = "moderate"
__maturity__ = "stable"
__distribution__ = "pipeline"