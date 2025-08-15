# ScriptCraft Tool Distributable

This is a streamlined distributable package for ScriptCraft tools.

## 🚀 Quick Start

1. **Place your input files** in the `input/` folder
2. **Run the tool** by double-clicking `run.bat`
3. **Check results** in the `output/` folder
4. **View logs** in the `logs/` folder

## 📁 Structure

```
distributable/
├── run.bat          # Main launcher
├── run.py           # Python runner script
├── embed_py311/     # Embedded Python with scriptcraft
├── input/           # Place input files here
├── output/          # Results will appear here
├── logs/            # Log files
└── README.md        # This file
```

## 🔧 How It Works

- **Embedded Python**: Contains Python 3.11 with the `scriptcraft` package pre-installed
- **Simple Launcher**: `run.bat` calls `run.py` which imports and runs the tool from the PyPI package
- **No Configuration**: The tool automatically detects what to run based on the package structure

## 🐛 Troubleshooting

If you get import errors:
1. Make sure the `embed_py311/` folder is present
2. Check that `scriptcraft` is installed: `embed_py311\python.exe -m pip show scriptcraft`
3. View the logs in `logs/run_log.txt`

## 📦 Package Information

- **Tool**: Automatically detected from package structure
- **Python**: 3.11 (embedded)
- **ScriptCraft**: Latest version from PyPI
- **Dependencies**: All included in embedded Python

---

*Built with ScriptCraft - Data Processing Framework*
