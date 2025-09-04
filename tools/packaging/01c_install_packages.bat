@echo off
setlocal EnableDelayedExpansion

::: ================================
::: 🔧 Component 1c: Install Packages
::: ================================
set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%..\.."
set "TEMPLATE_EMBED_DIR=%ROOT_DIR%\templates\distributable_template\embed_py311"
set "PYTHON=%TEMPLATE_EMBED_DIR%\python.exe"

echo 🔧 Component 1c: Installing Packages
echo ===============================
echo 🕒 %DATE% %TIME%
echo ===============================

::: ================================
::: 📋 Load configuration from generated config.bat
::: ================================
set "TEMPLATE_DIR=%ROOT_DIR%\templates\distributable_template"
if not exist "%TEMPLATE_DIR%\config.bat" (
    echo ❌ ERROR: config.bat not found at %TEMPLATE_DIR%\config.bat
    exit /b 1
)
call "%TEMPLATE_DIR%\config.bat"
set "TOOL_NAME=%TOOL_TO_SHIP%"

::: ================================
::: 📦 Get tool-specific packages from config.bat
::: ================================
echo 📦 Reading tool-specific packages from config.bat...
set "TOOL_PACKAGES=%TOOL_PACKAGES%"
if "%TOOL_PACKAGES%"=="" (
    echo ⚠️ No tool-specific packages defined; using common packages only.
)

echo 📦 Tool-specific packages: %TOOL_PACKAGES%

::: ================================
::: 📦 Install tool-specific packages (if any)
::: ================================
if not "%TOOL_PACKAGES%"=="" (
    echo 📦 Installing tool-specific packages: %TOOL_PACKAGES%
    pushd "%TEMPLATE_EMBED_DIR%"
    "%PYTHON%" -m pip install --no-cache-dir %TOOL_PACKAGES% --no-warn-script-location
    if errorlevel 1 (
        echo ❌ ERROR: Failed installing tool-specific packages
        exit /b 1
    )
    popd
    echo ✅ Tool-specific packages installed successfully
) else (
    echo ℹ️ No tool-specific packages to install
)

::: ================================
::: 🧾 List installed packages
::: ================================
echo 📋 Final installed packages:
"%PYTHON%" -m pip list

echo ✅ Component 1c Complete: Packages Installed
exit /b 0
