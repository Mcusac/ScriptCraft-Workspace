# Dictionary Cleaner 🧹

Clean and standardize your dictionary data files with ease. Perfect for ensuring consistent formatting and structure in your data.

---

📅 **Build Date:** [INSERT_DATE_HERE]

This build was packaged on the date above.  
For reproducibility and support, always refer to this date when sharing logs or output.

---

## 📂 Directory Structure

```
dictionary_cleaner_shippable/
├── input/                  # Place dictionaries here
├── output/                # Cleaned results
├── logs/                  # Execution logs
├── scripts/               # Core implementation (no need to modify)
├── embed_py311/          # Embedded Python environment
├── rules/                # Cleaning rules
├── config.bat            # Configuration settings
└── run.bat              # Start the cleaner
```

---

## 🚀 Quick Start

1. **Prepare your data**:
   - Place dictionary files in `input/`
   - Supports JSON, YAML, Excel
2. **Double-click `run.bat`**
3. **Check results** in `output/`:
   - `cleaned_dict.json`: Clean data
   - `report.txt`: Changes made
   - `validation.txt`: Data checks

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

1. **Cleaning Settings**
   - Rule selection
   - Key formatting
   - Value handling
   - Duplicate strategy

2. **Input Settings**
   - File formats
   - Required keys
   - Data types

3. **Output Settings**
   - Output format
   - Report detail
   - Log level

---

## 📊 Example Usage

### Basic Cleaning
1. Copy dictionary to `input/`
2. Run the cleaner
3. Get cleaned data from `output/`

### Custom Rules
1. Edit config.bat to set:
   - Rule set name
   - Key patterns
   - Value formats
2. Run the cleaner
3. Review changes

---

## 🔎 Troubleshooting

### Common Issues

1. **"File Not Found"**
   - Symptom: Missing input file
   - Solution: Check input/ folder

2. **"Invalid Format"**
   - Symptom: Bad dictionary format
   - Solution: Validate structure

3. **"Key Error"**
   - Symptom: Missing required keys
   - Solution: Check completeness

### Error Messages

- `[DC001]`: Input file missing
- `[DC002]`: Invalid format
- `[DC003]`: Missing keys
- `[DC004]`: Value error

---

## 📞 Support

- Check `logs/run_log.txt` for details
- Contact: data.support@organization.com
- Hours: Monday-Friday, 9am-5pm CST
- Response time: Within 1 business day

---

## 📝 Release Notes

### Current Version (1.1.0)
- Added format detection
- Improved cleaning rules
- Better error messages
- Enhanced reporting

### Known Issues
- Large files slow processing
- Some formats need conversion
- Special characters may change
- Workaround: Split large files

--- 