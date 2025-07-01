# 🏗️ ScriptCraft Package Architecture & Module Boundaries

**Version**: v2.0.0  
**Last Updated**: 2025-01-02  
**Status**: Initial Definition (Subject to refinement after exemplar implementation)

---

## 📋 **Overview**

This document defines the clear module boundaries, responsibilities, and architectural patterns for the ScriptCraft package. It establishes the foundation for scalable, maintainable code organization following DRY principles.

**Scope**: All packages except individual tools in the `tools/` package (tools package structure will be defined after exemplar implementation).

---

## 🎯 **Architectural Principles**

### **Core Principles**
1. **Single Responsibility**: Each package/module has one clear purpose
2. **DRY (Don't Repeat Yourself)**: No code duplication across packages
3. **Scalability**: Easy to add new functionality without breaking existing code
4. **Predictability**: Consistent patterns and naming conventions
5. **Import Clarity**: Clear import paths and dependency relationships

### **Import Patterns**
- **Internal Development**: `import scriptcraft.common as cu` (wildcard imports for scalability)
- **Public APIs**: Explicit imports for controlled interfaces
- **Relative Imports**: Within packages for maintainability
- **Absolute Imports**: Between packages for clarity

---

## 📦 **Package Architecture**

### **🏠 Root Package (`scriptcraft/`)**
**Purpose**: Main entry point and package coordination

**Responsibilities**:
- Package version management (`_version.py`)
- High-level imports and exports
- Tool discovery and registration
- Package-level documentation

**Key Files**:
- `__init__.py` - Main package interface
- `_version.py` - Centralized version management
- `ROADMAP_v2.0.0.md` - Development roadmap

**Import Pattern**:
```python
# Main package imports
from scriptcraft import BaseTool, Config, setup_logger
from scriptcraft.tools import RHQFormAutofiller
from scriptcraft.common import load_data, compare_dataframes
```

---

### **🔧 Common Package (`scriptcraft/common/`)**
**Purpose**: Shared utilities and core functionality for all tools

**Responsibilities**:
- Base classes and core patterns
- Data processing utilities
- I/O operations
- Logging and error handling
- CLI utilities
- Pipeline execution
- Time utilities
- Plugin system

**Subpackages**:

#### **Core (`scriptcraft/common/core/`)**
**Purpose**: Foundation classes and configuration management

**Responsibilities**:
- Base classes (`BaseTool` - the ONLY base class needed)
- Configuration management (`Config`)
- Legacy compatibility aliases
- Core patterns and interfaces

**Key Exports**:
```python
from scriptcraft.common.core import BaseTool, Config
```

#### **Data (`scriptcraft/common/data/`)**
**Purpose**: Data processing, validation, and manipulation utilities

**Responsibilities**:
- Data cleaning and preprocessing
- Data comparison utilities
- Data validation functions
- DataFrame manipulation
- Data processing patterns
- Universal data processor

**Key Exports**:
```python
from scriptcraft.common.data import (
    compare_dataframes, FlaggedValue, ColumnValidator,
    load_data, save_data, validate_input_paths
)
```

#### **I/O (`scriptcraft/common/io/`)**
**Purpose**: File and path operations

**Responsibilities**:
- File loading and saving
- Path resolution and validation
- Directory operations
- Workspace path management
- Domain-specific path handling

**Key Exports**:
```python
from scriptcraft.common.io import (
    get_project_root, resolve_path, get_domain_paths,
    load_data, save_data, ensure_output_dir
)
```

#### **Logging (`scriptcraft/common/logging/`)**
**Purpose**: Centralized logging system

**Responsibilities**:
- Logger setup and configuration
- Log formatting and handlers
- Context-aware logging
- Domain-specific logging
- Progress tracking

**Key Exports**:
```python
from scriptcraft.common.logging import (
    setup_logger, log_and_print, qc_log_context,
    with_domain_logger
)
```

#### **CLI (`scriptcraft/common/cli/`)**
**Purpose**: Command-line interface utilities

**Responsibilities**:
- Unified CLI system
- Argument parsing
- Tool execution
- Error handling
- Help generation

**Key Exports**:
```python
from scriptcraft.common.cli import (
    run_tool_main, run_tool_from_cli, parse_tool_args
)
```

#### **Tools (`scriptcraft/common/tools/`)**
**Purpose**: Tool patterns and utilities

**Responsibilities**:
- Tool creation patterns
- Runner functions
- Tool metadata
- Expected value patterns
- Tool validation utilities

**Key Exports**:
```python
from scriptcraft.common.tools import (
    create_standard_tool, create_runner_function,
    ExpectedValue, PatternMatcher
)
```

#### **Pipeline (`scriptcraft/common/pipeline/`)**
**Purpose**: Pipeline execution utilities

**Responsibilities**:
- Pipeline execution engine
- Step coordination
- Pipeline validation
- Execution monitoring

**Key Exports**:
```python
from scriptcraft.common.pipeline import (
    PipelineExecutor, run_pipeline_step
)
```

#### **Time (`scriptcraft/common/time/`)**
**Purpose**: Time-related utilities

**Responsibilities**:
- Date standardization
- Time column validation
- Date format detection
- Time-based operations

**Key Exports**:
```python
from scriptcraft.common.time import (
    standardize_date_column, is_date_column
)
```

#### **Plugins (`scriptcraft/common/plugins/`)**
**Purpose**: Plugin system and registry

**Responsibilities**:
- Plugin registration
- Plugin discovery
- Plugin execution
- Plugin validation

**Key Exports**:
```python
from scriptcraft.common.plugins import (
    PluginBase, UnifiedPluginRegistry, register_validator
)
```

**Import Pattern**:
```python
# Recommended for internal development
import scriptcraft.common as cu
cu.BaseTool, cu.load_data, cu.setup_logger

# For public APIs
from scriptcraft.common import BaseTool, Config, setup_logger
```

---

### **🛠️ CLI Package (`scriptcraft/cli/`)**
**Purpose**: High-level CLI coordination

**Responsibilities**:
- Main CLI entry points
- Tool discovery and routing
- Global CLI configuration
- Help and documentation

**Key Exports**:
```python
from scriptcraft.cli import main, list_tools, run_tool
```

---

### **🔄 Pipelines Package (`scriptcraft/pipelines/`)**
**Purpose**: Pipeline orchestration and management

**Responsibilities**:
- Pipeline definition and execution
- Step coordination
- Pipeline validation
- Pipeline monitoring and reporting

**Key Files**:
- `base_pipeline.py` - Base pipeline classes
- `pipeline_utils.py` - Pipeline utilities
- `pipeline_steps.py` - Standard pipeline steps

**Key Exports**:
```python
from scriptcraft.pipelines import (
    BasePipeline, PipelineStep, run_pipeline
)
```

---

### **🚀 Enhancements Package (`scriptcraft/enhancements/`)**
**Purpose**: Specialized enhancement tools and utilities

**Responsibilities**:
- Data enhancement tools
- Supplement processing
- Advanced data transformations
- Specialized workflows

**Current Tools**:
- `dictionary_supplementer/` - Dictionary enhancement
- `supplement_prepper/` - Supplement preparation
- `supplement_splitter/` - Supplement splitting

**Key Exports**:
```python
from scriptcraft.enhancements import (
    DictionarySupplementer, SupplementPrepper, SupplementSplitter
)
```

---

### **📚 Misc Package (`scriptcraft/misc/`)**
**Purpose**: Miscellaneous utilities and experimental features

**Responsibilities**:
- Experimental features
- Utility scripts
- Development tools
- Temporary functionality

**Note**: This package is for experimental or temporary functionality. Features should be moved to appropriate packages once proven.

---

### **🧪 Tests Package (`scriptcraft/tests/`)**
**Purpose**: Testing framework and test utilities

**Responsibilities**:
- Unit tests
- Integration tests
- Performance tests
- Test utilities and fixtures
- Test configuration

**Structure**:
- `tools/` - Tool-specific tests
- `integration/` - Integration tests
- `performance/` - Performance tests
- `system/` - System-level tests
- `pipelines/` - Pipeline tests
- `enhancements/` - Enhancement tests

**Key Exports**:
```python
from scriptcraft.tests import (
    BaseToolTestCase, PipelineTestCase, TestConfig
)
```

---

## 🎯 **Exemplar Tool Structure**

### **RHQ Form Autofiller (`scriptcraft/tools/rhq_form_autofiller/`)**
**Purpose**: Reference implementation for tool structure and patterns

**Responsibilities**:
- Demonstrates proper tool organization
- Shows DRY patterns in action
- Illustrates best practices
- Serves as template for other tools

**Structure**:
```
rhq_form_autofiller/
├── __init__.py          # Tool metadata and exports
├── main.py              # Main tool logic
├── utils.py             # Tool-specific utilities
├── env.py               # Environment configuration
├── README.md            # Tool documentation
├── README_devs.md       # Developer documentation
└── README_distributable.md  # Distribution documentation
```

**Key Patterns**:
- Inherits from `BaseTool`
- Uses `import scriptcraft.common as cu`
- Follows DRY principles
- Implements unified CLI system
- Comprehensive documentation

**Import Pattern**:
```python
from scriptcraft.tools.rhq_form_autofiller import RHQFormAutofiller
```

---

## 🔗 **Dependency Relationships**

### **Import Hierarchy**
```
scriptcraft/ (root)
├── common/ (foundation)
│   ├── core/ (base classes)
│   ├── data/ (data utilities)
│   ├── io/ (file operations)
│   ├── logging/ (logging system)
│   ├── cli/ (CLI utilities)
│   ├── tools/ (tool patterns)
│   ├── pipeline/ (pipeline utilities)
│   ├── time/ (time utilities)
│   └── plugins/ (plugin system)
├── cli/ (CLI coordination)
├── pipelines/ (pipeline orchestration)
├── enhancements/ (specialized tools)
├── misc/ (experimental features)
├── tests/ (testing framework)
└── tools/ (individual tools - structure TBD)
```

### **Dependency Rules**
1. **No Circular Dependencies**: Packages cannot import from each other circularly
2. **Clear Hierarchy**: Dependencies flow from core → utilities → tools
3. **Minimal Coupling**: Packages should be loosely coupled
4. **Explicit Dependencies**: All dependencies should be explicit and documented

---

## 📋 **Package Responsibility Matrix**

| Package | Core Functionality | Data Processing | I/O Operations | Logging | CLI | Testing |
|---------|-------------------|-----------------|----------------|---------|-----|---------|
| `common/core/` | ✅ Base classes, Config | ❌ | ❌ | ❌ | ❌ | ❌ |
| `common/data/` | ❌ | ✅ Processing, Validation | ❌ | ❌ | ❌ | ❌ |
| `common/io/` | ❌ | ❌ | ✅ File operations | ❌ | ❌ | ❌ |
| `common/logging/` | ❌ | ❌ | ❌ | ✅ Logging system | ❌ | ❌ |
| `common/cli/` | ❌ | ❌ | ❌ | ❌ | ✅ CLI utilities | ❌ |
| `common/tools/` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `common/pipeline/` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `common/time/` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `common/plugins/` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `cli/` | ❌ | ❌ | ❌ | ❌ | ✅ CLI coordination | ❌ |
| `pipelines/` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `enhancements/` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `misc/` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `tests/` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ Testing framework |

---

## 🚀 **Migration Guidelines**

### **For New Tools**
1. Follow the exemplar tool structure (`rhq_form_autofiller`)
2. Use `import scriptcraft.common as cu`
3. Inherit from `BaseTool`
4. Implement unified CLI system
5. Follow DRY principles

### **For Existing Tools**
1. Migrate to unified CLI system
2. Update imports to use `scriptcraft.common as cu`
3. Inherit from `BaseTool`
4. Remove duplicate code
5. Update documentation

### **For Package Development**
1. Follow single responsibility principle
2. Use clear, descriptive names
3. Document all public APIs
4. Maintain backward compatibility during migration
5. Test thoroughly before changes

---

## 📝 **Notes**

- **Tools Package**: Structure will be defined after exemplar implementation
- **Breaking Changes**: v2.0.0 may include breaking changes for import paths
- **Migration**: Comprehensive migration guide will be provided
- **Documentation**: This document will be updated as patterns evolve
- **Testing**: All packages should have comprehensive test coverage

---

## 🔄 **Next Steps**

1. **Exemplar Implementation**: Complete exemplar tool implementation
2. **Tools Package Structure**: Define structure for individual tools
3. **Migration**: Migrate existing tools to new patterns
4. **Validation**: Test all packages and dependencies
5. **Documentation**: Update all documentation to reflect new structure 