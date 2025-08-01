# Unit Tests

This directory contains unit test code for the ProjectManagement system.

Unit tests verify the smallest testable parts of the software in isolation, such as functions, methods, or classes.

Please organize your unit test scripts here.

---

## Overview

Unit tests are designed to verify the correctness of individual components in isolation. This includes functions, methods, and classes within the backend modules.

---

## Organization

- Test files are organized to mirror the source code structure:
  - `test_main_modules/` for tests related to `project_management.modules.main_modules`
  - `test_services/` for tests related to `project_management.modules.services`

---

## Running Tests

- Use `pytest` or `unittest` to run tests.
- Ensure the `PYTHONPATH` includes the `project_management` directory.
- Example command:

```bash
PYTHONPATH=project_management pytest Tests/TestingCode/UnitTests/
```

---

## Updating Test Documentation

- After running tests and fixing issues, update `DETAILED_TEST_PLAN.md` and this README to reflect current test coverage and status.
PYTHONPATH=project_management pytest Tests/TestingCode/UnitTests/
