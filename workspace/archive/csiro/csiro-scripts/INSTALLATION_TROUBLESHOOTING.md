# Installation Troubleshooting

## Windows Path Length Issue

If you get errors like:
```
ERROR: Could not install packages due to an OSError: [Errno 2] No such file or directory: 
'C:\\Users\\...\\...\\predicated_tile_access_iterator_residual_last.h'
```

This is a Windows path length limit issue (260 characters). Here are solutions:

### Solution 1: Use a Virtual Environment in a Short Path (RECOMMENDED)

Create a virtual environment in a short path:

```bash
# Create venv in a short path (e.g., C:\venv\csiro)
python -m venv C:\venv\csiro

# Activate it
C:\venv\csiro\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Solution 2: Enable Long Path Support in Windows (Requires Admin)

1. Open PowerShell as Administrator
2. Run:
   ```powershell
   New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
   ```
3. Restart your computer
4. Try installing again

### Solution 3: Install Python from python.org (Instead of Windows Store)

1. Download Python from https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Install to a short path like `C:\Python311\`
4. Use this Python instead of Windows Store Python

### Solution 4: Use Conda/Miniconda

Conda handles long paths better:

```bash
# Install Miniconda from https://docs.conda.io/en/latest/miniconda.html
# Then create environment
conda create -n csiro python=3.11
conda activate csiro
pip install -r requirements.txt
```

### Solution 5: Install to User Directory (May Still Have Issues)

```bash
pip install --user -r requirements.txt
```

**Note**: This may still fail due to path length, but worth trying.

## Recommended Approach

For this project, **Solution 1 (Virtual Environment in Short Path)** is recommended:
- No admin rights needed
- Works immediately
- Keeps dependencies isolated
- Avoids path length issues

Example:
```bash
# From your project directory
cd C:\Users\mdc0431\OneDrive - UNT System\Documents\Kaggle\CSIRO
python -m venv venv
venv\Scripts\activate
pip install -r csiro-scripts\requirements.txt
```
