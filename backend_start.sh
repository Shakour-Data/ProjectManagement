#!/bin/bash
# Start backend server on Unix-like systems
source venv/bin/activate
uvicorn backend.api:app --host 0.0.0.0 --port 5050
