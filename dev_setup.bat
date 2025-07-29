@echo off
REM Developer setup script for Windows

REM Clone the repository
git clone https://github.com/Shakour-Data/ProjectManagement.git

cd ProjectManagement || exit /b 1

REM Run the setup script automatically
call setup_and_run.bat
