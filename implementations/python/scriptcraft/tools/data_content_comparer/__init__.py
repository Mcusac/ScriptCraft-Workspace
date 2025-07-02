"""
🔄 Data Content Comparer Tool

Compares content between datasets to identify differences, changes, and inconsistencies.
Supports multiple comparison modes and provides detailed analysis reports.

Features:
- 🔄 Multi-mode comparison (standard, RHQ, domain-specific)
- 📊 Detailed difference analysis
- 📋 Change tracking and reporting
- 🔍 Content validation
- 📈 Statistical summaries
- ⚠️ Inconsistency detection

Author: ScriptCraft Team
"""

from .main import DataContentComparer

# Tool metadata
__description__ = "🔄 Compares content between datasets to identify differences and changes"
__tags__ = ["comparison", "validation", "analysis", "differences", "changes"]
__data_types__ = ["csv", "xlsx", "xls"]
__domains__ = ["clinical", "biomarkers", "genomics", "imaging"]
__complexity__ = "moderate"
__maturity__ = "stable"
__distribution__ = "pipeline"
