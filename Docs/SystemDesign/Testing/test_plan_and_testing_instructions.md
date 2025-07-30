# Test Plan and Testing Instructions

*Last updated: 2025-07-27*

## Test Plan

### Overview

This test plan covers all necessary tests to ensure the ProjectManagement system works correctly and reliably.

### 1. Installation and Setup Tests

| Test Description | Initial Run | Latest Run | Latest Test Date | Notes |
| --- | --- | --- | --- | --- |
| Verify package installs correctly via `pip install auto_pm`. | ⬜ | ⬜ |  |  |
| Confirm package metadata (name, version, dependencies) is accurate. | ⬜ | ⬜ |  |  |
| Test installation in a clean virtual environment. | ⬜ | ⬜ |  |  |
| Verify package uninstallation works cleanly. | ⬜ | ⬜ |  |  |
| Test `auto_pm install` command executes without errors and creates input directory. | ⬜ | ⬜ |  |  |

### 2. Command Line Interface (CLI) Tests

| Test Description | Initial Run | Latest Run | Latest Test Date | Notes |
| --- | --- | --- | --- | --- |
| Test `auto_pm start` command runs successfully with valid inputs. | ⬜ | ⬜ |  |  |
| Test `auto_pm status` command displays correct status. | ⬜ | ⬜ |  |  |
| Test `auto_pm setup` command guides user interactively and validates inputs. | ⬜ | ⬜ |  |  |
| Test `auto_pm help` command displays usage instructions. | ⬜ | ⬜ |  |  |
| Test CLI argument parsing and invalid command handling. | ⬜ | ⬜ |  |  |

### 3. Input File Handling Tests

| Test Description | Initial Run | Latest Run | Latest Test Date | Notes |
| --- | --- | --- | --- | --- |
| Test `setup` command with all required JSON input files present and valid. | ⬜ | ⬜ |  |  |
| Test `setup` command with missing input files and verify appropriate warnings. | ⬜ | ⬜ |  |  |
| Test `setup` command with invalid JSON files and verify error messages. | ⬜ | ⬜ |  |  |
| Test handling of empty input directory. | ⬜ | ⬜ |  |  |

### 4. Workflow and Reporting Tests

| Test Description | Initial Run | Latest Run | Latest Test Date | Notes |
| --- | --- | --- | --- | --- |
| Test full workflow: install -> setup -> start -> status. | ⬜ | ⬜ |  |  |
| Verify reports and outputs generated correctly. | ⬜ | ⬜ |  |  |
| Test data flow and interaction between modules. | ⬜ | ⬜ |  |  |

### 5. Robustness and Error Handling Tests

| Test Description | Initial Run | Latest Run | Latest Test Date | Notes |
| --- | --- | --- | --- | --- |
| Test behavior when input files are updated between runs. | ⬜ | ⬜ |  |  |
| Test behavior with corrupted or malformed input files. | ⬜ | ⬜ |  |  |
| Test unexpected user inputs during interactive setup. | ⬜ | ⬜ |  |  |
| Test system resource limits and error recovery. | ⬜ | ⬜ |  |  |
| Test concurrent runs and file access conflicts. | ⬜ | ⬜ |  |  |

### 6. Performance Tests

| Test Description | Initial Run | Latest Run | Latest Test Date | Notes |
| --- | --- | --- | --- | --- |
| Test performance with large input files. | ⬜ | ⬜ |  |  |
| Test memory and CPU usage under load. | ⬜ | ⬜ |  |  |
| Test responsiveness of CLI commands. | ⬜ | ⬜ |  |  |

### 7. Security Tests

| Test Description | Initial Run | Latest Run | Latest Test Date | Notes |
| --- | --- | --- | --- | --- |
| Test secure handling of sensitive data (e.g., secret keys). | ⬜ | ⬜ |  |  |
| Verify no sensitive data is logged or exposed. | ⬜ | ⬜ |  |  |

### 8. Documentation and Usability Tests

| Test Description | Initial Run | Latest Run | Latest Test Date | Notes |
| --- | --- | --- | --- | --- |
| Verify `auto_pm help` command displays accurate and complete information. | ⬜ | ⬜ |  |  |
| Verify README and HELP.md files are up to date and clear. | ⬜ | ⬜ |  |  |
| Test links and references in documentation. | ⬜ | ⬜ |  |  |

### 9. Shell Integration and Terminal Tests

| Test Description | Initial Run | Latest Run | Latest Test Date | Notes |
| --- | --- | --- | --- | --- |
| Verify integrated terminal opens with correct shell on Linux. | ⬜ | ⬜ |  |  |
| Verify integrated terminal opens with correct shell on macOS. | ⬜ | ⬜ |  |  |
| Verify integrated terminal opens with correct shell on Windows. | ⬜ | ⬜ |  |  |
| Verify "Shell Integration Unavailable" issue is resolved. | ⬜ | ⬜ |  |  |
| Verify command outputs are visible in the terminal. | ⬜ | ⬜ |  |  |
| Verify VSCode reload and terminal restart apply the shell settings correctly. | ⬜ | ⬜ |  |  |

## Testing Instructions

### Prerequisites

- Python 3.7 or higher installed.
- `pip` package manager installed.

### Setting Up the Environment

1. Create a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install required packages:

```bash
pip install -r requirements.txt
pip install pytest
```

### Running Tests

The source code is located in the `project_management` directory. To allow Python to find the modules during testing, set the `PYTHONPATH` environment variable to include the `project_management` directory.

#### On Linux/macOS

```bash
PYTHONPATH=project_management pytest tests/
```

#### On Windows (PowerShell)

```powershell
$env:PYTHONPATH="project_management"
pytest tests/
```

#### On Windows (Command Prompt)

```cmd
set PYTHONPATH=project_management
pytest tests/
```

### Running Specific Test Files

To run a specific test file, for example `tests/test_progress_report.py`, use:

```bash
PYTHONPATH=project_management pytest tests/test_progress_report.py
```

### Notes

- Ensure you run the commands from the root directory of the project.
- If you encounter permission issues, ensure your user has the necessary rights to execute the commands.
- If you add new dependencies, update `requirements.txt` accordingly.

### Troubleshooting

- Verify that the `project_management` directory contains an `__init__.py` file to mark it as a package.
- Make sure you activate the virtual environment before running tests.
- Check that the `PYTHONPATH` is correctly set in your shell environment.

---

Following these instructions should allow you to run the tests successfully without import errors.
