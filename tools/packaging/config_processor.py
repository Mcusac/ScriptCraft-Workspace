#!/usr/bin/env python3
"""
🔧 ScriptCraft Config Processor
Handles configuration processing for distributable packaging
"""

import yaml
import sys
from pathlib import Path
from typing import Dict, Any, List


def load_config(config_path: Path) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Error loading config from {config_path}: {e}")
        sys.exit(1)


def generate_config_bat(config: Dict[str, Any], template_dir: Path, timestamp: str) -> str:
    """Generate config.bat content from configuration."""
    packaging_config = config.get('packaging', {})
    tool_to_ship = packaging_config.get('tool_to_ship', '')
    tool_config = config.get('tools', {}).get(tool_to_ship, {})
    
    # Get common packages with fallback
    common_packages = packaging_config.get('common_packages', [
        'setuptools', 'wheel', 'pandas', 'numpy', 'openpyxl', 
        'python-docx', 'pyyaml', 'pytz', 'python-dateutil', 'selenium'
    ])
    common_packages_str = ' '.join(common_packages)
    
    # Get tool-specific packages
    tool_packages = tool_config.get('packages', [])
    tool_packages_str = ' '.join(tool_packages) if tool_packages else ''
    
    # Get tool metadata
    tool_description = tool_config.get('description', '')
    entry_command = tool_config.get('entry_command', 'main')
    
    # Generate config.bat content - simplified
    config_bat_content = f'''@echo off
:: ScriptCraft Configuration (Auto-Generated)
:: Generated from config.yaml for tool: {tool_to_ship}
:: Last updated: {timestamp}

set "TOOL_TO_SHIP={tool_to_ship}"
set "TOOL_DESCRIPTION={tool_description}"
set "ENTRY_COMMAND={entry_command}"
set "COMMON_PACKAGES={common_packages_str}"
set "TOOL_PACKAGES={tool_packages_str}"

echo ✅ Configuration loaded successfully
echo 🎯 Tool to ship: %TOOL_TO_SHIP%
echo 📝 Description: %TOOL_DESCRIPTION%
echo 🚀 Entry command: %ENTRY_COMMAND%
echo 📦 Common packages: %COMMON_PACKAGES%
echo 📦 Tool packages: %TOOL_PACKAGES%
'''
    
    return config_bat_content


def generate_run_bat(config: Dict[str, Any], tool_name: str, export_dir: Path) -> str:
    """Generate tool-specific run.bat content from configuration."""
    tool_config = config.get('tools', {}).get(tool_name, {})
    tool_description = tool_config.get('description', f'{tool_name} Tool')
    entry_command = tool_config.get('entry_command', 'main')
    
    # Simple, consistent run.bat template
    run_bat_content = f'''@echo off
setlocal EnableDelayedExpansion

:: =======================
:: 🚀 {tool_description}
:: =======================
set "BASE_DIR=%~dp0"
set "PYTHON_PATH=%BASE_DIR%embed_py311\\python.exe"
set "LOG_FILE=%BASE_DIR%logs\\run_log.txt"

:: =======================
:: 📁 Ensure logs folder
:: =======================
if not exist "%BASE_DIR%logs" mkdir "%BASE_DIR%logs"

:: =======================
:: 📝 Begin Logging
:: =======================
(
echo 🚀 Running {tool_description}...
echo 🔧 Current Directory: %cd%
echo ====================
echo 🕒 Run started: %DATE% %TIME%
echo ====================

:: =======================
:: 🔍 Check Python exists
:: =======================
if not exist "%PYTHON_PATH%" (
    echo ❌ Missing Python at: %PYTHON_PATH%
    echo 💡 Make sure embed_py311 folder is present
    exit /b 1
)

echo ✅ Python found: %PYTHON_PATH%

:: =======================
:: 📂 Show input folder
:: =======================
echo 📂 Input folder contents:
if exist "%BASE_DIR%input" (
    dir "%BASE_DIR%input"
) else (
    echo ⚠️ Input folder is empty
)

:: =======================
:: 🔄 Execute Python script
:: =======================
echo 🔄 Executing {tool_description}...
echo --------------------------------
"%PYTHON_PATH%" {entry_command} %*
echo --------------------------------

echo.
echo ✅ Process complete. Log saved to logs\\run_log.txt
) > "%LOG_FILE%" 2>&1

:: =======================
:: 🖨️ Show Log
:: =======================
type "%LOG_FILE%"
pause
'''
    
    return run_bat_content


def main():
    """Main entry point for config processing."""
    if len(sys.argv) < 3:
        print("Usage: python config_processor.py <action> <config_path> [output_path] [tool_name]")
        print("Actions: config_bat, run_bat")
        sys.exit(1)
    
    action = sys.argv[1]
    config_path = Path(sys.argv[2])
    
    # Load configuration
    config = load_config(config_path)
    
    if action == "config_bat":
        if len(sys.argv) < 4:
            print("❌ Missing output path for config_bat action")
            sys.exit(1)
        
        template_dir = Path(sys.argv[3])
        timestamp = sys.argv[4] if len(sys.argv) > 4 else "Unknown"
        
        # Generate config.bat
        config_bat_content = generate_config_bat(config, template_dir, timestamp)
        output_path = template_dir / "config.bat"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(config_bat_content)
        
        tool_to_ship = config.get('packaging', {}).get('tool_to_ship', '')
        print(f"✅ config.bat generated successfully for tool: {tool_to_ship}")
        print(f"📁 Location: {output_path}")
        
    elif action == "run_bat":
        if len(sys.argv) < 5:
            print("❌ Missing output path and tool name for run_bat action")
            sys.exit(1)
        
        export_dir = Path(sys.argv[3])
        tool_name = sys.argv[4]
        
        # Generate run.bat
        run_bat_content = generate_run_bat(config, tool_name, export_dir)
        output_path = export_dir / "run.bat"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(run_bat_content)
        
        tool_config = config.get('tools', {}).get(tool_name, {})
        tool_description = tool_config.get('description', f'{tool_name} Tool')
        print(f"✅ Tool-specific run.bat generated for: {tool_description}")
        print(f"📁 Location: {output_path}")
        
    else:
        print(f"❌ Unknown action: {action}")
        print("Supported actions: config_bat, run_bat")
        sys.exit(1)


if __name__ == "__main__":
    main()
