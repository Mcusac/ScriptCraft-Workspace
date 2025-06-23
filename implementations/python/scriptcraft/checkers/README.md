# ScriptCraft Checkers

## Overview
Quality control components that analyze data quality, consistency, and integrity. These checkers validate data against various rules and standards to ensure research data quality.

## 🔍 Available Checkers

### ✅ Dictionary Driven Checker
**Purpose**: Comprehensive data validation against dictionary rules using a plugin-based architecture.

**Key Features**:
- Plugin-based validation system (numeric, text, date validators)
- Dictionary-driven rule enforcement
- Detailed QC reporting with statistics
- Support for multiple data domains
- Configurable validation plugins

**Usage**:
```python
from scriptcraft.checkers.dictionary_driven_checker import DictionaryDrivenChecker

checker = DictionaryDrivenChecker()
checker.run(input_paths=["data.xlsx"], dictionary_path="dict.xlsx")
```

**Plugins**:
- **Numeric Plugin**: Validates numeric ranges, required values
- **Text Plugin**: Validates categorical values, patterns  
- **Date Plugin**: Validates date formats, ranges

### 🔢 Score Totals Checker
**Purpose**: Validates calculated scores and totals against expected values and rules.

**Key Features**:
- Score calculation validation
- Total verification across domains
- Mathematical consistency checks
- Missing value analysis

**Usage**:
```python
from scriptcraft.checkers.score_totals_checker import ScoreTotalsChecker

checker = ScoreTotalsChecker()
checker.run(input_paths=["data.xlsx"])
```

### 🔄 Release Consistency Checker  
**Purpose**: Ensures consistency across different data releases and versions.

**Key Features**:
- Cross-release comparison
- Participant tracking across releases
- Data structure consistency validation
- Change tracking and reporting

**Usage**:
```python
from scriptcraft.checkers.release_consistency_checker import ReleaseConsistencyChecker

checker = ReleaseConsistencyChecker()
checker.run(domain="Clinical", input_paths=["current_release.xlsx"])
```

**Distribution**: ✅ Available as standalone distributable

### 📈 Feature Change Checker
**Purpose**: Tracks and validates feature changes across study visits and timepoints.

**Key Features**:
- Feature evolution tracking
- Cross-visit consistency validation
- Change pattern analysis
- Temporal data validation

**Usage**:
```python
from scriptcraft.checkers.feature_change_checker import FeatureChangeChecker

checker = FeatureChangeChecker()
checker.run(input_paths=["visit_data.xlsx"])
```

## 🏗️ Checker Architecture

### Base Pattern
All checkers follow the ScriptCraft checker pattern:

```python
from scriptcraft import BaseTool

class MyChecker(BaseTool):
    def __init__(self):
        super().__init__()
        self.tool_name = "my_checker"
        self.description = "Checker description"
    
    def run(self, **kwargs):
        self.log_start()
        try:
            # Validation logic
            self.validate_data(**kwargs)
            self.generate_reports()
            self.log_completion()
        except Exception as e:
            self.log_error(f"Validation failed: {e}")
            raise
    
    def validate_data(self, **kwargs):
        # Implement specific validation logic
        pass
    
    def generate_reports(self):
        # Generate QC reports
        pass
```

### Plugin System
Advanced checkers support plugin architectures:

```python
# Dictionary Driven Checker plugins
from scriptcraft.checkers.dictionary_driven_checker.plugins import (
    NumericPlugin,
    TextPlugin, 
    DatePlugin
)

# Register custom plugins
checker = DictionaryDrivenChecker()
checker.register_plugin('custom', MyCustomPlugin())
```

### Reporting
All checkers generate standardized reports:

```python
# Common report structure
reports = {
    'summary': {
        'total_records': 1000,
        'passed': 950,
        'failed': 50,
        'warnings': 25
    },
    'details': [
        # Detailed validation results
    ],
    'statistics': {
        # Statistical summaries
    }
}
```

## 📊 Quality Control Workflow

### Individual Checker Usage
```python
from scriptcraft.checkers import DictionaryDrivenChecker

# Single domain validation
checker = DictionaryDrivenChecker()
results = checker.run(
    input_paths=["clinical_data.xlsx"],
    dictionary_path="clinical_dict.xlsx"
)
```

### Multi-Checker Workflow
```python
from scriptcraft.checkers import (
    DictionaryDrivenChecker,
    ScoreTotalsChecker,
    ReleaseConsistencyChecker
)

# Comprehensive QC pipeline
checkers = [
    DictionaryDrivenChecker(),
    ScoreTotalsChecker(), 
    ReleaseConsistencyChecker()
]

for checker in checkers:
    results = checker.run(input_paths=["data.xlsx"])
    if not results.passed:
        print(f"❌ {checker.tool_name} failed validation")
    else:
        print(f"✅ {checker.tool_name} passed validation")
```

### Integration with Other Components
```python
from scriptcraft import setup_logger, load_data
from scriptcraft.transformers import DictionaryCleaner
from scriptcraft.checkers import DictionaryDrivenChecker

# Data processing + validation pipeline
logger = setup_logger("qc_pipeline")

# 1. Load and clean data
data = load_data("raw_data.xlsx")
cleaner = DictionaryCleaner()
cleaned_data = cleaner.run(data)

# 2. Validate cleaned data
checker = DictionaryDrivenChecker()
validation_results = checker.run(cleaned_data)

# 3. Process results
if validation_results.passed:
    logger.info("✅ Data passed all quality checks")
else:
    logger.warning(f"⚠️ Found {validation_results.failed_count} validation issues")
```

## 🔧 Development

### Adding New Checkers

1. **Create checker directory**:
   ```
   checkers/my_new_checker/
   ├── __init__.py
   ├── __main__.py          # Entry point
   ├── tool.py              # Main validation logic
   ├── utils.py             # Checker-specific utilities
   ├── README.md            # Documentation
   └── tests/               # Checker tests
   ```

2. **Implement checker class**:
   ```python
   from scriptcraft import BaseTool
   
   class MyNewChecker(BaseTool):
       def run(self, **kwargs):
           self.log_start()
           # Validation implementation
           results = self.validate_data(**kwargs)
           self.generate_reports(results)
           self.log_completion()
           return results
   ```

3. **Add tests**:
   ```python
   def test_my_new_checker():
       checker = MyNewChecker()
       results = checker.run(input_paths=["test_data.xlsx"])
       assert results.passed
   ```

### Plugin Development
For checkers that support plugins:

```python
from scriptcraft.checkers.dictionary_driven_checker.plugins.validators import BaseValidator

class MyCustomValidator(BaseValidator):
    def validate(self, value, rule):
        # Custom validation logic
        return ValidationResult(passed=True, message="Validation passed")
```

## 🧪 Testing

```bash
# Test all checkers
python -m pytest implementations/python/scriptcraft/tests/checkers/

# Test specific checker
python -m pytest implementations/python/scriptcraft/tests/checkers/test_dictionary_driven_checker.py

# Integration tests
python -m pytest implementations/python/scriptcraft/tests/integration/test_checker_integration.py
```

## 🔗 Related Components

- **`scriptcraft.common`** - Shared utilities and base classes
- **`scriptcraft.validators`** - Lower-level data validation components
- **`scriptcraft.transformers`** - Data transformation for pre-validation cleanup
- **`scriptcraft.tools`** - Standalone tools that may include validation

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details. 