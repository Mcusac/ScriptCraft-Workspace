@echo off
setlocal EnableDelayedExpansion

:: ==========================
:: 🚀 Setup and Paths
:: ==========================
set "ROOT_DIR=%~dp0"
set "SOURCE_CONFIG=%ROOT_DIR%config.yaml"
set "LOG_DIR=%ROOT_DIR%logs"
set "LOG_FILE=%LOG_DIR%\packaging_log.txt"

:: =======================
:: 📝 Timestamp
:: =======================
:: Use simple date command instead of PowerShell to avoid drive access issues
set TIMESTAMP=%DATE:~-4%-%DATE:~4,2%-%DATE:~7,2%

:: ==========================
:: 📁 Ensure logs folder
:: ==========================
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
echo 🚀 Packaging started: %DATE% %TIME% > "%LOG_FILE%"

:: ==========================
:: 📋 Extract values from config.yaml using PowerShell
:: ==========================
:: Extract tool_name
for /f "tokens=2 delims=:" %%A in ('findstr /i "tool_to_ship:" "%SOURCE_CONFIG%"') do (
    set "TOOL_NAME=%%A"
    set "TOOL_NAME=!TOOL_NAME: =!"
    set "TOOL_NAME=!TOOL_NAME:"=!"
)

:: Extract TOOLS_DIR and COMMON_DIR from config.yaml's `paths` block
for /f "tokens=2 delims=:" %%A in ('findstr /i "tools_dir:" "%SOURCE_CONFIG%"') do (
    set "TOOLS_DIR=%%A"
    set "TOOLS_DIR=!TOOLS_DIR: =!"
)

:: Extract common_dir
for /f "tokens=2 delims=:" %%A in ('findstr /i "common_dir:" "%SOURCE_CONFIG%"') do (
    set "COMMON_DIR=%%A"
    set "COMMON_DIR=!COMMON_DIR: =!"
)

:: Extract embed_builder_path
for /f "tokens=2 delims=:" %%A in ('findstr /i "embed_builder_path:" "%SOURCE_CONFIG%"') do (
    set "EMBED_BUILDER=%%A"
    set "EMBED_BUILDER=!EMBED_BUILDER: =!"
    set "EMBED_BUILDER=!EMBED_BUILDER:"=!"
)

:: Extract packages (single line with [] list)
for /f "tokens=2 delims=:" %%A in ('findstr /i "packages:" "%SOURCE_CONFIG%"') do (
    set "PACKAGES=%%A"
    set "PACKAGES=!PACKAGES:[=!"
    set "PACKAGES=!PACKAGES:]=!"
    set "PACKAGES=!PACKAGES:,=!"
)

:: Now that TOOL_NAME is known, compute export path
set "PACKAGE_DIR=%ROOT_DIR%%TOOLS_DIR%\%TOOL_NAME%"
set "COMMON_DIR=%ROOT_DIR%%COMMON_DIR%"
set "TEMPLATE_DIR=%ROOT_DIR%templates\distributable_template"
set "EXPORT_DIR=%ROOT_DIR%distributables\%TOOL_NAME%_distributable"
set "FINAL_ZIP=%ROOT_DIR%distributables\%TOOL_NAME%_distributable_%DATE:/=-%_%TIME::=-%.zip"

:: ==========================
:: Debugging config extraction
:: ==========================
@REM echo Using config.yaml at: %SOURCE_CONFIG%
@REM if not exist "%SOURCE_CONFIG%" (
@REM     echo ❌ config.yaml not found in root directory. Aborting.
@REM     exit /b 1
@REM )
@REM echo 🚀 DEBUG: Dumping config.yaml contents... >> "%LOG_FILE%"
@REM type "%SOURCE_CONFIG%" >> "%LOG_FILE%"
@REM echo 🔍 END of config.yaml dump. >> "%LOG_FILE%"

:: ==========================
:: 📝 Log extracted values
:: ==========================
echo 🔍 TOOL_NAME: %TOOL_NAME% >> "%LOG_FILE%"
echo 📂 TOOLS_DIR: %TOOLS_DIR% >> "%LOG_FILE%"
echo 📂 COMMON_DIR: %COMMON_DIR% >> "%LOG_FILE%"
echo 📦 PACKAGES: %PACKAGES% >> "%LOG_FILE%"
echo 🔧 EMBED_BUILDER: %EMBED_BUILDER% >> "%LOG_FILE%"

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
:: 📋 Generate config.bat in distributable folder
:: ==========================
echo 📋 Creating config.bat in distributable... >> "%LOG_FILE%"
python "%ROOT_DIR%tools\yaml_to_bat_converter.py" "%SOURCE_CONFIG%" "%EXPORT_DIR%\config.bat"
if not exist "%EXPORT_DIR%\config.bat" (
    echo ❌ config.bat generation failed. Aborting. >> "%LOG_FILE%"
    goto :error
)
echo ✅ config.bat created successfully. >> "%LOG_FILE%"

:: ==========================
:: 📁 Inject tool + common code
:: ==========================
echo 📁 Copying tool files from %PACKAGE_DIR%... >> "%LOG_FILE%"
xcopy /e /i /y "%PACKAGE_DIR%\*" "%EXPORT_DIR%\scripts" >> "%LOG_FILE%" 2>&1
echo ✅ Tool files copied to: %EXPORT_DIR%\scripts >> "%LOG_FILE%"

