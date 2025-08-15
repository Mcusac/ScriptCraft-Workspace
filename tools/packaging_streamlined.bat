@echo off
setlocal EnableDelayedExpansion

:: ==========================
:: 🚀 Streamlined Packaging Script (Ultra-Simple)
:: ==========================
set "ROOT_DIR=%~dp0"
set "SOURCE_CONFIG=%ROOT_DIR%..\config.yaml"
set "LOG_DIR=%ROOT_DIR%logs"
set "LOG_FILE=%LOG_DIR%\packaging_streamlined.txt"

:: =======================
:: 📝 Timestamp
:: =======================
set TIMESTAMP=%DATE:~-4%-%DATE:~4,2%-%DATE:~7,2%

:: ==========================
:: 📁 Ensure logs folder
:: ==========================
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
echo 🚀 Streamlined Packaging started: %DATE% %TIME% > "%LOG_FILE%"

:: ==========================
:: 📋 Extract tool name from config.yaml
:: ==========================
for /f "tokens=2 delims=:" %%A in ('findstr /i "tool_to_ship:" "%SOURCE_CONFIG%"') do (
    set "TOOL_NAME=%%A"
    set "TOOL_NAME=!TOOL_NAME: =!"
    set "TOOL_NAME=!TOOL_NAME:"=!"
)

set "TEMPLATE_DIR=%ROOT_DIR%..\templates\distributable_modern_template"
set "EXPORT_DIR=%ROOT_DIR%..\distributables\%TOOL_NAME%_distributable"

:: ==========================
:: 🧼 Clean export folder
:: ==========================
echo 🧹 Cleaning previous export directory... >> "%LOG_FILE%"
if exist "%EXPORT_DIR%" rmdir /s /q "%EXPORT_DIR%"
mkdir "%EXPORT_DIR%" 2>nul
echo ✅ Fresh Export directory created: %EXPORT_DIR% >> "%LOG_FILE%"

:: ==========================
:: 📁 Copy template files
:: ==========================
echo 📁 Copying package template... >> "%LOG_FILE%"
xcopy /e /i /y "%TEMPLATE_DIR%\*" "%EXPORT_DIR%" >> "%LOG_FILE%" 2>&1
echo ✅ Template files copied to: %EXPORT_DIR% >> "%LOG_FILE%"

:: ==========================
:: 📋 Generate simple config.bat
:: ==========================
echo 📋 Creating simple config.bat... >> "%LOG_FILE%"
(
echo @echo off
echo set "TOOL_NAME=%TOOL_NAME%"
echo set "TOOL_DESCRIPTION=ScriptCraft %TOOL_NAME% Tool"
) > "%EXPORT_DIR%\config.bat"
echo ✅ Simple config.bat created. >> "%LOG_FILE%"

:: ==========================
:: 📄 Copy tool-specific README
:: ==========================
set "README_SRC=%ROOT_DIR%..\implementations\python-package\scriptcraft\tools\%TOOL_NAME%\README_distributable.md"
echo 📄 Copying tool-specific README... >> "%LOG_FILE%"
if exist "%README_SRC%" (
    copy "%README_SRC%" "%EXPORT_DIR%\README.md" >nul 2>&1
    echo ✅ Tool-specific README copied. >> "%LOG_FILE%"
) else (
    echo ⚠️ Tool-specific README not found at: "%README_SRC%" >> "%LOG_FILE%"
)

:: ==========================
:: 🐍 Build embedded Python (if needed)
:: ==========================
echo 🐍 Building embedded Python... >> "%LOG_FILE%"
set "EMBED_BUILDER=%ROOT_DIR%py_embed_setup\build_embed_python.bat"
cmd /c ""%EMBED_BUILDER%" %TOOL_NAME%" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ❌ Embedded Python build failed. >> "%LOG_FILE%"
    goto :error
)
echo ✅ Embedded Python built successfully. >> "%LOG_FILE%"

:: ==========================
:: 🐍 Copy embedded Python using robocopy (handles long paths)
:: ==========================
echo 🐍 Copying embedded Python using robocopy... >> "%LOG_FILE%"
set "SOURCE_EMBED=%ROOT_DIR%py_embed_setup\embed_py311"
set "TARGET_EMBED=%EXPORT_DIR%\embed_py311"

if exist "%SOURCE_EMBED%" (
    robocopy "%SOURCE_EMBED%" "%TARGET_EMBED%" /E /R:3 /W:1 >> "%LOG_FILE%" 2>&1
    if errorlevel 8 (
        echo ❌ Robocopy failed with error level 8 or higher. >> "%LOG_FILE%"
        goto :error
    )
    echo ✅ Embedded Python copied successfully. >> "%LOG_FILE%"
) else (
    echo ❌ Embedded Python not found at: %SOURCE_EMBED% >> "%LOG_FILE%"
    goto :error
)

:: ==========================
:: 📦 Copy local scriptcraft package
:: ==========================
echo 📦 Copying local scriptcraft package... >> "%LOG_FILE%"
set "SCRIPTCRAFT_SRC=%ROOT_DIR%..\implementations\python-package\scriptcraft"
set "SCRIPTCRAFT_DST=%TARGET_EMBED%\Lib\site-packages\scriptcraft"
if exist "%SCRIPTCRAFT_SRC%" (
    robocopy "%SCRIPTCRAFT_SRC%" "%SCRIPTCRAFT_DST%" /E /R:3 /W:1 >> "%LOG_FILE%" 2>&1
    if errorlevel 8 (
        echo ❌ Failed to copy scriptcraft package. >> "%LOG_FILE%"
        goto :error
    )
    echo ✅ Local scriptcraft package copied. >> "%LOG_FILE%"
) else (
    echo ❌ Local scriptcraft package not found at: %SCRIPTCRAFT_SRC% >> "%LOG_FILE%"
    goto :error
)

:: ==========================
:: 🧼 Clean up unnecessary files
:: ==========================
echo 🧼 Cleaning up unnecessary files... >> "%LOG_FILE%"
del "%EXPORT_DIR%\import_embed.bat" >nul 2>&1
del "%EXPORT_DIR%\config.bat" >nul 2>&1
echo ✅ Cleaned up unnecessary files. >> "%LOG_FILE%"

:: ==========================
:: 🧪 Test the distributable
:: ==========================
echo 🧪 Testing distributable... >> "%LOG_FILE%"
pushd "%EXPORT_DIR%"
echo Testing Python installation... >> "%LOG_FILE%"
"%TARGET_EMBED%\python.exe" -c "import scriptcraft; print('✅ scriptcraft package found')" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ❌ scriptcraft package not found in embedded Python. >> "%LOG_FILE%"
    popd
    goto :error
)
echo ✅ scriptcraft package verified. >> "%LOG_FILE%"
popd

:: ==========================
:: ✅ Finish
:: ==========================
echo ✅ Streamlined packaging complete! >> "%LOG_FILE%"
echo 📦 Distributable created at: %EXPORT_DIR% >> "%LOG_FILE%"
echo 🎯 To run: cd "%EXPORT_DIR%" ^& run.bat >> "%LOG_FILE%"
start notepad "%LOG_FILE%"
exit /b 0

:error
echo ❌ Streamlined packaging failed. >> "%LOG_FILE%"
start notepad "%LOG_FILE%"
exit /b 1
