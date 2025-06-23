@echo off
setlocal EnableDelayedExpansion

:: =======================
:: 📁 Ensure logs folder exists
:: =======================
if not exist logs mkdir logs

:: =======================
:: 📦 Setup dynamic paths
:: =======================
set "BASE_DIR=%~dp0"
set "SOURCE_EMBED=%~dp0..\..\tools\py_embed_setup\embed_py311"
set "TARGET_EMBED=%BASE_DIR%embed_py311"
set "LOG_FILE=logs\import_embed.txt"

:: =======================
:: 🛠️ Start Log
:: =======================
echo 🛠️ Import Embed started for %BASE_DIR% > "%LOG_FILE%"
echo =============================== >> "%LOG_FILE%"
echo 🕒 %DATE% %TIME% >> "%LOG_FILE%"
echo =============================== >> "%LOG_FILE%"

:: =======================
:: 🧹 Remove old embed folder
:: =======================
if exist "%TARGET_EMBED%" rmdir /s /q "%TARGET_EMBED%"

:: =======================
:: 📁 Copy fresh embed
:: =======================
echo 📁 Copying embed from: %SOURCE_EMBED% >> "%LOG_FILE%"
if not exist "%SOURCE_EMBED%" (
    echo ❌ Source embed not found at: %SOURCE_EMBED% >> "%LOG_FILE%"
    exit /b 1
)

xcopy /e /i /y "%SOURCE_EMBED%" "%TARGET_EMBED%" >> "%LOG_FILE%" 2>&1

echo ✅ Import complete! >> "%LOG_FILE%"
echo 🕒 Import completed at %DATE% %TIME% >> "%LOG_FILE%"
echo =============================== >> "%LOG_FILE%"
exit /b 0