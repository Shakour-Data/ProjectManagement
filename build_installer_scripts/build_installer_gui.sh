#!/bin/bash
# Build standalone executable for graphical installer using PyInstaller

set -e

SCRIPT_PATH="./installer_gui/installer.py"
DIST_DIR="./dist_installers"
VENV_PATH="./venv"

mkdir -p $DIST_DIR

echo "Building graphical installer executable for Linux using Flask-based UI..."
source $VENV_PATH/bin/activate
pyinstaller --onefile --name ProjectManagementInstaller_Linux --add-data "installer_gui/ui:ui" $SCRIPT_PATH
mv dist/ProjectManagementInstaller_Linux $DIST_DIR/

echo "Build complete. Executable is in $DIST_DIR"
