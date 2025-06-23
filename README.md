# Release Workspace

A comprehensive data processing and quality control workspace for research data releases. This project provides tools for data validation, processing pipelines, form automation, and package deployment.

## 🚀 Quick Start

### 1. Initial Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd release-workspace
   ```

2. **Create your configuration:**
   ```bash
   cp sample_config.yaml config.yaml
   ```

3. **Edit `config.yaml`** with your specific settings:
   - Update `study_name` with your study identifier
   - Modify `domains` list to match your data structure
   - Update URL templates and tool-specific settings
   - Configure paths if using non-standard directory structure

### 2. Data Organization

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

### 3. Running Tools

**Individual Tools:**
```bash
python -m scripts.tools.data_content_comparer
python -m scripts.checkers.dictionary_driven_checker
```

**Pipeline Execution:**
```bash
python run_all.py --domain Clinical --pipeline data_quality
python run_all.py --pipeline full_processing
```

**Package Tools for Distribution:**
```bash
packaging.bat rhq_form_autofiller
```

## 🏗️ Project Architecture

### Core Components

- **`scripts/common/`** - Shared utilities and common functionality
- **`scripts/tools/`** - Standalone data processing tools
- **`scripts/checkers/`** - Data validation and quality control tools
- **`scripts/transformers/`** - Data transformation utilities
- **`scripts/validators/`** - Data integrity validators
- **`scripts/pipelines/`** - Pipeline orchestration system

### Pipeline System

The project uses a centralized pipeline system defined in `config.yaml`:

- **`data_preparation`** - Prepare and standardize data
- **`data_quality`** - Comprehensive validation and QC
- **`release_management`** - Release consistency and change tracking
- **`external_tools`** - Form filling and external integrations
- **`full_processing`** - Complete end-to-end processing

### Tool Packaging

Tools can be packaged into self-contained distributions with embedded Python:

1. Configure tool in `config.yaml`
2. Run `packaging.bat <tool_name>`
3. Find packaged tool in `shippables/` directory

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

## 🔧 Configuration

The `config.yaml` file controls all aspects of the system:

### Key Configuration Sections

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
- **`input/`, `output/`, `logs/`** - Runtime directories are gitignored
- **`config.yaml`** - Your configuration file is gitignored
- **`shippables/`** - Built packages are gitignored

Only the code structure and templates are tracked in git.

## 🛠️ Development

### Adding New Tools

1. Create tool directory in appropriate category (`tools/`, `checkers/`, etc.)
2. Implement tool following the standard pattern
3. Add configuration to `config.yaml`
4. Update pipeline definitions if needed
5. Test and package

### Code Standards

- Follow PEP 8 with 4-space indentation
- Use type hints and Google-style docstrings
- Leverage `scripts.common` utilities (DRY principle)
- Use emoji in log messages for readability
- Include proper error handling and logging

### Testing

```bash
# Run individual tool tests
python -m pytest scripts/tests/tools/

# Run integration tests
python -m pytest scripts/tests/integration/

# Test pipeline execution
python run_all.py --pipeline test
```

## 📁 Directory Structure

```
Release Workspace/
├── scripts/           # Main codebase
│   ├── common/       # Shared utilities
│   ├── tools/        # Data processing tools
│   ├── checkers/     # Validation tools
│   ├── transformers/ # Data transformation
│   ├── validators/   # Data integrity
│   └── pipelines/    # Pipeline system
├── domains/          # Domain-specific data (gitignored)
├── input/            # Input files (gitignored)
├── output/           # Output files (gitignored)
├── logs/             # Log files (gitignored)
├── shippables/       # Packaged tools (gitignored)
├── templates/        # Code and package templates
├── tools/            # Build and development tools
├── config.yaml       # Main configuration (gitignored)
├── sample_config.yaml # Configuration example
└── README.md         # This file
```

## 🤝 Contributing

1. Follow the established code patterns and standards
2. Ensure all new tools integrate with the common utilities
3. Update configuration and documentation
4. Test thoroughly before committing
5. Keep sensitive data out of the repository

## 📄 License

[Add your license information here]

---

**Note:** This workspace is designed for research data processing. Always ensure compliance with your institution's data security and privacy policies. 