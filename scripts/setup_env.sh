#!/bin/bash

# Check if virtual environment directory "venv" exists in project root
if [ ! -d "venv" ]; then
  echo "Virtual environment not found in project root. Creating one..."
  python3 -m venv venv
  if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment. Please ensure python3-venv is installed."
    exit 1
  fi
else
  echo "Virtual environment found in project root."
fi

# Activate the virtual environment from project root
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt

echo "Setup complete. Virtual environment is ready and packages are installed."
