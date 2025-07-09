# 🧪 ScriptCraft Testing Framework

This directory contains the comprehensive test suite for ScriptCraft, organized to keep the Python package clean while providing thorough testing coverage.

## 📁 Test Structure

```
tests/
├── unit/                          # Unit tests for individual components
│   ├── test_common/              # Tests for common utilities
│   ├── test_tools/               # Tests for base tool framework
│   └── test_pipelines/           # Tests for pipeline components
├── integration/                   # Integration tests
│   ├── test_pipelines/           # Pipeline integration tests
│   └── test_workflows/           # End-to-end workflow tests
├── performance/                   # Performance and benchmark tests
├── tools/                         # Tool-specific tests
│   ├── test_data_content_comparer.py
│   ├── test_rhq_form_autofiller.py
│   └── ...
├── conftest.py                    # Shared test fixtures
├── pytest.ini                    # Pytest configuration
├── requirements-test.txt          # Testing dependencies
└── run_tests.py                   # Simple test runner
```

## 🚀 Quick Start

### Install Testing Dependencies
```bash
pip install -r tests/requirements-test.txt
```

### Run All Tests
```bash
# From workspace root
python tests/run_tests.py

# Or directly with pytest
pytest tests/
```

### Run Specific Test Categories
```bash
# Unit tests only
pytest tests/unit/

# Tool tests only
pytest tests/tools/

# Performance tests only
pytest tests/performance/

# Integration tests only
pytest tests/integration/
```

### Run Specific Tool Tests
```bash
# Data Content Comparer tests
pytest tests/tools/test_data_content_comparer.py

# RHQ Form Autofiller tests
pytest tests/tools/test_rhq_form_autofiller.py
```

## 🎯 Test Categories

### Unit Tests (`tests/unit/`)
- **test_common/**: Tests for common utilities, configuration, logging
- **test_tools/**: Tests for base tool framework and common tool functionality
- **test_pipelines/**: Tests for pipeline components and utilities

### Integration Tests (`tests/integration/`)
- **test_pipelines/**: Tests for complete pipeline workflows
- **test_workflows/**: Tests for end-to-end workspace workflows

### Performance Tests (`tests/performance/`)
- Memory usage benchmarks
- Processing speed tests
- Scalability tests for large datasets

### Tool Tests (`tests/tools/`)
- Individual tool functionality tests
- Tool-specific error handling
- Tool integration with workspace

## 🔧 Test Configuration

### Pytest Configuration (`pytest.ini`)
- Coverage reporting for the package submodule
- Test discovery and categorization
- Logging and output settings

### Test Fixtures (`conftest.py`)
- Common test data generation
- Temporary directory management
- Package import helpers

### Coverage Reporting
Tests automatically generate coverage reports:
- Terminal output with missing lines
- HTML report in `htmlcov/` directory
- Coverage for the package submodule only

## 📊 Running Tests with Coverage

```bash
# Run with coverage
pytest tests/ --cov=implementations/python-package/scriptcraft --cov-report=html

# View coverage report
open htmlcov/index.html
```

## 🛠️ Writing Tests

### Test File Naming
- Unit tests: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Test Organization
```python
class TestToolName:
    """Test suite for ToolName."""
    
    def test_basic_functionality(self):
        """Test basic tool functionality."""
        # Test implementation
        
    def test_error_handling(self):
        """Test error handling."""
        # Test error cases
        
    def test_integration(self):
        """Test integration with other components."""
        # Test integration
```

### Using Test Fixtures
```python
def test_with_fixtures(sample_comparison_files, temp_output_dir):
    """Test using provided fixtures."""
    file1, file2 = sample_comparison_files
    # Use the test files and output directory
```

## 🎯 Testing Strategy

### 1. Unit Tests
- Test individual functions and methods
- Mock external dependencies
- Fast execution (< 1 second per test)

### 2. Integration Tests
- Test component interactions
- Use real file I/O
- Test complete workflows

### 3. Performance Tests
- Benchmark memory usage
- Measure processing speed
- Test scalability limits

### 4. Tool-Specific Tests
- Test each tool's unique functionality
- Verify error handling
- Test CLI interfaces

## 🔍 Test Data

### Generated Test Data
Tests use dynamically generated data to avoid storing large files:
- CSV files with sample data
- Excel files with test content
- Temporary directories for output

### Test Data Fixtures
- `sample_comparison_files`: Two similar CSV files with differences
- `sample_excel_file`: Excel file with test data
- `temp_output_dir`: Temporary directory for test outputs

## 🚨 Error Handling Tests

### Common Test Patterns
```python
def test_error_handling(self):
    """Test error handling."""
    with pytest.raises(ValueError, match="expected error message"):
        # Code that should raise an error
        tool.run(invalid_input)
```

### Input Validation Tests
```python
def test_input_validation(self):
    """Test input validation."""
    # Test with invalid inputs
    # Test with missing required parameters
    # Test with wrong file formats
```

## 📈 Performance Testing

### Memory Usage Tests
```python
def test_memory_usage(self):
    """Test memory usage with different dataset sizes."""
    import psutil
    # Measure memory before and after
    # Verify memory usage is reasonable
```

### Processing Speed Tests
```python
def test_processing_speed(self):
    """Test processing speed."""
    import time
    # Measure processing time
    # Verify performance meets requirements
```

## 🔄 Continuous Integration

### GitHub Actions
Tests are automatically run on:
- Push to main branch
- Pull requests
- Multiple Python versions (3.8-3.12)

### Quality Gates
- Minimum test coverage: 90%
- All tests must pass
- Performance benchmarks must be met

## 🐛 Debugging Tests

### Verbose Output
```bash
pytest tests/ -v --tb=long
```

### Debug Specific Test
```bash
pytest tests/tools/test_data_content_comparer.py::TestDataContentComparer::test_basic_comparison -v -s
```

### Run with Print Statements
```bash
pytest tests/ -s
```

## 📋 Test Checklist

Before committing, ensure:
- [ ] All tests pass
- [ ] New functionality has tests
- [ ] Error cases are tested
- [ ] Performance is acceptable
- [ ] Coverage is maintained
- [ ] Tests are well-documented

## 🎯 Next Steps

### Immediate Actions
1. **Run existing tests**: `python tests/run_tests.py`
2. **Add missing tests**: Create tests for untested functionality
3. **Improve coverage**: Target 90%+ coverage
4. **Performance benchmarks**: Establish baseline metrics

### Future Improvements
1. **Automated testing**: Set up CI/CD pipeline
2. **Test data management**: Organize test datasets
3. **Performance monitoring**: Track performance over time
4. **Test documentation**: Improve test documentation

---

*This testing framework ensures ScriptCraft maintains high quality while keeping the package clean and focused.* 