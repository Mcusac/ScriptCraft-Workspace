@echo off

REM Basic path setup
set "SCRIPT_DIR=%~dp0"
for %%i in ("%SCRIPT_DIR%..\..\") do set "ROOT_DIR=%%~fi"

REM Setup logging
for %%i in ("%ROOT_DIR%\data\logs") do set "LOG_DIR=%%~fi"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
set "LOG_FILE=%LOG_DIR%\02_setup_template.txt"

REM Start logging
echo Component 2: Setup Distributable Template > "%LOG_FILE%"
echo ========================================= >> "%LOG_FILE%"
echo %DATE% %TIME% >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

echo Component 2: Setup Distributable Template
echo =========================================

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
echo Setting up template for tool: %TOOL_TO_SHIP%

REM Setup paths
set "TOOL_NAME=%TOOL_TO_SHIP%"
set "EXPORT_DIR=%ROOT_DIR%\distributables\%TOOL_NAME%_distributable"
set "EMBED_SOURCE=%TEMPLATE_DIR%\embed_py311"

echo Template directory: %TEMPLATE_DIR% >> "%LOG_FILE%"
echo Export directory: %EXPORT_DIR% >> "%LOG_FILE%"
echo Embed source: %EMBED_SOURCE% >> "%LOG_FILE%"

REM Clean export folder
echo Preparing export directory... >> "%LOG_FILE%"
echo Preparing export directory...
if exist "%EXPORT_DIR%" (
    echo Cleaning previous export directory... >> "%LOG_FILE%"
    echo Cleaning previous export directory...
    rd /s /q "%EXPORT_DIR%" >> "%LOG_FILE%" 2>&1
)

mkdir "%EXPORT_DIR%" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: Failed to create export directory >> "%LOG_FILE%"
    echo ERROR: Failed to create export directory
    exit /b 1
)
echo Fresh export directory created >> "%LOG_FILE%"

REM Verify template directory exists
echo Checking template directory... >> "%LOG_FILE%"
echo Checking template directory...
if not exist "%TEMPLATE_DIR%" (
    echo ERROR: Template directory not found at %TEMPLATE_DIR% >> "%LOG_FILE%"
    echo ERROR: Template directory not found at %TEMPLATE_DIR%
    exit /b 1
)

REM Copy template files (excluding embed_py311)
echo Copying distributable template files... >> "%LOG_FILE%"
echo Copying distributable template files...
robocopy "%TEMPLATE_DIR%" "%EXPORT_DIR%" /E /XD embed_py311 /NFL /NDL /NP >> "%LOG_FILE%" 2>&1
if %ERRORLEVEL% GTR 7 (
    echo ERROR: Failed to copy template files, error level %ERRORLEVEL% >> "%LOG_FILE%"
    echo ERROR: Failed to copy template files, error level %ERRORLEVEL%
    exit /b 1
)
echo Template files copied successfully >> "%LOG_FILE%"

REM Create required directories
echo Creating required directories... >> "%LOG_FILE%"
echo Creating required directories...
if not exist "%EXPORT_DIR%\input" mkdir "%EXPORT_DIR%\input"
if not exist "%EXPORT_DIR%\output" mkdir "%EXPORT_DIR%\output"
if not exist "%EXPORT_DIR%\logs" mkdir "%EXPORT_DIR%\logs"
echo Required directories created >> "%LOG_FILE%"

REM Verify embedded Python source exists
echo Checking embedded Python source... >> "%LOG_FILE%"
echo Checking embedded Python source...
if not exist "%EMBED_SOURCE%" (
    echo ERROR: Embedded Python not found at %EMBED_SOURCE% >> "%LOG_FILE%"
    echo ERROR: Embedded Python not found at %EMBED_SOURCE%
    echo Run Component 0 first: 00_build_common_python.bat >> "%LOG_FILE%"
    echo Run Component 0 first: 00_build_common_python.bat
    exit /b 1
)

REM Copy embedded Python
echo Copying embedded Python... >> "%LOG_FILE%"
echo Copying embedded Python...
robocopy "%EMBED_SOURCE%" "%EXPORT_DIR%\embed_py311" /E /NFL /NDL /NP >> "%LOG_FILE%" 2>&1
if %ERRORLEVEL% GTR 7 (
    echo ERROR: Failed to copy embedded Python, error level %ERRORLEVEL% >> "%LOG_FILE%"
    echo ERROR: Failed to copy embedded Python, error level %ERRORLEVEL%
    exit /b 1
)
echo Embedded Python copied successfully >> "%LOG_FILE%"

REM Copy tool-specific README if available
echo Checking for tool-specific README... >> "%LOG_FILE%"
echo Checking for tool-specific README...
set "README_SRC=%ROOT_DIR%\implementations\python-package\scriptcraft\tools\%TOOL_NAME%\README_distributable.md"
if exist "%README_SRC%" (
    echo Copying tool-specific README... >> "%LOG_FILE%"
    echo Copying tool-specific README...
    copy "%README_SRC%" "%EXPORT_DIR%\README.md" >> "%LOG_FILE%" 2>&1
    echo Tool-specific README copied >> "%LOG_FILE%"
) else (
    echo Tool-specific README not found, using default >> "%LOG_FILE%"
    echo Tool-specific README not found, using default
)

REM Clean up unnecessary files
echo Cleaning up unnecessary files... >> "%LOG_FILE%"
echo Cleaning up unnecessary files...
if exist "%EXPORT_DIR%\import_embed.bat" del "%EXPORT_DIR%\import_embed.bat" >> "%LOG_FILE%" 2>&1

echo SUCCESS: Component 2 completed successfully >> "%LOG_FILE%"
echo SUCCESS: Template setup complete
echo Export directory: %EXPORT_DIR%
echo Log: %LOG_FILE%

exit /b 0