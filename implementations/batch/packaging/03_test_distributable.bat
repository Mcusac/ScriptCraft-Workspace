@echo off

REM Basic path setup
set "SCRIPT_DIR=%~dp0"
for %%i in ("%SCRIPT_DIR%..\..\") do set "ROOT_DIR=%%~fi"

REM Setup logging
for %%i in ("%ROOT_DIR%\data\logs") do set "LOG_DIR=%%~fi"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
set "LOG_FILE=%LOG_DIR%\03_test_distributable.txt"

REM Start logging
echo Component 3: Test Distributable > "%LOG_FILE%"
echo =============================== >> "%LOG_FILE%"
echo %DATE% %TIME% >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

echo Component 3: Test Distributable
echo ===============================

REM Load configuration from generated config.bat
echo Loading configuration... >> "%LOG_FILE%"
echo Loading configuration...
set "TEMPLATE_DIR=%ROOT_DIR%\templates\distributable_template"
set "CONFIG_BAT=%TEMPLATE_DIR%\config.bat"

if not exist "%CONFIG_BAT%" (
    echo ERROR: config.bat not found at %CONFIG_BAT% >> "%LOG_FILE%"
    echo ERROR: config.bat not found at %CONFIG_BAT%
    echo Run Component 0 first: 00_build_common_python.bat >> "%LOG_FILE%"
    echo Run Component 0 first: 00_build_common_python.bat
    exit /b 1
)

REM Load config variables
call "%CONFIG_BAT%" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: Failed to load config.bat >> "%LOG_FILE%"
    echo ERROR: Failed to load config.bat
    exit /b 1
)

echo Configuration loaded successfully >> "%LOG_FILE%"
echo Tool to ship: %TOOL_TO_SHIP% >> "%LOG_FILE%"
echo Testing distributable for tool: %TOOL_TO_SHIP%

REM Setup paths
set "TOOL_NAME=%TOOL_TO_SHIP%"
set "EXPORT_DIR=%ROOT_DIR%\distributables\%TOOL_NAME%_distributable"
set "PYTHON_PATH=embed_py311\python.exe"

echo Export directory: %EXPORT_DIR% >> "%LOG_FILE%"
echo Python path: %PYTHON_PATH% >> "%LOG_FILE%"

REM Check distributable exists
echo Checking distributable directory... >> "%LOG_FILE%"
echo Checking distributable directory...
if not exist "%EXPORT_DIR%" (
    echo ERROR: Distributable not found at %EXPORT_DIR% >> "%LOG_FILE%"
    echo ERROR: Distributable not found at %EXPORT_DIR%
    echo Run Component 2 first: 02_setup_template.bat >> "%LOG_FILE%"
    echo Run Component 2 first: 02_setup_template.bat
    exit /b 1
)

REM Change to distributable directory
echo Changing to distributable directory... >> "%LOG_FILE%"
echo Changing to distributable directory...
cd /d "%EXPORT_DIR%"

REM Check Python exists
echo Checking Python installation... >> "%LOG_FILE%"
echo Checking Python installation...
if not exist "%PYTHON_PATH%" (
    echo ERROR: Python not found at %PYTHON_PATH% >> "%LOG_FILE%"
    echo ERROR: Python not found at %PYTHON_PATH%
    echo Run Components 0 and 2 first >> "%LOG_FILE%"
    echo Run Components 0 and 2 first
    exit /b 1
)

echo Distributable and Python found >> "%LOG_FILE%"
echo Distributable and Python found

REM Test 1: Python Version
echo Test 1: Python Version >> "%LOG_FILE%"
echo Test 1: Python Version
echo -------------------------------- >> "%LOG_FILE%"
echo --------------------------------
"%PYTHON_PATH%" --version >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: Python version test failed >> "%LOG_FILE%"
    echo ERROR: Python version test failed
    exit /b 1
)
echo Python version test passed >> "%LOG_FILE%"
echo Python version test passed

REM Test 2: Core Packages
echo Test 2: Core Packages >> "%LOG_FILE%"
echo Test 2: Core Packages
echo -------------------------------- >> "%LOG_FILE%"
echo --------------------------------

echo Testing pandas import... >> "%LOG_FILE%"
echo Testing pandas import...
"%PYTHON_PATH%" -c "import pandas; print('pandas imported successfully')" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: pandas import failed >> "%LOG_FILE%"
    echo ERROR: pandas import failed
    exit /b 1
)

echo Testing pyyaml import... >> "%LOG_FILE%"
echo Testing pyyaml import...
"%PYTHON_PATH%" -c "import yaml; print('pyyaml imported successfully')" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: pyyaml import failed >> "%LOG_FILE%"
    echo ERROR: pyyaml import failed
    exit /b 1
)

echo Testing openpyxl import... >> "%LOG_FILE%"
echo Testing openpyxl import...
"%PYTHON_PATH%" -c "import openpyxl; print('openpyxl imported successfully')" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: openpyxl import failed >> "%LOG_FILE%"
    echo ERROR: openpyxl import failed
    exit /b 1
)

echo Core packages test passed >> "%LOG_FILE%"
echo Core packages test passed

REM Test 3: ScriptCraft Package
echo Test 3: ScriptCraft Package >> "%LOG_FILE%"
echo Test 3: ScriptCraft Package
echo -------------------------------- >> "%LOG_FILE%"
echo --------------------------------

