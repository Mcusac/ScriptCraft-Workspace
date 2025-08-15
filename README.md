# ScriptCraft Workspace

A comprehensive data processing and quality control workspace for research workflows, featuring automated tools, validation frameworks, and pipeline orchestration.

## 🚀 Overview

ScriptCraft provides a unified framework for data processing, quality control, and automation in research environments. Built with scalability and reusability in mind, it offers:

- **🔧 Automated Tools**: Data validation, cleaning, comparison, and form automation
- **📊 Quality Control**: Comprehensive validation frameworks with plugin support
- **🔄 Pipeline Orchestration**: Multi-step workflows for complex data processing
- **📦 Packaging System**: Easy distribution of tools to end users
- **🎯 Research Focus**: Specialized tools for clinical and biomarker data processing

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

### Workflows
- **Dictionary Workflow**: Complete dictionary processing pipeline

## 🚀 Quick Start

### Using Individual Tools

```python
import scriptcraft.common as cu
from scriptcraft.tools import DataContentComparer

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
from scriptcraft.pipelines import run_pipeline

# Run a complete workflow
run_pipeline("dictionary_pipeline", {
    "dictionary": "dictionary.xlsx",
    "raw_data": "data.csv"
})
```

### Command Line Usage

```bash
# Run a specific tool
python -m scriptcraft.tools.data_content_comparer input1.csv input2.csv

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

Tools can be packaged for distribution using the built-in packaging system:

```bash
# Package a tool for distribution
packaging.bat

# The packaged tool will be available in distributables/
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