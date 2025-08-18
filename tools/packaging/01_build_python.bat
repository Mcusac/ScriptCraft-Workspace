@echo off
setlocal EnableDelayedExpansion

:: ================================
:: 🔧 Component 1: Build Python Environment (Orchestrator)
:: ================================
set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%..\.."
set "LOG_FILE=%ROOT_DIR%\logs\01_build_python.txt"

:: ================================
:: 📁 Ensure centralized logs folder
:: ================================
if not exist "%ROOT_DIR%\logs" mkdir "%ROOT_DIR%\logs"

:: ================================
:: 📝 Begin logging
:: ================================
(
echo 🔧 Component 1: Building Python Environment
echo ===============================
echo 🕒 %DATE% %TIME%
echo ===============================
echo.

:: ================================
:: 🔧 Component 1a: Check Environment
:: ================================
echo 🔧 Component 1a: Checking Environment
echo ===============================
call "%SCRIPT_DIR%01a_check_environment.bat"
if errorlevel 1 (
    echo ❌ Component 1a failed
    exit /b 1
)
echo ✅ Component 1a completed successfully

:: ================================
:: 🔧 Component 1b: Load Configuration
:: ================================
echo.
echo 🔧 Component 1b: Loading Configuration
echo ===============================
call "%SCRIPT_DIR%01b_load_config.bat"
if errorlevel 1 (
    echo ❌ Component 1b failed
    exit /b 1
)
echo ✅ Component 1b completed successfully

:: ================================
:: 🔧 Component 1c: Install Packages
:: ================================
echo.
echo 🔧 Component 1c: Installing Packages
echo ===============================
call "%SCRIPT_DIR%01c_install_packages.bat"
if errorlevel 1 (
    echo ❌ Component 1c failed
    exit /b 1
)
echo ✅ Component 1c completed successfully

echo.
echo ✅ Component 1 Complete: Python Environment Ready
echo 📁 Location: %ROOT_DIR%\templates\distributable_template\embed_py311
echo 📋 Log: %LOG_FILE%
) > "%LOG_FILE%" 2>&1

echo.
echo ✅ Component 1 Complete: Python Environment Ready
echo 📁 Location: %ROOT_DIR%\templates\distributable_template\embed_py311
echo 📋 Log: %LOG_FILE%

exit /b 0
