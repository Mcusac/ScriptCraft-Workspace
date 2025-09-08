#!/usr/bin/env python3
"""
🚀 Simple Git Sync Script

Just run this file to sync your git repository automatically.
No manual commands needed!

Usage:
    python sync.py
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Run automated git sync."""
    print("🚀 Starting automated git sync...")
    
    try:
        # Use the updated ScriptCraft command
        result = subprocess.run([
            sys.executable, "-m", "scriptcraft.cli.release_cli", "git-sync"
        ], check=True, capture_output=True, text=True, encoding='utf-8')
        
        print(result.stdout)
        print("✅ Git sync completed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git sync failed: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ ScriptCraft not found. Install with: pip install scriptcraft-python")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
