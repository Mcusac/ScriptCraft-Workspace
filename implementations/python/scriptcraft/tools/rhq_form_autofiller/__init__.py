"""
🔄 RHQ Form Autofiller Tool

Automatically fills RHQ (Research Health Questionnaire) forms with data from Excel files.
Supports form automation and document generation for research workflows.

Features:
- 📄 Document template filling
- 🏷️ Automatic label generation
- 📊 Excel data processing
- 🔄 Batch processing support
- 📋 Multiple output formats

Author: ScriptCraft Team
"""

from .main import RHQFormAutofiller

# Tool metadata
__description__ = "🔄 Automatically fills RHQ forms with data from Excel files"
__tags__ = ["automation", "forms", "documents", "excel", "templates"]
__data_types__ = ["csv", "xlsx", "docx"]
__domains__ = ["clinical", "biomarkers", "genomics", "imaging"]
__complexity__ = "moderate"
__maturity__ = "stable"
__distribution__ = "standalone"
