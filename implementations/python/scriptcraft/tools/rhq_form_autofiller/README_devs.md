---

### 📄 README\_devs.md

# RHQ Form Autofiller 🤖

A Python tool for automatically filling RHQ web forms using pre-processed data from an Excel file. Supports both development mode (within the workspace) and a distributable version for distribution.

---

📅 **Build Date:** [INSERT_DATE_HERE]

This build was packaged on the date above.  
For reproducibility and support, always refer to this date when sharing logs or output.

---

## 📦 Project Structure

```

If in Distributable:
rhq\_form\_autofiller\_distributable/
├── input/                  # Place your Excel files here
├── output/                 # Outputs from form submissions
├── logs/                   # Log file of the most recent run
├── scripts/
│   ├── main.py             # Entry point for form autofilling
│   ├── utils.py            # Core logic for Selenium automation
│   ├── common/             # Shared utilities
│   │   ├── common\_utils.py
│   │   ├── file\_path\_utils.py
│   │   ├── logging\_utils.py
│   │   ├── ... (other shared files)
│   └── **init**.py         # (Optional) package marker
├── embed\_py311/            # Embedded Python environment
├── config.bat              # Predefined configuration (no need to edit)
└── run.bat                 # The entry point for execution

```
```

If in Dev Workspace:
Release Workspace/
├── input/                  # (Optional) Example Excel input for testing
├── output/                 # (Optional) Test outputs
├── logs/                   # Run logs
├── scripts/
│   ├── tools/
│   │   ├── rhq\_form\_autofiller/
│   │   │   ├── main.py
│   │   │   ├── utils.py
│   │   │   ├── **init**.py
│   ├── common/
│   │   ├── common\_utils.py
│   │   ├── file\_path\_utils.py
│   │   ├── logging\_utils.py
│   │   ├── ... (other shared files)
│   └── pipelines/
│       ├── pipeline\_utils.py
│       ├── ... (other pipeline helpers)
├── templates/
│   ├── package\_template/
│   ├── ... (other templates)
├── distributables/         # Output of packaged distributables
└── config.yaml             # Central config

````

---

## 🚀 Usage (Development)

To run directly:

```bash
python -m tools.rhq_form_autofiller.main --input input.xlsx --med_id 12345
````

* `--input`: Path to the Excel file containing addresses.
* `--med_id`: (Optional) Specific Med\_ID to filter.
* `--validate`: (Optional) Enable field validation for entries.

---

## ⚙️ Features

✅ Automatic data entry into web form panels.
✅ Supports dynamic block addition and removal.
✅ Seamless handling of multiple address blocks per panel.
✅ Intelligent field skipping for empty or 'MISSING' entries.
✅ Logs of each automation step for easy debugging.

---

## 🔧 Dev Tips

* Check `utils.py` for customization of the panel-filling logic.
* Use `logs/` to monitor each run's progress and troubleshoot issues.
* Update `FIELD_LABEL_MAP` in `utils.py` if field labels on the web form change (e.g., for Spanish versions).

---

## 🗂️ Future Improvements

* Support for multiple languages and dynamic panel header detection.
* Enhanced form validation and error reporting.
* Integration with future domain-based QC tools.

---

````