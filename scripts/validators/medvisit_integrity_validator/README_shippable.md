# MedVisit Integrity Validator 🏥

Validate the integrity and consistency of your medical visit data. Perfect for ensuring data quality and compliance.

---

📅 **Build Date:** [INSERT_DATE_HERE]

This build was packaged on the date above.  
For reproducibility and support, always refer to this date when sharing logs or output.

---

## 📂 Directory Structure

```
medvisit_integrity_validator_shippable/
├── input/                  # Place visit data here
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
   - Place visit files in `input/`
   - Supports CSV, Excel, JSON
2. **Double-click `run.bat`**
3. **Check results** in `output/`:
   - `validation.json`: Results
   - `report.txt`: Summary
   - `errors.txt`: Issues found

---

## 📋 Requirements

- Windows 10 or later
- 4GB RAM minimum
- 500MB free disk space
- Files must be:
  - Valid visit data format
  - Not corrupted
  - Under 500MB each

---

## ⚙️ Configuration

Default settings work for most cases, but you can customize:

1. **Validation Settings**
   - Rule selection
   - Error thresholds
   - Reference checks
   - Temporal rules

2. **Input Settings**
   - File formats
   - Required fields
   - Data types

3. **Output Settings**
   - Report format
   - Error detail
   - Log level

---

## 📊 Example Usage

### Basic Validation
1. Copy visit data to `input/`
2. Run the validator
3. Check results in `output/`

### Custom Rules
1. Edit config.bat to set:
   - Rule set name
   - Error levels
   - Field mappings
2. Run the validator
3. Review findings

---

## 🔎 Troubleshooting

### Common Issues

1. **"File Not Found"**
   - Symptom: Missing input file
   - Solution: Check input/ folder

2. **"Invalid Format"**
   - Symptom: Bad data format
   - Solution: Check file structure

3. **"Reference Error"**
   - Symptom: Missing references
   - Solution: Check dependencies

### Error Messages

- `[MV001]`: Input file missing
- `[MV002]`: Invalid format
- `[MV003]`: Reference error
- `[MV004]`: Rule violation

---

## 📞 Support

- Check `logs/run_log.txt` for details
- Contact: meddata.support@organization.com
- Hours: Monday-Friday, 9am-5pm CST
- Response time: Within 1 business day

---

## 📝 Release Notes

### Current Version (1.4.0)
- Added temporal validation
- Improved error reporting
- Better reference checks
- Enhanced summaries

### Known Issues
- Large files slow processing
- Some formats need conversion
- Complex rules take time
- Workaround: Split large files

--- 