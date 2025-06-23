# 📦 Shippable Package Template

This template provides the base structure for creating shippable packages. It contains only the essential directory structure and batch files needed for deployment.

## 📁 Directory Structure

- `input/` - Directory for input files
- `output/` - Directory for output files
- `logs/` - Directory for log files
- `run.bat` - Main execution script
- `import_embed.bat` - Script for embedding dependencies

## 🚀 Usage

1. This template is used by the packaging process
2. The actual tool code and dependencies will be copied here during packaging
3. Do not modify the contents of this template directly

## ⚠️ Important Notes

- The `scripts` directory will be populated during packaging
- All dependencies will be embedded during the packaging process
- Batch files are configured for standalone execution 