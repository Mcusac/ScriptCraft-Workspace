# Scripts Directory Structure

## Overview
This directory contains all the data processing, validation, and quality control scripts organized by their primary function.

## Categories

### Data Validators (`/validators`)
Components that validate data structure, format, and content rules.
- `dictionary_validator`: Validates data against dictionary rules
- `medvisit_integrity_validator`: Validates visit data integrity

### Data Transformers (`/transformers`)
Components that transform data format or structure.
- `date_format_standardizer`: Standardizes date formats
- `dictionary_cleaner`: Cleans and standardizes dictionary entries

### Quality Checkers (`/checkers`)
Components that analyze data quality and consistency.
- `score_totals_checker`: Validates score calculations
- `release_consistency_checker`: Checks release-to-release consistency
- `feature_change_checker`: Tracks feature changes across visits

### Dictionary Tools (`/dictionary_tools`)
Consolidated dictionary-related functionality.
- Links to `dictionary_cleaner` (transformer)
- Links to `dictionary_validator` (validator)
- `dictionary_driven_checker`: Dictionary-based data validation

## Package Organization Rules

1. **Single Responsibility**
   - Each package should have a clear, single purpose
   - Avoid mixing validation, transformation, and checking logic

2. **Consistent Interfaces**
   - Validators implement `BaseValidator`
   - Transformers implement `BaseTransformer`
   - Checkers implement `BaseChecker`

3. **Plugin Architecture**
   - Each category supports plugins for extensibility
   - Common functionality shared through base classes
   - Category-specific utilities in respective base packages

4. **Dependencies**
   - Validators can depend on transformers
   - Checkers can depend on validators
   - Dictionary tools can depend on any category

## Usage

Each component can be used independently or as part of a pipeline:

```python
# As part of a pipeline
pipeline_steps = [
    "dictionary_cleaner",
    "dictionary_validator",
    "score_totals_checker"
]

# Standalone usage
from validators.medvisit_integrity_validator import validator
validator.run(domain="Clinical", input_path="data.csv")
```
