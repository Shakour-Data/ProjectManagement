@echo off
REM Start backend server on Windows
call venv\Scripts\activate.bat
uvicorn backend.api:app --host 0.0.0.0 --port 5050
