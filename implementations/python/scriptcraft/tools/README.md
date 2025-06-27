# ScriptCraft Tools

## Overview
This package contains all tools for data processing, validation, transformation, and automation in the ScriptCraft ecosystem. All tools follow consistent patterns and can be used independently or as part of larger workflows.

## 🎯 Tool Categories

### 📊 Analysis Tools
**Purpose**: Data analysis, comparison, schema detection

#### Data Content Comparer
- **Purpose**: Compare data content between different releases, domains, or datasets
- **Key Features**: Multiple comparison modes, detailed difference reporting, statistical metrics
- **Plugin Modes**: Domain old vs new, RHQ mode, standard mode
- **Distribution**: ✅ Available as standalone distributable

#### Schema Detector 🆕
- **Purpose**: Automatically detect and generate database schemas from datasets
- **Key Features**: Healthcare pattern recognition, privacy-safe analysis, multiple output formats, HIPAA compliance
- **Outputs**: SQL DDL, JSON schema, YAML schema, comprehensive documentation
- **Distribution**: ✅ Available as part of package

### ✅ Validation Tools  
**Purpose**: Data quality control, consistency checks, and integrity validation

#### Dictionary Driven Checker
- **Purpose**: Comprehensive data validation against dictionary rules
- **Key Features**: Plugin-based validation system, detailed QC reporting, configurable plugins
- **Plugins**: Numeric, text, date validators
- **Distribution**: Available as part of package

#### Release Consistency Checker
- **Purpose**: Ensures consistency across different data releases and versions
- **Key Features**: Cross-release comparison, participant tracking, change tracking
- **Distribution**: ✅ Available as standalone distributable

#### Score Totals Checker
- **Purpose**: Validates calculated scores and totals against expected values
- **Key Features**: Score calculation validation, mathematical consistency checks
- **Distribution**: Available as part of package

#### Feature Change Checker
- **Purpose**: Tracks and validates feature changes across study visits and timepoints
- **Key Features**: Feature evolution tracking, cross-visit consistency, temporal validation
- **Distribution**: Available as part of package

#### Dictionary Validator
- **Purpose**: Validates dictionary data structure and format
- **Key Features**: Key uniqueness validation, value constraints, reference validation
- **Distribution**: Available as part of package

#### MedVisit Integrity Validator
- **Purpose**: Validates medical visit data integrity
- **Key Features**: Temporal consistency, cross-reference validation, medical data patterns
- **Distribution**: Available as part of package

### 🔄 Transformation Tools
**Purpose**: Data cleaning, formatting, and standardization

#### Dictionary Cleaner
- **Purpose**: Cleans and standardizes dictionary data
- **Key Features**: Duplicate removal, format standardization, consistency checks
- **Distribution**: Available as part of package

#### Date Format Standardizer
- **Purpose**: Standardizes date formats across datasets
- **Key Features**: Multiple input format support, configurable output formats, validation
- **Distribution**: Available as part of package

### ⚡ Automation Tools
**Purpose**: Automated workflows and form processing

#### RHQ Form Autofiller
- **Purpose**: Automated filling of Residential History Questionnaire (RHQ) forms
- **Key Features**: Excel data processing, web automation, batch processing, credential management
- **Distribution**: ✅ Available as standalone distributable

#### Automated Labeler
- **Purpose**: Generates professional labels and documentation for research data packages
- **Key Features**: Excel-based input, Word template generation, batch processing
- **Distribution**: ✅ Available as standalone distributable

## 🏗️ Architecture

### Unified Tool Interface
All tools follow the ScriptCraft tool pattern:

```python
from scriptcraft.tools import DataContentComparer, DictionaryDrivenChecker

# Direct tool usage
comparer = DataContentComparer()
comparer.run(mode="domain_old_vs_new", domain="Clinical")

# Discovery interface  
from scriptcraft.tools import get_available_tools, list_tools_by_category

# Get all tools
tools = get_available_tools()

# Get tools by category
validation_tools = list_tools_by_category("validation")
```

### Base Tool Pattern
```python
from scriptcraft.common.core import BaseTool

class MyTool(BaseTool):
    def __init__(self):
        super().__init__()
        self.tool_name = "my_tool"
        self.description = "Tool description"
    
    def run(self, **kwargs):
        self.log_start()
        try:
            # Tool-specific logic
            self.log_completion()
        except Exception as e:
            self.log_error(f"Tool failed: {e}")
            raise
```

### Plugin Support
Advanced tools support plugin architectures:

