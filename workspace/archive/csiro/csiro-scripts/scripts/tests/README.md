# Test Package

This package contains tests to verify the codebase is working correctly.

## test_imports.py

**Automatic module discovery** - This test automatically discovers and tests all Python modules in the codebase. No need to manually maintain a list of modules!

### Features

- **Automatic Discovery**: Recursively finds all Python modules in key packages
- **DRY Design**: No hardcoded module lists - automatically discovers everything
- **Comprehensive Testing**: Tests all imports including contest abstraction
- **API Verification**: Verifies all API imports work correctly

### Usage

Run from the scripts directory:

```bash
python tests/test_imports.py
```

For verbose output (shows full tracebacks):

```bash
python tests/test_imports.py --verbose
# or
python tests/test_imports.py -v
```

### What it tests

The test automatically discovers and tests:

1. **Contest Package**: All contest base classes, CSIRO implementation, and registry
2. **Config Package**: All config modules including evaluation_constants and path_constants
3. **API Verification**: Verifies all API imports work correctly (TARGET_WEIGHTS, PRIMARY_TARGETS, etc.)
4. **Dataset Manipulation**: All data loading and streaming modules
5. **Modeling**: All evaluation, models, training, and testing modules
6. **Pipelines**: All atomic and workflow pipelines
7. **Utils**: All utility modules
8. **CLI**: All CLI modules
9. **Integration**: Verifies contest abstraction is properly integrated with existing code

### Missing Dependencies

**Note**: The test automatically detects missing external dependencies. These are **required** to use the codebase:
- Install dependencies: `pip install -r requirements.txt`
- Or install individually: `pip install torch tqdm pandas numpy ...`

The test distinguishes between:
- **Structural errors**: Actual import problems in the codebase (need fixing)
- **Missing dependencies**: External packages that need to be installed (not errors, just need installation)

### Test Results

- `[PASS]`: Module imported successfully
- `[DEPS]`: Missing external dependency (install to use)
- `[FAIL]`: Structural import error (needs fixing)

### Exit Codes

- `0`: All critical tests passed (contest, config, integration)
- `1`: One or more critical tests failed

### How it works

1. **Discovery**: Recursively walks package directories to find all Python modules
2. **Testing**: Attempts to import each discovered module
3. **Verification**: Tests key attributes and functions for API correctness
4. **Integration**: Verifies contest abstraction works with existing code
