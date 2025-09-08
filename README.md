# ScriptCraft Workspace

A comprehensive data processing and quality control workspace for research workflows, featuring automated tools, validation frameworks, and pipeline orchestration.

## 🚀 Overview

ScriptCraft provides a unified framework for data processing, quality control, and automation in research environments. Built with scalability and reusability in mind, it offers:

- **🔧 Automated Tools**: Data validation, cleaning, comparison, and form automation
- **📊 Quality Control**: Comprehensive validation frameworks with plugin support
- **🔄 Pipeline Orchestration**: Multi-step workflows for complex data processing
- **📦 Packaging System**: Easy distribution of tools to end users
- **🎯 Research Focus**: Specialized tools for clinical and biomarker data processing
- **🚀 Release Management**: Automated PyPI and Git release workflows
- **⚙️ Config-Driven**: Single source of truth configuration system

## 🛡️ Security & Privacy

This workspace is designed with security and privacy in mind:

- **🔒 Data Protection**: All sensitive research data is excluded from version control
- **📁 Safe Structure**: Directory structure maintained without actual data files
- **⚙️ Generic Configuration**: No institution-specific URLs or credentials
- **🧪 Template-Based**: Uses sample data and placeholder configurations

**Important**: This repository contains only the framework and tools. Actual research data, credentials, and institution-specific configurations are excluded via `.gitignore`.

## 📦 Installation

### Prerequisites
- Python 3.8+
- Git

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/ScriptCraft-Workspace.git
cd ScriptCraft-Workspace

# Install the Python package
cd implementations/python-package
pip install -e .
```

## 🧰 Available Tools

### Data Processing
- **Data Content Comparer**: Compare datasets for consistency and changes
- **Dictionary Cleaner**: Clean and standardize dictionary files
- **Date Format Standardizer**: Standardize date formats across datasets
- **Schema Detector**: Automatic schema detection and validation

### Quality Control
- **Dictionary Validator**: Validate dictionary structures and content
- **Dictionary Driven Checker**: Check data against dictionary definitions
- **MedVisit Integrity Validator**: Validate medical visit data integrity
- **Score Totals Checker**: Validate score calculations and totals

### Automation
- **RHQ Form Autofiller**: Automate form filling for research questionnaires
- **Automated Labeler**: Generate labels and documentation from schemas
- **Feature Change Checker**: Track feature changes across releases

### Release Management
- **PyPI Release Tool**: Automated PyPI package testing and release
- **Git Workspace Tool**: Git repository management and operations
- **Git Submodule Tool**: Git submodule synchronization and management
- **Generic Release Tool**: Flexible release workflow orchestration

### Workflows
- **Dictionary Workflow**: Complete dictionary processing pipeline

## 🚀 Quick Start

### Using Individual Tools

```python
import scriptcraft.common as cu
from scriptcraft.tools.data_content_comparer import DataContentComparer

# Initialize tool
comparer = DataContentComparer()

# Process data
comparer.run(
    input_paths=["data1.csv", "data2.csv"],
    output_dir="output/"
)
```

### Using Pipelines

```python
from scriptcraft.pipelines.git_pipelines import create_pypi_test_pipeline

# Create and run a pipeline
pipeline = create_pypi_test_pipeline()
pipeline.run()
```

### Command Line Usage

#### Industry-Standard CLI (Recommended)
```bash
# List available tools and pipelines
scriptcraft list

# Run a specific tool
scriptcraft data_content_comparer

# Run a pipeline
scriptcraft dictionary_pipeline

# Use release CLI
scriptcraft-release pypi-test
scriptcraft-release git-sync

# Use release manager directly (RECOMMENDED)
python -c "from scriptcraft.tools.release_manager import ReleaseManager; ReleaseManager().run(mode='python_package', version_type='patch', auto_push=True)"

# See docs/RELEASE_USAGE_GUIDE.md for comprehensive release examples
```

#### Legacy run_all.py (Still Supported)
```bash
# Run a specific tool
python run_all.py --tool data_content_comparer

# Run a pipeline
python run_all.py --pipeline dictionary_pipeline
```

## 📁 Project Structure

```
ScriptCraft-Workspace/
├── implementations/python-package/  # Main Python package
│   └── scriptcraft/
│       ├── common/                  # Shared utilities
│       ├── tools/                   # Individual tools
│       └── pipelines/               # Pipeline orchestration
├── data/                           # Workspace data (gitignored)
│   ├── domains/                    # Domain-specific data
│   ├── input/                      # Input files
│   ├── output/                     # Output files
│   └── logs/                       # Log files
├── templates/                      # Tool templates
├── distributables/                 # Packaged tools
└── config.yaml                     # Central configuration
```

## 🔧 Configuration

The workspace uses a centralized configuration system in `config.yaml`:

```yaml
# Example configuration
workspaces:
  data:
    study_name: "RESEARCH_STUDY"
    domains: ["Clinical", "Biomarkers", "Genomics", "Imaging"]
    id_columns: ["Med_ID", "Visit_ID"]

tools:
  data_content_comparer:
    description: "📊 Compares data content between releases"
    packages: [pandas, numpy, openpyxl]
```

## 📦 Packaging & Distribution

ScriptCraft provides multiple distribution methods:

### PyPI Distribution
```bash
# Install from PyPI
pip install scriptcraft-python

# Use CLI commands
scriptcraft-release pypi-test
scriptcraft rhq_form_autofiller

# Use release manager for version bumps
python -c "from scriptcraft.tools.release_manager import ReleaseManager; ReleaseManager().run(mode='python_package', version_type='patch', auto_push=True)"
```

### Local Packaging
```bash
# Package a tool for distribution
python run_all.py --tool rhq_form_autofiller

# The packaged tool will be available in distributables/
```

### Development Installation
```bash
# Install in development mode
cd implementations/python-package
pip install -e .
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest

# Run specific test categories
python -m pytest tests/unit/
python -m pytest tests/integration/
```

## 📚 Documentation

- **Tool Documentation**: See individual tool README files in `implementations/python-package/scriptcraft/tools/`
- **API Reference**: Available in the main package documentation
- **Examples**: Check the `templates/` directory for usage examples

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for details on:

- Code style and standards
- Testing requirements
- Documentation updates
- Security considerations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ScriptCraft-Workspace/issues)
- **Documentation**: See the `docs/` directory for detailed documentation
- **PyPI Package**: [scriptcraft](https://pypi.org/project/scriptcraft/)

## 🙏 Acknowledgments

- Built for the research community
- Developed with support from research institutions
- Thanks to all contributors and users

---

**ScriptCraft Workspace** - Making research data processing easier, one tool at a time. 🚀 