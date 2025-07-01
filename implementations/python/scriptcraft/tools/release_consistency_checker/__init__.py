"""
🔄 Release Consistency Checker Tool

Validates data consistency between different releases of the same dataset.
Identifies changes, missing data, and potential issues across releases.

Features:
- 🔄 Cross-release comparison
- 📊 Change detection and analysis
- ⚠️ Missing data identification
- 📋 Comprehensive reporting
- 🔍 Detailed difference tracking

Author: ScriptCraft Team
"""

from .tool import ReleaseConsistencyChecker

# Tool metadata
__description__ = "🔄 Validates data consistency between different releases"
__tags__ = ["validation", "releases", "consistency", "comparison", "versioning"]
__data_types__ = ["csv", "xlsx", "xls"]
__domains__ = ["clinical", "biomarkers", "genomics", "imaging"]
__complexity__ = "moderate"
__maturity__ = "stable"
__distribution__ = "hybrid"

# Export the main tool
__all__ = ['ReleaseConsistencyChecker']
