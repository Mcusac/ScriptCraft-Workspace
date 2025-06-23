# ScriptCraft Python Package

## Overview
A comprehensive Python package for research data processing, validation, and quality control. ScriptCraft provides both standalone tools and reusable components for building data processing workflows.

## 🚀 Quick Start

### Installation
```bash
# Install from GitHub
pip install git+https://github.com/mcusac/ScriptCraft-Workspace.git#subdirectory=implementations/python

# Or if published to PyPI
pip install scriptcraft
```

### Basic Usage
```python
from scriptcraft import setup_logger, Config, BaseTool, load_data

# Core utilities (most common usage)
logger = setup_logger("my_project")
config = Config.from_yaml("config.yaml")
data = load_data("research_data.xlsx")

# Use specific tools
from scriptcraft.tools.rhq_form_autofiller import RHQFormAutofiller
rhq = RHQFormAutofiller()
rhq.run(input_paths=["patient_data.xlsx"])
```

## 📦 Package Structure

### Core Components (`scriptcraft.common`)
Shared utilities and foundational classes used across all tools:
- **Configuration management** - `Config` class for YAML and environment-based config
- **Logging utilities** - Standardized logging with emoji support
- **Data loading/saving** - Common data I/O operations
- **Base classes** - `BaseTool`, `BaseValidator`, etc.
- **File operations** - Path resolution, directory management

### Standalone Tools (`scriptcraft.tools`)
Complete applications that can be run independently or as part of workflows:
- **RHQ Form Autofiller** ⚡ - Automated residential history form filling
- **Data Content Comparer** 📊 - Compare data between releases  
- **Automated Labeler** 🏷️ - Generate labels and documentation

### Data Validators (`scriptcraft.validators`)
Components that validate data structure, format, and content rules:
- **Dictionary Validator** 📚 - Validates data against dictionary rules
- **MedVisit Integrity Validator** 🏥 - Validates visit data integrity

### Data Transformers (`scriptcraft.transformers`)
Components that transform data format or structure:
- **Date Format Standardizer** 📅 - Standardizes date formats
- **Dictionary Cleaner** 🧹 - Cleans and standardizes dictionary entries

### Quality Checkers (`scriptcraft.checkers`)
Components that analyze data quality and consistency:
- **Dictionary Driven Checker** ✅ - Dictionary-based data validation with plugins
- **Score Totals Checker** 🔢 - Validates score calculations
- **Release Consistency Checker** 🔄 - Checks release-to-release consistency
- **Feature Change Checker** 📈 - Tracks feature changes across visits

### Data Enhancements (`scriptcraft.enhancements`)
Tools for enhancing and supplementing data:
- **Dictionary Supplementer** 📝 - Enhance data dictionaries
- **Supplement Prepper** 🔧 - Prepare data supplements  
- **Supplement Splitter** ✂️ - Split and organize supplements

## 🏗️ Architecture Principles

### 1. **Single Responsibility**
Each component has a clear, focused purpose:
- **Validators** check data correctness
- **Transformers** modify data format/structure  
- **Checkers** analyze data quality
- **Tools** provide complete workflow solutions

### 2. **Consistent Interfaces**
All components follow standardized patterns:
```python
from scriptcraft import BaseTool

class MyTool(BaseTool):
    def run(self, **kwargs):
        self.log_start()
        # Tool logic here
        self.log_completion()
```

### 3. **Plugin Architecture**
Many components support plugins for extensibility:
```python
# Dictionary Driven Checker with plugins
from scriptcraft.checkers.dictionary_driven_checker import DictionaryDrivenChecker

checker = DictionaryDrivenChecker()
checker.run(input_paths=["data.xlsx"])  # Auto-loads appropriate plugins
```

### 4. **Configuration-Driven**
All tools support flexible configuration:
```python
from scriptcraft import Config

# From YAML file
config = Config.from_yaml("config.yaml")

# From environment variables (for distributables)
config = Config.from_environment()
```

## 🔧 Common Usage Patterns

### Data Processing Pipeline
```python
from scriptcraft import setup_logger, load_data
from scriptcraft.transformers import DateFormatStandardizer
from scriptcraft.validators import DictionaryValidator
from scriptcraft.checkers import ScoreTotalsChecker

logger = setup_logger("data_pipeline")

# Load and transform data
data = load_data("input.xlsx")
transformer = DateFormatStandardizer()
cleaned_data = transformer.run(data)

# Validate data
validator = DictionaryValidator()
validator.run(cleaned_data, dictionary_path="dict.xlsx")

# Check quality
checker = ScoreTotalsChecker()
checker.run(cleaned_data)
```

### Quality Control Workflow
```python
from scriptcraft.checkers import (
    DictionaryDrivenChecker,
    ReleaseConsistencyChecker, 
    FeatureChangeChecker
)

# Comprehensive QC
checkers = [
    DictionaryDrivenChecker(),
    ReleaseConsistencyChecker(),
    FeatureChangeChecker()
]

for checker in checkers:
    checker.run(input_paths=["current_data.xlsx"])
```

### Standalone Tool Usage
```python
from scriptcraft.tools import RHQFormAutofiller, DataContentComparer

# Form automation
rhq = RHQFormAutofiller()
rhq.run(input_paths=["patient_data.xlsx"])

# Data comparison
comparer = DataContentComparer()
comparer.run(mode="domain_old_vs_new", domain="Clinical")
```

## 🧪 Testing

The package includes comprehensive tests organized by category:

```bash
# Run all tests
python -m pytest implementations/python/scriptcraft/tests/

# Test specific components
python -m pytest implementations/python/scriptcraft/tests/tools/
python -m pytest implementations/python/scriptcraft/tests/checkers/
```

## 🔗 Integration with ScriptCraft Workspace

This Python package is part of the larger ScriptCraft Workspace ecosystem:

- **Package source**: `implementations/python/scriptcraft/`
- **Workspace tools**: Build and packaging utilities
- **Distributables**: Standalone tool packages for end users
- **Templates**: Development templates and examples

For full workspace functionality including pipelines and packaging tools, see the main repository.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- **Repository**: https://github.com/mcusac/ScriptCraft-Workspace
- **Issues**: https://github.com/mcusac/ScriptCraft-Workspace/issues
- **Documentation**: https://github.com/mcusac/ScriptCraft-Workspace/wiki
