@echo off
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
