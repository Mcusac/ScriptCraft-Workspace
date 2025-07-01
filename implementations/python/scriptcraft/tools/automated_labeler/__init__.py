"""
🏷️ Automated Labeler Tool

Automatically generates labels and fills document templates with data from Excel files.
Supports form automation and document generation for research workflows.

Features:
- 📄 Document template filling
- 🏷️ Automatic label generation
- 📊 Excel data processing
- 🔄 Batch processing support
- 📋 Multiple output formats

Author: ScriptCraft Team
"""

from .tool import AutomatedLabeler

# Tool metadata
__description__ = "🏷️ Automatically generates labels and fills document templates"
__tags__ = ["automation", "documents", "forms", "labels", "templates"]
__data_types__ = ["csv", "xlsx", "docx"]
__domains__ = ["clinical", "biomarkers", "genomics", "imaging"]
__complexity__ = "simple"
__maturity__ = "stable"
__distribution__ = "hybrid"

# Export the main tool
__all__ = ['AutomatedLabeler']
