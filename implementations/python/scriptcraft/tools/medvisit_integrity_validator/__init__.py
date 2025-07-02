"""
🔒 Med/Visit Integrity Validator Tool

Validates the integrity of medical ID and visit ID combinations across datasets.
Ensures data consistency and identifies potential data integrity issues.

Features:
- 🔒 ID combination validation
- 🔍 Duplicate detection
- 📊 Cross-dataset consistency checking
- ⚠️ Integrity violation reporting
- 📋 Data quality metrics

Author: ScriptCraft Team
"""

from .main import MedVisitIntegrityValidator

# Tool metadata
__description__ = "🔒 Validates Med/Visit ID integrity across datasets"
__tags__ = ["validation", "integrity", "ids", "quality-control", "consistency"]
__data_types__ = ["csv", "xlsx", "xls"]
__domains__ = ["clinical", "biomarkers", "genomics", "imaging"]
__complexity__ = "simple"
__maturity__ = "stable"
__distribution__ = "pipeline"
