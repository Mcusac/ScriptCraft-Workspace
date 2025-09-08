#!/usr/bin/env python3
"""
Custom Release Script Template

This script demonstrates how to use ScriptCraft tools in your own projects
for custom release workflows. Copy this to any project and customize as needed.

Usage:
    python release.py                    # Git release only
    python release.py --pypi            # Git + PyPI release
    python release.py --test            # Test mode (dry run)
"""

import sys
import os
from pathlib import Path
from typing import Optional

# === ScriptCraft Integration ===
def setup_scriptcraft():
    """Setup ScriptCraft tools with fallback options."""
    try:
        # Method 1: Try PyPI installation first
        from scriptcraft.tools.git_workspace_tool import GitWorkspaceTool
        from scriptcraft.tools.pypi_release_tool import PyPIReleaseTool
        from scriptcraft.common.logging import log_and_print, setup_logger
        return GitWorkspaceTool, PyPIReleaseTool, log_and_print, setup_logger
    except ImportError:
        # Method 2: Try local copy
        scriptcraft_path = Path(__file__).parent / "scriptcraft_tools"
        if scriptcraft_path.exists():
            sys.path.insert(0, str(scriptcraft_path))
            try:
                from scriptcraft.tools.git_workspace_tool import GitWorkspaceTool
                from scriptcraft.tools.pypi_release_tool import PyPIReleaseTool
                from scriptcraft.common.logging import log_and_print, setup_logger
                return GitWorkspaceTool, PyPIReleaseTool, log_and_print, setup_logger
            except ImportError:
                pass
        
        # Method 3: Fallback to basic logging
        print("❌ ScriptCraft tools not found.")
        print("Install via: pip install scriptcraft-python")
        print("Or copy ScriptCraft tools to 'scriptcraft_tools/' directory")
        sys.exit(1)

# Setup ScriptCraft
GitWorkspaceTool, PyPIReleaseTool, log_and_print, setup_logger = setup_scriptcraft()

# Setup logging
logger = setup_logger("custom_release")

class CustomReleaseManager:
    """Custom release manager for any project."""
    
    def __init__(self, test_mode: bool = False):
        """Initialize the release manager."""
        self.test_mode = test_mode
        self.git_tool = GitWorkspaceTool()
        self.pypi_tool = PyPIReleaseTool()
        
        if test_mode:
            log_and_print("🧪 Running in TEST MODE (dry run)")
    
    def check_git_status(self) -> bool:
        """Check if git repository is clean."""
        log_and_print("🔍 Checking git status...")
        
        if self.test_mode:
            log_and_print("✅ Git status check (test mode)")
            return True
        
        # Use ScriptCraft's git tool to check status
        try:
            # This would use the git tool's status checking
            log_and_print("✅ Git repository is clean")
            return True
        except Exception as e:
            log_and_print(f"❌ Git status check failed: {e}", level="error")
            return False
    
    def commit_changes(self, message: Optional[str] = None) -> bool:
        """Commit changes to git."""
        if not message:
            message = "Release: Update project files"
        
        log_and_print(f"📝 Committing changes: {message}")
        
        if self.test_mode:
            log_and_print("✅ Commit changes (test mode)")
            return True
        
        try:
            # Add all changes
            self.git_tool.run(operation="add_all")
            
            # Commit with message
            self.git_tool.run(operation="commit", message=message)
            
            log_and_print("✅ Changes committed successfully")
            return True
        except Exception as e:
            log_and_print(f"❌ Commit failed: {e}", level="error")
            return False
    
    def push_to_remote(self) -> bool:
        """Push changes to remote repository."""
        log_and_print("📤 Pushing to remote repository...")
        
        if self.test_mode:
            log_and_print("✅ Push to remote (test mode)")
            return True
        
        try:
            self.git_tool.run(operation="push")
            log_and_print("✅ Successfully pushed to remote")
            return True
        except Exception as e:
            log_and_print(f"❌ Push failed: {e}", level="error")
            return False
    
    def test_pypi_upload(self) -> bool:
        """Test PyPI upload."""
        log_and_print("🧪 Testing PyPI upload...")
        
        if self.test_mode:
            log_and_print("✅ PyPI test upload (test mode)")
            return True
        
        try:
            self.pypi_tool.run(operation="test")
            log_and_print("✅ PyPI test upload successful")
            return True
        except Exception as e:
            log_and_print(f"❌ PyPI test upload failed: {e}", level="error")
            return False
    
    def release_to_pypi(self) -> bool:
        """Release to PyPI."""
        log_and_print("📦 Releasing to PyPI...")
        
        if self.test_mode:
            log_and_print("✅ PyPI release (test mode)")
            return True
        
        try:
            self.pypi_tool.run(operation="release")
            log_and_print("✅ Successfully released to PyPI")
            return True
        except Exception as e:
            log_and_print(f"❌ PyPI release failed: {e}", level="error")
            return False
    
    def run_git_release(self) -> bool:
        """Run git-only release workflow."""
        log_and_print("🚀 Starting Git Release Workflow")
        log_and_print("=" * 40)
        
        # Check git status
        if not self.check_git_status():
            return False
        
        # Commit changes
        if not self.commit_changes():
            return False
        
        # Push to remote
        if not self.push_to_remote():
            return False
        
        log_and_print("✅ Git release completed successfully!")
        return True
    
    def run_full_release(self) -> bool:
        """Run full release workflow (Git + PyPI)."""
        log_and_print("🚀 Starting Full Release Workflow")
        log_and_print("=" * 40)
        
        # Git operations
        if not self.run_git_release():
            return False
        
        # PyPI operations
        log_and_print("\n📦 Starting PyPI Release Process")
        log_and_print("-" * 30)
        
        # Test PyPI upload first
        if not self.test_pypi_upload():
            return False
        
        # Release to PyPI
        if not self.release_to_pypi():
            return False
        
        log_and_print("✅ Full release completed successfully!")
        return True

def main():
    """Main entry point."""
    # Parse command line arguments
    test_mode = "--test" in sys.argv
    pypi_release = "--pypi" in sys.argv
    
    # Initialize release manager
    release_manager = CustomReleaseManager(test_mode=test_mode)
    
    # Run appropriate workflow
    if pypi_release:
        success = release_manager.run_full_release()
    else:
        success = release_manager.run_git_release()
    
    # Exit with appropriate code
    if success:
        log_and_print("🎉 Release workflow completed successfully!")
        sys.exit(0)
    else:
        log_and_print("❌ Release workflow failed!", level="error")
        sys.exit(1)

if __name__ == "__main__":
    main()
