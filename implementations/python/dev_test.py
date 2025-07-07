#!/usr/bin/env python3
"""
Quick development test script.
Run this to test your changes: python dev_test.py
"""

import sys
from pathlib import Path

def main():
    print("Quick Development Test")
    print("=" * 30)
    
    # Test imports
    try:
        import scriptcraft
        print("scriptcraft imported")
        
        import scriptcraft.common as cu
        print("scriptcraft.common imported")
        
        from scriptcraft.tools import AutomatedLabeler
        print("AutomatedLabeler imported")
        
        # Test instantiation
        tool = AutomatedLabeler()
        print(f"Tool created: {tool.name}")
        
        print("\nAll tests passed! Your changes are active.")
        
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
