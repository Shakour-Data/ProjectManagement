@echo off
REM Setup and run ProjectManagement on Windows

REM Check if venv directory exists
IF NOT EXIST venv (
    echo Creating virtual environment...
    python -m venv venv
) ELSE (
    echo Virtual environment already exists.
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip

REM Install Python dependencies
pip install -r requirements.txt

REM Install uvicorn if not installed
pip install uvicorn

REM Start backend server in background on port 5050
start "" cmd /c "call venv\Scripts\activate.bat && uvicorn backend.api:app --host 0.0.0.0 --port 5050"

REM Start frontend server in background on port 5051
cd frontend
start "" cmd /c "npm install"
start "" cmd /c "npm start"
cd ..

echo Setup complete. Backend running on http://localhost:5050 and frontend on http://localhost:5051
pause
