# ScriptCraft Release Usage Guide

## 🎯 **Tested and Working Release Patterns**

This guide contains **tested and verified** release patterns that work correctly with the current ScriptCraft release system.

---

## 🚀 **Quick Start - Industry Standard Console Commands**

### **1. Git Operations (Most Common)**
```bash
# Check git status
python -m scriptcraft.cli.release_cli git-status

# Fully automated git sync (commits + pushes)
python -m scriptcraft.cli.release_cli git-sync
```
**What git-sync does:**
- ✅ Syncs submodules automatically
- ✅ Commits any uncommitted changes
- ✅ Pushes commits and tags to remote
- ✅ Works in any git repository

### **2. PyPI Operations**
```bash
# Test PyPI upload (safe testing)
python -m scriptcraft.cli.release_cli pypi-test

# Release to PyPI (production)
python -m scriptcraft.cli.release_cli pypi-release
```
**What pypi-release does:**
- ✅ Builds package automatically
- ✅ Uploads to PyPI
- ✅ Creates git tags
- ✅ Pushes to remote

### **3. Full Release Workflow**
```bash
# Complete release (PyPI + Git)
python -m scriptcraft.cli.release_cli full-release
```
**What full-release does:**
- ✅ Tests PyPI upload first
- ✅ Releases to PyPI
- ✅ Syncs git repository
- ✅ Complete automated workflow

---

## 🔧 **Advanced Usage Patterns**

### **4. Using Pipelines (Alternative)**
```bash
# Use pipeline instead of individual tools
scriptcraft-release pypi-test --pipeline
scriptcraft-release git-sync --pipeline
```

### **5. Python API (For Custom Scripts)**
```python
# For custom automation scripts
from scriptcraft.tools.git_workspace_tool import GitWorkspaceTool
from scriptcraft.tools.pypi_release_tool import PyPIReleaseTool

# Git operations
git_tool = GitWorkspaceTool()
git_tool.run(operation="sync")

# PyPI operations
pypi_tool = PyPIReleaseTool()
pypi_tool.run(operation="test")
```

### **6. Legacy Release Manager (Still Supported)**
```bash
# For complex version management
python -c "from scriptcraft.tools.release_manager import ReleaseManager; ReleaseManager().run(mode='python_package', version_type='patch', auto_push=True)"
```
**Use this when:**
- You need specific version bumping
- Custom commit messages
- Complex release workflows

---

## 📍 **Where to Run Commands**

### **From Any Git Repository** (Industry Standard)
```bash
# Navigate to any git repository
cd /path/to/your/project

# Install ScriptCraft (one time)
pip install scriptcraft-python

# Use console commands anywhere
scriptcraft-release git-sync
scriptcraft-release pypi-test
```

### **From ScriptCraft Workspace**
```bash
cd /path/to/ScriptCraft-Workspace
scriptcraft-release git-sync
scriptcraft-release pypi-release
```

**Console commands work everywhere** - they automatically detect the project structure.

---

## ⚠️ **Important Notes**

### **Console Commands are Fully Automated**
**No parameters needed!** Console commands automatically:
- ✅ Commit and push changes
- ✅ Handle version management
- ✅ Sync submodules
- ✅ Upload to PyPI

### **Installation Required**
```bash
# Install ScriptCraft globally
pip install scriptcraft-python

# Commands work in any directory after installation
scriptcraft-release --help
```

---

## 🎯 **Release Workflow Examples**

### **Complete Release Workflow**
```bash
# 1. Make your changes
# 2. Test your changes
# 3. Sync git changes
scriptcraft-release git-sync

# 4. Test PyPI upload
scriptcraft-release pypi-test

# 5. Release to PyPI
scriptcraft-release pypi-release

# 6. Verify on PyPI
pip install scriptcraft-python --upgrade
```

### **Simple Git Sync Workflow**
```bash
# For any git repository (most common use case)
cd /path/to/your/project
scriptcraft-release git-sync
```

### **Full Release Workflow**
```bash
# Complete automated release
scriptcraft-release full-release
```

---

## 🔍 **Verification Steps**

After running a release, verify:

### **1. Git Operations**
```bash
git log --oneline -3
# Should show your release commit with proper message

git tag -l | tail -3
# Should show your new tag

git status
# Should be clean
```

### **2. PyPI Upload**
```bash
pip install scriptcraft-python --upgrade
# Should install your new version

pip show scriptcraft-python
# Should show correct version
```

### **3. GitHub Release**
- Visit: https://github.com/Mcusac/ScriptCraft-Python/releases
- Should see new release with tag

---

## 🚨 **Troubleshooting**

### **"Path not found" Error**
**Problem**: `[WinError 3] The system cannot find the path specified: 'implementations\\python-package'`

**Solution**: This was fixed! The release manager now correctly detects when you're already in the python-package directory.

### **"No changes to commit" Warning**
**Problem**: Release manager says no changes to commit

**Solution**: 
```bash
# Check what changes exist
git status
git diff

# If you have changes, use --force
python -c "from scriptcraft.tools.release_manager import ReleaseManager; ReleaseManager().run(mode='python_package', version_type='patch', auto_push=True, force=True)"
```

### **PyPI Upload Fails**
**Problem**: Git operations succeed but PyPI upload fails

**Solution**:
```bash
# Re-upload to PyPI only
python -c "from scriptcraft.tools.release_manager import ReleaseManager; ReleaseManager().run(mode='pypi')"
```

### **Forgot to Push**
**Problem**: Release succeeded but forgot `auto_push=True`

**Solution**:
```bash
# Push manually
git push origin main
git push origin v1.6.1  # Replace with your tag
```

---

## 📊 **Release History**

| Version | Type | Date | Notes |
|---------|------|------|-------|
| v1.6.1 | patch | 2025-01-02 | Fixed path resolution in release manager |
| v1.6.0 | minor | Previous | Previous stable version |

---

## 🎉 **Best Practices**

1. **Always use `auto_push=True`** - Don't forget to push changes
2. **Test before releasing** - Make sure your changes work
3. **Use descriptive commit messages** - The default messages are good, but custom ones are better for specific fixes
4. **Verify after release** - Check PyPI and GitHub
5. **Use patch for bug fixes** - Reserve minor/major for significant changes
6. **Run from workspace root** - More reliable path detection

---

## 🔗 **Related Documentation**

- [Release Manager README](implementations/python-package/scriptcraft/tools/release_manager/README.md)
- [Main README](README.md)
- [Package README](implementations/python-package/README.md)
- [Tool Usage Strategies](TOOL_USAGE_STRATEGIES.md)

---

*This guide contains tested and verified patterns. All examples have been tested and work correctly with the current ScriptCraft release system.*
