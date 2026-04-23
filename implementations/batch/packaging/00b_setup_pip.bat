@echo off

REM Basic path setup
set "SCRIPT_DIR=%~dp0"
for %%i in ("%SCRIPT_DIR%..\..\py_embed_setup\embed_py311") do set "EMBED_DIR=%%~fi"
set "PYTHON=%EMBED_DIR%\python.exe"

REM Setup logging
for %%i in ("%SCRIPT_DIR%..\..\data\logs") do set "LOG_DIR=%%~fi"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
set "LOG_FILE=%LOG_DIR%\00b_setup_pip.txt"

REM Start logging
echo Component 0b: Setup Pip and Base Packages > "%LOG_FILE%"
echo ========================================== >> "%LOG_FILE%"
echo %DATE% %TIME% >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

echo Component 0b: Setup Pip and Base Packages
echo ==========================================

REM Check if Python exists
echo Validating Python installation... >> "%LOG_FILE%"
echo Validating Python installation...
if not exist "%PYTHON%" (
    echo ERROR: Python not found at %PYTHON% >> "%LOG_FILE%"
    echo ERROR: Python not found at %PYTHON%
    echo Run component 0a first >> "%LOG_FILE%"
    echo Run component 0a first
    exit /b 1
)

echo Python found: %PYTHON% >> "%LOG_FILE%"
echo Python found: %PYTHON%
echo. >> "%LOG_FILE%"
echo.

REM Go to Python directory
cd /d "%EMBED_DIR%"

echo Downloading get-pip.py... >> "%LOG_FILE%"
echo Downloading get-pip.py...
powershell -Command "Invoke-WebRequest https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: Failed to download get-pip.py >> "%LOG_FILE%"
    echo ERROR: Failed to download get-pip.py
    exit /b 1
)
echo Download completed >> "%LOG_FILE%"

echo Installing pip... >> "%LOG_FILE%"
echo Installing pip...
"%PYTHON%" get-pip.py --no-warn-script-location >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: pip installation failed >> "%LOG_FILE%"
    echo ERROR: pip installation failed
    exit /b 1
)

echo Cleaning up... >> "%LOG_FILE%"
echo Cleaning up...
del get-pip.py

echo Enabling site packages... >> "%LOG_FILE%"
echo Enabling site packages...
powershell -Command "(Get-Content 'python311._pth') -replace '#import site', 'import site' | Set-Content 'python311._pth'" >> "%LOG_FILE%" 2>&1

echo Installing setuptools and wheel... >> "%LOG_FILE%"
echo Installing setuptools and wheel...
"%PYTHON%" -m pip install --no-cache-dir setuptools wheel >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: Failed to install setuptools and wheel >> "%LOG_FILE%"
    echo ERROR: Failed to install setuptools and wheel
    exit /b 1
)

echo SUCCESS: Component 0b completed successfully >> "%LOG_FILE%"
echo SUCCESS: Pip and base packages installed
exit /b 0