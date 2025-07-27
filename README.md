# ProjectManagement

ProjectManagement is a comprehensive Python-based project management system designed to help teams and individuals efficiently plan, track, and manage their projects. This package provides tools for task management, progress tracking, resource allocation, reporting, and automation to streamline project workflows.

## Features

- Task and workflow management with detailed tracking
- Progress calculation and reporting dashboards
- Resource allocation and leveling tools
- Integration with version control for commit tracking
- Automated task prioritization based on importance and urgency
- Extensive documentation and modular design for easy customization

## Installation

1. Ensure you have Python 3.7 or higher installed.
2. Clone this repository:
   ```bash
   git clone <repository-url>
   ```
3. Navigate to the project root directory:
   ```bash
   cd ProjectManagement
   ```
4. For a quick setup, run the setup script to create a virtual environment and install dependencies:
   ```bash
   ./scripts/setup_env.sh
   ```
5. For a full interactive setup including input validation and guided human resources data entry, run:
   ```bash
   python scripts/setup_interactive.py
   ```
6. (Optional) Activate the virtual environment manually if needed:
   ```bash
   source venv/bin/activate
   ```
7. (Optional) Install the package:
   ```bash
   python project_management/setup.py install
   ```

## Usage

- Run the main project management system:
  ```bash
  python project_management/main.py
  ```
- Use the CLI commands available in `project_management/cli.py` for various project operations.
- Refer to the `project_management/modules` directory for modular components and scripts.
- Documentation files are available in the `Docs/` and `project_management/docs/` directories for detailed instructions and guides.

## Quick Start Example

To quickly start managing your project, after setup, run:
```bash
python project_management/main.py
```
Use the CLI commands to add tasks, track progress, and generate reports. Refer to the documentation for detailed command usage.

## Accessing the Local Web Interface

The ProjectManagement system includes a web-based interface for easier project management.

1. Start the local web server by running the frontend development server:
   ```bash
   cd frontend
   npm install
   npm start
   ```
2. Open your web browser and navigate to:
   ```
   http://localhost:3000
   ```
3. Use the web interface to quickly add tasks, track progress, allocate resources, and generate reports through an intuitive graphical interface.

For detailed usage instructions, refer to the `frontend/README.md` or the documentation in the `Docs/` directory.

## Documentation

The project documentation is organized into detailed design and management documents located primarily in the `Docs/SystemDesign/` directory:

- Document Creation Plan: `Docs/SystemDesign/01_DocumentCreationPlan.md` - Overview of the documentation structure and objectives.
- Project Features and Functional Specifications: `Docs/SystemDesign/02_project_features_and_functional_specifications.md` - Detailed software features and requirements.
- Implementation Plan: `Docs/SystemDesign/03_implementation_plan.md` - Phased development plan and milestones.
- Work Breakdown Structure and Project Management Overview: `Docs/SystemDesign/04_work_breakdown_structure_and_project_management_overview.md` - Task breakdown and management approach.
- Requirements Specification Document: `Docs/SystemDesign/05_requirements_specification_document.md` - Functional and non-functional requirements.
- System Design Document: `Docs/SystemDesign/06_system_design_document.md` - System architecture and components.
- Test Plan and Testing Instructions: `Docs/SystemDesign/07_test_plan_and_testing_instructions.md` - Testing strategies and instructions.
- Standard Operating Procedures and Help Documentation: `Docs/SystemDesign/08_standard_operating_procedures_and_help_documentation.md` - SOPs and user guides.
- Change Management and Versioning Plan: `Docs/SystemDesign/09_change_management_and_versioning_plan.md` - Change control and versioning.
- Communication, Risk Management, and Documentation Plan: `Docs/SystemDesign/10_communication_risk_management_and_documentation_plan.md` - Communication and risk protocols.
- Project Management Package Scenarios: `Docs/SystemDesign/11_project_management_package_scenarios.md` - Use case scenarios.
- Dashboards Overview: `Docs/SystemDesign/12_dashboards.md` - Reporting dashboards and metrics.
- Reports Overview: `Docs/SystemDesign/13_Reports.md` - Reporting mechanisms.
- Test Checklist and Testing Instructions: `Docs/SystemDesign/TEST_CHECKLIST.md`, `Docs/SystemDesign/TESTING_INSTRUCTIONS.md` - Testing checklists and instructions.
- Full Project Management Package Scenarios: `Docs/ProjectManagementPackage_FullScenarios.md`, `Docs/ProjectManagementPackage_FullScenarios_FA.md` - Comprehensive scenario documentation.

Additional documentation related to JSON standards and workflow definitions can be found in the `Docs/json_inputs_standard/` directory.

For detailed instructions and guides, also refer to the `project_management/general_docs/` and `project_management/docs/` directories.


## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Write tests for your changes.
4. Submit a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For questions or support, please open an issue on the repository.
