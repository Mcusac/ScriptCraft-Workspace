"""
✅ Dictionary Validator Tool

Validates data dictionary structure and content against expected standards.
Ensures dictionary completeness and consistency across domains.

Features:
- 📋 Structure validation
- 🔍 Content completeness checking
- 📊 Cross-domain consistency
- ⚠️ Missing field detection
- 📄 Validation reporting

Author: ScriptCraft Team
"""

from .main import DictionaryValidator

# Tool metadata
__description__ = "✅ Validates data dictionary structure and content"
__tags__ = ["validation", "dictionaries", "structure", "completeness", "quality"]
__data_types__ = ["csv", "xlsx", "xls"]
__domains__ = ["clinical", "biomarkers", "genomics", "imaging"]
__complexity__ = "simple"
__maturity__ = "stable"
__distribution__ = "pipeline"
