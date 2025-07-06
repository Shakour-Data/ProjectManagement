# Instructions for Converting Project WBS to JSON Format

This document provides a step-by-step guideline to convert a project's Work Breakdown Structure (WBS) into a structured JSON format suitable for programmatic use and project management.

---

## Overview

The goal is to represent the hierarchical WBS in JSON, including task IDs, titles, subtasks, time estimates, and dependencies, following CPM (Critical Path Method) rules.

---

## Step-by-Step Instructions

### 1. Prepare the WBS Content

- Start with a detailed WBS document outlining all project tasks.
- Ensure the WBS is hierarchical, with clear levels and lowest-level tasks defined.
- Each task should have a unique ID and a descriptive title.

### 2. Define the JSON Structure

- Represent the WBS as a JSON array of top-level tasks.
- Each task object should include:
  - `id`: Unique identifier (string or number).
  - `title`: Task name.
  - `subtasks`: Array of child tasks (empty if none).
  - For lowest-level tasks only:
    - `optimistic_hours`: Estimated optimistic duration.
    - `normal_hours`: Estimated normal duration.
    - `pessimistic_hours`: Estimated pessimistic duration.
    - `predecessors`: Array of task IDs that are prerequisites.

### 3. Add Milestone Tasks

- Add two milestone tasks:
  - **Start** task with ID `"0"` and zero duration.
  - **End** task with ID `"99"` and zero duration.
- These milestones represent the project start and end points.

### 4. Assign Dependencies

- For each lowest-level task:
  - If it has no predecessors, set its `predecessors` to include the `"0"` (Start) task.
  - If it is not a predecessor of any other task, it should be considered to precede the `"99"` (End) task.
- Dependencies can be across different branches or within the same branch at the lowest level.

### 5. Time Estimation

- Provide three time estimates for each lowest-level task:
  - `optimistic_hours`: Best-case scenario.
  - `normal_hours`: Most likely scenario.
  - `pessimistic_hours`: Worst-case scenario.
- Leave these fields empty or omit them for higher-level tasks; their durations will be calculated from subtasks.

### 6. Maintain and Update

- Keep the JSON file updated as the project evolves.
- Use this JSON as the authoritative source for project scheduling, tracking, and reporting.

---

## Example JSON Snippet

```json
{
  "id": "1.1.1",
  "title": "Create Python package structure",
  "optimistic_hours": 2,
  "normal_hours": 4,
  "pessimistic_hours": 6,
  "predecessors": ["0"],
  "subtasks": []
}
```

---

## Summary

Following this guideline ensures consistent, clear, and machine-readable project WBS representations, facilitating automation, dependency management, and accurate project planning.

For any questions or assistance, please contact the project management team.

---

*Note: This document is recommended to be stored in the main project documentation directory to be accessible for all projects.*
