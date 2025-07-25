Help En



# Project Management Package Help

This document provides help and guidance for using the Project Management package.

## Overview

The Project Management package is a Python-based automation system designed to streamline software project management. It integrates with GitHub and Visual Studio Code (VS Code) to automate task management, progress tracking, resource allocation, and reporting.

## Installation

* Install the package using pip or from source.
* Use the provided setup scripts (`scripts/setup_env.sh` and `scripts/setup_interactive.py`) to prepare the environment and input data.

## Usage

* Use the CLI commands to install, setup, start, and check the status of the project management system.
* Provide JSON input files defining the Work Breakdown Structure (WBS), workflow, resources, and allocations.
* Interact with the system via the VS Code chat interface for natural language task management.

## Commands

* `install`: Sets up the project directory and input files.
* `setup`: Validates inputs and prepares the environment.
* `start`: Starts the automation processes.
* `status`: Displays the current status of the project management system.
* `help`: Displays this help document.

## Input Files

Required JSON files include:

* detailed\_wbs.json
* workflow\_definition.json
* resource\_allocation.json
* task\_resource\_allocation.json
* wbs\_data.json
* wbs\_scores.json
* human\_resources.json (created interactively)

## Reports and Outputs

* The system generates progress reports, dashboards, and changelogs.
* Outputs are saved in designated directories for review.

## Troubleshooting

* Ensure all required JSON input files are present and valid.
* Use the interactive setup script to enter human resources data.
* Check the virtual environment is activated before running commands.
* Review logs for errors during automation.

## Support

For further assistance, refer to the comprehensive documentation in the `docs/` directory or contact the development team.