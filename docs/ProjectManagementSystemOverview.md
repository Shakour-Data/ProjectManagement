# Project Management System Overview

## Introduction

This Project Management System is a fully automated, Python-based tool designed to serve as the "brain" of any software project. It manages the entire project lifecycle from an empty project folder, transforming creative user inputs into formal tasks, tracking progress, managing resources, and generating reports and dashboards. The system integrates deeply with GitHub and Visual Studio Code (VS Code) to provide seamless automation and real-time project management.

---

## Foundational Workflow

### Starting a New Project

- Every software project begins with an empty folder created by the user.
- The project management package is installed into this folder.
- The user provides essential input data to enable the system to function effectively.

### Critical Inputs

1. **Project Start Date**
   - Defines the official start of the project timeline.

2. **Work Breakdown Structure (WBS) JSON**
   - A 6-level hierarchical JSON structure defining all project tasks.
   - The first 3 levels are common across software projects.
   - The last 3 levels are project-specific, detailing tasks down to the product level.
   - The lowest level (level 6) contains actionable tasks.

3. **Human Resources JSON**
   - Defines the human resources available for the project, including roles and attributes.

4. **Resource Allocation JSON**
   - Assigns resources specifically to level 6 WBS activities.
   - Resource leveling is performed to optimize resource usage and task scheduling.

---

## Processing Workflow

### Input Handling

- The system reads and validates all input JSON files.
- Ensures the WBS is properly structured to 6 levels.
- Loads human resources and resource allocation data.

### Task and Resource Management

- Parses the WBS and resource data to build an internal task and resource model.
- Performs resource leveling based on dependencies and allocations.
- Calculates task start and end dates accordingly.

### Progress Tracking

- Integrates with Git to analyze commit history.
- Maps commits to tasks using commit messages and file changes.
- Calculates progress based on commit data and workflow stage completion.
- Computes dynamic importance and urgency scores for tasks based on deadlines, dependencies, and priorities.

### Automation and Integration

- Automates Git commit and push operations with meaningful commit messages.
- Synchronizes task statuses with GitHub Issues and Project boards.
- Provides an interactive VS Code chat interface for natural language task management.
- Generates daily updated reports, changelogs, decision logs, and visual dashboards.

---

## Outputs

### JSON Files

- **commit_task_database.json**
  - Maps Git commits to tasks with detailed metadata.
  - Used for audit trails, progress tracking, and reporting.

- **commit_progress.json**
  - Summarizes progress ratios per task group.
  - Used by progress calculators and reporting modules.

- **Other JSON files**
  - Include enriched WBS data, resource allocations, workflow definitions, and scoring data.

### Reports and Dashboards

- Markdown reports on task progress, priority, and urgency.
- Visual dashboards accessible within VS Code and GitHub.
- Archived historical reports for tracking project evolution.

### Git Commits

- Automated commits with conventional commit messages linked to tasks.
- Pushes to remote repositories to maintain synchronization.

---

## Integration with Workflow and Tools

- Workflow stages are defined with weights to measure progress accurately.
- The system supports multiple project management methodologies including PMBOK, Scrum, and Kanban.
- Deep integration with GitHub APIs for issues, pull requests, and project boards.
- VS Code extension provides an interactive chat interface and real-time dashboards.

---

## Documentation and Maintenance

- Input JSON files must conform to defined standards for structure and content.
- The system includes validation and error handling for inputs.
- Comprehensive documentation is maintained and regularly updated.
- Backup and recovery mechanisms ensure data integrity and continuity.

---

## References

For detailed information on specific components, please refer to:

- [Detailed Work Breakdown Structure (WBS)](project_management/detailed_wbs.md)
- [Priority, Urgency, and Eisenhower Matrix Instructions](project_management/importance_urgency_priority_instructions.md)
- [Task Resource Allocation](project_management/task_resource_allocation.md)
- [JSON Files Overview and Standards](json_standards/json_files_overview.md)
- [Detailed Workflow Definitions](json_standards/workflow_definition_detailed.md)
- [Auto Commit Process](docs/json_standards/auto_commit_process.md)

---

## Summary

This Project Management System provides a powerful, automated framework to manage software projects from inception to completion. By leveraging structured inputs, automated processing, and seamless integration with development tools, it enables efficient project tracking, resource management, and reporting, serving as the central "brain" of any software project.
