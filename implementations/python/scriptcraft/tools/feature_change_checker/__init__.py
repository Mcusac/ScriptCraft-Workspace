"""
🔄 Feature Change Checker Tool

Tracks and categorizes changes in feature values between visits or timepoints.
Provides longitudinal analysis and change detection capabilities.

Features:
- 🔄 Visit-to-visit change tracking
- 📊 Change categorization and analysis
- 📈 Longitudinal trend analysis
- 📋 Change summary reporting
- 🎯 Feature-specific analysis

Author: ScriptCraft Team
"""

from .tool import FeatureChangeChecker

# Tool metadata
__description__ = "🔄 Tracks and categorizes changes in feature values between visits"
__tags__ = ["tracking", "changes", "longitudinal", "features", "analysis"]
__data_types__ = ["csv", "xlsx", "xls"]
__domains__ = ["clinical", "biomarkers", "genomics"]
__complexity__ = "moderate"
__maturity__ = "stable"
__distribution__ = "pipeline"

# Export the main tool
__all__ = ['FeatureChangeChecker']
