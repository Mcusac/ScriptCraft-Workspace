@echo off
setlocal EnableDelayedExpansion

:: =======================
:: 📁 Set paths
:: =======================
set "BASE_DIR=%~dp0"
set "PYTHON_PATH=%BASE_DIR%embed_py311\python.exe"
set "LOG_FILE=%BASE_DIR%logs\run_log.txt"

:: =======================
:: 📁 Ensure logs folder
:: =======================
if not exist "%BASE_DIR%logs" (
    mkdir "%BASE_DIR%logs"
)

:: =======================
:: 📝 Begin Logging
:: =======================
(
echo 🚀 Running ScriptCraft Tool...
echo 🔧 Current Directory: %cd%
echo ====================
echo 🕒 Run started: %DATE% %TIME%
echo ====================

if not exist "%PYTHON_PATH%" (
    echo ❌ Missing Python at: !PYTHON_PATH!
    exit /b 1
)

echo 📂 Input folder contents:
dir "%BASE_DIR%input"

echo 🔎 Python Version:
"%PYTHON_PATH%" --version

echo 🔄 Executing Python script...
echo --------------------------------
"%PYTHON_PATH%" "%BASE_DIR%run.py" %*
echo --------------------------------

echo.
echo ✅ Process complete. Log saved to logs\run_log.txt
) > "%LOG_FILE%" 2>&1

:: =======================
:: 🖨️ Show Log
:: =======================
type "%LOG_FILE%"
pause
