@echo off

REM Basic path setup
set "SCRIPT_DIR=%~dp0"
for %%i in ("%SCRIPT_DIR%..\..\py_embed_setup\embed_py311") do set "EMBED_DIR=%%~fi"
set "PYTHON=%EMBED_DIR%\python.exe"

REM Setup logging
for %%i in ("%SCRIPT_DIR%..\..\data\logs") do set "LOG_DIR=%%~fi"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
set "LOG_FILE=%LOG_DIR%\00c_install_common.txt"

REM Start logging
echo Component 0c: Install Common Packages > "%LOG_FILE%"
echo ===================================== >> "%LOG_FILE%"
echo %DATE% %TIME% >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

echo Component 0c: Install Common Packages
echo =====================================

REM Check if Python exists
echo Validating Python installation... >> "%LOG_FILE%"
echo Validating Python installation...
if not exist "%PYTHON%" (
    echo ERROR: Python not found at %PYTHON% >> "%LOG_FILE%"
    echo ERROR: Python not found at %PYTHON%
    echo Run components 0a and 0b first >> "%LOG_FILE%"
    echo Run components 0a and 0b first
    exit /b 1
)

echo Python found: %PYTHON% >> "%LOG_FILE%"
echo Python found: %PYTHON%
echo. >> "%LOG_FILE%"
echo.

REM Go to Python directory
cd /d "%EMBED_DIR%"

echo Installing pandas... >> "%LOG_FILE%"
echo Installing pandas...
"%PYTHON%" -m pip install --no-cache-dir pandas --quiet >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: Failed to install pandas >> "%LOG_FILE%"
    echo ERROR: Failed to install pandas
    exit /b 1
)

echo Installing numpy... >> "%LOG_FILE%"
echo Installing numpy...
"%PYTHON%" -m pip install --no-cache-dir numpy --quiet >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: Failed to install numpy >> "%LOG_FILE%"
    echo ERROR: Failed to install numpy
    exit /b 1
)

echo Installing openpyxl... >> "%LOG_FILE%"
echo Installing openpyxl...
"%PYTHON%" -m pip install --no-cache-dir openpyxl --quiet >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: Failed to install openpyxl >> "%LOG_FILE%"
    echo ERROR: Failed to install openpyxl
    exit /b 1
)

echo Installing python-docx... >> "%LOG_FILE%"
echo Installing python-docx...
"%PYTHON%" -m pip install --no-cache-dir python-docx --quiet >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: Failed to install python-docx >> "%LOG_FILE%"
    echo ERROR: Failed to install python-docx
    exit /b 1
)

echo Installing pyyaml... >> "%LOG_FILE%"
echo Installing pyyaml...
"%PYTHON%" -m pip install --no-cache-dir pyyaml --quiet >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: Failed to install pyyaml >> "%LOG_FILE%"
    echo ERROR: Failed to install pyyaml
    exit /b 1
)

echo Installing pytz... >> "%LOG_FILE%"
echo Installing pytz...
"%PYTHON%" -m pip install --no-cache-dir pytz --quiet >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: Failed to install pytz >> "%LOG_FILE%"
    echo ERROR: Failed to install pytz
    exit /b 1
)

echo Installing python-dateutil... >> "%LOG_FILE%"
echo Installing python-dateutil...
"%PYTHON%" -m pip install --no-cache-dir python-dateutil --quiet >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: Failed to install python-dateutil >> "%LOG_FILE%"
    echo ERROR: Failed to install python-dateutil
    exit /b 1
)

echo Installing selenium... >> "%LOG_FILE%"
echo Installing selenium...
"%PYTHON%" -m pip install --no-cache-dir selenium --quiet >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: Failed to install selenium >> "%LOG_FILE%"
    echo ERROR: Failed to install selenium
    exit /b 1
)

echo Installing ScriptCraft package... >> "%LOG_FILE%"
echo Installing ScriptCraft package...
"%PYTHON%" -m pip install --no-cache-dir scriptcraft-python --force-reinstall --quiet >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: Failed to install ScriptCraft package >> "%LOG_FILE%"
    echo ERROR: Failed to install ScriptCraft package
    exit /b 1
)

echo Verifying ScriptCraft installation... >> "%LOG_FILE%"
echo Verifying ScriptCraft installation...
"%PYTHON%" -c "import scriptcraft; print('ScriptCraft version:', scriptcraft.__version__)" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: ScriptCraft import failed >> "%LOG_FILE%"
    echo ERROR: ScriptCraft import failed
    exit /b 1
)

echo SUCCESS: Component 0c completed successfully >> "%LOG_FILE%"
echo SUCCESS: All packages installed
exit /b 0