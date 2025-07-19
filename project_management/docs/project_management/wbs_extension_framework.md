# Framework for Extending WBS with User-Defined Levels

## Overview

This document provides guidelines and a template for users to extend the default Work Breakdown Structure (WBS) in software projects by adding three additional hierarchical levels specific to their project needs.

The default WBS covers levels 0 to 4, which are standardized for software projects. Users should add levels 5, 6, and 7 in their JSON files located in `project_inputs/PM_JSON/user_inputs/wbs_parts`.

---

## Default WBS Levels (0 to 4)

- **Level 0:** Software Project (root)
- **Level 1:** Major Phases (e.g., Requirements Analysis, Design, Implementation)
- **Level 2:** Sub-Phases (e.g., Gather Requirements, Architectural Design)
- **Level 3:** Activities (e.g., Identify Stakeholders, Define System Architecture)
- **Level 4:** Sub-Activities (e.g., Document Analysis, Module Design)

---

## User-Defined Levels (5 to 7)

Users should create JSON files in the `wbs_parts` directory that add the following levels:

- **Level 5:** Detailed Tasks  
  Example: "Conduct Stakeholder Interviews"

- **Level 6:** Sub-Tasks  
  Example: "Prepare Interview Questions"

- **Level 7:** Work Packages  
  Example: "Schedule Interview Sessions"

---

## JSON Structure Template

Each JSON file should follow this structure:

```json
{
  "id": "WBS-<level>-<unique_id>",
  "name": "<Task Name>",
  "description": "<Task Description>",
  "level_0": "Software Project",
  "level_1": "...",
  "level_2": "...",
  "level_3": "...",
  "level_4": "...",
  "level_5": "<User Defined Level 5>",
  "level_6": "<User Defined Level 6>",
  "level_7": "<User Defined Level 7>",
  "subtasks": [
    {
      "id": "WBS-<level>-<unique_id>",
      "name": "...",
      "description": "...",
      "level_5": "...",
      "level_6": "...",
      "level_7": "...",
      "subtasks": []
    }
  ]
}
```

---

## Merging Process

- The system automatically merges all JSON files in `wbs_parts` using the `wbs_merger.py` script.
- The merged output is saved as `detailed_wbs.json`.
- This process preserves the default levels and appends user-defined levels seamlessly.

---

## Workflow Definition

- Users define workflows only for the last user-defined level (level 7).
- Workflow JSON files should correspond to these detailed tasks and work packages.
- The system will dynamically generate or update `workflow_definition.json` based on these inputs.

---

## Best Practices

- Maintain consistent and unique IDs across all JSON files.
- Provide clear and descriptive names and descriptions for each task.
- Validate JSON files for correctness before merging.
- Use the provided `wbs_merger.py` script to automate merging.

---

This framework ensures flexibility for users to tailor the WBS to their specific project needs while maintaining a standardized core structure.
