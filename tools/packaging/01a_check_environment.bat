@echo off
setlocal EnableDelayedExpansion

echo [DEBUG] Starting Component 1a...
echo [DEBUG] Script directory: %~dp0

:: ================================
:: 🔧 Component 1a: Check Environment
:: ================================
echo [DEBUG] Setting SCRIPT_DIR...
set "SCRIPT_DIR=%~dp0"
echo [DEBUG] SCRIPT_DIR set to: %SCRIPT_DIR%

echo [DEBUG] About to change directory...
:: Get absolute path to root directory
cd /d "%SCRIPT_DIR%"
echo [DEBUG] Changed to script directory: %CD%

echo [DEBUG] About to go up two levels...
cd ..\..
echo [DEBUG] Changed to: %CD%

echo [DEBUG] Setting ROOT_DIR...
set "ROOT_DIR=%CD%"
echo [DEBUG] ROOT_DIR set to: %ROOT_DIR%

echo [DEBUG] Returning to script directory...
cd /d "%SCRIPT_DIR%"
echo [DEBUG] Back to: %CD%

echo [DEBUG] Setting TEMPLATE_EMBED_DIR...
set "TEMPLATE_EMBED_DIR=%ROOT_DIR%\templates\distributable_template\embed_py311"
echo [DEBUG] TEMPLATE_EMBED_DIR set to: %TEMPLATE_EMBED_DIR%

echo [DEBUG] Setting PYTHON...
set "PYTHON=%TEMPLATE_EMBED_DIR%\python.exe"
echo [DEBUG] PYTHON set to: %PYTHON%

echo [DEBUG] About to display main header...
echo Component 1a: Checking Environment
echo ===============================
echo Time: %DATE% %TIME%
echo ===============================

echo [DEBUG] About to check if template directory exists...
echo [DEBUG] Starting template directory check...
echo [DEBUG] About to test if statement...
if exist "C:\Users\mdc0431\OneDrive - UNT System\Documents\Projects\ScriptCraft-Workspace\templates\distributable_template\embed_py311" echo [DEBUG] Template directory exists
if not exist "C:\Users\mdc0431\OneDrive - UNT System\Documents\Projects\ScriptCraft-Workspace\templates\distributable_template\embed_py311" (
echo [DEBUG] Template directory does not exist
echo ERROR: Common embedded Python not found
exit /b 1
)
echo [DEBUG] Template directory check passed

echo [DEBUG] About to check if python.exe exists...
if exist "C:\Users\mdc0431\OneDrive - UNT System\Documents\Projects\ScriptCraft-Workspace\templates\distributable_template\embed_py311\python.exe" echo [DEBUG] Python executable exists
if not exist "C:\Users\mdc0431\OneDrive - UNT System\Documents\Projects\ScriptCraft-Workspace\templates\distributable_template\embed_py311\python.exe" (
echo [DEBUG] Python executable does not exist
echo ERROR: python.exe not found
exit /b 1
)
echo [DEBUG] Python executable check passed

echo [DEBUG] About to display success messages...
echo SUCCESS: Common embedded Python found
echo SUCCESS: Python executable found

echo [DEBUG] About to exit...
exit /b 0
