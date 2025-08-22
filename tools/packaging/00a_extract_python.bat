@echo off
setlocal EnableDelayedExpansion

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::: Component 0a: Extract Python Base
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: Setup paths (DRY pattern from packaging_common.bat)
set "SCRIPT_DIR=%~dp0"
set "ROOT_REL=%SCRIPT_DIR%..\.."
for %%i in ("%ROOT_REL%") do set "ROOT_DIR=%%~fi"

set "EMBED_ROOT_REL=%ROOT_DIR%\py_embed_setup"
if defined SC_EMBED_ROOT set "EMBED_ROOT_REL=%SC_EMBED_ROOT%"
for %%i in ("%EMBED_ROOT_REL%") do set "EMBED_ROOT=%%~fi"

set "EMBED_DIR_REL=%EMBED_ROOT%\embed_py311"
set "EMBED_ZIP_REL=%EMBED_ROOT%\embed_py311.zip"
for %%i in ("%EMBED_DIR_REL%") do set "EMBED_DIR=%%~fi"
for %%i in ("%EMBED_ZIP_REL%") do set "EMBED_ZIP=%%~fi"
set "PYTHON=%EMBED_DIR%\python.exe"

for %%i in ("%ROOT_DIR%\data\logs") do set "LOG_DIR=%%~fi"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
set "LOG_FILE=%LOG_DIR%\00a_extract_python.txt"

::: Main execution with logging
(
echo.
echo Component 0a: Extract Python Base
echo ================================
echo %DATE% %TIME%
echo ================================

echo Validating ZIP file...
if not exist "%EMBED_ZIP%" (
    echo ERROR: Python archive not found
    echo Expected: %EMBED_ZIP%
    echo Download embed_py311.zip from python.org and place it in py_embed_setup/
    exit /b 1
)
echo ZIP file found: %EMBED_ZIP%

echo.
echo Preparing destination directory...
if not exist "%EMBED_DIR%" mkdir "%EMBED_DIR%"
echo Destination ready: %EMBED_DIR%

echo.
echo Extracting Python archive...
powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -LiteralPath '%EMBED_ZIP%' -DestinationPath '%EMBED_DIR%' -Force"
if errorlevel 1 (
    echo ERROR: Archive extraction failed
    exit /b 1
)

echo.
echo Validating extraction...
if not exist "%PYTHON%" (
    echo ERROR: Python executable not found after extraction
    echo Expected: %PYTHON%
    exit /b 1
)

echo.
echo SUCCESS: Component 0a completed successfully
echo Python location: %EMBED_DIR%

) > "%LOG_FILE%" 2>&1

echo Component 0a: Extract Python Base - SUCCESS
echo Log: %LOG_FILE%
exit /b 0