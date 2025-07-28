@echo off
REM This batch script builds the Windows standalone executable for cross_platform_setup.py using PyInstaller.
REM It assumes Python and PyInstaller are installed in the environment.

set SCRIPT_PATH=..\cross_platform_setup.py
set DIST_DIR=..\dist_installers

if not exist %DIST_DIR% (
    mkdir %DIST_DIR%
)

echo Building Windows executable...
pyinstaller --onefile --name ProjectManagementSetup_Windows.exe --windowed %SCRIPT_PATH%
move dist\ProjectManagementSetup_Windows.exe %DIST_DIR%\

echo Build complete. Executable is in %DIST_DIR%
pause
