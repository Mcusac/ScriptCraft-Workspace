# Feature Change Checker 📊

Track and analyze how specific features (like cognitive scores) change between visits. Perfect for monitoring longitudinal changes and identifying patterns.

---

📅 **Build Date:** [INSERT_DATE_HERE]

This build was packaged on the date above.  
For reproducibility and support, always refer to this date when sharing logs or output.

---

## 📂 Directory Structure

```
feature_change_checker_shippable/
├── input/                  # Place your clinical data files here
├── output/                # Change analysis reports
├── logs/                  # Detailed execution logs
├── scripts/               # Core implementation (no need to modify)
├── embed_py311/          # Embedded Python environment
├── config.bat            # Configuration settings
└── run.bat              # Start the checker
```

---

## 🚀 Quick Start

1. **Place your data file** in the `input/` folder
   - Must be an Excel file (.xlsx)
   - Must contain visit information
   - Must include the feature column (e.g., CDX_Cog)
2. **Double-click `run.bat`**
3. **Check results** in the `output/` folder:
   - `change_report.xlsx`: Detailed changes
   - `summary.txt`: Quick overview
   - `visualizations/`: Change patterns (if enabled)

---

## 📋 Requirements

- Windows 10 or later
- 4GB RAM minimum
- 500MB free disk space
- Data files must have:
  - Visit information column
  - Feature value column
  - Subject identifiers
  - Consistent formatting

---

## ⚙️ Configuration

Default settings work for most cases, but you can customize:

1. **Feature Settings**
   - Feature name to track
   - Change categorization rules
   - Threshold values

2. **Analysis Options**
   - Raw vs. categorized changes
   - Visit comparison method
   - Missing data handling

3. **Output Settings**
   - Report detail level
   - Visualization options
   - Log verbosity

---

## 📊 Example Usage

### Basic Analysis
1. Copy your clinical data to `input/`
2. Run the checker
3. Review change patterns in reports

### Advanced Analysis
1. Edit config.bat to set:
   - Custom feature name
   - Categorization rules
   - Output preferences
2. Run the checker
3. Check detailed reports

---

## 🔎 Troubleshooting

### Common Issues

1. **"Feature Not Found"**
   - Symptom: Can't find specified feature
   - Solution: Check feature column name

2. **"Missing Visit Data"**
   - Symptom: Visit information incomplete
   - Solution: Verify visit column format

3. **"Invalid Values"**
   - Symptom: Feature values not numeric
   - Solution: Check data formatting

### Error Messages

- `[FC001]`: Missing required columns
- `[FC002]`: Invalid feature values
- `[FC003]`: Visit data issues
- `[FC004]`: Processing error

---

## 📞 Support

- Check `logs/run_log.txt` for detailed error information
- Contact: data.support@organization.com
- Hours: Monday-Friday, 9am-5pm CST
- Response time: Within 1 business day

---

## 📝 Release Notes

### Current Version (1.3.0)
- Added change categorization
- Improved visualization options
- Better handling of missing data
- Enhanced reporting format

### Known Issues
- Limited to one feature at a time
- Some special characters in feature names cause issues
- Workaround: Use simple feature names
- Maximum file size: 1GB

--- 