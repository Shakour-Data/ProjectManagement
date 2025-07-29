@echo off
REM This batch script builds the Windows standalone executable for installer_gui/installer.py using PyInstaller.
REM It assumes Python and PyInstaller are installed in the environment.

set SCRIPT_PATH=.\installer_gui\installer.py
set DIST_DIR=..\dist_installers

if not exist %DIST_DIR% (
    mkdir %DIST_DIR%
)

echo Building Windows graphical installer executable...
pyinstaller --onefile --name ProjectManagementSetup_Windows.exe --windowed --clean --exclude-module cross_platform_setup --exclude-module project_management --exclude-module backend --exclude-module frontend %SCRIPT_PATH%
move dist\ProjectManagementSetup_Windows.exe %DIST_DIR%\

echo Build complete. Executable is in %DIST_DIR%
pause
