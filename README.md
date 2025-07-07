# ProjectManagement

## Overview

ProjectManagement is a comprehensive Python-based project management tool designed to automate and streamline software project workflows. It integrates deeply with GitHub and VS Code to provide real-time task tracking, progress calculation, resource allocation, and reporting. The tool supports JSON-based inputs for Work Breakdown Structure (WBS), tasks, resources, and workflow definitions, enabling flexible and extensible project control.

## Features

- Automated installation with virtual environment setup and dependency management.
- Deep GitHub integration: issues, projects, pull requests, and actions.
- Intelligent task management with dynamic importance and urgency scoring.
- Real-time progress tracking combining git commit history and workflow steps.
- Resource allocation and cost management dashboards.
- Automated report and dashboard generation with archiving.
- Role-based security and permissions.
- CLI commands for setup, status checks, and report generation.
- Extensible plugin architecture and VS Code extension support.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ProjectManagement
   ```

2. Install the package and dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python setup.py install
   ```

3. The installation script will automatically create the `PM_Input` folder for JSON inputs and set up necessary VS Code extensions.

## Usage

1. Place all project input JSON files (WBS, tasks, resources, workflow definitions) into the `PM_Input` folder.

2. Use the CLI or run the main script to initialize and start project management:
   ```bash
   python Project_Management/main.py
   ```

3. The tool will:
   - Parse inputs and git commit history.
   - Calculate task progress, importance, and urgency.
   - Generate and save dashboards and reports in the `project_test/reports` folder.
   - Archive previous reports automatically.

4. Use VS Code integration for chat-based task input and real-time updates.

## Project Structure

- `Project_Management/`: Main package containing modules and tests.
- `Project_Management/modules/`: Core modules for input handling, progress calculation, reporting, task management, etc.
- `Project_Management/tests/`: Automated tests for core functionalities.
- `project_test/`: Test project with sample JSON inputs and manual test scripts.
- `docs/`: Documentation files detailing features, instructions, and implementation plans.

## Testing

- Automated tests are located in `Project_Management/tests/`.
- Run tests using:
  ```bash
  python -m unittest discover Project_Management/tests
  ```
- Manual integration test script available at `project_test/run_project_management_test.py`.

## Contribution

Contributions are welcome! Please follow these guidelines:

- Fork the repository and create feature branches.
- Write clear, concise commit messages.
- Include tests for new features or bug fixes.
- Update documentation as needed.
- Submit pull requests for review.

## Support

For questions or assistance, please contact the project management office or open an issue on GitHub.

## License

This project is licensed under the MIT License.
