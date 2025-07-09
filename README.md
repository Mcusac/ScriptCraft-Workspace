# ScriptCraft Workspace

A comprehensive data processing and quality control workspace for research data workflows. This project provides both a **Python package for developers** and a **complete workspace for research teams**, featuring tools for data validation, processing pipelines, form automation, and package deployment.

## 🚀 Quick Start

### For New Users (Quick Setup)

1. **Clone and configure:**
   ```bash
   git clone https://github.com/mcusac/ScriptCraft-Workspace.git
   cd ScriptCraft-Workspace
   cp config_template.yaml config.yaml
   ```

2. **Edit `config.yaml`** with your settings (URLs, study name, etc.)

3. **Start using tools:**
   ```bash
   # Run data content comparison (all domains)
   python -m implementations.python-package.scriptcraft.tools.data_content_comparer.main --mode release_consistency
   
   # Run individual domain comparison
   python -m implementations.python-package.scriptcraft.tools.data_content_comparer.main --mode release_consistency --domain Clinical
   
   # Or use the workspace pipeline system
   python run_all.py --pipeline test
   ```

### Option 1: Install Python Package (Recommended for Developers)

```bash
# Install from GitHub
pip install git+https://github.com/mcusac/ScriptCraft-Workspace.git#subdirectory=implementations/python

# Or if published to PyPI
pip install scriptcraft
```

**Basic Usage:**
```python
from scriptcraft import setup_logger, Config, BaseTool, load_data

# Quick data processing setup
logger = setup_logger("my_project")
data = load_data("research_data.xlsx")

# Use specific tools
from scriptcraft.tools.rhq_form_autofiller import RHQFormAutofiller
rhq = RHQFormAutofiller()
rhq.run(input_paths=["patient_data.xlsx"])
```

### Option 2: Full Workspace Setup (Research Teams)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mcusac/ScriptCraft-Workspace.git
   cd ScriptCraft-Workspace
   ```

2. **Create your configuration:**
   ```bash
   cp config_template.yaml config.yaml
   ```

3. **Edit `config.yaml`** with your specific settings:
   - Update `study_name` with your study identifier
   - Modify `domains` list to match your data structure
   - Update URL templates and tool-specific settings
   - Configure paths if using non-standard directory structure

### 3. Data Organization (Workspace Mode)

Create your domain directories and data files:

```
domains/
├── Clinical/
│   ├── raw_data/
│   ├── processed_data/
│   ├── merged_data/
│   ├── old_data/
│   ├── dictionary/
│   ├── qc_logs/
│   └── qc_output/
├── Biomarkers/
├── Genomics/
└── Imaging/
```

### 4. Running Tools

**Python Package Mode:**
```python
import scriptcraft as sc

# Core utilities (most common usage)
logger = sc.setup_logger("analysis")
config = sc.Config.from_yaml("config.yaml")
data = sc.load_data("input.xlsx")

# Specialized tools
from scriptcraft.checkers import DictionaryDrivenChecker
checker = DictionaryDrivenChecker()
checker.run(input_paths=["data.xlsx"])
```

**Workspace Mode:**
```bash
# Data Content Comparison (Recommended)
python -m implementations.python-package.scriptcraft.tools.data_content_comparer.main --mode release_consistency
python -m implementations.python-package.scriptcraft.tools.data_content_comparer.main --mode release_consistency --domain Clinical

# Other Individual Tools
python -m implementations.python-package.scriptcraft.tools.rhq_form_autofiller.main
python -m implementations.python-package.scriptcraft.tools.dictionary_driven_checker.main

# Pipeline Execution  
python run_all.py --domain Clinical --pipeline data_quality
python run_all.py --pipeline full_processing

