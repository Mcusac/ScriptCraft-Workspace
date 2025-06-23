# Dictionary Supplementer 📚

Enhance your cleaned dictionaries with domain-specific supplements automatically. Perfect for adding additional data and validations to your domain dictionaries.

---

📅 **Build Date:** [INSERT_DATE_HERE]

This build was packaged on the date above.  
For reproducibility and support, always refer to this date when sharing logs or output.

---

## 📂 Directory Structure

```
dictionary_supplementer_shippable/
├── input/                  # Place your cleaned dictionaries here
│   └── supplements/       # Place domain supplements here
├── output/                # Enhanced dictionaries
├── logs/                  # Detailed execution logs
├── scripts/               # Core implementation (no need to modify)
├── embed_py311/          # Embedded Python environment
├── config.bat            # Configuration settings
└── run.bat              # Start the supplementer
```

---

## 🚀 Quick Start

1. **Prepare your files**:
   - Place cleaned dictionaries in `input/`
   - Place domain supplements in `input/supplements/`
2. **Double-click `run.bat`**
3. **Check results** in the `output/` folder:
   - Enhanced dictionaries
   - Enhancement report
   - Validation log

---

## 📋 Requirements

- Windows 10 or later
- 4GB RAM minimum
- 500MB free disk space
- Files must be:
  - Excel (.xlsx) or CSV
  - Not password protected
  - Follow naming convention:
    - Dictionaries: `[Domain]_cleaned_dictionary.xlsx`
    - Supplements: `[Domain]_supplement.xlsx`
  - Have matching column names
  - Under 50MB each

---

## ⚙️ Configuration

Default settings work for most cases, but you can customize:

1. **Domain Settings**
   - Specific domains to process
   - Domain naming patterns
   - Required columns

2. **Enhancement Settings**
   - Update behavior
   - Validation rules
   - Merge strategy
   - Column mapping

3. **Output Settings**
   - File format
   - Report detail level
   - Log verbosity

---

## 📊 Example Usage

### Basic Enhancement
1. Copy cleaned dictionaries to `input/`
2. Copy supplements to `input/supplements/`
3. Run the supplementer
4. Check enhanced outputs

### Selective Enhancement
1. Edit config.bat to specify domains
2. Place required files
3. Run the supplementer
4. Check selected outputs

---

## 🔎 Troubleshooting

### Common Issues

1. **"Missing Dictionary"**
   - Symptom: Can't find dictionary files
   - Solution: Verify files are in input folder

2. **"Missing Supplement"**
   - Symptom: Can't find supplement files
   - Solution: Check supplement folder

3. **"Format Error"**
   - Symptom: Column mismatch
   - Solution: Check column names match

### Error Messages

- `[DS001]`: Missing input files
- `[DS002]`: Invalid file format
- `[DS003]`: Column mismatch
- `[DS004]`: Processing error

---

## 📞 Support

- Check `logs/run_log.txt` for detailed error information
- Contact: data.support@organization.com
- Hours: Monday-Friday, 9am-5pm CST
- Response time: Within 1 business day

---

## 📝 Release Notes

### Current Version (1.2.0)
- Added selective domain processing
- Improved error messages
- Better validation rules
- Enhanced reporting

### Known Issues
- Maximum 50MB per dictionary
- Some Excel formulas may be lost
- Special characters in headers cause issues
- Workaround: Use simple column names

--- 