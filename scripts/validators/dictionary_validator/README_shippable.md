# Dictionary Validator 📚

Validate your dictionary data to ensure it meets required standards, formats, and relationships. Perfect for maintaining data quality and consistency.

---

📅 **Build Date:** [INSERT_DATE_HERE]

This build was packaged on the date above.  
For reproducibility and support, always refer to this date when sharing logs or output.

---

## 📂 Directory Structure

```
dictionary_validator_shippable/
├── input/                  # Place dictionaries here
├── output/                # Validation results
├── logs/                  # Execution logs
├── scripts/               # Core implementation (no need to modify)
├── embed_py311/          # Embedded Python environment
├── rules/                # Validation rules
├── config.bat            # Configuration settings
└── run.bat              # Start the validator
```

---

## 🚀 Quick Start

1. **Prepare your data**:
   - Place dictionary files in `input/`
   - Supports JSON, YAML, Excel
2. **Double-click `run.bat`**
3. **Check results** in `output/`:
   - `validation.json`: Results
   - `report.txt`: Summary
   - `errors.txt`: Issues found

---

## 📋 Requirements

- Windows 10 or later
- 2GB RAM minimum
- 200MB free disk space
- Files must be:
  - Valid dictionary format
  - Not corrupted
  - Under 100MB each

---

## ⚙️ Configuration

Default settings work for most cases, but you can customize:

1. **Validation Settings**
   - Rule selection
   - Schema checks
   - Key validation
   - Value constraints

2. **Input Settings**
   - File formats
   - Required keys
   - Data types

3. **Output Settings**
   - Report format
   - Error detail
   - Log level

---

## 📊 Example Usage

### Basic Validation
1. Copy dictionary to `input/`
2. Run the validator
3. Check results in `output/`

### Custom Rules
1. Edit config.bat to set:
   - Rule set name
   - Schema file
   - Key patterns
2. Run the validator
3. Review findings

---

## 🔎 Troubleshooting

### Common Issues

1. **"File Not Found"**
   - Symptom: Missing input file
   - Solution: Check input/ folder

2. **"Invalid Format"**
   - Symptom: Bad dictionary format
   - Solution: Check file structure

3. **"Schema Error"**
   - Symptom: Invalid structure
   - Solution: Fix dictionary format

### Error Messages

- `[DV001]`: Input file missing
- `[DV002]`: Invalid format
- `[DV003]`: Schema error
- `[DV004]`: Value error

---

## 📞 Support

- Check `logs/run_log.txt` for details
- Contact: data.support@organization.com
- Hours: Monday-Friday, 9am-5pm CST
- Response time: Within 1 business day

---

## 📝 Release Notes

### Current Version (1.2.0)
- Added schema validation
- Improved error reporting
- Better key checking
- Enhanced summaries

### Known Issues
- Large files slow processing
- Some formats need conversion
- Complex schemas take time
- Workaround: Split large files

--- 