@echo off
setlocal EnableDelayedExpansion

:: ================================
:: 🔧 Build Common Embedded Python (Run Once)
:: ================================
set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%..\.."
set "CONFIG_PATH=%ROOT_DIR%\config.yaml"
set "LOG_FILE=%ROOT_DIR%\logs\00_build_common_python.txt"
set "EMBED_DIR=%SCRIPT_DIR%..\py_embed_setup\embed_py311"
set "EMBED_ZIP=%SCRIPT_DIR%..\py_embed_setup\embed_py311.zip"
set "PYTHON=%EMBED_DIR%\python.exe"
set "TEMPLATE_EMBED_DIR=%ROOT_DIR%\templates\distributable_template\embed_py311"

:: ================================
:: 📁 Ensure logs folder
:: ================================
if not exist "%SCRIPT_DIR%logs" mkdir "%SCRIPT_DIR%logs"

:: ================================
:: 📝 Begin logging
:: ================================
(
echo 🔧 Building Common Embedded Python (Run Once)
echo ===============================
echo 🕒 %DATE% %TIME%
echo ===============================
echo.

:: ================================
:: 🔍 Check if already built (always rebuild for packaging)
:: ================================
if exist "%TEMPLATE_EMBED_DIR%" (
    echo 🔁 Common embedded Python exists at: %TEMPLATE_EMBED_DIR%
    echo 🔄 Removing existing template for fresh build...
    rd /s /q "%TEMPLATE_EMBED_DIR%" 2>nul
)

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
    echo 💡 Download embed_py311.zip from python.org and place it in py_embed_setup/
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
:: 🔧 Enable site packages for pip to work
:: ================================
echo 🔧 Enabling site packages in python311._pth...
powershell -Command "(Get-Content 'python311._pth') -replace '#import site', 'import site' | Set-Content 'python311._pth'"

:: ================================
:: 📦 Installing setuptools + wheel
:: ================================
echo 🔧 Installing setuptools and wheel...
"%PYTHON%" -m pip install --no-cache-dir setuptools wheel

:: ================================
:: 📦 Install common packages initially (hardcoded list)
:: ================================
echo 📦 Installing common packages first...
set "COMMON_PACKAGES=setuptools wheel pandas numpy openpyxl python-docx pyyaml pytz python-dateutil selenium"

echo 📦 Common packages: !COMMON_PACKAGES!
for %%p in (!COMMON_PACKAGES!) do (
    echo 📦 Installing: %%p
    "%PYTHON%" -m pip install --no-cache-dir %%p --no-warn-script-location
    if errorlevel 1 (
        echo ❌ ERROR: Failed installing %%p
        exit /b 1
    )
)

:: ================================
:: 📋 Generate config.bat from config.yaml (after pyyaml is installed)
:: ================================
echo 📋 Generating config.bat from config.yaml...
python "%SCRIPT_DIR%config_processor.py" config_bat "%CONFIG_PATH%" "%ROOT_DIR%\templates\distributable_template" "%DATE% %TIME%"
if errorlevel 1 (
    echo ❌ ERROR: Failed to generate config.bat
    exit /b 1
)

echo 📦 Common packages: !COMMON_PACKAGES!
for %%p in (!COMMON_PACKAGES!) do (
    echo 📦 Installing: %%p
    "%PYTHON%" -m pip install --no-cache-dir %%p --no-warn-script-location
    if errorlevel 1 (
        echo ❌ ERROR: Failed installing %%p
        exit /b 1
    )
)

:: ================================
:: 📦 Install/Update ScriptCraft package from PyPI (Common Package for all Distributables)
:: ================================
echo 📦 Installing/updating ScriptCraft package from PyPI (common package for all distributables)...
"%PYTHON%" -m pip install --no-cache-dir scriptcraft-python --force-reinstall
if errorlevel 1 (
    echo ❌ ERROR: Failed installing ScriptCraft package from PyPI
    exit /b 1
)
echo ✅ ScriptCraft package installed/updated successfully from PyPI

:: ================================
:: ✅ Verify ScriptCraft installation
:: ================================
echo ✅ Verifying ScriptCraft installation...
"%PYTHON%" -c "import scriptcraft; print('ScriptCraft version:', scriptcraft.__version__)"
if errorlevel 1 (
    echo ❌ ERROR: ScriptCraft import failed after installation
    exit /b 1
)

:: ================================
:: 🧹 Fix distutils-precedence.pth issue
:: ================================
echo 🧹 Fixing distutils-precedence.pth issue...
if exist "%EMBED_DIR%\Lib\site-packages\distutils-precedence.pth" (
    del "%EMBED_DIR%\Lib\site-packages\distutils-precedence.pth"
    echo ✅ Removed problematic distutils-precedence.pth file
) else (
    echo ℹ️ distutils-precedence.pth not found (already fixed)
)

:: ================================
:: 🧾 List installed packages
:: ================================
echo 📋 Final installed packages:
"%PYTHON%" -m pip list

:: ================================
:: 📁 Copy to template directory
:: ================================
echo 📁 Copying to template directory...
if exist "%TEMPLATE_EMBED_DIR%" (
    rd /s /q "%TEMPLATE_EMBED_DIR%"
)
xcopy /e /i /y "%EMBED_DIR%" "%TEMPLATE_EMBED_DIR%" >nul 2>&1
echo ✅ Common embedded Python copied to template

:: ================================
:: 🧹 Cleanup build directory
:: ================================
echo 🧹 Cleaning up build directory...
rd /s /q "%EMBED_DIR%" 2>nul

popd

echo.
echo ✅ Common Embedded Python Built Successfully
echo 📁 Template location: %TEMPLATE_EMBED_DIR%
echo 📋 Log: %LOG_FILE%
) > "%LOG_FILE%" 2>&1

echo.
echo ✅ Common Embedded Python Built Successfully
echo 📁 Template location: %TEMPLATE_EMBED_DIR%
echo 📋 Log: %LOG_FILE%

exit /b 0
