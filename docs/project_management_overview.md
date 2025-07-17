# Project Management Tool Overview

## Introduction

The Project Management Tool is a sophisticated, Python-based automation system designed to streamline and enhance software project management. It integrates deeply with GitHub and Visual Studio Code (VS Code) to provide a seamless, automated experience covering all phases of project management from planning to closure.

This document provides a comprehensive overview of the tool’s architecture, features, usage workflow, and best practices.

---

## Key Features

- **Automated Project Lifecycle Management:** Covers planning, execution, monitoring, and closure phases with minimal manual input.
- **GitHub Integration:** Synchronizes with GitHub Issues, Projects, Pull Requests, Wikis, and Actions for real-time project updates.
- **VS Code Chat Interface:** Interactive natural language interface within VS Code for easy task creation and management.
- **Task Management:** Intelligent parsing of creative inputs into formal tasks with prioritization, scheduling, dependencies, and status tracking.
- **Progress Tracking:** Combines commit history analysis and workflow step completion for accurate progress metrics.
- **Reporting and Dashboards:** Generates detailed reports, changelogs, decision logs, and visual dashboards accessible in VS Code and GitHub.
- **Resource Management:** Supports resource allocation, cost, risk, and quality management aligned with PMBOK standards.
- **Security:** Role-based access control and secure encrypted storage of GitHub authentication tokens.
- **Extensibility:** Plugin system for adding new features and integrations.
- **Backup and Recovery:** Automated backups and robust recovery mechanisms to ensure data integrity.

---

## Architecture and Technology Stack

- **Backend:** Python core logic handling input parsing, task management, progress calculation, and reporting.
- **CLI:** Command-line interface for installation, starting automation, and status checks.
- **GitHub API:** For issue tracking, project boards, pull requests, and CI/CD workflows.
- **VS Code Extension API:** Provides an interactive chat interface and integrates dashboards.
- **Data Storage:** JSON files for inputs and outputs, local project files, and GitHub repositories.
- **Testing:** Unit, integration, and end-to-end tests ensure reliability.
- **Security:** Encrypted token storage and API rate limit compliance.

---

## Installation and Setup

1. Install the tool as a Python package.
2. Automatic creation of a Python virtual environment and dependency installation.
3. Automatic installation of essential VS Code extensions (e.g., BLACKBOX AI).
4. Secure storage of GitHub tokens and project state initialization.
5. Immediate interaction via VS Code chat interface without complex configuration.

---

## Usage Workflow

- Users provide creative inputs (text, code snippets, images) in natural language.
- The tool converts inputs into formal tasks with attributes like priority, dependencies, and deadlines.
- Task statuses synchronize with GitHub Issues and Project boards.
- Automates coding, testing, documentation, and progress tracking.
- Generates daily updated reports and real-time dashboards.
- Sends notifications for stalled tasks, upcoming deadlines, and required reviews.

---

## Input Data and File Structure

- **PM_Input Directory:** Contains JSON files such as `detailed_wbs.json`, `workflow_definition.json`, `commit_progress.json`, and others.
- **Task Attributes:** Include id, title, description, deadline, dependencies, assigned users, status, priority, and progress.
- **Resource Allocation:** Managed via JSON files linking resources to tasks with allocation percentages and roles.

---

## Progress Calculation

- Combines commit-based progress (analyzing git commit messages) and workflow-based progress (completion of workflow steps).
- Calculates dynamic importance and urgency scores for tasks based on deadlines, dependencies, priority, and status.
- Enriches tasks with progress and scoring for prioritization and reporting.

---

## Reporting and Dashboards

- Generates reports on top important and urgent tasks.
- Categorizes tasks using the Eisenhower matrix.
- Saves reports and dashboards as markdown files in designated directories.
- Archives previous reports for historical tracking.

---

## Security and Backup

- Secure handling and encrypted storage of GitHub authentication tokens.
- Role-based access control for multi-user projects.
- Automated backups of project state and documentation.
- Recovery mechanisms to handle data loss or corruption.

---

## Extensibility

- Plugin architecture allows adding new features and integrations.
- Extensive use of GitHub Actions and internal bots for automation and notifications.

---

## Summary

This tool is a powerful, fully automated project management assistant that integrates deeply with GitHub and VS Code. It manages all phases of software projects, streamlining planning, execution, monitoring, and closure. Users simply start interacting via VS Code, and the tool handles the rest, providing powerful automation, real-time tracking, and flexible reporting to enhance productivity and collaboration.

---

For more detailed instructions on building, setup, and usage, please refer to the [General Instructions](general_instructions.md) document.
