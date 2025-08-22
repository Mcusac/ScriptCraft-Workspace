@echo off

echo Build Common Embedded Python
echo =============================
echo %DATE% %TIME%
echo.

REM Clean up any existing builds
for %%i in ("%~dp0..\..\py_embed_setup\embed_py311") do set "EMBED_DIR=%%~fi"
for %%i in ("%~dp0..\..\templates\distributable_template\embed_py311") do set "TEMPLATE_EMBED_DIR=%%~fi"

if exist "%EMBED_DIR%" (
    echo Removing previous build...
    rd /s /q "%EMBED_DIR%" 2>nul
)

if exist "%TEMPLATE_EMBED_DIR%" (
    echo Removing existing template...
    rd /s /q "%TEMPLATE_EMBED_DIR%" 2>nul
)

echo.
echo Running Component 0a: Extract Python Base
call "%~dp000a_extract_python.bat"
if errorlevel 1 (
    echo ERROR: Component 0a failed
    exit /b 1
)
echo Component 0a: SUCCESS

echo.
echo Running Component 0b: Setup Pip and Base Packages
call "%~dp000b_setup_pip.bat"
if errorlevel 1 (
    echo ERROR: Component 0b failed
    exit /b 1
)
echo Component 0b: SUCCESS

echo.
echo Running Component 0c: Install Common Packages
call "%~dp000c_install_common.bat"
if errorlevel 1 (
    echo ERROR: Component 0c failed
    exit /b 1
)
echo Component 0c: SUCCESS

echo.
echo Running Component 0d: Finalize Template
call "%~dp000d_finalize_template.bat"
if errorlevel 1 (
    echo ERROR: Component 0d failed
    exit /b 1
)
echo Component 0d: SUCCESS

echo.
echo ===================================
echo SUCCESS: Common Python Build Complete
echo ===================================
exit /b 0