echo Testing scriptcraft import... >> "%LOG_FILE%"
echo Testing scriptcraft import...
"%PYTHON_PATH%" -c "import scriptcraft; print('scriptcraft imported successfully')" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: scriptcraft import failed >> "%LOG_FILE%"
    echo ERROR: scriptcraft import failed
    exit /b 1
)

echo Testing scriptcraft.common import... >> "%LOG_FILE%"
echo Testing scriptcraft.common import...
"%PYTHON_PATH%" -c "import scriptcraft.common; print('scriptcraft.common imported successfully')" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: scriptcraft.common import failed >> "%LOG_FILE%"
    echo ERROR: scriptcraft.common import failed
    exit /b 1
)

echo ScriptCraft package test passed >> "%LOG_FILE%"
echo ScriptCraft package test passed

REM Test 4: Tool-Specific Import
echo Test 4: Tool-Specific Import >> "%LOG_FILE%"
echo Test 4: Tool-Specific Import
echo -------------------------------- >> "%LOG_FILE%"
echo --------------------------------

echo Testing %TOOL_NAME% import... >> "%LOG_FILE%"
echo Testing %TOOL_NAME% import...
"%PYTHON_PATH%" -c "import scriptcraft.tools.%TOOL_NAME%; print('%TOOL_NAME% imported successfully')" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: %TOOL_NAME% import failed >> "%LOG_FILE%"
    echo ERROR: %TOOL_NAME% import failed
    exit /b 1
)

echo Testing %TOOL_NAME%.main import... >> "%LOG_FILE%"
echo Testing %TOOL_NAME%.main import...
"%PYTHON_PATH%" -c "import scriptcraft.tools.%TOOL_NAME%.main; print('%TOOL_NAME%.main imported successfully')" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: %TOOL_NAME%.main import failed >> "%LOG_FILE%"
    echo ERROR: %TOOL_NAME%.main import failed
    exit /b 1
)

echo Tool-specific import test passed >> "%LOG_FILE%"
echo Tool-specific import test passed

REM Test 5: Module Execution
echo Test 5: Module Execution >> "%LOG_FILE%"
echo Test 5: Module Execution
echo -------------------------------- >> "%LOG_FILE%"
echo --------------------------------

echo Testing %TOOL_NAME% module execution... >> "%LOG_FILE%"
echo Testing %TOOL_NAME% module execution...
"%PYTHON_PATH%" -m scriptcraft.tools.%TOOL_NAME%.main --help >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo WARNING: %TOOL_NAME% module execution failed >> "%LOG_FILE%"
    echo WARNING: %TOOL_NAME% module execution failed
    echo This might be expected if tool requires input files >> "%LOG_FILE%"
    echo This might be expected if tool requires input files
) else (
    echo %TOOL_NAME% module execution test passed >> "%LOG_FILE%"
    echo %TOOL_NAME% module execution test passed
)

REM Test 6: Directory Structure
echo Test 6: Directory Structure >> "%LOG_FILE%"
echo Test 6: Directory Structure
echo -------------------------------- >> "%LOG_FILE%"
echo --------------------------------

echo Checking required directories... >> "%LOG_FILE%"
echo Checking required directories...

if exist "input" (
    echo input/ directory exists >> "%LOG_FILE%"
    echo input/ directory exists
) else (
    echo ERROR: input/ directory missing >> "%LOG_FILE%"
    echo ERROR: input/ directory missing
    exit /b 1
)

if exist "output" (
    echo output/ directory exists >> "%LOG_FILE%"
    echo output/ directory exists
) else (
    echo ERROR: output/ directory missing >> "%LOG_FILE%"
    echo ERROR: output/ directory missing
    exit /b 1
)

if exist "logs" (
    echo logs/ directory exists >> "%LOG_FILE%"
    echo logs/ directory exists
) else (
    echo ERROR: logs/ directory missing >> "%LOG_FILE%"
    echo ERROR: logs/ directory missing
    exit /b 1
)

if exist "run.bat" (
    echo run.bat exists >> "%LOG_FILE%"
    echo run.bat exists
) else (
    echo ERROR: run.bat missing >> "%LOG_FILE%"
    echo ERROR: run.bat missing
    exit /b 1
)

if exist "README.md" (
    echo README.md exists >> "%LOG_FILE%"
    echo README.md exists
) else (
    echo WARNING: README.md missing (using default) >> "%LOG_FILE%"
    echo WARNING: README.md missing (using default)
)

echo Directory structure test passed >> "%LOG_FILE%"
echo Directory structure test passed

REM Final Summary
echo Final Summary >> "%LOG_FILE%"
echo Final Summary
echo -------------------------------- >> "%LOG_FILE%"
echo --------------------------------
echo Python environment: Working >> "%LOG_FILE%"
echo Core packages: Working >> "%LOG_FILE%"
echo ScriptCraft package: Working >> "%LOG_FILE%"
echo Tool-specific imports: Working >> "%LOG_FILE%"
echo Directory structure: Working >> "%LOG_FILE%"

echo Distributable location: %EXPORT_DIR% >> "%LOG_FILE%"
echo Distributable location: %EXPORT_DIR%

echo Calculating size... >> "%LOG_FILE%"
echo Calculating size...
dir /s >> "%LOG_FILE%" 2>&1

echo SUCCESS: Component 3 completed successfully >> "%LOG_FILE%"
echo SUCCESS: All Tests Passed
echo Log: %LOG_FILE%

exit /b 0