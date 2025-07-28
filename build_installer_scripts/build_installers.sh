#!/bin/bash
# This script builds standalone executables for cross_platform_setup.py using PyInstaller for Linux, Windows, and macOS.
# It assumes PyInstaller is installed in the environment.

set -e

SCRIPT_PATH="../cross_platform_setup.py"
DIST_DIR="../dist_installers"

mkdir -p $DIST_DIR

echo "Building Linux executable..."
pyinstaller --onefile --name ProjectManagementSetup_Linux $SCRIPT_PATH
mv dist/ProjectManagementSetup_Linux $DIST_DIR/

echo "Building Windows executable..."
pyinstaller --onefile --name ProjectManagementSetup_Windows.exe --windowed $SCRIPT_PATH
mv dist/ProjectManagementSetup_Windows.exe $DIST_DIR/

echo "Building macOS executable..."
pyinstaller --onefile --name ProjectManagementSetup_macOS $SCRIPT_PATH
mv dist/ProjectManagementSetup_macOS $DIST_DIR/

echo "Build complete. Executables are in $DIST_DIR"
