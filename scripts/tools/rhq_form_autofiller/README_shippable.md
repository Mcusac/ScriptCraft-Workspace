---

### 📄 README_shippable.md

# RHQ Form Autofiller 📝

Automatically fill out RHQ (Residential History Questionnaire) web forms using participant data from Excel files. Uses browser automation to fill forms efficiently and accurately.

---

📅 **Build Date:** [INSERT_DATE_HERE]

This build was packaged on the date above.  
For reproducibility and support, always refer to this date when sharing logs or output.

---

## 📂 Directory Structure

```
rhq_form_autofiller_shippable/
├── input/                  # Place your Excel data files here
├── output/                # (No output files - forms filled directly on web)
├── logs/                  # Execution logs
├── scripts/               # Core implementation (no need to modify)
├── embed_py311/          # Embedded Python environment
├── config.bat            # Configuration settings
└── run.bat              # Start the autofiller
```

---

## 🚀 Quick Start

1. **Prepare your data**:
   - Place Excel file with participant data in `input/`
   - File should contain columns for address information
   - Use format: `rhq_data.xlsx` or any `.xlsx` file
2. **Double-click `run.bat`**
3. **Browser will open automatically**:
   - Tool will navigate to RHQ website
   - Forms will be filled automatically
   - Monitor progress in console window

---

## 📋 Requirements

- Windows 10 or later
- 4GB RAM minimum
- 200MB free disk space
- Internet connection required
- Input data must be:
  - Excel format (.xlsx)
  - Contain participant address data
  - Have proper column headers
  - Under 100MB

---

## ⚙️ Configuration

Default settings work for most cases, but you can customize in config.bat:

1. **Browser Settings**
   - Login credentials
   - Browser timeout
   - Form wait time
   - Auto-login behavior

2. **Input Settings**
   - Excel file detection
   - Column mapping
   - Data validation

3. **Processing Settings**
   - Error handling
   - Retry attempts
   - Log detail level

---

## 📊 Example Usage

### Basic Form Filling
1. Copy participant data Excel file to `input/`
2. Run the autofiller
3. Watch browser automatically fill forms

### Multiple Participants
1. Excel file can contain multiple participants
2. Tool processes each participant sequentially
3. Monitor progress in console

---

## 🔎 Troubleshooting

### Common Issues

1. **"Excel File Not Found"**
   - Symptom: Can't find input file
   - Solution: Check input/ folder contains .xlsx file

2. **"Browser Failed to Load"**
   - Symptom: Browser automation error
   - Solution: Check internet connection and website availability

3. **"Form Fields Not Found"**
   - Symptom: Can't locate form elements
   - Solution: Website may have changed - contact support

### Error Messages

- `[RHQ001]`: Input Excel file missing
- `[RHQ002]`: Browser automation failed
- `[RHQ003]`: Form element not found
- `[RHQ004]`: Network/website error

---

## 📞 Support

- Check `logs/run_log.txt` for detailed error information
- Contact: data.support@organization.com
- Hours: Monday-Friday, 9am-5pm CST
- Response time: Within 1 business day

---

## 📝 Release Notes

### Current Version (2.0.0)
- Enhanced browser automation
- Improved form field detection
- Better error handling
- Multi-language form support

### Known Issues
- Requires active internet connection
- Browser must remain open during processing
- Some form fields may need manual verification
- Workaround: Monitor browser during operation

---
```

Let me know if you'd like to tweak these or expand any sections!
