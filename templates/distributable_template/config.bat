@echo off
:: ScriptCraft Configuration (Auto-Generated)
:: Generated from config.yaml for tool: rhq_form_autofiller
:: Last updated: Mon 08/18/2025 11:03:17.28

set "TOOL_TO_SHIP=rhq_form_autofiller"
set "TOOL_DESCRIPTION=🏠 Automatically fills RHQ residential history forms using participant data"
set "ENTRY_COMMAND=-m scriptcraft.tools.rhq_form_autofiller.main"
set "COMMON_PACKAGES=setuptools wheel pandas numpy openpyxl python-docx pyyaml pytz python-dateutil selenium"
set "TOOL_PACKAGES=pyyaml pandas python-docx openpyxl selenium pytz"

echo ✅ Configuration loaded successfully
echo 🎯 Tool to ship: %TOOL_TO_SHIP%
echo 📝 Description: %TOOL_DESCRIPTION%
echo 🚀 Entry command: %ENTRY_COMMAND%
echo 📦 Common packages: %COMMON_PACKAGES%
echo 📦 Tool packages: %TOOL_PACKAGES%
