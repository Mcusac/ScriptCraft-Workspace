# ScriptCraft Tool Distributable

This is a lightweight distributable package for ScriptCraft tools.

## 🚀 Quick Start

1. **Place your input files** in the `input/` folder
2. **Double-click `run.bat`**
3. **Check results** in the `output/` folder
4. **View logs** in the `logs/` folder

## 📁 Structure

```
distributable/
├── run.bat          # Main launcher (double-click this!)
├── run.py           # Python runner script
├── embed_py311/     # Embedded Python with scriptcraft
├── input/           # Place input files here
├── output/          # Results will appear here
├── logs/            # Log files
└── README.md        # This file
```

## 🔧 How It Works

- **Embedded Python**: Contains Python 3.11 with all required packages
- **Simple Launcher**: `run.bat` calls `run.py` which runs the tool automatically
- **No Configuration**: The tool automatically detects what to run

## 🐛 Troubleshooting

If you get errors:
1. Make sure the `embed_py311/` folder is present
2. Check that input files are in the `input/` folder
3. View the logs in `logs/run_log.txt`

## 📦 Package Information

- **Tool**: Automatically detected from package name
- **Python**: 3.11 (embedded)
- **Dependencies**: All included in embedded Python

---

*Built with ScriptCraft - Data Processing Framework*
