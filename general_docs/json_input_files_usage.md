# JSON Input Files and Their Usage in the Project Management System

## Introduction

This document provides a comprehensive and detailed description of the JSON input files used by the Project Management System. It explains the structure, purpose, and usage of each JSON file, along with examples and diagrams to facilitate understanding and effective use.

---

## Overview of JSON Input Files

The system uses JSON files as the primary data source for managing tasks, resources, progress, and workflows. These files are now organized into a unified folder structure under `PM_JSON/` with two subfolders:

### Data Sources and Categorization

1. **User Input JSON Files**
   - Located in the `PM_JSON/user_inputs/` directory.
   - These files are provided or edited by users to define project tasks, resources, workflows, and planning data.
   - Files:
     - `detailed_wbs.json`
     - `human_resources.json`
     - `resource_allocation.json`
     - `task_resource_allocation.json`
     - `workflow_definition.json`
     - `wbs_data.json`

2. **System-Generated JSON Files**
   - Located in the `PM_JSON/system_outputs/` directory.
   - These files are generated or updated by the system during project execution and tracking.
   - Files:
     - `commit_progress.json`
     - `commit_task_database.json`
     - `wbs_scores.json`

---

## List of Key JSON Input Files

| File Name                      | Location                     | Data Source Category               | Description                                                                                  |
|-------------------------------|------------------------------|----------------------------------|----------------------------------------------------------------------------------------------|
| `commit_progress.json`         | `PM_Input/ and docs/db_json/`| Commit Data                      | Tracks progress data related to commits and tasks.                                          |
| `commit_task_database.json`    | `PM_Input/ and docs/db_json/`| Commit Data                      | Contains task-related data linked to commits.                                               |
| `wbs_data.json`                | `PM_Input/ and docs/db_json/`| Project Definition and Planning  | Defines the Work Breakdown Structure (WBS) with tasks, hierarchy, and relationships.        |
| `wbs_scores.json`              | `PM_Input/ and docs/db_json/`| Project Definition and Planning  | Contains importance and urgency scores for tasks to aid prioritization.                      |
| `human_resources.json`         | `PM_Input/ and docs/db_json/`| Project Definition and Planning  | Details human resources involved in the project.                                            |
| `resource_allocation.json`     | `PM_Input/ and docs/db_json/`| Project Definition and Planning  | Contains data about resource allocation to tasks or projects.                               |
| `task_resource_allocation.json`| `PM_Input/ and docs/db_json/`| Project Definition and Planning  | Maps tasks to resource allocations in detail.                                               |
| `workflow_definition.json`     | `PM_Input/ and docs/db_json/`| Project Definition and Planning  | Defines workflows and steps for task completion and progress tracking.                      |

---

## JSON Schema and Structure

### General Principles

- Each JSON file contains an array of objects representing entities such as tasks, resources, or workflow steps.
- Attributes use consistent and descriptive key names.
- Data types include strings, integers, floats, booleans, and arrays.
- Hierarchical relationships are represented using parent-child references via IDs.

### Example: Task Object Schema

```json
{
  "id": "1.1",
  "title": "Create Python package structure",
  "description": "Set up the initial package layout",
  "level": 2,
  "importance": 0.8,
  "urgency": 0.6,
  "status": "Not Started",
  "progress": 0.0,
  "parent_id": "1",
  "subtasks": []
}
```

### Hierarchical Relationships

Tasks are organized hierarchically using the `parent_id` field to reference the parent task. This allows representing complex project structures with multiple levels.

---

## Detailed Description of Key JSON Files

### 1. `wbs_data.json`

- Contains the Work Breakdown Structure (WBS) tasks.
- Each task has an `id`, `title`, `level`, optional `description`, and `subtasks`.
- Example snippet:

```json
[
  {
    "id": "1",
    "title": "Project Setup",
    "level": 1,
    "subtasks": [
      {
        "id": "1.1",
        "title": "Create Python package structure",
        "level": 2,
        "subtasks": []
      }
    ]
  }
]
```

### 2. `wbs_scores.json`

- Contains importance and urgency scores for each task by `id`.
- Used for dynamic prioritization.
- Example snippet:

```json
{
  "1.1": {
    "importance": 0.8,
    "urgency": 0.6
  }
}
```

### 3. `human_resources.json`

- Lists human resources with attributes such as name, role, availability.
- Example snippet:

```json
[
  {
    "id": "hr1",
    "name": "Alice",
    "role": "Developer",
    "availability": 1.0
  }
]
```

### 4. `resource_allocation.json` and `task_resource_allocation.json`

- Define how resources are allocated to tasks.
- Include allocation percentages and roles.
- Example snippet:

```json
[
  {
    "task_id": "1.1",
    "resource_id": "hr1",
    "allocation": 0.5
  }
]
```

### 5. `workflow_definition.json`

- Defines the ordered steps in workflows.
- Used to track task progress through stages.
- Example snippet:

```json
[
  "To Do",
  "In Progress",
  "Code Review",
  "Done"
]
```

---

## Diagrams

### Task Hierarchy Diagram

```
Project Setup (id: 1)
├── Create Python package structure (id: 1.1)
├── Implement virtual environment (id: 1.2)
└── Automate configuration setup (id: 1.3)
```

### Resource Allocation Flow

```
[Human Resources] --> [Resource Allocation JSON] --> [Tasks]
```

---

## Best Practices

- Keep JSON files well-formatted and human-readable.
- Use consistent naming conventions.
- Validate JSON files against schemas before use.
- Maintain version control for JSON files.
- Handle missing or optional fields gracefully.
- Use parent-child references for hierarchical data instead of deep nesting.

---

## Summary

This document details the JSON input files used by the Project Management System, their structure, and usage. The system operates directly on these JSON files without a database, enabling flexible and dynamic project management workflows.

For further assistance, please contact the project management office.

---
