@echo off
setlocal EnableDelayedExpansion

:: ================================
:: ⚡ ScriptCraft Quick Packaging System
:: ================================
echo ⚡ ScriptCraft Quick Packaging System
echo ===============================
echo 🕒 %DATE% %TIME%
echo ===============================
echo.

:: ================================
:: 🔧 Component 1: Check Python Environment
:: ================================
echo 🔧 Component 1: Checking Python Environment
echo ===============================
call "%~dp001_build_python.bat"
if errorlevel 1 (
    echo ❌ Component 1 failed
    exit /b 1
)
echo ✅ Component 1 completed successfully

:: ================================
:: 📁 Component 2: Setup Template
:: ================================
echo.
echo 📁 Component 2: Setup Distributable Template
echo ===============================
call "%~dp002_setup_template.bat"
if errorlevel 1 (
    echo ❌ Component 2 failed
    exit /b 1
)
echo ✅ Component 2 completed successfully

:: ================================
:: 🧪 Component 3: Test Distributable
:: ================================
echo.
echo 🧪 Component 3: Test Distributable
echo ===============================
call "%~dp003_test_distributable.bat"
if errorlevel 1 (
    echo ❌ Component 3 failed
    exit /b 1
)
echo ✅ Component 3 completed successfully

:: ================================
:: 🎉 Final Summary
:: ================================
echo.
echo ⚡ Quick Packaging Complete!
echo ===============================
echo ✅ Python Environment: Ready (using existing common Python)
echo ✅ Template Setup: Completed
echo ✅ Testing: All tests passed
echo.
echo 📦 Distributable created successfully
echo 🎯 To run: distributables\rhq_form_autofiller_distributable\run.bat
echo.
echo 🕒 Completed: %DATE% %TIME%

exit /b 0
