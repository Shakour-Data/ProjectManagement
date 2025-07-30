# Instructions for Running Tests in the ProjectManagement Repository

This document provides detailed instructions to set up the environment and run the tests successfully, avoiding common import errors related to the `src` directory.

## Prerequisites

- Python 3.7 or higher installed.
- `pip` package manager installed.

## Setting Up the Environment

1. **Create a virtual environment (recommended):**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install required packages:**

```bash
pip install -r config/requirements.txt
pip install pytest
```

## Running Tests

The source code is located in the `src` directory, which is not installed as a package. To allow Python to find the `src` modules during testing, you need to set the `PYTHONPATH` environment variable to include the `src` directory.

### On Linux/macOS

Run tests with:

```bash
PYTHONPATH=src pytest tests/
```

### On Windows (PowerShell)

Run tests with:

```powershell
$env:PYTHONPATH="src"
pytest tests/
```

### On Windows (Command Prompt)

Run tests with:

```cmd
set PYTHONPATH=src
pytest tests/
```

## Running Specific Test Files

To run a specific test file, for example `tests/test_progress_report.py`, use:

```bash
PYTHONPATH=src pytest tests/test_progress_report.py
```

## Notes

- Ensure you run the commands from the root directory of the project (`/workspaces/ProjectManagement`).
- If you encounter permission issues, ensure your user has the necessary rights to execute the commands.
- If you add new dependencies, update `config/requirements.txt` accordingly.

## Troubleshooting

- If you still get import errors, verify that the `src` directory contains an `__init__.py` file to mark it as a package.
- Make sure you activate the virtual environment before running tests.
- Check that the `PYTHONPATH` is correctly set in your shell environment.

---

Following these instructions should allow you to run the tests successfully without import errors.