echo 📁 Copying common files from %COMMON_DIR%... >> "%LOG_FILE%"
xcopy /e /i /y "%COMMON_DIR%\*" "%EXPORT_DIR%\scripts\common" >> "%LOG_FILE%" 2>&1
echo ✅ Common files copied to: %EXPORT_DIR%\scripts\common >> "%LOG_FILE%"

:: ==========================
:: 📄 Update ReadMe's
:: ==========================
echo 📄 Updating ReadMe files with build date... >> "%LOG_FILE%"

for %%R in (README.md README_distributable.md) do (
    set "README_PATH=%EXPORT_DIR%\scripts\%%R"
    if exist "!README_PATH!" (
        powershell -Command ^
        "$content = Get-Content '!README_PATH!';" ^
        "if ($content -match '\[INSERT_DATE_HERE\]') {" ^
        "    $content -replace '\[INSERT_DATE_HERE\]', '%TIMESTAMP%' | Set-Content '!README_PATH!'" ^
        "} else {" ^
        "    Add-Content '!README_PATH!' ''; Add-Content '!README_PATH!' '📅 Build Date: %TIMESTAMP%'" ^
        "}"
        echo 📄 %%R updated with build date: %TIMESTAMP% >> "%LOG_FILE%"
    ) else (
        echo ⚠️ %%R not found. >> "%LOG_FILE%"
    )
)
echo ✅ ReadMe Files updated with build date: %TIMESTAMP% >> "%LOG_FILE%"

:: ==========================
:: 📄 Move ReadMe_distributable to root of distributable as ReadMe
:: ==========================
echo 📄 Moving README_distributable.md to root of distributable... >> "%LOG_FILE%"
if exist "%EXPORT_DIR%\scripts\README_distributable.md" (
    move /y "%EXPORT_DIR%\scripts\README_distributable.md" "%EXPORT_DIR%\README.md" >> "%LOG_FILE%" 2>&1
) else (
    echo ⚠️ README_distributable.md not found in scripts folder. >> "%LOG_FILE%"
)
echo ✅ README_distributable.md moved to: %EXPORT_DIR%\README.md >> "%LOG_FILE%"

:: ==========================
:: 🐍 Build Python environment
:: ==========================
echo 🐍 Building embedded Python using: %EMBED_BUILDER% >> "%LOG_FILE%"
cmd /c ""%EMBED_BUILDER%" %TOOL_NAME%" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ❌ Embedded Python build failed. >> "%LOG_FILE%"
    goto :error
)
echo ✅ Embedded Python built successfully. >> "%LOG_FILE%"

:: ==========================
:: 📥 Import embedded Python
:: ==========================
echo 📥 Importing embedded Python to distributable... >> "%LOG_FILE%"
pushd "%EXPORT_DIR%"
call import_embed.bat >> "%LOG_FILE%" 2>&1
popd
echo ✅ Embedded Python imported successfully. >> "%LOG_FILE%"

:: ==========================
:: 🧼 Clean Extras
:: ==========================
echo 🧼 Removing unnecessary files... >> "%LOG_FILE%"
del "%EXPORT_DIR%\import_embed.bat" >nul 2>&1
del "%EXPORT_DIR%\scripts\__pycache__" /s /q >nul 2>&1
del "%EXPORT_DIR%\scripts\common\__pycache__" /s /q >nul 2>&1
if exist "%EXPORT_DIR%\scripts\plugins\__pycache__" (
    del "%EXPORT_DIR%\scripts\plugins\__pycache__" /s /q >nul 2>&1
)
echo ✅ Cleaned up import_embed.bat. >> "%LOG_FILE%"

:: ==========================
:: 🧪 Optional test run
:: ==========================
echo 🧪 Test run using run.bat... >> "%LOG_FILE%"
pushd "%EXPORT_DIR%"
call run.bat >> "%LOG_FILE%" 2>&1
popd
echo ✅ Test run completed. >> "%LOG_FILE%"

:: ==========================
:: 🗜 Create final zip
:: ==========================
@REM echo 🗜 Creating archive: %FINAL_ZIP% >> "%LOG_FILE%"
@REM powershell -Command "Compress-Archive -Path '%EXPORT_DIR%\*' -DestinationPath '%FINAL_ZIP%' -Force" >> "%LOG_FILE%" 2>&1

:: ==========================
:: ✅ Finish
:: ==========================
echo ✅ Packaging complete! >> "%LOG_FILE%"
@REM echo 📦 Final archive: %FINAL_ZIP% >> "%LOG_FILE%"
start notepad "%LOG_FILE%"
exit /b 0

:error
echo ❌ Packaging failed. >> "%LOG_FILE%"
start notepad "%LOG_FILE%"
exit /b 1

::: Remove test directories during packaging
:remove_test_dirs
echo Removing test directories...
for /r %%i in (tests) do (
    if exist "%%i" (
        echo Removing: %%i
        rd /s /q "%%i"
    )
)
goto :eof

:: Add this before final packaging steps
call :remove_test_dirs
