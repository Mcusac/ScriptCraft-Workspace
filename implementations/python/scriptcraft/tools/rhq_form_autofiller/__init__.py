"""
🌐 RHQ Form Autofiller Tool

Automates filling of web forms for Residence History Questionnaire (RHQ) data.
Uses Selenium WebDriver to interact with web interfaces and submit form data.

Features:
- 🌐 Web form automation
- 🔄 Batch processing support
- 🏠 Address data handling
- 🔐 Authentication support
- 📊 Excel data integration

Author: ScriptCraft Team
"""

from .main import RHQFormAutofiller

# Tool metadata
__description__ = "🌐 Automates filling of RHQ web forms with data"
__tags__ = ["automation", "web-forms", "rhq", "selenium", "data-entry"]
__data_types__ = ["csv", "xlsx", "xls"]
__domains__ = ["clinical"]
__complexity__ = "complex"
__maturity__ = "stable"
__distribution__ = "standalone"

# Export the main tool
__all__ = ['RHQFormAutofiller']
