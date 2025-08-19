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
if defined TOOL_DESCRIPTION (
    echo 🚀 Running %TOOL_DESCRIPTION%...
) else (
    echo 🚀 Running ScriptCraft Tool...
)
echo 🔧 Current Directory: %cd%
echo ====================
echo 🕒 Run started: %DATE% %TIME%
echo ====================

:: =======================
:: 🔍 Check Python exists
:: =======================
if not exist "%PYTHON_PATH%" (
    echo ❌ Missing Python at: %PYTHON_PATH%
    echo 💡 Make sure embed_py311 folder is present
    exit /b 1
)

echo ✅ Python found: %PYTHON_PATH%

:: =======================
:: 📋 Load configuration from config.bat
:: =======================
if exist "%BASE_DIR%config.bat" (
    call "%BASE_DIR%config.bat"
    echo ✅ Configuration loaded from config.bat
) else (
    echo ⚠️ config.bat not found, using defaults
)

:: =======================
:: 📂 Show input folder
:: =======================
echo 📂 Input folder contents:
if exist "%BASE_DIR%input" (
    dir "%BASE_DIR%input"
) else (
    echo ⚠️ Input folder is empty
)

:: =======================
:: 🔄 Execute Python script
:: =======================
if defined TOOL_DESCRIPTION (
    echo 🔄 Executing %TOOL_DESCRIPTION%...
) else (
    echo 🔄 Executing Python script...
)
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
