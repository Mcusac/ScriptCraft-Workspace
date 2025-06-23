# Dictionary Driven Checker 📚

Validate your data against a data dictionary to ensure it meets all requirements. Perfect for quality control and data validation workflows.

---

📅 **Build Date:** [INSERT_DATE_HERE]

This build was packaged on the date above.  
For reproducibility and support, always refer to this date when sharing logs or output.

---

## 📂 Directory Structure

```
dictionary_driven_checker_distributable/
├── input/                  # Place your data and dictionary files here
├── output/                # Validation reports
├── logs/                  # Detailed execution logs
├── scripts/               # Core implementation (no need to modify)
├── embed_py311/          # Embedded Python environment
├── config.bat            # Configuration settings
└── run.bat              # Start the checker
```

---

## 🚀 Quick Start

1. **Place your files** in the `input/` folder:
   - Your data file (e.g., `clinical_data.xlsx`)
   - Dictionary file (e.g., `Clinical_dictionary.csv`)
2. **Double-click `run.bat`**
3. **Check results** in the `output/` folder:
   - `validation_report.xlsx`: Detailed findings
   - `summary.txt`: Quick overview
   - `outliers.csv`: Identified outliers

---

## 📋 Requirements

- Windows 10 or later
- 4GB RAM minimum
- 500MB free disk space
- Files must be:
  - Data: Excel (.xlsx) or CSV
  - Dictionary: CSV format
  - Not password protected
  - Follow naming convention:
    - Data: any name
    - Dictionary: `[Domain]_dictionary.csv`

---

## ⚙️ Configuration

Default settings work for most cases, but you can customize:

1. **Validation Rules**
   - Outlier detection method
   - Text validation rules
   - Date format requirements
   - Custom validation rules

2. **Input Settings**
   - File naming patterns
   - Required columns
   - Domain settings

3. **Output Settings**
   - Report format
   - Error highlighting
   - Log detail level

---

## 📊 Example Usage

### Basic Validation
1. Copy your files to `input/`:
   - `clinical_data.xlsx`
   - `Clinical_dictionary.csv`
2. Run the checker
3. Review validation report

### Advanced Validation
1. Edit config.bat to set:
   - Custom validation rules
   - Domain-specific settings
   - Output preferences
2. Run the checker
3. Check detailed reports

---

## 🔎 Troubleshooting

### Common Issues

1. **"Dictionary Not Found"**
   - Symptom: Can't find dictionary file
   - Solution: Check file naming (must be `[Domain]_dictionary.csv`)

2. **"Invalid Column"**
   - Symptom: Column missing from dictionary
   - Solution: Update dictionary or check column names

3. **"Data Type Error"**
   - Symptom: Data doesn't match dictionary type
   - Solution: Check data format matches dictionary

### Error Messages

- `[DD001]`: Missing dictionary file
- `[DD002]`: Invalid data format
- `[DD003]`: Column validation error
- `[DD004]`: Outlier detected

---

## 📞 Support

- Check `logs/run_log.txt` for detailed error information
- Contact: data.support@organization.com
- Hours: Monday-Friday, 9am-5pm CST
- Response time: Within 1 business day

---

## 📝 Release Notes

### Current Version (2.0.0)
- Added plugin system for custom validation
- Improved outlier detection
- Better error reporting
- Enhanced dictionary support

### Known Issues
- Large files (>1GB) may be slow
- Some special characters in column names cause issues
- Maximum 1000 columns per file
- Workaround: Split large files

--- 