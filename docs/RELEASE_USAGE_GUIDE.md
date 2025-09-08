# ScriptCraft Release Usage Guide

## 🎯 **Tested and Working Release Patterns**

This guide contains **tested and verified** release patterns that work correctly with the current ScriptCraft release system.

---

## 🚀 **Quick Start - Most Common Use Cases**

### **1. Standard Patch Release (Most Common)**
```bash
# From workspace root or python-package directory
python -c "from scriptcraft.tools.release_manager import ReleaseManager; ReleaseManager().run(mode='python_package', version_type='patch', auto_push=True)"
```
**What this does:**
- ✅ Bumps version (e.g., 1.6.0 → 1.6.1)
- ✅ Updates `_version.py`
- ✅ Builds package
- ✅ Uploads to PyPI
- ✅ Commits with message: "🐛 Bug Fix Release: ScriptCraft Python v1.6.1"
- ✅ Creates git tag v1.6.1
- ✅ Pushes commits and tags to remote

### **2. Minor Release (New Features)**
```bash
python -c "from scriptcraft.tools.release_manager import ReleaseManager; ReleaseManager().run(mode='python_package', version_type='minor', auto_push=True)"
```
**What this does:**
- ✅ Bumps version (e.g., 1.6.0 → 1.7.0)
- ✅ Uses commit message: "✨ Feature Release: ScriptCraft Python v1.7.0"

### **3. Major Release (Breaking Changes)**
```bash
python -c "from scriptcraft.tools.release_manager import ReleaseManager; ReleaseManager().run(mode='python_package', version_type='major', auto_push=True)"
```
**What this does:**
- ✅ Bumps version (e.g., 1.6.0 → 2.0.0)
- ✅ Uses commit message: "🚀 Major Release: ScriptCraft Python v2.0.0"

---

## 🔧 **Advanced Usage Patterns**

### **4. Custom Commit Message**
```bash
python -c "from scriptcraft.tools.release_manager import ReleaseManager; ReleaseManager().run(mode='python_package', version_type='patch', auto_push=True, custom_message='🔧 Fix: Resolved Unicode encoding issues in subprocess calls')"
```

### **5. Git-Only Release (Skip PyPI)**
```bash
python -c "from scriptcraft.tools.release_manager import ReleaseManager; ReleaseManager().run(mode='python_package', version_type='patch', auto_push=True, skip_pypi=True)"
```
**Use this when:**
- You want to tag a version without uploading to PyPI
- Testing release process
- Internal versioning

### **6. Re-upload Existing Version to PyPI**
```bash
python -c "from scriptcraft.tools.release_manager import ReleaseManager; ReleaseManager().run(mode='pypi')"
```
**Use this when:**
- PyPI upload failed but git operations succeeded
- Need to re-upload same version

---

## 📍 **Where to Run Commands**

### **From Workspace Root** (Recommended)
```bash
cd /path/to/ScriptCraft-Workspace
python -c "from scriptcraft.tools.release_manager import ReleaseManager; ReleaseManager().run(mode='python_package', version_type='patch', auto_push=True)"
```

### **From Python Package Directory**
```bash
cd /path/to/ScriptCraft-Workspace/implementations/python-package
python -c "from scriptcraft.tools.release_manager import ReleaseManager; ReleaseManager().run(mode='python_package', version_type='patch', auto_push=True)"
```

**Both locations work correctly** - the release manager automatically detects the correct paths.

---

## ⚠️ **Critical Parameters**

### **`auto_push=True` (REQUIRED)**
**Always include this parameter!** Without it:
- ❌ Commits are created locally but not pushed
- ❌ Tags are created locally but not pushed
- ❌ Remote repository won't be updated

### **`version_type` (REQUIRED)**
Must be one of:
- `patch` - Bug fixes (1.6.0 → 1.6.1)
- `minor` - New features (1.6.0 → 1.7.0)
- `major` - Breaking changes (1.6.0 → 2.0.0)

---

## 🎯 **Release Workflow Examples**

### **Complete Release Workflow**
```bash
# 1. Make your changes
# 2. Test your changes
# 3. Run release
python -c "from scriptcraft.tools.release_manager import ReleaseManager; ReleaseManager().run(mode='python_package', version_type='patch', auto_push=True)"

# 4. Verify on PyPI
pip install scriptcraft-python --upgrade

# 5. Verify on GitHub
# Check: https://github.com/Mcusac/ScriptCraft-Python/releases
```

### **Emergency Hotfix Workflow**
```bash
# 1. Create hotfix branch
git checkout -b hotfix/critical-bug

# 2. Make critical fix
# ... make changes ...

# 3. Release immediately
python -c "from scriptcraft.tools.release_manager import ReleaseManager; ReleaseManager().run(mode='python_package', version_type='patch', auto_push=True, custom_message='🚨 Hotfix: Critical bug fix')"

# 4. Merge back to main
git checkout main
git merge hotfix/critical-bug
git push origin main
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
