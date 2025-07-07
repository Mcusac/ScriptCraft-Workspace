# 🚀 ScriptCraft Development Workflow Guide

## Overview

This guide explains how to manage development vs production environments when working with ScriptCraft. The key is ensuring you're testing your development changes, not the installed version.

## ✅ Current Status: Development Mode Active

Your environment is correctly set up for development:
- ✅ Using editable pip installation (`pip install -e .`)
- ✅ Pointing to development directory
- ✅ Changes are reflected immediately

## 🔧 Development Workflow

### 1. **Verify You're in Development Mode**

Run this to check your installation:
```bash
python dev_workflow.py
```

You should see:
```
✅ Using DEVELOPMENT installation (editable)
✅ Installation is editable (development mode)
```

### 2. **Test Your Changes**

After making changes to the code, run:
```bash
python dev_test.py
```

This verifies that your changes are active and working.

### 3. **Quick Development Test**

For even faster testing, you can run:
```python
python -c "import scriptcraft; print('Changes are active!')"
```

## 🚨 Common Issues & Solutions

### Issue: Changes Not Reflected
**Symptoms**: You modify code but see old behavior

**Solutions**:
1. **Restart Python interpreter** - Python caches imports
2. **Check installation mode**: `python dev_workflow.py`
3. **Reinstall if needed**: `pip install -e . --force-reinstall`

### Issue: Wrong Version Being Used
**Symptoms**: Code points to site-packages instead of development

**Solutions**:
1. **Uninstall production version**: `pip uninstall scriptcraft`
2. **Reinstall in editable mode**: `pip install -e .`
3. **Verify path**: `python -c "import scriptcraft; print(scriptcraft.__file__)"`

### Issue: Import Conflicts
**Symptoms**: Import errors or wrong modules loaded

**Solutions**:
1. **Clear Python cache**: Delete `__pycache__` directories
2. **Restart Python interpreter**
3. **Check PYTHONPATH**: Ensure it's not pointing to wrong locations

## 📋 Development Checklist

Before starting development:
- [ ] Run `python dev_workflow.py` to verify development mode
- [ ] Run `python dev_test.py` to verify everything works
- [ ] Make your changes
- [ ] Run `python dev_test.py` again to test changes
- [ ] If issues, restart Python interpreter

## 🔄 Production vs Development

### Development Mode (Current)
- Uses `pip install -e .` (editable)
- Points to your development directory
- Changes reflected immediately
- Good for active development

### Production Mode
- Uses `pip install scriptcraft` (regular install)
- Installs to site-packages
- Changes require reinstallation
- Good for end users

## 🛠️ Switching Between Modes

### To Development Mode:
```bash
pip uninstall scriptcraft -y
pip install -e .
python dev_workflow.py  # Verify
```

### To Production Mode:
```bash
pip uninstall scriptcraft -y
pip install scriptcraft
```

## 📝 Best Practices

1. **Always use development mode** when actively developing
2. **Test changes immediately** after making them
3. **Keep dev_test.py handy** for quick verification
4. **Restart Python interpreter** if changes aren't reflected
5. **Use version control** to track your changes
6. **Test in production mode** before releasing

## 🎯 For Your Specific Concern

**Your worry**: "Will there be an issue when I am testing new things in the common folder but I am overriding it with the latest version on pip?"

**Answer**: No, because:
1. You're using `pip install -e .` (editable mode)
2. This creates a link to your development directory
3. Python loads from your development files, not site-packages
4. Changes are reflected immediately

**To verify**: Run `python dev_test.py` after making changes - if it works, you're testing your development version.

## 🚀 Next Steps

1. **Continue development** - your setup is correct
2. **Use dev_test.py** for quick verification
3. **Run dev_workflow.py** if you have issues
4. **Move to v2.0.0 roadmap items** - pip installation is working!

Your development environment is properly configured and ready for active development! 🎉 