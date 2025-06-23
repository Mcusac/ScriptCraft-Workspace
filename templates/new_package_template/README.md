# New Package Template 📦

Template for creating new tools in the Release Workspace project following the consolidated main.py pattern.

---

## 📋 Template Structure

This template provides the standardized structure for new tools:

```
[tool_name]/
├── __init__.py           # Package interface and registry registration  
├── main.py              # Core implementation with CLI entry point
├── utils.py             # Tool-specific utility functions
├── README_devs.md       # Developer documentation (copy from templates/ReadMe's/)
└── README_shippable.md  # End-user documentation (copy from templates/ReadMe's/)
```

**Note:** README templates are located in `templates/ReadMe's/` and should be copied and customized for each new tool.

---

## 🚀 Creating a New Tool

### 1. Copy Template
```bash
# Copy the template
cp -r templates/new_package_template scripts/tools/[your_tool_name]

# Copy README templates
cp templates/ReadMe's/README_devs.md scripts/tools/[your_tool_name]/
cp templates/ReadMe's/README_shippable.md scripts/tools/[your_tool_name]/
```

### 2. Customize Template Files

#### A. Update `main.py`
- Replace `[Tool Name]` with your tool's actual name
- Replace `[tool_name]` with your tool's package name
- Implement your specific CLI arguments in `parse_cli_args()`
- Add tool-specific configuration loading

#### B. Update `utils.py` 
- Replace `ToolNameUtils` class name
- Implement `validate_input_file()` for your input requirements
- Implement `process_data()` methods for your processing logic
- Add any tool-specific utility functions

#### C. Update `__init__.py`
- Replace tool name and description
- Update imports if you add new public functions

#### D. Update README Files
- Customize `README_devs.md` with tool-specific information
- Customize `README_shippable.md` with user instructions
- Update build dates and feature lists

### 3. Add to Configuration
```yaml
# Add to config.yaml
tools:
  [your_tool_name]:
    description: "Your tool description with emoji 🛠️"
    default_output_dir: "output"
    # Add tool-specific configuration
```

### 4. Test Implementation
```bash
# Test in development
python -m scripts.tools.[your_tool_name] --help

# Test packaging
packaging.bat [your_tool_name]
```

---

## 🏗️ Architecture Pattern

This template follows the **consolidated main.py pattern**:

### Environment Detection
- Automatically detects development vs shippable environments
- Sets up appropriate import paths
- No manual configuration needed

### Dual Import System
```python
# Development imports
from scripts.common.logging.core import setup_logger, log_and_print

# Shippable imports  
from common.logging.core import setup_logger, log_and_print
```

### Utility Separation
- **`main.py`**: Core tool logic, environment detection, CLI interface
- **`utils.py`**: Tool-specific utilities not suitable for scripts.common
- **`scripts.common`**: General utilities shared across tools

### CLI Entry Point
- No `__main__.py` file needed
- CLI entry point is built into `main.py`
- Supports both `python -m scripts.tools.[tool_name]` and `python main.py`

---

## 🔧 Key Features

### Automatic Environment Detection
```python
def setup_imports():
    """Detects dev vs shippable and sets up imports."""
    is_shippable = (Path(__file__).parent / 'common').exists()
    # ... handles import setup
```

### Flexible Input Handling
- Auto-discovery of input files
- Direct path specification
- Directory processing
- Validation pipeline

### Standardized Error Handling
```python
try:
    # Operation
    log_and_print("✅ Operation successful")
except Exception as e:
    log_and_print(f"❌ Error: {e}", level="error")
    raise
```

### Pipeline Integration
```python
def main_runner(**kwargs):
    """Entry point for pipeline execution."""
    # Handles pipeline interface
```

### Configuration Integration
- Automatic config.yaml loading
- Environment-appropriate paths
- Fallback to defaults

---

## 📝 Implementation Guidelines

### What to Implement
1. **Tool-specific logic** in the `ToolName` class
2. **Input validation** in `utils.py`
3. **Data processing** methods for different modes
4. **CLI arguments** specific to your tool
5. **Configuration options** in config.yaml

### What NOT to Change
1. **Environment detection** logic
2. **Import setup** system
3. **Basic CLI structure** (add arguments, don't replace)
4. **Pipeline interface** (main_runner function signature)

### DRY Principles
- Use existing utilities from `scripts.common`
- Don't duplicate logging setup
- Reuse configuration patterns
- Leverage existing data loading functions

---

## 🧪 Testing Checklist

### Development Testing
- [ ] Tool runs with `python -m scripts.tools.[tool_name]`
- [ ] CLI arguments work correctly
- [ ] Input validation functions properly
- [ ] Output is generated in correct format
- [ ] Error handling works as expected
- [ ] Debug mode provides useful information

### Environment Testing
- [ ] Imports work in development environment
- [ ] Environment detection is accurate
- [ ] Configuration loads properly
- [ ] Pipeline integration works

### Packaging Testing
- [ ] Tool packages successfully with `packaging.bat`
- [ ] Shippable version runs correctly
- [ ] Imports work in shippable environment
- [ ] All dependencies are included

---

## 📚 Reference Files

### Study These Examples
- `scripts/tools/rhq_form_autofiller/main.py` - Reference implementation
- `scripts/tools/data_content_comparer/main.py` - Another example
- `scripts/common/` - Available utilities

### README Templates
- `templates/ReadMe's/README_devs.md` - Developer documentation template
- `templates/ReadMe's/README_shippable.md` - End-user documentation template

### Configuration Examples
- `config.yaml` - Tool configuration examples
- `scripts/pipelines/` - Pipeline integration patterns

---

## ⚠️ Common Pitfalls

### Import Issues
- ❌ Don't modify environment detection logic
- ❌ Don't use absolute imports for cross-environment compatibility
- ✅ Use the provided import system

### Code Duplication
- ❌ Don't reimplement logging setup
- ❌ Don't create custom argument parsers from scratch
- ✅ Use existing patterns and utilities

### File Structure
- ❌ Don't create `__main__.py` file
- ❌ Don't put core logic in utils.py
- ✅ Follow the established template structure

### Configuration
- ❌ Don't hardcode paths or settings
- ❌ Don't create tool-specific config files
- ✅ Use config.yaml for all configuration

---

## 🎯 Success Criteria

Your tool is ready when:
- [ ] Follows the consolidated main.py pattern
- [ ] Works in both development and shippable environments
- [ ] Integrates with the pipeline system
- [ ] Has comprehensive error handling
- [ ] Uses emoji-enhanced logging
- [ ] Reuses existing utilities
- [ ] Has complete documentation
- [ ] Passes all testing phases 