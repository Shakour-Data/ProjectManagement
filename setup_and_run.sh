#!/bin/bash

# Clone the repository
git clone https://github.com/Shakour-Data/ProjectManagement.git

cd ProjectManagement || exit 1

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend || exit 1
npm install

# Start backend server in background on port 5050
cd ..
source venv/bin/activate
uvicorn backend.api:app --host 0.0.0.0 --port 5050 &

# Start frontend server in background on port 5051
cd frontend || exit 1
PORT=5051 npm start &

# Open frontend URL in default browser
xdg-open http://localhost:5051

# Wait for background processes
wait
