# [Package Name] 🏷️

[Brief description of the package's purpose and main functionality]

---

📅 **Build Date:** [INSERT_DATE_HERE]

This package was last updated on the date above.  
For reproducibility and support, always refer to this date when sharing logs or output.

---

## 📦 Project Structure

```
package_name/
├── __init__.py         # Package interface and version info
├── __main__.py         # CLI entry point
├── tool.py            # Core implementation
├── utils.py           # Helper functions
├── tests/             # Test suite
│   ├── __init__.py
│   ├── test_integration.py
│   └── test_[feature].py
├── plugins/           # Optional extensions
│   ├── __init__.py
│   └── registry.py
└── README.md         # This documentation
```

---

## 🚀 Usage (Development)

### Command Line
```bash
python -m package_name --arg1 value1 --arg2 value2
```

### Python API
```python
from package_name import tool

# Example usage
result = tool.process(arg1, arg2)
```

Arguments:
- `arg1`: Description
- `arg2`: Description
[Add all CLI arguments and their descriptions]

---

## ⚙️ Features

- [Key feature 1]
- [Key feature 2]
- [Add all major features]

---

## 🔧 Dev Tips

- [Development best practice 1]
- [Development best practice 2]
- [Add important development guidelines]

---

## 🧪 Testing

### Unit Tests
```bash
python -m pytest tests/test_[feature].py
```

### Integration Tests
```bash
python -m pytest tests/test_integration.py
```

### Test Data
Example files needed:
- [List required test files]
- [Include sample data types]
- [Note any special test requirements]

---

## 🔄 Dependencies

Required packages:
- [package1] >= [version]
- [package2] >= [version]
- Python >= [version]

System requirements:
- Memory: [minimum requirement]
- Storage: [minimum requirement]
- CPU: [requirements if any]

---

## 🚨 Error Handling

Common errors and solutions:
1. [Error Category 1]
   - Cause: [Description]
   - Solution: [Steps to resolve]
2. [Error Category 2]
   - Cause: [Description]
   - Solution: [Steps to resolve]

---

## 📊 Performance

Expectations:
- Processing speed: [expected metrics]
- Memory usage: [expected metrics]
- File size limits: [limitations]

Optimization tips:
- [Performance tip 1]
- [Performance tip 2]
- [Resource management guidelines]

---

## 📋 Development Checklist

### 1. File Structure ⬜
- [ ] Standard package layout
  - [ ] __init__.py with version info
  - [ ] __main__.py for CLI
  - [ ] tool.py for core functionality
  - [ ] utils.py for helpers
  - [ ] tests/ directory
  - [ ] README.md
- [ ] Clean organization
- [ ] No deprecated files

### 2. Documentation ⬜
- [ ] Version information
- [ ] Package-level docstring
- [ ] Function docstrings
- [ ] Type hints
- [ ] README.md
- [ ] API documentation
- [ ] Error code reference
- [ ] Troubleshooting guide

### 3. Code Implementation ⬜
- [ ] Core functionality
- [ ] CLI interface
- [ ] Error handling
- [ ] Input validation
- [ ] Type checking
- [ ] Performance optimization
- [ ] Security considerations

### 4. Testing ⬜
- [ ] Unit tests
- [ ] Integration tests
- [ ] Performance tests
- [ ] Edge case tests
- [ ] Error condition tests
- [ ] Test data examples

### 5. Error Handling ⬜
- [ ] Custom exceptions
- [ ] Error messages
- [ ] Error logging
- [ ] Error recovery
- [ ] Input validation

### 6. Performance ⬜
- [ ] Large dataset testing
- [ ] Memory optimization
- [ ] Progress reporting
- [ ] Chunked processing
- [ ] Performance metrics

### 7. Configuration ⬜
- [ ] Command-line arguments
- [ ] Configuration validation
- [ ] Environment variables
- [ ] Default settings
- [ ] Documentation

### 8. Packaging ⬜
- [ ] Dependencies specified
- [ ] Version information
- [ ] Package structure
- [ ] Installation tested
- [ ] Distribution tested

---

## 📋 Current Status and Future Improvements

### ✅ Completed Items
[List completed features and implementations]
1. **Category 1**
   - [Completed item 1]
   - [Completed item 2]

2. **Category 2**
   - [Completed item 1]
   - [Completed item 2]

### 🔄 Partially Complete
[List items that need additional work]
1. **Category 1**
   - ✅ [Completed aspect]
   - ❌ [Incomplete aspect]

2. **Category 2**
   - ✅ [Completed aspect]
   - ❌ [Incomplete aspect]

### 🎯 Prioritized Improvements

#### High Priority
1. **Category 1**
   - [Improvement 1]
   - [Improvement 2]

2. **Category 2**
   - [Improvement 1]
   - [Improvement 2]

#### Medium Priority
3. **Category 1**
   - [Improvement 1]
   - [Improvement 2]

4. **Category 2**
   - [Improvement 1]
   - [Improvement 2]

#### Low Priority
5. **Category 1**
   - [Improvement 1]
   - [Improvement 2]

6. **Category 2**
   - [Improvement 1]
   - [Improvement 2]

---

## 🤝 Contributing

1. Branch naming: `feature/[package]-[name]`
2. Required for all changes:
   - Unit tests
   - Documentation updates
   - Checklist review
3. Code review process in CONTRIBUTING.md

---
