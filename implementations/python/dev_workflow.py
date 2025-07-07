#!/usr/bin/env python3
"""
Development Workflow Script for ScriptCraft

This script helps manage development vs production environments and ensures
you're testing the correct version of your code.
"""

import sys
import os
from pathlib import Path
import subprocess

def check_installation_mode():
    """Check if we're using editable or production installation."""
    print("🔍 Checking installation mode...")
    
    try:
        import scriptcraft
        scriptcraft_path = Path(scriptcraft.__file__).parent
        
        # Check if it's pointing to our development directory
        dev_path = Path(__file__).parent / "scriptcraft"
        
        if scriptcraft_path == dev_path:
            print("✅ Using DEVELOPMENT installation (editable)")
            print(f"   Path: {scriptcraft_path}")
            return "development"
        else:
            print("⚠️ Using PRODUCTION installation")
            print(f"   Path: {scriptcraft_path}")
            return "production"
    except Exception as e:
        print(f"❌ Error checking installation: {e}")
        return "unknown"

def check_pip_installation():
    """Check pip installation status."""
    print("\n🔍 Checking pip installation...")
    
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "list"], 
                              capture_output=True, text=True)
        
        if "scriptcraft" in result.stdout:
            print("✅ ScriptCraft is installed via pip")
            
            # Check if it's editable
            if "-e" in result.stdout or "editable" in result.stdout:
                print("✅ Installation is editable (development mode)")
                return True
            else:
                print("⚠️ Installation is not editable (production mode)")
                return False
        else:
            print("❌ ScriptCraft not found in pip list")
            return False
    except Exception as e:
        print(f"❌ Error checking pip: {e}")
        return False

def setup_development_mode():
    """Set up development mode with editable install."""
    print("\n🔧 Setting up development mode...")
    
    try:
        # Uninstall any existing installation
        print("📦 Uninstalling existing installation...")
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "scriptcraft", "-y"], 
                      check=False)
        
        # Install in editable mode
        print("📦 Installing in editable mode...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Development mode set up successfully")
            return True
        else:
            print(f"❌ Failed to set up development mode: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error setting up development mode: {e}")
        return False

def test_development_changes():
    """Test that changes to development code are reflected."""
    print("\n🧪 Testing development changes...")
    
    try:
        # Test basic import
        import scriptcraft
        print("✅ Basic import works")
        
        # Test common utilities
        import scriptcraft.common as cu
        print("✅ Common utilities import works")
        
        # Test tool import
        from scriptcraft.tools import AutomatedLabeler
        print("✅ Tool import works")
        
        # Test tool instantiation
        tool = AutomatedLabeler()
        print(f"✅ Tool instantiation works: {tool.name}")
        
        return True
    except Exception as e:
        print(f"❌ Development test failed: {e}")
        return False

def create_test_script():
    """Create a simple test script for development."""
    test_script = """
#!/usr/bin/env python3
\"\"\"
Quick development test script.
Run this to test your changes: python dev_test.py
\"\"\"

import sys
from pathlib import Path

def main():
    print("🚀 Quick Development Test")
    print("=" * 30)
    
    # Test imports
    try:
        import scriptcraft
        print("✅ scriptcraft imported")
        
        import scriptcraft.common as cu
        print("✅ scriptcraft.common imported")
        
        from scriptcraft.tools import AutomatedLabeler
        print("✅ AutomatedLabeler imported")
        
        # Test instantiation
        tool = AutomatedLabeler()
        print(f"✅ Tool created: {tool.name}")
        
        print("\\n🎉 All tests passed! Your changes are active.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
"""
    
    with open("dev_test.py", "w") as f:
        f.write(test_script)
    
    print("📝 Created dev_test.py - run 'python dev_test.py' to test changes")

def show_development_tips():
    """Show development workflow tips."""
    print("\n💡 Development Workflow Tips:")
    print("=" * 40)
    print("1. Always use 'pip install -e .' for development")
    print("2. Run 'python dev_test.py' to test changes")
    print("3. Check installation mode with this script")
    print("4. If changes aren't reflected, restart Python interpreter")
    print("5. Use 'pip uninstall scriptcraft' before reinstalling")
    print("6. Keep this script handy for troubleshooting")

def main():
    """Main development workflow function."""
    print("🚀 ScriptCraft Development Workflow")
    print("=" * 50)
    
    # Check current state
    mode = check_installation_mode()
    pip_ok = check_pip_installation()
    
    print(f"\n📊 Current Status:")
    print(f"   Mode: {mode}")
    print(f"   Pip: {'✅ OK' if pip_ok else '❌ Issues'}")
    
    if mode == "development" and pip_ok:
        print("\n✅ You're in development mode! Changes should be reflected immediately.")
        
        # Test that everything works
        if test_development_changes():
            print("\n🎉 Development environment is working correctly!")
        else:
            print("\n⚠️ Some issues detected. Consider reinstalling.")
            
    else:
        print("\n⚠️ Not in development mode. Setting up...")
        if setup_development_mode():
            if test_development_changes():
                print("\n🎉 Development mode set up successfully!")
            else:
                print("\n❌ Setup completed but tests failed.")
        else:
            print("\n❌ Failed to set up development mode.")
    
    # Create test script
    create_test_script()
    
    # Show tips
    show_development_tips()

if __name__ == "__main__":
    main() 