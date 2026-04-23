@echo off
setlocal EnableDelayedExpansion

:: ================================
:: 🔧 Component 1b: Load Configuration
:: ================================
set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%..\.."
set "TEMPLATE_DIR=%ROOT_DIR%\templates\distributable_template"

echo 🔧 Component 1b: Loading Configuration
echo ===============================
echo 🕒 %DATE% %TIME%
echo ===============================

:: ================================
:: 📋 Load configuration from generated config.bat
:: ================================
if not exist "%TEMPLATE_DIR%\config.bat" (
    echo ❌ ERROR: config.bat not found at %TEMPLATE_DIR%\config.bat
    exit /b 1
)

echo 📋 Loading configuration from: %TEMPLATE_DIR%\config.bat
call "%TEMPLATE_DIR%\config.bat"
set "TOOL_NAME=%TOOL_TO_SHIP%"

if "%TOOL_NAME%"=="" (
    echo ❌ ERROR: TOOL_NAME not set after loading config.bat
    exit /b 1
)

echo ✅ Configuration loaded successfully
echo 🎯 Tool name: %TOOL_NAME%

exit /b 0
