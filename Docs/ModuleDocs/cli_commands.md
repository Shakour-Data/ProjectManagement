# cli_commands Module

## Overview
The `cli_commands` module provides command line interface commands for the Project Management Tool. It supports project setup, status checking, and utility functions to run shell commands and prompt user input.

## Functions

- `run_command(command)`
  - Runs a shell command using subprocess.
  - Parameters:
    - `command` (list): List of command arguments.
  - Logs errors if the command fails.

- `prompt_user(question, default=None)`
  - Prompts the user for input with an optional default value.
  - Parameters:
    - `question` (str): The prompt question.
    - `default` (str, optional): Default answer if user input is empty.
  - Returns: User input or default.

- `setup_project()`
  - Sets up the project environment by:
    - Removing obsolete `PM_UserInputs` directory.
    - Initializing a git repository.
    - Ensuring `.gitignore` excludes the virtual environment.
    - Creating `requirements.txt`.
    - Creating a virtual environment.
    - Installing dependencies.
  - Logs progress and instructions.

- `status()`
  - Checks and logs the status of the project environment:
    - Git repository presence.
    - Virtual environment presence.
    - `requirements.txt` file presence.
    - User input JSON directory presence.

- `main()`
  - Parses CLI arguments and runs the specified command (`setup` or `status`).
  - Prints help if no valid command is provided.

## Usage
Run the module as a script to use the CLI commands:

```bash
python cli_commands.py setup
python cli_commands.py status
```

---

This documentation provides an overview of the `cli_commands` module to assist developers in using the CLI commands for project setup and status checking.
