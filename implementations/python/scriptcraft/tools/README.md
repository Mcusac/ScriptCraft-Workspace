# ScriptCraft Tools

## Overview
Complete standalone applications that can be run independently or as part of workflows. These tools provide end-to-end functionality for specific research data processing needs.

## 🔧 Available Tools

### 🏷️ Automated Labeler
**Purpose**: Generates professional labels and documentation for research data packages.

**Key Features**:
- Excel-based label data input
- Word document template generation  
- Batch processing capabilities
- Professional formatting

**Usage**:
```python
from scriptcraft.tools.automated_labeler import AutomatedLabeler

labeler = AutomatedLabeler()
labeler.run(input_paths=["label_data.xlsx"])
```

**Distribution**: ✅ Available as standalone distributable

### 📊 Data Content Comparer
**Purpose**: Compare data content between different releases, domains, or datasets.

**Key Features**:
- Multiple comparison modes (domain old vs new, RHQ mode, standard mode)
- Detailed difference reporting
- Statistical comparison metrics
- Plugin-based architecture for different comparison types

**Usage**:
```python
from scriptcraft.tools.data_content_comparer import DataContentComparer

comparer = DataContentComparer()
comparer.run(mode="domain_old_vs_new", domain="Clinical")
```

**Distribution**: ✅ Available as standalone distributable

### ⚡ RHQ Form Autofiller  
**Purpose**: Automated filling of Residential History Questionnaire (RHQ) forms using patient data.

**Key Features**:
- Excel data input processing
- Web form automation using Selenium
- Batch processing for multiple patients
- Error handling and logging
- Credential management

**Usage**:
```python
from scriptcraft.tools.rhq_form_autofiller import RHQFormAutofiller

rhq = RHQFormAutofiller()
rhq.run(input_paths=["patient_data.xlsx"])
```

**Distribution**: ✅ Available as standalone distributable

## 🏗️ Tool Architecture

### Common Pattern
All tools follow the ScriptCraft tool pattern:

```python
from scriptcraft import BaseTool

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
Tools can support plugin architectures for extensibility:

```python
# Data Content Comparer plugins
from scriptcraft.tools.data_content_comparer.plugins import (
    DomainOldVsNewMode,
    RHQMode, 
    StandardMode
)
```

### Configuration
Tools support flexible configuration through:

```python
from scriptcraft import Config

# YAML configuration
config = Config.from_yaml("config.yaml")

# Environment variables (for distributables)
config = Config.from_environment()
```

## 📦 Distribution

### Standalone Packages
Selected tools are available as standalone distributable packages that include:
- Embedded Python runtime
- All dependencies
- Batch scripts for easy execution
- User-friendly documentation

### Python Package Integration
All tools are also available through the main `scriptcraft` package:

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
   └── tests/               # Tool tests
   ```

2. **Implement tool class**:
   ```python
   from scriptcraft import BaseTool
   
   class MyNewTool(BaseTool):
       def run(self, **kwargs):
           self.log_start()
           # Implementation
           self.log_completion()
   ```

3. **Add configuration** (if distributable):
   ```yaml
   # config.yaml
   tools:
     my_new_tool:
       description: "🚀 My new tool description"
       packages: [required, packages]
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

## 🧪 Testing

```bash
# Test all tools
python -m pytest implementations/python/scriptcraft/tests/tools/

# Test specific tool
python -m pytest implementations/python/scriptcraft/tests/tools/test_automated_labeler.py
```

## 🔗 Related Components

- **`scriptcraft.common`** - Shared utilities and base classes
- **`scriptcraft.checkers`** - Data quality checking components  
- **`scriptcraft.validators`** - Data validation components
- **`scriptcraft.transformers`** - Data transformation components

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details. 