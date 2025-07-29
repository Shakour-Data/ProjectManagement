#!/bin/bash

# Developer setup script for Linux

# Clone the repository
git clone https://github.com/Shakour-Data/ProjectManagement.git

cd ProjectManagement || exit 1

# Run the setup script automatically
chmod +x setup_and_run.sh
./setup_and_run.sh
