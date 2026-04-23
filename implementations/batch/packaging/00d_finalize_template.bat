@echo off

REM Basic path setup
set "SCRIPT_DIR=%~dp0"
for %%i in ("%SCRIPT_DIR%..\..\py_embed_setup\embed_py311") do set "EMBED_DIR=%%~fi"
for %%i in ("%SCRIPT_DIR%..\..\templates\distributable_template\embed_py311") do set "TEMPLATE_EMBED_DIR=%%~fi"
for %%i in ("%SCRIPT_DIR%..\..\config.yaml") do set "CONFIG_PATH=%%~fi"

REM Setup logging
for %%i in ("%SCRIPT_DIR%..\..\data\logs") do set "LOG_DIR=%%~fi"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
set "LOG_FILE=%LOG_DIR%\00d_finalize_template.txt"

REM Start logging
echo Component 0d: Finalize Template > "%LOG_FILE%"
echo =============================== >> "%LOG_FILE%"
echo %DATE% %TIME% >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

echo Component 0d: Finalize Template
echo ===============================

REM Check if embedded Python exists
echo Validating embedded Python... >> "%LOG_FILE%"
echo Validating embedded Python...
if not exist "%EMBED_DIR%" (
    echo ERROR: Embedded Python not found at %EMBED_DIR% >> "%LOG_FILE%"
    echo ERROR: Embedded Python not found at %EMBED_DIR%
    echo Run components 0a, 0b, and 0c first >> "%LOG_FILE%"
    echo Run components 0a, 0b, and 0c first
    exit /b 1
)

echo Embedded Python found: %EMBED_DIR% >> "%LOG_FILE%"
echo Embedded Python found: %EMBED_DIR%
echo. >> "%LOG_FILE%"
echo.

REM Generate config.bat if config.yaml exists
echo Checking for config.yaml... >> "%LOG_FILE%"
echo Checking for config.yaml...
if exist "%CONFIG_PATH%" (
    echo Generating config.bat... >> "%LOG_FILE%"
    echo Generating config.bat...
    python "%SCRIPT_DIR%config_processor.py" config_bat "%CONFIG_PATH%" "%SCRIPT_DIR%..\..\templates\distributable_template" "%DATE% %TIME%" >> "%LOG_FILE%" 2>&1
    if errorlevel 1 (
        echo ERROR: Failed to generate config.bat >> "%LOG_FILE%"
        echo ERROR: Failed to generate config.bat
        exit /b 1
    )
    echo Config.bat generated >> "%LOG_FILE%"
    echo Config.bat generated
) else (
    echo WARNING: config.yaml not found, skipping config.bat generation >> "%LOG_FILE%"
    echo WARNING: config.yaml not found, skipping config.bat generation
)

echo Preparing template directory... >> "%LOG_FILE%"
echo Preparing template directory...
if exist "%TEMPLATE_EMBED_DIR%" (
    echo Removing existing template... >> "%LOG_FILE%"
    echo Removing existing template...
    rd /s /q "%TEMPLATE_EMBED_DIR%" 2>nul
)

REM Ensure template directory exists
for %%i in ("%SCRIPT_DIR%..\..\templates\distributable_template") do set "TEMPLATE_DIR=%%~fi"
if not exist "%TEMPLATE_DIR%" mkdir "%TEMPLATE_DIR%"

echo Copying files... >> "%LOG_FILE%"
echo Copying files...
xcopy /e /i /y "%EMBED_DIR%" "%TEMPLATE_EMBED_DIR%" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: Failed to copy to template >> "%LOG_FILE%"
    echo ERROR: Failed to copy to template
    exit /b 1
)

echo Cleaning up build directory... >> "%LOG_FILE%"
echo Cleaning up build directory...
rd /s /q "%EMBED_DIR%" 2>nul

echo SUCCESS: Component 0d completed successfully >> "%LOG_FILE%"
echo SUCCESS: Template finalized
echo Location: %TEMPLATE_EMBED_DIR%
exit /b 0