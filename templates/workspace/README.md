# ScriptCraft Workspace Template

This template provides the basic structure for a ScriptCraft workspace.

## 📁 Directory Structure

```
workspace/
├── config.yaml           # Workspace configuration (copy from config_template.yaml)
├── domains/              # Domain-specific data (gitignored)
├── input/                # Input files for processing (gitignored)
├── output/               # Generated output files (gitignored)
├── logs/                 # Tool execution logs (gitignored)
└── README.md            # This file
```

## 🚀 Getting Started

1. **Copy this template** to create a new workspace:
   ```bash
   cp -r templates/workspace workspaces/my-new-project
   ```

2. **Configure your workspace**:
   ```bash
   cd workspaces/my-new-project
   cp config_template.yaml config.yaml
   # Edit config.yaml with your specific settings
   ```

3. **Add your data**:
   - Place domain data in `domains/`
   - Add input files to `input/`
   - Logs and output will be generated automatically

4. **Run tools** from the ScriptCraft root:
   ```bash
   cd ../../  # Back to ScriptCraft root
   python run_all.py --config workspaces/my-new-project/config.yaml --pipeline data_quality
   ```

## 📝 Configuration

Edit `config.yaml` to customize:
- Study name and domains
- Tool-specific settings
- Pipeline definitions
- Logging preferences

## 🔒 Security Note

The `domains/`, `input/`, `output/`, and `logs/` directories are gitignored to protect sensitive data. Only the structure and configuration templates are tracked in git. 