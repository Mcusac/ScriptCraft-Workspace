# Common Framework 🛠️

Core framework and utilities that provide the foundation for all release workspace packages. This framework standardizes development patterns, reduces code duplication, and ensures consistency across tools.

---

📅 **Build Date:** [INSERT_DATE_HERE]

This framework was last updated on the date above.  
For reproducibility and support, always refer to this date when reporting issues.

---

## 📦 Package Structure

```
common/
├── __init__.py              # Package interface and core exports
├── base.py                  # Base classes (Tool, Validator, etc.)
├── config_manager.py        # Configuration management
├── comparison_utils.py      # Data comparison utilities
├── dataframe_utils.py       # DataFrame operations
├── date_utils.py           # Date handling utilities
├── expected_values.py      # Value validation
├── file_operations.py      # File I/O operations
├── import_utils.py         # Dynamic imports
├── input_validation.py     # Input validation
├── logging_utils.py        # Logging setup and utilities
├── paths_and_constants.py  # Path management
├── plugin_registry.py      # Plugin system
├── timepoint_utils.py      # Time handling
├── tool_runner.py          # CLI execution
└── value_cleaning.py       # Data cleaning utilities
```

---

## 🎯 Core Components

### Base Classes
```python
from scripts.common import BaseTool, BaseValidator, BaseTransformer

class MyTool(BaseTool):
    def run(self, **kwargs):
        self.log_start()
        # Tool implementation
        self.log_completion()
```

### Configuration
```python
from scripts.common import get_config, update_config

config = get_config()
update_config({'key': 'value'})
```

### Logging
```python
from scripts.common import setup_logging, log_and_print

setup_logging('my_tool.log')
log_and_print("Processing started", level="info")
```

### File Operations
```python
from scripts.common import (
    ensure_output_dir,
    resolve_path,
    get_project_root
)

output_dir = ensure_output_dir(
    resolve_path('output', get_project_root())
)
```

---

## 🧪 Testing

### Framework Tests
```bash
python -m pytest tests/common/
```

### Test Utilities
```python
from scripts.common import (
    create_test_file,
    setup_test_env,
    cleanup_test_env
)
```

### Coverage
```bash
python -m pytest --cov=scripts.common tests/common/
```

---

## 🔄 Dependencies

Core dependencies:
- pandas >= 1.3.0
- numpy >= 1.20.0
- python-dateutil >= 2.8.2
- PyYAML >= 5.4.1
- typing-extensions >= 4.0.0
- Python >= 3.8

Development dependencies:
- pytest >= 6.2.5
- pytest-cov >= 2.12.1
- black >= 21.12b0
- mypy >= 0.910

---

## 📋 Current Status and Future Improvements

### ✅ Completed Components
1. **Core Architecture**
   - Base classes implemented
   - Plugin system working
   - Configuration management
   - Logging infrastructure

2. **Utilities**
   - File operations
   - Data frame handling
   - Date utilities
   - Value cleaning
   - Path management

3. **Documentation**
   - Basic usage examples
   - API documentation
   - Error handling guides
   - Development patterns

4. **Testing**
   - Basic test framework
   - Coverage reporting
   - Test utilities
   - Environment management

### 🔄 Partially Complete
1. **Type System**
   - ✅ Basic type hints
   - ✅ Core class typing
   - ❌ Need comprehensive typing
   - ❌ Need type checking in CI

2. **Error Handling**
   - ✅ Basic error classes
   - ✅ Context preservation
   - ❌ Need standardized codes
   - ❌ Need better recovery

3. **Performance**
   - ✅ Basic optimizations
   - ✅ Memory management
   - ❌ Need benchmarking
   - ❌ Need profiling tools

### 🎯 Prioritized Improvements

#### High Priority (Framework Critical)
1. **Type System Enhancement**
   - Complete type coverage
   - Add runtime checks
   - Improve type exports
   - Add validation decorators

2. **Error System Standardization**
   - Create error code system
   - Implement recovery patterns
   - Add context managers
   - Enhance debugging tools

3. **Performance Framework**
   - Add benchmarking tools
   - Create profiling utilities
   - Implement monitoring
   - Add performance tests

#### Medium Priority (Developer Experience)
4. **Documentation Enhancement**
   - Create interactive examples
   - Add tutorial notebooks
   - Improve API docs
   - Add architecture guide

5. **Development Tools**
   - Add code generators
   - Create debug tools
   - Improve test utilities
   - Add CI/CD helpers

#### Low Priority (Future-Proofing)
6. **Framework Evolution**
   - Add async support
   - Enhance plugin system
   - Add caching framework
   - Create migration tools

7. **Monitoring & Metrics**
   - Add telemetry
   - Create dashboards
   - Add health checks
   - Implement alerting

---

## 🏗️ Package Development

### Creating New Tools

1. **Choose Base Class**
```python
from scripts.common import BaseTool

class NewTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="New Tool",
            description="Tool description"
        )
```

2. **Implement Required Methods**
```python
def run(self, **kwargs):
    self.log_start()
    self.validate_inputs(kwargs)
    # Implementation
    self.log_completion()
```

3. **Add CLI Support**
```python
def main():
    tool = NewTool()
    parser = tool.create_parser()
    # Add arguments
    args = parser.parse_args()
    tool.run(**vars(args))

if __name__ == "__main__":
    main()
```

### Framework Extensions

1. **Adding Utilities**
   - Place in appropriate module
   - Add type hints
   - Include docstrings
   - Write unit tests

2. **Modifying Base Classes**
   - Update in base.py
   - Maintain backwards compatibility
   - Update all inheriting classes
   - Document changes

---

## 📚 Best Practices

### Tool Development
1. Inherit from base classes
2. Use provided utilities
3. Follow logging patterns
4. Handle errors gracefully

### Framework Usage
1. Import from top level
2. Use type hints
3. Follow patterns
4. Write tests

### Plugin Development
1. Use plugin registry
2. Follow naming conventions
3. Document interfaces
4. Version appropriately

---

## 🤝 Contributing

1. **Framework Changes**
   - Discuss major changes first
   - Maintain backwards compatibility
   - Update all examples
   - Test thoroughly

2. **Documentation**
   - Keep examples current
   - Document breaking changes
   - Update type hints
   - Add migration guides

3. **Testing**
   - Add regression tests
   - Update benchmarks
   - Check compatibility
   - Verify examples

4. **Review Process**
   - Code review required
   - Breaking change review
   - Performance review
   - Documentation review

--- 