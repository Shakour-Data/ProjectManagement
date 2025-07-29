#!/bin/bash
# Build standalone executable for graphical installer using PyInstaller

set -e

SCRIPT_PATH="./installer_gui/installer.py"
DIST_DIR="./dist_installers"

mkdir -p $DIST_DIR

echo "Building graphical installer executable for Linux..."
pyinstaller --onefile --name ProjectManagementInstaller_Linux --hidden-import=PyQt5.QtWebEngineWidgets --hidden-import=PyQtWebEngineWidgets $SCRIPT_PATH
mv dist/ProjectManagementInstaller_Linux $DIST_DIR/

echo "Build complete. Executable is in $DIST_DIR"
