@echo off
setlocal EnableDelayedExpansion

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::: ScriptCraft Full Packaging System
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: Setup paths (DRY pattern)
set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%..\.."
for %%i in ("%ROOT_DIR%\data\logs") do set "LOG_DIR=%%~fi"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
set "LOG_FILE=%LOG_DIR%\package_all.txt"

::: Load tool name from generated config
set "TEMPLATE_DIR=%ROOT_DIR%\templates\distributable_template"
if exist "%TEMPLATE_DIR%\config.bat" (
    call "%TEMPLATE_DIR%\config.bat"
    set "TOOL_NAME=%TOOL_TO_SHIP%"
) else (
    set "TOOL_NAME=rhq_form_autofiller"
)

echo.
echo ScriptCraft Full Packaging System
echo =================================
echo %DATE% %TIME%
echo =================================
echo Tool: %TOOL_NAME%
echo.

echo ================================
echo Component 0: Build Common Python
echo ================================
call "%SCRIPT_DIR%00_build_common_python.bat"
if errorlevel 1 (
    echo ERROR: Component 0 failed
    exit /b 1
)
echo SUCCESS: Component 0 completed

echo.
echo ====================================
echo Component 1: Check Python Environment
echo ====================================
call "%SCRIPT_DIR%01_build_python.bat"
if errorlevel 1 (
    echo ERROR: Component 1 failed
    exit /b 1
)
echo SUCCESS: Component 1 completed

echo.
echo ================================
echo Component 2: Setup Template
echo ================================
call "%SCRIPT_DIR%02_setup_template.bat"
if errorlevel 1 (
    echo ERROR: Component 2 failed
    exit /b 1
)
echo SUCCESS: Component 2 completed

echo.
echo ==============================
echo Component 3: Test Distributable
echo ==============================
call "%SCRIPT_DIR%03_test_distributable.bat"
if errorlevel 1 (
    echo ERROR: Component 3 failed
    exit /b 1
)
echo SUCCESS: Component 3 completed

echo.
echo =====================================
echo SUCCESS: Full Packaging Complete
echo =====================================
echo Tool: %TOOL_NAME%
echo Log: %LOG_FILE%

exit /b 0