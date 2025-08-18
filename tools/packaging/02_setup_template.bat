@echo off
setlocal EnableDelayedExpansion

:: ================================
:: 📁 Component 2: Setup Distributable Template
:: ================================
set "SCRIPT_DIR=%~dp0"

:: Get absolute path to root directory using a more direct approach
set "ROOT_DIR=%SCRIPT_DIR%..\.."
for %%i in ("%ROOT_DIR%") do set "ROOT_DIR=%%~fi"

:: Verify ROOT_DIR is correct
echo [DEBUG] SCRIPT_DIR: %SCRIPT_DIR%
echo [DEBUG] ROOT_DIR: %ROOT_DIR%

set "CONFIG_PATH=%ROOT_DIR%\config.yaml"
set "LOG_FILE=%ROOT_DIR%\logs\02_setup_template.txt"

:: ================================
:: 📁 Ensure logs folder
:: ================================
if not exist "%SCRIPT_DIR%logs" mkdir "%SCRIPT_DIR%logs"

:: ================================
:: 📝 Component 2: Setup Distributable Template
:: ================================
echo 📁 Component 2: Setup Distributable Template
echo ===============================
echo 🕒 %DATE% %TIME%
echo ===============================
echo.

:: ================================
:: 📋 Load configuration from generated config.bat
:: ================================
set "TEMPLATE_DIR=%ROOT_DIR%\templates\distributable_template"
set "SAVED_ROOT_DIR=%ROOT_DIR%"
call "%TEMPLATE_DIR%\config.bat"
set "ROOT_DIR=%SAVED_ROOT_DIR%"
set "TOOL_NAME=%TOOL_TO_SHIP%"

echo 🔧 Setting up template for tool: %TOOL_NAME%

:: ================================
:: 📁 Setup paths
:: ================================
set "EXPORT_DIR=%ROOT_DIR%\distributables\%TOOL_NAME%_distributable"
set "EMBED_SOURCE=%ROOT_DIR%\templates\distributable_template\embed_py311"

echo 📁 Template directory: %TEMPLATE_DIR%
echo 📁 Export directory: %EXPORT_DIR%
echo 📁 Embed source: %EMBED_SOURCE%
echo [DEBUG] ROOT_DIR: %ROOT_DIR%
echo [DEBUG] EMBED_SOURCE: %EMBED_SOURCE%

:: ================================
:: 🧼 Clean export folder
:: ================================
if exist "%EXPORT_DIR%" (
    echo 🧹 Cleaning previous export directory...
    rd /s /q "%EXPORT_DIR%"
)
mkdir "%EXPORT_DIR%" 2>nul
echo ✅ Fresh export directory created: %EXPORT_DIR%

:: ================================
:: 📁 Copy template files (excluding embed_py311 for now)
:: ================================
echo 📁 Copying distributable template...
if exist "%TEMPLATE_DIR%" (
    xcopy /e /i /y "%TEMPLATE_DIR%\*" "%EXPORT_DIR%" >> "%LOG_FILE%" 2>&1
    echo ✅ Template files copied successfully
) else (
    echo ❌ ERROR: Template directory not found at %TEMPLATE_DIR%
    exit /b 1
)

:: ================================
:: 📁 Ensure required directories exist
:: ================================
echo 📁 Creating required directories...
if not exist "%EXPORT_DIR%\input" mkdir "%EXPORT_DIR%\input"
if not exist "%EXPORT_DIR%\output" mkdir "%EXPORT_DIR%\output"
if not exist "%EXPORT_DIR%\logs" mkdir "%EXPORT_DIR%\logs"
echo ✅ Required directories created

:: ================================
:: 🔎 Verify config.bat present (from Component 0)
:: ================================
if not exist "%EXPORT_DIR%\config.bat" (
    echo ❌ ERROR: config.bat missing in export.
    echo 💡 Run Component 0 first: tools\packaging\00_build_common_python.bat
    exit /b 1
)
echo ✅ config.bat present

:: ================================
:: 🐍 Copy embedded Python with robocopy
:: ================================
echo 🐍 Copying embedded Python with robocopy...
if exist "%EMBED_SOURCE%" (
    robocopy "%EMBED_SOURCE%" "%EXPORT_DIR%\embed_py311" /E /R:3 /W:1 /NP >> "%LOG_FILE%" 2>&1
    if %ERRORLEVEL% GTR 7 (
        echo ❌ ERROR: robocopy failed with error level %ERRORLEVEL%
        exit /b 1
    )
    echo ✅ Embedded Python copied successfully with robocopy
) else (
    echo ❌ ERROR: Embedded Python not found at %EMBED_SOURCE%
    echo 💡 Run Component 0 first: tools\packaging\00_build_common_python.bat
    exit /b 1
)

:: ================================
:: 📄 Copy tool-specific README
:: ================================
echo 📄 Copying tool-specific README...
set "README_SRC=%ROOT_DIR%\implementations\python-package\scriptcraft\tools\%TOOL_NAME%\README_distributable.md"
if exist "%README_SRC%" (
    copy "%README_SRC%" "%EXPORT_DIR%\README.md" >nul 2>&1
    echo ✅ Tool-specific README copied
) else (
    echo ⚠️ Tool-specific README not found at: %README_SRC%
    echo ℹ️ Using default README from template
)

:: ================================
:: 🧼 Clean up unnecessary files
:: ================================
echo 🧼 Cleaning up unnecessary files...
if exist "%EXPORT_DIR%\import_embed.bat" del "%EXPORT_DIR%\import_embed.bat" >nul 2>&1
echo ✅ Cleaned up unnecessary files

:: ================================
:: 📋 Generate tool-specific run.bat from config
:: ================================
echo 📋 Generating tool-specific run.bat from config...
python "%SCRIPT_DIR%config_processor.py" run_bat "%CONFIG_PATH%" "%EXPORT_DIR%" "%TOOL_NAME%"

echo ✅ Tool-specific run.bat generated

:: ================================
:: 📊 Show final structure
:: ================================
echo 📊 Final distributable structure:
dir "%EXPORT_DIR%" /b


echo.
echo ✅ Component 2 Complete: Template Setup
echo 📁 Export directory: %EXPORT_DIR%
echo 📋 Log: %LOG_FILE%
) >> "%LOG_FILE%" 2>&1

echo.
echo ✅ Component 2 Complete: Template Setup
echo 📁 Export directory: %EXPORT_DIR%
echo 📋 Log: %LOG_FILE%

exit /b 0
