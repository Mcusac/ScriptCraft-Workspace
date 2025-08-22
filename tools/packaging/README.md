# ScriptCraft Modular Packaging System

This modular packaging system creates lightweight distributables for ScriptCraft tools that can be distributed to users without Python knowledge.

## 🚀 Quick Start

```bash
# Full packaging (builds common Python + packages tool)
tools\packaging\package_all.bat

# Quick packaging (uses existing common Python)
tools\packaging\package_quick.bat
```

## 📁 System Structure

```
tools/packaging/
├── package_all.bat              # Full packaging (includes Component 0)
├── package_quick.bat            # Quick packaging (skips Component 0)
├── 00_build_common_python.bat   # Component 0: Build common Python (run once)
├── 01_build_python.bat          # Component 1: Check Python environment
├── 02_setup_template.bat        # Component 2: Setup distributable template
├── 03_test_distributable.bat    # Component 3: Test the distributable
└── config_processor.py          # Configuration processor utility

data/
└── logs/                        # Centralized logs folder (all component logs here)
```

## 🔧 Components

### Component 0: Build Common Python (`00_build_common_python.bat`)
- **Run once** to build common embedded Python with all common packages
- Extracts Python 3.11 embedded
- Installs pip, setuptools, wheel
- Installs common packages from `config.yaml` (packaging.common_packages)
- Installs/updates ScriptCraft package (common package for all distributables)
- Generates tool-specific config.bat from config.yaml
- Verifies ScriptCraft installation and shows version
- Fixes common issues (distutils-precedence.pth)
- Copies to template directory for reuse

### Component 1: Check Python Environment (`01_build_python.bat`)
- Checks if common Python exists in template
- Installs tool-specific packages (if any) from `config.yaml`
- Validates Python environment is ready

### Component 2: Setup Template (`02_setup_template.bat`)
- Copies distributable template
- Copies embedded Python with all packages
- Generates tool-specific `run.bat`
- Copies tool-specific README
- Creates proper directory structure

### Component 3: Test Distributable (`03_test_distributable.bat`)
- Tests Python version
- Tests core package imports (pandas, pyyaml, openpyxl)
- Tests ScriptCraft package imports
- Tests tool-specific imports
- Tests module execution
- Validates directory structure

## 📦 What Gets Created

```
distributables/tool_name_distributable/
├── embed_py311/          # Complete Python with all common packages + ScriptCraft
├── input/                # User puts files here
├── output/               # Results appear here
├── logs/                 # Log files
├── run.bat               # User double-clicks this
└── README.md             # User instructions
```

## 🎯 For End Users

1. **Double-click `run.bat`**
2. **That's it!** No Python knowledge needed
3. **All dependencies included** in embedded Python

## 🛠️ Individual Component Testing

You can test each component individually:

```bash
# Build common Python (run once)
tools\packaging\00_build_common_python.bat

# Test Component 1 only
tools\packaging\01_build_python.bat

# Test Component 2 only
tools\packaging\02_setup_template.bat

# Test Component 3 only
tools\packaging\03_test_distributable.bat
```

## ⚡ Quick vs Full Packaging

### Quick Packaging (`package_quick.bat`)
- **Speed**: ⚡ Very fast (skips Component 0)
- **Use when**: Common Python already exists
- **What it does**: Components 1, 2, 3 only
- **Time**: ~30 seconds

### Full Packaging (`package_all.bat`)
- **Speed**: 🐌 Slower (includes Component 0)
- **Use when**: First time, ScriptCraft updates, or missing common Python
- **What it does**: All components (0, 1, 2, 3)
- **Time**: ~5-10 minutes

## 📋 Configuration

### Tool Selection
Set the tool to package in `config.yaml`:
```yaml
packaging:
  tool_to_ship: "rhq_form_autofiller"
```

### Common Packages
Edit `config.yaml` under `packaging.common_packages` to add/remove packages for all tools.

### Tool-Specific Packages
Tool-specific packages are defined in `config.yaml` under each tool's configuration.

## 🐛 Troubleshooting

### Component 0 Fails
- Check that `embed_py311.zip` exists in `py_embed_setup/` (at workspace root)
- Verify internet connection for pip downloads
- Check log: `data/logs/00_build_common_python.txt`

### Component 1 Fails
- Ensure Component 0 completed successfully
- Check that common Python exists in template
- Check log: `data/logs/01_build_python.txt`

### Component 2 Fails
- Ensure Component 1 completed successfully
- Check that distributable template exists
- Check log: `data/logs/02_setup_template.txt`

### Component 3 Fails
- Ensure Components 1 and 2 completed successfully
- Check that ScriptCraft package is properly installed
- Check log: `data/logs/03_test_distributable.txt`

## 📊 Benefits

- **Modular**: Each component has a single responsibility
- **Debuggable**: Easy to see which step failed
- **Maintainable**: Can update individual components
- **Testable**: Can test each component independently
- **Scalable**: Easy to add new tools or requirements

## 🔄 Workflow

### First Time Setup:
1. **Set tool in config.yaml**
2. **Run `package_all.bat`** (builds common Python + packages tool)
3. **Check logs in `data/logs/` if any component fails**
4. **Distribute the created package**

### Subsequent Packaging:
1. **Set tool in config.yaml**
2. **Run `package_quick.bat`** (uses existing common Python - much faster!)
3. **Check logs in `data/logs/` if any component fails**
4. **Distribute the created package**

### When to Use Each:

- **`package_all.bat`**: First time, after ScriptCraft updates, or when common Python is missing
- **`package_quick.bat`**: Regular packaging when common Python already exists

## 🔄 ScriptCraft Updates

ScriptCraft is automatically updated as part of Component 0:

- **Automatic**: Component 0 always installs latest ScriptCraft with `--force-reinstall`
- **Version Check**: Shows ScriptCraft version after installation
- **Verification**: Confirms ScriptCraft import works after installation

---

*Built with ScriptCraft - Data Processing Framework*