# Package Tools for Distribution
packaging.bat rhq_form_autofiller
```

## 🏗️ Project Architecture

ScriptCraft provides both a **Python package** for developers and a **complete workspace** for research teams.

### Python Package (`scriptcraft`)

The installable Python package provides:

- **`scriptcraft.common`** - Core utilities for data processing (most used)
- **`scriptcraft.tools`** - Standalone tools (RHQ Form Autofiller, Data Comparer, etc.)
- **`scriptcraft.checkers`** - Data validation and quality control
- **`scriptcraft.validators`** - Data integrity validation  
- **`scriptcraft.transformers`** - Data transformation utilities
- **`scriptcraft.enhancements`** - Data enhancement tools

### Workspace Components

- **`implementations/python/`** - Python package source code
- **`distributables/`** - Self-contained tool packages
- **`templates/`** - Development templates and examples
- **`tools/`** - Build and packaging utilities
- **`workspaces/`** - Example workspace configurations

### Pipeline System

The workspace includes a centralized pipeline system defined in `config.yaml`:

- **`data_preparation`** - Prepare and standardize data
- **`data_quality`** - Comprehensive validation and QC
- **`release_management`** - Release consistency and change tracking
- **`external_tools`** - Form filling and external integrations
- **`full_processing`** - Complete end-to-end processing

📖 **For Developers**: See [`docs/package_architecture.md`](docs/package_architecture.md) for detailed technical architecture, package boundaries, and development guidelines.

## 📊 Available Tools

### Data Processing
- **Data Content Comparer** - Compare data between releases
- **Date Format Standardizer** - Standardize date formats
- **Dictionary Cleaner** - Clean and validate data dictionaries

### Quality Control
- **Dictionary Driven Checker** - Validate data against dictionaries
- **MedVisit Integrity Validator** - Validate medical visit data integrity
- **Score Totals Checker** - Validate calculated scores and totals
- **Release Consistency Checker** - Check consistency across releases

### External Tools
- **RHQ Form Autofiller** - Automated residential history form filling
- **Automated Labeler** - Generate labels and documentation

### Research Enhancements
- **Dictionary Supplementer** - Enhance data dictionaries
- **Supplement Prepper** - Prepare data supplements
- **Supplement Splitter** - Split and organize supplements

## 🔧 Configuration

### Python Package Configuration
```python
from scriptcraft import Config

# Load from YAML
config = Config.from_yaml("config.yaml")

# Or from environment variables (for distributables)
config = Config.from_environment()
```

### Workspace Configuration
The `config.yaml` file controls all aspects of the workspace system:

```yaml
# Study-specific settings
study_name: YOUR_STUDY_NAME
domains: [Clinical, Biomarkers, Genomics, Imaging]

# Tool configurations
tools:
  tool_name:
    description: "Tool description with emoji"
    packages: [required, python, packages]
    
# Pipeline definitions
pipelines:
  pipeline_name:
    description: "Pipeline description"
    steps: [list of processing steps]
```

## 🔒 Security and Data Protection

This repository is configured to **exclude all sensitive data**:

- **`domains/`** - All domain data is gitignored
- **`input/`, `output/`, `logs/`** - Runtime directories are gitignored (with `.gitkeep` files to maintain structure)
- **`config.yaml`** - Your configuration file is gitignored
- **`config_template.yaml`** - Safe template for public repositories
- **`distributables/`** - Built packages are gitignored

Only the code structure and templates are tracked in git. The `config_template.yaml` provides a safe starting point for new users.

## 🛠️ Development

### Using the Python Package

```python
from scriptcraft import BaseTool

class MyTool(BaseTool):
    def run(self, **kwargs):
        self.log_start()
        # Custom tool logic
        self.log_completion()

# Use common utilities
from scriptcraft import setup_logger, load_data, ensure_output_dir
```

### Adding New Tools to Workspace

1. Create tool directory in appropriate category (`tools/`, `checkers/`, etc.)
2. Implement tool following the standard pattern
3. Add configuration to `config.yaml`
4. Update pipeline definitions if needed
5. Test and package

### Code Standards

- Follow PEP 8 with 4-space indentation
- Use type hints and Google-style docstrings
- Leverage `scriptcraft.common` utilities (DRY principle)
- Use emoji in log messages for readability
- Include proper error handling and logging

📖 **For Developers**: See [`docs/package_architecture.md`](docs/package_architecture.md) for detailed development guidelines, package structure, and architectural patterns.

## 📁 Directory Structure

```
ScriptCraft-Workspace/
├── implementations/
│   └── python/          # Python package source
│       └── scriptcraft/ # Installable package
├── distributables/      # Self-contained tool packages (gitignored)
├── templates/           # Development templates
├── tools/               # Build and packaging utilities
├── domains/             # Domain data directories (gitignored, with .gitkeep)
├── input/               # Input data directory (gitignored, with .gitkeep)
├── output/              # Output directory (gitignored, with .gitkeep)
├── logs/                # Logs directory (gitignored, with .gitkeep)
├── config.yaml          # Main configuration (gitignored)
├── config_template.yaml # Safe configuration template
└── README.md            # This file
```

## 📦 Installation Options

### For Python Developers
```bash
# Basic installation
pip install scriptcraft

# With web automation tools
pip install scriptcraft[web]

# Development installation
pip install scriptcraft[dev]

# All features
pip install scriptcraft[all]
```

### For Research Teams
```bash
# Clone the full workspace
git clone https://github.com/mcusac/ScriptCraft-Workspace.git
cd ScriptCraft-Workspace

# Install Python package in development mode
cd implementations/python
pip install -e .
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly (both package and workspace modes)
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- **Repository:** https://github.com/mcusac/ScriptCraft-Workspace
- **Issues:** https://github.com/mcusac/ScriptCraft-Workspace/issues
- **Documentation:** https://github.com/mcusac/ScriptCraft-Workspace/wiki 