"""
🧮 Score Totals Checker Tool

Validates calculated score totals against their component values to ensure
mathematical accuracy and data integrity in scoring systems.

Features:
- 🧮 Total score validation
- 📊 Component value checking
- ⚠️ Discrepancy detection
- 📋 Accuracy reporting
- 🔍 Score integrity analysis

Author: ScriptCraft Team
"""

from .tool import ScoreTotalsChecker

# Tool metadata
__description__ = "🧮 Validates calculated score totals against component values"
__tags__ = ["validation", "scores", "totals", "calculation", "integrity"]
__data_types__ = ["csv", "xlsx", "xls"]
__domains__ = ["clinical", "biomarkers"]
__complexity__ = "simple"
__maturity__ = "stable"
__distribution__ = "pipeline"

# Export the main tool
__all__ = ['ScoreTotalsChecker']
