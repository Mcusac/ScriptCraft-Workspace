#!/usr/bin/env python3
"""
ScriptCraft Project Integration Setup

This script helps you integrate ScriptCraft tools into any project.
It provides multiple methods for using ScriptCraft tools in your own projects.

Usage:
    python setup_scriptcraft_in_project.py --method pip
    python setup_scriptcraft_in_project.py --method copy
    python setup_scriptcraft_in_project.py --method submodule
"""

import sys
import os
import subprocess
import shutil
from pathlib import Path
from typing import Optional

def log(message: str, level: str = "info"):
    """Simple logging function."""
    emoji = {"info": "ℹ️", "success": "✅", "error": "❌", "warning": "⚠️"}
    print(f"{emoji.get(level, 'ℹ️')} {message}")

def check_pip_installation():
    """Check if ScriptCraft is available via pip."""
    try:
        import scriptcraft
        log("ScriptCraft is already installed via pip", "success")
        return True
    except ImportError:
        log("ScriptCraft not found via pip", "warning")
        return False

def install_via_pip():
    """Install ScriptCraft via pip."""
    log("Installing ScriptCraft via pip...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "scriptcraft-python"], 
                      check=True, capture_output=True, text=True)
        log("ScriptCraft installed successfully via pip!", "success")
        return True
    except subprocess.CalledProcessError as e:
        log(f"Failed to install via pip: {e}", "error")
        return False

def copy_scriptcraft_tools(source_path: str):
    """Copy ScriptCraft tools to project directory."""
    target_dir = Path("scriptcraft_tools")
    
    if target_dir.exists():
        log("scriptcraft_tools directory already exists", "warning")
        response = input("Overwrite? (y/N): ").lower()
        if response != 'y':
            log("Copy cancelled", "info")
            return False
        shutil.rmtree(target_dir)
    
    log(f"Copying ScriptCraft tools from {source_path}...")
    try:
        shutil.copytree(source_path, target_dir)
        log("ScriptCraft tools copied successfully!", "success")
        return True
    except Exception as e:
        log(f"Failed to copy tools: {e}", "error")
        return False

def setup_git_submodule():
    """Setup ScriptCraft as git submodule."""
    log("Setting up ScriptCraft as git submodule...")
    try:
        # Add submodule (you'll need to replace with actual repo URL)
        subprocess.run([
            "git", "submodule", "add", 
            "https://github.com/your-org/scriptcraft.git", 
            "scriptcraft_tools"
        ], check=True, capture_output=True, text=True)
        
        # Initialize submodule
        subprocess.run([
            "git", "submodule", "update", "--init", "--recursive"
        ], check=True, capture_output=True, text=True)
        
        log("ScriptCraft submodule setup successfully!", "success")
        return True
    except subprocess.CalledProcessError as e:
        log(f"Failed to setup submodule: {e}", "error")
        return False

def create_example_script():
    """Create an example usage script."""
    example_script = """#!/usr/bin/env python3
'''
Example ScriptCraft Integration

This script demonstrates how to use ScriptCraft tools in your project.
'''

import sys
from pathlib import Path

# Add ScriptCraft to path (if using local copy)
scriptcraft_path = Path(__file__).parent / "scriptcraft_tools"
if scriptcraft_path.exists():
    sys.path.insert(0, str(scriptcraft_path))

try:
    from scriptcraft.tools.git_workspace_tool import GitWorkspaceTool
    from scriptcraft.common.logging import log_and_print
    log_and_print("🚀 ScriptCraft tools loaded successfully!")
    
    # Example: Use git tool
    git_tool = GitWorkspaceTool()
    log_and_print("📝 Git tool ready for use")
    
except ImportError as e:
    print(f"❌ ScriptCraft tools not available: {e}")
    print("Run setup_scriptcraft_in_project.py to install")
    sys.exit(1)

if __name__ == "__main__":
    log_and_print("✅ ScriptCraft integration working!")
"""
    
    with open("example_scriptcraft_usage.py", "w") as f:
        f.write(example_script)
    
    log("Created example_scriptcraft_usage.py", "success")

def main():
    """Main setup function."""
    log("🚀 ScriptCraft Project Integration Setup")
    log("=" * 50)
    
    # Parse arguments
    method = "pip"  # default
    if "--method" in sys.argv:
        try:
            method_index = sys.argv.index("--method")
            method = sys.argv[method_index + 1]
        except (IndexError, ValueError):
            log("Invalid --method argument", "error")
            sys.exit(1)
    
    # Check current status
    if check_pip_installation():
        log("ScriptCraft is already available via pip!", "success")
        create_example_script()
        return
    
    # Setup based on method
    success = False
    
    if method == "pip":
        log("Setting up ScriptCraft via pip installation...")
        success = install_via_pip()
    
    elif method == "copy":
        source_path = input("Enter path to ScriptCraft directory: ").strip()
        if not source_path or not Path(source_path).exists():
            log("Invalid source path", "error")
            sys.exit(1)
        success = copy_scriptcraft_tools(source_path)
    
    elif method == "submodule":
        success = setup_git_submodule()
    
    else:
        log(f"Unknown method: {method}", "error")
        log("Available methods: pip, copy, submodule", "info")
        sys.exit(1)
    
    if success:
        create_example_script()
        log("🎉 ScriptCraft integration setup complete!", "success")
        log("Run 'python example_scriptcraft_usage.py' to test", "info")
    else:
        log("❌ Setup failed", "error")
        sys.exit(1)

if __name__ == "__main__":
    main()
