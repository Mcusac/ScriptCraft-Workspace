# Supplement Prepper 🧹

Merge and clean multiple supplement files into a single, standardized file ready for domain-specific processing. Perfect for preparing data supplements for further analysis.

---

📅 **Build Date:** [INSERT_DATE_HERE]

This build was packaged on the date above.  
For reproducibility and support, always refer to this date when sharing logs or output.

---

## 📂 Directory Structure

```
supplement_prepper_shippable/
├── input/                  # Place your supplement files here
├── output/                # Merged and cleaned supplement
├── logs/                  # Detailed execution logs
├── scripts/               # Core implementation (no need to modify)
├── embed_py311/          # Embedded Python environment
├── config.bat            # Configuration settings
└── run.bat              # Start the prepper
```

---

## 🚀 Quick Start

1. **Prepare your files**:
   - Place supplement files in `input/`
   - Supported formats: .xlsx, .xls, .csv
2. **Double-click `run.bat`**
3. **Check results** in the `output/` folder:
   - Merged supplement file
   - Cleaning report
   - Validation log

---

## 📋 Requirements

- Windows 10 or later
- 4GB RAM minimum
- 500MB free disk space
- Files must be:
  - Excel (.xlsx, .xls) or CSV
  - Not password protected
  - Have consistent column names
  - No special formatting
  - Under 100MB each

---

## ⚙️ Configuration

Default settings work for most cases, but you can customize:

1. **Input Settings**
   - File naming patterns
   - Required columns
   - Date formats
   - Character encoding

2. **Cleaning Settings**
   - Column standardization
   - Missing value handling
   - Duplicate handling
   - Data validation rules

3. **Output Settings**
   - File format
   - Report detail level
   - Log verbosity

---

## 📊 Example Usage

### Basic Merge
1. Copy supplement files to `input/`
2. Run the prepper
3. Check merged output

### Custom Configuration
1. Edit config.bat
2. Place input files
3. Run the prepper
4. Check customized output

---

## 🔎 Troubleshooting

### Common Issues

1. **"Missing Files"**
   - Symptom: Can't find input files
   - Solution: Verify files are in input folder

2. **"Format Error"**
   - Symptom: Column mismatch
   - Solution: Check column names match

3. **"Memory Error"**
   - Symptom: Process stops
   - Solution: Split large files first

### Error Messages

- `[SP001]`: Missing input files
- `[SP002]`: Invalid file format
- `[SP003]`: Column mismatch
- `[SP004]`: Memory error

---

## 📞 Support

- Check `logs/run_log.txt` for detailed error information
- Contact: data.support@organization.com
- Hours: Monday-Friday, 9am-5pm CST
- Response time: Within 1 business day

---

## 📝 Release Notes

### Current Version (1.3.0)
- Added CSV support
- Improved memory handling
- Better error messages
- Enhanced cleaning rules

### Known Issues
- Maximum 100MB per input file
- Some Excel formulas may be lost
- Special characters in headers cause issues
- Workaround: Use simple column names

--- 