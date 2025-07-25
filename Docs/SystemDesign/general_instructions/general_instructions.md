General Instructions



# General Instructions for Building the Project Management Tool

## Overview

This document provides comprehensive instructions for building, setting up, and using the Project Management Tool. The tool is a sophisticated, Python-based system designed to autonomously manage software projects with deep integration into GitHub and seamless interaction through Visual Studio Code (VS Code). It automates nearly all aspects of project management, enabling users to focus on creative and critical work while minimizing manual overhead.

---

## Technology Stack and Architecture

* **Backend Framework:** Flask (Python) for RESTful APIs handling GitHub integration, task management, automation workflows, and VS Code communication.
* **Core Logic:** Python implements core functionalities including parsing user inputs, task prioritization, scheduling, dependency management, documentation handling, progress tracking, and workflow automation.
* **GitHub Integration:** Uses GitHub API for Issues, Projects, Pull Requests, Wikis, and Actions. GitHub Actions power CI/CD, scheduled tasks, and notifications.
* **VS Code Integration:** VS Code Extension API provides an interactive chat interface. Essential extensions like BLACKBOX AI are installed automatically.
* **Data Storage:** Local project files and GitHub repositories serve as primary data stores. Configuration files and secure encrypted storage manage GitHub tokens and project state.
* **Testing:** Unit, integration, API endpoint, and end-to-end testing ensure code quality and reliability.
* **Reporting:** Automated markdown and text-based reports, real-time dashboards integrated into VS Code and GitHub Projects.
* **Security:** Secure handling and encrypted storage of authentication tokens, role-based access control, and compliance with GitHub API rate limits.
* **Extensibility:** Plugin architecture allows adding new features and integrations. Automated backups and recovery mechanisms ensure data integrity.

---

## Installation and Setup

1. Install the tool as a Python package/library.
2. The installation automatically creates a Python virtual environment and installs all dependencies.
3. Essential VS Code extensions (e.g., BLACKBOX AI) are installed automatically.
4. Initial setup securely stores GitHub tokens and initializes project state.
5. Users start interacting immediately via the VS Code chat interface without complex configuration.

---

## Usage Workflow

* Provide creative inputs such as text descriptions, code snippets, or images in a natural, unstructured manner.
* The tool converts these inputs into formal tasks with prioritization, scheduling, and dependency management.
* Task statuses synchronize with GitHub Issues and Project boards, linking tasks to Pull Requests and updating statuses based on PR reviews and merges.
* Automates coding, testing, documentation, and progress tracking workflows.
* Provides daily updated reports and real-time dashboards accessible within VS Code and GitHub.
* Sends notifications for stalled tasks, upcoming deadlines, and required reviews.

---

## Work Breakdown Structure (WBS)

* The WBS is a hierarchical decomposition of the project into manageable tasks.
* Tasks have attributes such as id, title, description, deadline, dependencies, assigned users, status, priority, and parent\_id.
* The tool supports automated WBS generation from creative inputs using AI-assisted parsing.
* WBS tasks can have multiple levels of subtasks enabling deep hierarchical breakdowns.
* WBS is used for task assignment, scheduling, and progress tracking.
* WBS can be converted to JSON format for programmatic use, including milestones, dependencies, and time estimates.

---

## Resource Management and Allocation

* Resources (e.g., human resources) are assigned to project tasks using a standardized process.
* Resource management includes Resource, Task, and Resource Allocation entities supporting many-to-many relationships, managed directly via JSON files without a database.
* Resource allocation JSON files link resources to tasks with allocation percentages, roles, and optional start/end dates.
* Best practices include ensuring resource availability, documenting roles, regularly updating allocations, and following PMBOK and PRINCE2 standards.
* Resource allocation integrates with project workflows and supports automated synchronization and reporting.

---

## JSON Resource File Design and Usage

* JSON resource files are structured for direct use by the project management tool for automation.
* Each JSON object corresponds to a project entity with keys matching attribute names.
* Supported data types include strings, integers, floats, booleans, and dates in ISO 8601 format.
* Hierarchical data should be represented using parent-child relationships via IDs.
* JSON files must be validated against schemas before use.
* Maintain version control and schedule regular synchronization.
* Follow best practices for formatting, naming conventions, and documentation.

---

## Progress Tracking and Reporting

* Project progress is calculated by combining commit-based and workflow-based metrics.
* Commit-based progress analyzes Git commit history and parses commit messages for task IDs.
* Workflow-based progress considers completion of defined workflow steps (e.g., coding, testing, documentation).
* Progress is averaged from both metrics and updated regularly.
* Best practices include consistent commit message formats, regular status updates, and automated synchronization with dashboards.

---

## Resource File Management Best Practices

* Store resource files in dedicated directories (e.g., `docs/resources/` or `config/resources/`).
* Use clear, descriptive, and standardized filenames.
* Maintain consistent file structures and naming conventions.
* Validate JSON syntax and schema compliance using automated tools.
* Use markdown format for human-readable text files.
* Automate updates and synchronization with project data.
* Include resource file validation in CI/CD pipelines.
* Align resource files with recognized project management standards.

---

## Security, Backup, and Extensibility

* Securely handle and encrypt GitHub authentication tokens.
* Implement role-based access control for multi-user projects.
* Comply with GitHub API rate limits and best practices.
* Automated backups of project state, documentation, and configuration files.
* Robust recovery mechanisms to handle data loss or corruption.
* Plugin and extension system to add new features or integrate external tools.
* Extensive use of GitHub Actions and internal bots for automation.

---

## Summary

This document provides detailed, standardized instructions for building and managing the Project Management Tool. Following these guidelines ensures efficient automation, reliable project control, and seamless collaboration. The tool leverages modern technologies and best practices to maximize productivity and minimize manual overhead, enabling users to focus on creative and critical work.

For further assistance, please contact the project management office.

---