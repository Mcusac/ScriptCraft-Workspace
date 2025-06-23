# Supplement Splitter 📑

Split a merged supplement file into separate domain-specific supplements automatically. Perfect for organizing and managing domain-specific data supplements.

---

📅 **Build Date:** [INSERT_DATE_HERE]

This build was packaged on the date above.  
For reproducibility and support, always refer to this date when sharing logs or output.

---

## 📂 Directory Structure

```
supplement_splitter_shippable/
├── input/                  # Place your merged supplement here
│   └── dictionaries/      # Place cleaned dictionaries here
├── output/                # Domain-specific supplements
├── logs/                  # Detailed execution logs
├── scripts/               # Core implementation (no need to modify)
├── embed_py311/          # Embedded Python environment
├── config.bat            # Configuration settings
└── run.bat              # Start the splitter
```

---

## 🚀 Quick Start

1. **Prepare your files**:
   - Place merged supplement in `input/`
   - Place cleaned dictionaries in `input/dictionaries/`
2. **Double-click `run.bat`**
3. **Check results** in the `output/` folder:
   - One supplement file per domain
   - Summary report of the split
   - Validation log

---

## 📋 Requirements

- Windows 10 or later
- 4GB RAM minimum
- 500MB free disk space
- Files must be:
  - Supplement: Excel (.xlsx)
  - Dictionaries: CSV format
  - Not password protected
  - Follow naming convention:
    - Supplement: any name
    - Dictionaries: `[Domain]_cleaned_dictionary.csv`

---

## ⚙️ Configuration

Default settings work for most cases, but you can customize:

1. **Domain Settings**
   - Specific domains to process
   - Domain naming patterns
   - Required columns

2. **Input Settings**
   - File naming patterns
   - Dictionary location
   - Validation rules

3. **Output Settings**
   - File naming format
   - Report detail level
   - Log verbosity

---

## 📊 Example Usage

### Basic Split
1. Copy merged supplement to `input/`
2. Copy cleaned dictionaries to `input/dictionaries/`
3. Run the splitter
4. Check domain-specific outputs

### Selective Split
1. Edit config.bat to specify domains
2. Place required files
3. Run the splitter
4. Check selected outputs

---

## 🔎 Troubleshooting

### Common Issues

1. **"Missing Dictionary"**
   - Symptom: Can't find dictionary files
   - Solution: Verify dictionaries are in correct folder

2. **"Invalid Supplement"**
   - Symptom: Supplement format issues
   - Solution: Check supplement file format

3. **"Domain Error"**
   - Symptom: Domain not recognized
   - Solution: Verify domain names match dictionaries

### Error Messages

- `[SS001]`: Missing input files
- `[SS002]`: Invalid file format
- `[SS003]`: Domain mismatch
- `[SS004]`: Processing error

---

## 📞 Support

- Check `logs/run_log.txt` for detailed error information
- Contact: data.support@organization.com
- Hours: Monday-Friday, 9am-5pm CST
- Response time: Within 1 business day

---

## 📝 Release Notes

### Current Version (1.4.0)
- Added selective domain processing
- Improved error handling
- Better progress reporting
- Enhanced validation checks

### Known Issues
- Large supplements (>100MB) may be slow
- Maximum 50 domains per split
- Some special characters in column names cause issues
- Workaround: Use simple column names

--- 