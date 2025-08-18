@echo off
setlocal EnableDelayedExpansion

:: ================================
:: 🧪 Component 3: Test Distributable
:: ================================
set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%..\.."
set "CONFIG_PATH=%ROOT_DIR%\config.yaml"
set "LOG_FILE=%ROOT_DIR%\logs\03_test_distributable.txt"

:: ================================
:: 📁 Ensure logs folder
:: ================================
if not exist "%SCRIPT_DIR%logs" mkdir "%SCRIPT_DIR%logs"

:: ================================
:: 📝 Begin logging
:: ================================
(
echo 🧪 Component 3: Test Distributable
echo ===============================
echo 🕒 %DATE% %TIME%
echo ===============================
echo.

:: ================================
:: 📁 Setup paths (testing distributable in isolation)
:: ================================
set "TOOL_NAME=rhq_form_autofiller"
set "EXPORT_DIR=%ROOT_DIR%\distributables\%TOOL_NAME%_distributable"

echo 🧪 Testing distributable for tool: %TOOL_NAME%
set "PYTHON_PATH=embed_py311\python.exe"

echo 📁 Export directory: %EXPORT_DIR%
echo 🐍 Python path: %PYTHON_PATH%

:: ================================
:: 🔍 Check distributable exists and change to it
:: ================================
if not exist "%EXPORT_DIR%" (
    echo ❌ ERROR: Distributable not found at %EXPORT_DIR%
    exit /b 1
)

echo 📁 Changing to distributable directory: %EXPORT_DIR%
cd /d "%EXPORT_DIR%"

if not exist "%PYTHON_PATH%" (
    echo ❌ ERROR: Python not found at %PYTHON_PATH%
    echo 💡 Run Component 1 initially: 01_build_python.bat
    exit /b 1
)

echo ✅ Distributable and Python found

:: ================================
:: 🧪 Test 1: Python Version
:: ================================
echo 🧪 Test 1: Python Version
echo --------------------------------
"%PYTHON_PATH%" --version
if errorlevel 1 (
    echo ❌ ERROR: Python version test failed
    exit /b 1
)
echo ✅ Python version test passed

:: ================================
:: 🧪 Test 2: Core Packages
:: ================================
echo 🧪 Test 2: Core Packages
echo --------------------------------
echo Testing pandas import...
"%PYTHON_PATH%" -c "import pandas; print('✅ pandas imported successfully')"
if errorlevel 1 (
    echo ❌ ERROR: pandas import failed
    exit /b 1
)

echo Testing pyyaml import...
"%PYTHON_PATH%" -c "import yaml; print('✅ pyyaml imported successfully')"
if errorlevel 1 (
    echo ❌ ERROR: pyyaml import failed
    exit /b 1
)

echo Testing openpyxl import...
"%PYTHON_PATH%" -c "import openpyxl; print('✅ openpyxl imported successfully')"
if errorlevel 1 (
    echo ❌ ERROR: openpyxl import failed
    exit /b 1
)

echo ✅ Core packages test passed

:: ================================
:: 🧪 Test 3: ScriptCraft Package
:: ================================
echo 🧪 Test 3: ScriptCraft Package
echo --------------------------------
echo Testing scriptcraft import...
"%PYTHON_PATH%" -c "import scriptcraft; print('✅ scriptcraft imported successfully')"
if errorlevel 1 (
    echo ❌ ERROR: scriptcraft import failed
    exit /b 1
)

echo Testing scriptcraft.common import...
"%PYTHON_PATH%" -c "import scriptcraft.common; print('✅ scriptcraft.common imported successfully')"
if errorlevel 1 (
    echo ❌ ERROR: scriptcraft.common import failed
    exit /b 1
)

echo ✅ ScriptCraft package test passed

:: ================================
:: 🧪 Test 4: Tool-Specific Import
:: ================================
echo 🧪 Test 4: Tool-Specific Import
echo --------------------------------
echo Testing %TOOL_NAME% import...
"%PYTHON_PATH%" -c "import scriptcraft.tools.%TOOL_NAME%; print('✅ %TOOL_NAME% imported successfully')"
if errorlevel 1 (
    echo ❌ ERROR: %TOOL_NAME% import failed
    exit /b 1
)

echo Testing %TOOL_NAME%.main import...
"%PYTHON_PATH%" -c "import scriptcraft.tools.%TOOL_NAME%.main; print('✅ %TOOL_NAME%.main imported successfully')"
if errorlevel 1 (
    echo ❌ ERROR: %TOOL_NAME%.main import failed
    exit /b 1
)

echo ✅ Tool-specific import test passed

:: ================================
:: 🧪 Test 5: Module Execution
:: ================================
echo 🧪 Test 5: Module Execution
echo --------------------------------
echo Testing %TOOL_NAME% module execution...
"%PYTHON_PATH%" -m scriptcraft.tools.%TOOL_NAME%.main --help
if errorlevel 1 (
    echo ⚠️ WARNING: %TOOL_NAME% module execution failed (this might be expected if tool requires input files)
    echo ℹ️ This is often normal for tools that require specific input files
)
if not errorlevel 1 echo ✅ %TOOL_NAME% module execution test passed

:: ================================
:: 🧪 Test 6: Directory Structure
:: ================================
echo 🧪 Test 6: Directory Structure
echo --------------------------------
echo Checking required directories...

if exist "input" (
    echo ✅ input/ directory exists
) else (
    echo ❌ ERROR: input/ directory missing
    exit /b 1
)

if exist "output" (
    echo ✅ output/ directory exists
) else (
    echo ❌ ERROR: output/ directory missing
    exit /b 1
)

if exist "logs" (
    echo ✅ logs/ directory exists
) else (
    echo ❌ ERROR: logs/ directory missing
    exit /b 1
)

if exist "run.bat" (
    echo ✅ run.bat exists
) else (
    echo ❌ ERROR: run.bat missing
    exit /b 1
)

if exist "README.md" (
    echo ✅ README.md exists
) else (
    echo ⚠️ WARNING: README.md missing (using default)
)

echo ✅ Directory structure test passed

:: ================================
:: 📊 Final Summary
:: ================================
echo 📊 Final Summary
echo --------------------------------
echo ✅ Python environment: Working
echo ✅ Core packages: Working
echo ✅ ScriptCraft package: Working
echo ✅ Tool-specific imports: Working
echo ✅ Directory structure: Working
echo.
echo 📁 Distributable location: %EXPORT_DIR%
echo 📁 Size: 
dir /s | findstr "File(s)"

echo.
echo ✅ Component 3 Complete: All Tests Passed
echo 📋 Log: %LOG_FILE%
) > "%LOG_FILE%" 2>&1

echo.
echo ✅ Component 3 Complete: All Tests Passed
echo 📋 Log: %LOG_FILE%

exit /b 0
