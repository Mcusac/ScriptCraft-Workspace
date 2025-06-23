@echo off
setlocal EnableDelayedExpansion

:: =======================
:: 📁 Set root-relative paths
:: =======================
set "BASE_DIR=%~dp0"
set "SCRIPT_DIR=%BASE_DIR%scripts"
set "PYTHON_PATH=%BASE_DIR%embed_py311\python.exe"
set "LOG_FILE=%BASE_DIR%logs\run_log.txt"

:: =======================
:: 📝 Timestamp
:: =======================
:: Use simple date command instead of PowerShell to avoid drive access issues
set TIMESTAMP=%DATE:~-4%-%DATE:~4,2%-%DATE:~7,2%

:: =======================
:: 📁 Ensure logs folder
:: =======================
if not exist "%BASE_DIR%logs" (
    mkdir "%BASE_DIR%logs"
)

:: =======================
:: 🔧 Load Configuration
:: =======================
call "%BASE_DIR%config.bat"

:: =======================
:: 📝 Begin Logging
:: =======================
(
echo 🚀 Running %ENTRY_COMMAND%...
echo 🔧 Current Directory: %cd%
echo ====================
echo 🕒 Run started: %TIMESTAMP%
echo ====================

:: =======================
:: 🧪 Sanity Checks
:: =======================
if not exist "%SCRIPT_DIR%" (
    echo ❌ Missing scripts folder at: !SCRIPT_DIR!
    exit /b
)
if not exist "%PYTHON_PATH%" (
    echo ❌ Missing Python at: !PYTHON_PATH!
    exit /b
)

:: =======================
:: ✅ Setup PYTHONPATH
:: =======================
set "PYTHONPATH=!SCRIPT_DIR!;!SCRIPT_DIR!\common"
set "PYTHONIOENCODING=utf-8"
echo 📚 PYTHONPATH Set To: !PYTHONPATH!

:: =======================
:: 📂 Input Folder Contents
:: =======================
echo 📂 Input folder contents:
dir "%BASE_DIR%input"

:: =======================
:: 🐍 Confirm Python Version
:: =======================
echo 🔎 Python Version:
"%PYTHON_PATH%" --version

:: =======================
:: 🏃 Run Script
:: =======================
echo 🔄 Executing: %ENTRY_COMMAND%
echo --------------------------------
pushd "!SCRIPT_DIR!"
"%PYTHON_PATH%" %ENTRY_COMMAND%
popd
echo --------------------------------

echo.
echo ✅ Process complete. Log saved to logs\run_log.txt
) > "%LOG_FILE%" 2>&1

:: =======================
:: 🖨️ Show Log
:: =======================
type "%LOG_FILE%"
pause
