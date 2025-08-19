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
    
    # Get tool-specific configuration
    url_template = tool_config.get('url_template', '')
    
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
set "URL_TEMPLATE={url_template}"

echo ✅ Configuration loaded successfully
echo 🎯 Tool to ship: %TOOL_TO_SHIP%
echo 📝 Description: %TOOL_DESCRIPTION%
echo 🚀 Entry command: %ENTRY_COMMAND%
echo 📦 Common packages: %COMMON_PACKAGES%
echo 📦 Tool packages: %TOOL_PACKAGES%
echo 🌐 URL template: %URL_TEMPLATE%
'''
    
    return config_bat_content





def main():
    """Main entry point for config processing."""
    if len(sys.argv) < 4:
        print("Usage: python config_processor.py config_bat <config_path> <output_path> [timestamp]")
        print("Only config_bat generation is supported - templates handle run.bat")
        sys.exit(1)
    
    action = sys.argv[1]
    config_path = Path(sys.argv[2])
    
    if action != "config_bat":
        print(f"❌ Unsupported action: {action}")
        print("Only 'config_bat' is supported - templates handle run.bat automatically")
        sys.exit(1)
    
    # Load configuration
    config = load_config(config_path)
    
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


if __name__ == "__main__":
    main()
