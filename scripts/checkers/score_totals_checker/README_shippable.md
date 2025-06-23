# Score Totals Checker 🔢

Automatically validates score totals in your Excel files, ensuring all calculations are correct and consistent.

---

📅 **Build Date:** [INSERT_DATE_HERE]

This build was packaged on the date above.  
For reproducibility and support, always refer to this date when sharing logs or output.

---

## 📂 Directory Structure

```
score_totals_checker_shippable/
├── input/                  # Place your Excel files here
├── output/                # Validation reports
├── logs/                  # Detailed execution logs
├── scripts/               # Core implementation (no need to modify)
├── embed_py311/          # Embedded Python environment
├── config.bat            # Configuration settings
└── run.bat              # Start the checker
```

---

## 🚀 Quick Start

1. **Place your Excel file** in the `input/` folder
2. **Double-click `run.bat`**
3. **Check results** in the `output/` folder
   - `validation_report.xlsx`: Detailed findings
   - `summary.txt`: Quick overview

---

## 📋 Requirements

- Windows 10 or later
- 4GB RAM minimum
- 500MB free disk space
- Excel files must be:
  - .xlsx format
  - Have score columns
  - Include total columns/rows
  - Not password protected

---

## ⚙️ Configuration

Default settings work for most cases, but you can customize:

1. **Input Settings**
   - Score column names
   - Total column/row identifiers
   - Sheet names to check

2. **Validation Settings**
   - Tolerance for floating point comparisons
   - Required vs optional totals
   - Missing data handling

3. **Output Settings**
   - Report format
   - Error highlighting
   - Log detail level

---

## 📊 Example Usage

### Basic Use
1. Copy `example_scores.xlsx` to `input/`
2. Run the checker
3. Review `validation_report.xlsx` in `output/`

### Advanced Use
- Multiple files: Place all files in `input/`
- Large files: See performance tips in logs
- Custom validation: Edit config.bat

---

## 🔎 Troubleshooting

### Common Issues

1. **"Missing Total Column"**
   - Symptom: Checker can't find totals
   - Solution: Verify total column name matches config

2. **"Calculation Mismatch"**
   - Symptom: Totals don't match calculated values
   - Solution: Check for hidden formulas or formatting

### Error Messages

- `[ST001]`: Missing required columns
- `[ST002]`: Total mismatch found
- `[ST003]`: Invalid data format

---

## 📞 Support

- Check `logs/run_log.txt` for detailed error information
- Contact: data.support@organization.com
- Hours: Monday-Friday, 9am-5pm CST
- Response time: Within 1 business day

---

## 📝 Release Notes

### Current Version (1.2.0)
- Added support for multiple sheets
- Improved error reporting
- Better handling of missing data

### Known Issues
- Large files (>1GB) may be slow
- Some special characters in sheet names cause issues
- Workaround: Rename sheets to simple names

--- 