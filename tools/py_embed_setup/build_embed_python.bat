@echo off
setlocal EnableDelayedExpansion

:: ================================
:: 🔧 Configuration
:: ================================
:: Use more robust path handling to avoid drive access issues
set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%..\.."
set "CONFIG_PATH=%ROOT_DIR%\config.yaml"
set "LOG_FILE=%SCRIPT_DIR%build_embed.log"
set "EMBED_DIR=%SCRIPT_DIR%embed_py311"
set "EMBED_ZIP=%SCRIPT_DIR%embed_py311.zip"
set "PYTHON=%EMBED_DIR%\python.exe"
set "TOOL_NAME=%~1"

:: ================================
:: 📝 Begin logging
:: ================================
(
echo 🔍 Starting embedded Python build process
echo ===============================
echo 🕒 %DATE% %TIME%
echo ===============================
echo.
echo 🔧 DEBUG: Path Information
echo SCRIPT_DIR: %SCRIPT_DIR%
echo ROOT_DIR: %ROOT_DIR%
echo CONFIG_PATH: %CONFIG_PATH%
echo EMBED_DIR: %EMBED_DIR%
echo EMBED_ZIP: %EMBED_ZIP%
echo.

:: ================================
:: 📦 Get packages from config.yaml
:: ================================
echo DEBUG: Tool name is: "%TOOL_NAME%"
if not "%TOOL_NAME%"=="" (
    echo DEBUG: Looking for packages in config.yaml for tool: %TOOL_NAME%
    for /f "usebackq tokens=*" %%P in (`python -c "import yaml, os; f=open(os.path.normpath(r'%CONFIG_PATH%'), encoding='utf-8'); c=yaml.safe_load(f); print(' '.join(c['tools']['%TOOL_NAME%']['packages']))"`) do (
        set "PACKAGES=%%P"
        echo DEBUG: Found packages: !PACKAGES!
        echo DEBUG: Raw packages string: [!PACKAGES!]
    )
)

:: ================================
:: ⛑️ Fallback if PACKAGES is empty
:: ================================
if "!PACKAGES!"=="" (
    echo ⚠️ No packages found for tool %TOOL_NAME%. Using fallback list.
    set "PACKAGES=pyyaml pandas numpy pytz python-dateutil"
)

:: ================================
:: 🔍 Requested packages
:: ================================
echo 🔍 Requested packages: !PACKAGES!

:: ================================
:: 🔁 Cleanup old build
:: ================================
if exist "%EMBED_DIR%" (
    echo 🔁 Removing previous embed_py311...
    rd /s /q "%EMBED_DIR%" 2>nul
)

:: ================================
:: 📦 Unzip embedded Python base
:: ================================
if not exist "%EMBED_ZIP%" (
    echo ❌ ERROR: %EMBED_ZIP% not found!
    exit /b 1
)
echo 📦 Extracting %EMBED_ZIP%...
powershell -Command "Expand-Archive -Path '%EMBED_ZIP%' -DestinationPath '%EMBED_DIR%' -Force"

:: ================================
:: ✅ Validate python
:: ================================
if not exist "%PYTHON%" (
    echo ❌ ERROR: python.exe not found after unzip!
    exit /b 1
)

:: ================================
:: 🐍 Download get-pip.py
:: ================================
echo 📥 Downloading get-pip.py...
pushd "%EMBED_DIR%"
powershell -Command "Invoke-WebRequest https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py"

:: ================================
:: 💾 Install pip
:: ================================
echo 🔧 Installing pip...
"%PYTHON%" get-pip.py --no-warn-script-location
if errorlevel 1 (
    echo ❌ ERROR: pip installation failed
    exit /b 1
)
del get-pip.py

:: ================================
:: 📦 Installing setuptools + wheel
:: ================================
echo 🔧 Installing setuptools and wheel...
"%PYTHON%" -m pip install --no-cache-dir setuptools wheel

:: ================================
:: 📦 Install additional packages
:: ================================
if not "!PACKAGES!"=="" (
    echo 📦 Installing packages: !PACKAGES!
    "%PYTHON%" -m pip install --no-cache-dir !PACKAGES! --no-warn-script-location
    if errorlevel 1 (
        echo ❌ ERROR: Failed installing packages
        exit /b 1
    )
)

:: ================================
:: 🧾 List installed packages
:: ================================
echo 📋 Final installed packages:
"%PYTHON%" -m pip list

popd

echo.
echo ✅ DONE %EMBED_DIR%
) > "%LOG_FILE%" 2>&1

exit /b 0
