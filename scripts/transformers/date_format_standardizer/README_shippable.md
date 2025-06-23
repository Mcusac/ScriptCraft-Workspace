# Date Format Standardizer 📅

Standardize date formats across your data files with ease. Perfect for ensuring consistent date representation in your data.

---

📅 **Build Date:** [INSERT_DATE_HERE]

This build was packaged on the date above.  
For reproducibility and support, always refer to this date when sharing logs or output.

---

## 📂 Directory Structure

```
date_format_standardizer_shippable/
├── input/                  # Place files with dates here
├── output/                # Standardized results
├── logs/                  # Execution logs
├── scripts/               # Core implementation (no need to modify)
├── embed_py311/          # Embedded Python environment
├── formats/              # Date format definitions
├── config.bat            # Configuration settings
└── run.bat              # Start the standardizer
```

---

## 🚀 Quick Start

1. **Prepare your data**:
   - Place files in `input/`
   - Supports CSV, Excel, Text
2. **Double-click `run.bat`**
3. **Check results** in `output/`:
   - `standardized_dates.csv`: Clean data
   - `report.txt`: Changes made
   - `errors.txt`: Problem dates

---

## 📋 Requirements

- Windows 10 or later
- 4GB RAM minimum
- 200MB free disk space
- Files must be:
  - Valid data format
  - Contain date columns
  - Under 500MB each

---

## ⚙️ Configuration

Default settings work for most cases, but you can customize:

1. **Format Settings**
   - Target format
   - Input formats
   - Locale settings
   - Timezone handling

2. **Input Settings**
   - File types
   - Date columns
   - Validation rules

3. **Output Settings**
   - Output format
   - Report detail
   - Log level

---

## 📊 Example Usage

### Basic Standardization
1. Copy files to `input/`
2. Run the standardizer
3. Get standardized data from `output/`

### Custom Format
1. Edit config.bat to set:
   - Target format
   - Input formats
   - Column names
2. Run the standardizer
3. Review changes

---

## 🔎 Troubleshooting

### Common Issues

1. **"File Not Found"**
   - Symptom: Missing input file
   - Solution: Check input/ folder

2. **"Invalid Date"**
   - Symptom: Date parsing failed
   - Solution: Check date format

3. **"Unknown Format"**
   - Symptom: Format not recognized
   - Solution: Add format to config

### Error Messages

- `[DS001]`: Input file missing
- `[DS002]`: Invalid date
- `[DS003]`: Unknown format
- `[DS004]`: Processing error

---

## 📞 Support

- Check `logs/run_log.txt` for details
- Contact: data.support@organization.com
- Hours: Monday-Friday, 9am-5pm CST
- Response time: Within 1 business day

---

## 📝 Release Notes

### Current Version (1.2.0)
- Added format detection
- Improved error handling
- Better locale support
- Enhanced reporting

### Known Issues
- Large files slow processing
- Some formats need manual setup
- Timezone conversion limited
- Workaround: Split large files

--- 