@echo off

REM Create a folder for Node.js installer
if not exist node_installer (
    mkdir node_installer
)

REM Download Node.js LTS Windows installer silently
powershell -Command "Invoke-WebRequest -Uri https://nodejs.org/dist/v18.17.1/node-v18.17.1-x64.msi -OutFile node_installer\\node-lts.msi"

REM Install Node.js silently
msiexec /i node_installer\\node-lts.msi /quiet /norestart

REM Delete the installer after installation
del /f /q node_installer\\node-lts.msi

REM Remove the installer folder if empty
rmdir node_installer

REM This script creates and activates a virtual environment for testing,
REM installs required dependencies, and runs all tests in the Tests folder.

REM Create virtual environment named test_env if it doesn't exist
if not exist test_env (
    python -m venv test_env
)

REM Activate the virtual environment
call test_env\Scripts\activate.bat

REM Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install pytest

REM Run tests and output results to test_results.xml
pytest Tests --junitxml=test_results.xml

REM Deactivate the virtual environment
deactivate
