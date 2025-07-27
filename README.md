# ProjectManagement

ProjectManagement is a comprehensive Python-based project management system designed to help teams and individuals efficiently plan, track, and manage their projects. This package provides tools for task management, progress tracking, resource allocation, reporting, and automation to streamline project workflows.

## Features

- Task and workflow management with detailed tracking
- Progress calculation and reporting dashboards
- Resource allocation and leveling tools
- Integration with version control for commit tracking
- Automated task prioritization based on importance and urgency
- Extensive documentation and modular design for easy customization

## Installation and Quick Start

To simplify installation and running the ProjectManagement system on any supported operating system, you can use the provided setup script which automates all prerequisites installation and launches the system with a single command.

### Prerequisites

- Python 3.7 or higher installed
- Node.js and npm installed (Node.js is required for frontend dependencies and running the frontend server)
- Git installed (required for cloning the repository if not already done)

### Single Command Setup and Run

Run the following command in your terminal to automatically install all dependencies, start the backend and frontend servers, and open the web interface in your default browser:

```bash
./setup_and_run.sh
```

> **Note for Windows users:**  
> The script uses Unix shell commands. You can run it in a Git Bash terminal or Windows Subsystem for Linux (WSL). Alternatively, you may need to adapt the script for Windows command prompt or PowerShell.

### How the system installation and startup process works

When you run the `./setup_and_run.sh` script, the system will perform the following steps automatically:

1. Clone the ProjectManagement repository if not already present.
2. Create a Python virtual environment and activate it.
3. Install all required Python dependencies from `requirements.txt`.
4. Navigate to the frontend directory and install all Node.js dependencies using npm.
5. Start the backend server using Uvicorn in the background.
6. Start the frontend development server in the background.
7. Open the default web browser and navigate to the local web interface at `http://localhost:3000`.
8. Wait for the backend and frontend servers to run, allowing you to interact with the system through the web interface.

### After running the script

Once the script completes, your system will be running and accessible via the web interface at:

```
http://localhost:3000
```

Use the web interface to manage your projects, add tasks, track progress, allocate resources, and generate reports through an intuitive graphical interface.

For advanced usage and CLI commands, refer to the documentation in the `Docs/` and `project_management/docs/` directories.

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