```python
# Dictionary Driven Checker plugins
from scriptcraft.tools.dictionary_driven_checker.plugins import (
    NumericPlugin,
    TextPlugin, 
    DatePlugin
)

# Data Content Comparer plugins  
from scriptcraft.tools.data_content_comparer.plugins import (
    DomainOldVsNewMode,
    RHQMode,
    StandardMode
)
```

## 📦 Distribution

### Standalone Packages
Selected tools are available as standalone distributable packages:
- **Data Content Comparer**: Complete comparison toolkit
- **Release Consistency Checker**: Cross-release validation
- **RHQ Form Autofiller**: Form automation suite
- **Automated Labeler**: Label generation toolkit

Each distributable includes:
- Embedded Python runtime
- All dependencies  
- Batch scripts for easy execution
- User-friendly documentation

### Python Package Integration
All tools are available through the main `scriptcraft` package:

```bash
pip install scriptcraft
```

## 🔧 Development

### Adding New Tools

1. **Create tool directory**:
   ```
   tools/my_new_tool/
   ├── __init__.py
   ├── __main__.py          # Entry point
   ├── tool.py              # Main logic
   ├── utils.py             # Tool-specific utilities  
   ├── README.md            # Documentation
   ├── tests/               # Tool tests
   └── plugins/             # Optional plugin system
   ```

2. **Implement tool class**:
   ```python
   from scriptcraft.common.core import BaseTool
   
   class MyNewTool(BaseTool):
       def run(self, **kwargs):
           self.log_start()
           # Implementation
           self.log_completion()
   ```

3. **Update tool categories** (in `tools/__init__.py`):
   ```python
   TOOL_CATEGORIES = {
       "analysis": ["data_content_comparer", "my_new_tool"],
       # ... other categories
   }
   ```

4. **Test thoroughly**:
   ```bash
   python -m pytest tools/my_new_tool/tests/
   ```

### Code Standards
- Follow the `BaseTool` pattern for consistency
- Use emoji in descriptions and log messages  
- Include comprehensive error handling
- Support both programmatic and CLI usage
- Add tests for all functionality
- Document with examples

## 🔮 Future Organization

As the tools package grows, we plan to implement the following organizational strategy:

### Phase 1: Current Flat Structure (✅ Current)
- All tools directly in `tools/` directory
- Simple discovery and imports
- Category metadata for organization

### Phase 2: Categorized Structure (15+ tools)
When the tools package reaches ~15+ tools, we will reorganize into functional subdirectories:

```
tools/
├── analysis/          # Data analysis and comparison tools
│   ├── data_content_comparer/
│   ├── schema_detector/
│   └── data_profiler/
├── validation/        # Quality control and validation tools  
│   ├── dictionary_driven_checker/
│   ├── release_consistency_checker/
│   └── integrity_validators/
├── transformation/    # Data cleaning and transformation tools
│   ├── dictionary_cleaner/
│   ├── date_format_standardizer/
│   └── data_normalizer/
├── automation/        # Workflow and form automation tools
│   ├── rhq_form_autofiller/
│   ├── automated_labeler/
│   └── batch_processors/
└── __init__.py       # Unified interface (backward compatible)
```

### Phase 3: Metadata-Driven Discovery (Future)
Advanced filtering and discovery using tool metadata:

```python
from scriptcraft.tools import find_tools

# Find tools by criteria
tools = find_tools(
    category="validation",
    complexity="beginner", 
    data_types=["clinical", "genomics"]
)
```

**Suggested Future Categories**:
- **analysis**: Data analysis, comparison, profiling, schema detection
- **validation**: Quality control, consistency checks, integrity validation  
- **transformation**: Data cleaning, formatting, standardization, normalization
- **automation**: Form processing, workflow automation, batch operations
- **reporting**: Report generation, visualization, documentation
- **integration**: Data import/export, API connectors, database tools

## 🧪 Testing

```bash
# Test all tools
python -m pytest implementations/python/scriptcraft/tests/tools/

# Test specific tool category
python -m pytest implementations/python/scriptcraft/tests/tools/validation/

# Test specific tool
python -m pytest implementations/python/scriptcraft/tests/tools/test_data_content_comparer.py
```

## 🔗 Related Components

- **`scriptcraft.common`** - Shared utilities and base classes
- **`scriptcraft.pipelines`** - Workflow orchestration
- **`scriptcraft.enhancements`** - Dictionary enhancement tools
- **`scriptcraft.cli`** - Command-line interfaces

## 🛠️ Quality Control Workflow Example

```python
from scriptcraft.tools import (
    DictionaryDrivenChecker,
    ScoreTotalsChecker,
    ReleaseConsistencyChecker,
    DataContentComparer
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

# Compare with previous release
comparer = DataContentComparer()
comparer.run(mode="domain_old_vs_new", domain="Clinical")
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.