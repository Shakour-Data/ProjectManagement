# Test Checklist for auto_pm Package

This checklist covers all necessary tests to ensure the auto_pm package works correctly and reliably.

| Test Description                                                                                     | Initial Run | Latest Run | Notes                                  |
|---------------------------------------------------------------------------------------------------|-------------|------------|----------------------------------------|
| Verify package installs correctly via `pip install auto_pm`.                                      | ✅          | ✅         |                                        |
| Confirm package metadata (name, version, dependencies) is accurate.                               | ✅          | ✅         |                                        |
| Test installation in a clean virtual environment.                                                 | ✅          | ✅         |                                        |
| Verify package uninstallation works cleanly.                                                     | ✅          | ✅         |                                        |
| Test `auto_pm install` command executes without errors and creates input directory.               | ✅          | ✅         |                                        |
| Test `auto_pm start` command runs successfully with valid inputs.                                 | ✅          | ✅         |                                        |
| Test `auto_pm status` command displays correct status.                                           | ✅          | ✅         |                                        |
| Test `auto_pm setup` command guides user interactively and validates inputs.                      | ✅          | ✅         |                                        |
| Test `auto_pm help` command displays usage instructions.                                         | ✅          | ✅         |                                        |
| Test CLI argument parsing and invalid command handling.                                          | ✅          | ✅         |                                        |
| Test `setup` command with all required JSON input files present and valid.                       | ✅          | ✅         |                                        |
| Test `setup` command with missing input files and verify appropriate warnings.                   | ✅          | ✅         |                                        |
| Test `setup` command with invalid JSON files and verify error messages.                          | ✅          | ✅         |                                        |
| Test `start` command behavior with valid and invalid inputs.                                    | ✅          | ✅         |                                        |
| Test handling of empty input directory.                                                          | ✅          | ✅         |                                        |
| Test full workflow: install -> setup -> start -> status.                                         | ✅          | ✅         |                                        |
| Verify reports and outputs generated correctly.                                                 | ✅          | ✅         |                                        |
| Test data flow and interaction between modules.                                                 | ✅          | ✅         |                                        |
| Test behavior when input files are updated between runs.                                        | ✅          | ✅         |                                        |
| Test behavior with corrupted or malformed input files.                                          | ✅          | ✅         |                                        |
| Test unexpected user inputs during interactive setup.                                           | ✅          | ✅         |                                        |
| Test system resource limits and error recovery.                                                | ⬜          | ⬜         |                                        |
| Test concurrent runs and file access conflicts.                                                | ⬜          | ⬜         |                                        |
| Test performance with large input files.                                                       | ✅          | ✅         |                                        |
| Test memory and CPU usage under load.                                                          | ✅          | ✅         |                                        |
| Test responsiveness of CLI commands.                                                           | ✅          | ✅         |                                        |
| Test file permission errors and handling.                                                      | ✅          | ✅         |                                        |
| Test secure handling of sensitive data (e.g., secret keys).                                    | ✅          | ✅         |                                        |
| Verify no sensitive data is logged or exposed.                                                 | ⬜          | ⬜         |                                        |
| Verify `auto_pm help` command displays accurate and complete information.                      | ✅          | ✅         |                                        |
| Verify README and HELP.md files are up to date and clear.                                      | ✅          | ✅         |                                        |
| Test links and references in documentation.                                                    | ✅          | ✅         |                                        |
| Verify integrated terminal opens with correct shell on Linux.                                  | ✅          | ✅         |                                        |
| Verify integrated terminal opens with correct shell on macOS.                                 | ✅          | ✅         |                                        |
| Verify integrated terminal opens with correct shell on Windows.                               | ✅          | ✅         |                                        |
| Verify "Shell Integration Unavailable" issue is resolved.                                     | ✅          | ✅         |                                        |
| Verify command outputs are visible in the terminal.                                           | ✅          | ✅         |                                        |
| Verify VSCode reload and terminal restart apply the shell settings correctly.                 | ✅          | ✅         |                                        |

## New Tests for Virtual Environment and .gitignore Handling

| Test Description                                                                                     | Initial Run | Latest Run | Notes                                  |
|---------------------------------------------------------------------------------------------------|-------------|------------|----------------------------------------|
| Verify .gitignore file is created if it does not exist before virtual environment creation.       | ⬜          | ⬜         | Implemented: Added setup_env.sh script to create venv and manage .gitignore |
| Verify .gitignore file is updated to include virtual environment directories before creation.     | ⬜          | ⬜         | Implemented: Added setup_env.sh script to create venv and manage .gitignore |
| Verify virtual environment directories (e.g., venv/, .venv/) are excluded from git tracking.      | ⬜          | ⬜         | Implemented: Added setup_env.sh script to create venv and manage .gitignore |
| Verify virtual environment is created only after .gitignore is ensured.                           | ⬜          | ⬜         | Implemented: Added setup_env.sh script to create venv and manage .gitignore |

---

This checklist should be used to systematically verify the package functionality and robustness before release.

## 9. Shell Integration and Terminal Tests
- ✅ Verify integrated terminal opens with correct shell on Linux.
- ✅ Verify integrated terminal opens with correct shell on macOS.
- ✅ Verify integrated terminal opens with correct shell on Windows.
- ✅ Verify "Shell Integration Unavailable" issue is resolved.
- ✅ Verify command outputs are visible in the terminal.
- ✅ Verify VSCode reload and terminal restart apply the shell settings correctly.
