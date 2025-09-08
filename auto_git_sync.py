#!/usr/bin/env python3
"""
🤖 Automated Git Sync Script

This script provides fully automated git synchronization for any repository.
It handles submodules, commits, and pushes in one command.

Usage:
    python auto_git_sync.py                    # Auto-commit and sync
    python auto_git_sync.py --message "Custom message"  # Custom commit message
    python auto_git_sync.py --dry-run          # See what would happen
"""

import sys
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="🤖 Automated Git Sync")
    parser.add_argument("--message", "-m", default="🤖 Auto-commit: Automated sync", 
                       help="Commit message")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show what would happen without making changes")
    
    args = parser.parse_args()
    
    try:
        # Import ScriptCraft tools
        from scriptcraft.tools.git_workspace_tool import GitWorkspaceTool
        from scriptcraft.tools.git_submodule_tool import GitSubmoduleTool
        import scriptcraft.common as cu
        
        cu.log_and_print('🚀 Starting automated git sync...')
        
        if args.dry_run:
            cu.log_and_print('🔍 DRY RUN MODE - No changes will be made')
            # Just check status
            workspace_tool = GitWorkspaceTool()
            workspace_tool.run(operation='status')
            return
        
        # Step 1: Sync submodules
        cu.log_and_print('📦 Syncing submodules...')
        submodule_tool = GitSubmoduleTool()
        submodule_success = submodule_tool.run(operation='sync')
        
        # Step 2: Commit any uncommitted changes
        cu.log_and_print('💾 Committing any uncommitted changes...')
        workspace_tool = GitWorkspaceTool()
        commit_success = workspace_tool.run(operation='commit', message=args.message)
        
        # Step 3: Push changes
        cu.log_and_print('📤 Pushing changes...')
        push_success = workspace_tool.run(operation='push')
        
        if submodule_success and commit_success and push_success:
            cu.log_and_print('✅ Automated git sync completed successfully!')
        else:
            cu.log_and_print('❌ Automated git sync failed')
            sys.exit(1)
            
    except ImportError:
        print("❌ ScriptCraft not found. Install with: pip install scriptcraft-python")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
