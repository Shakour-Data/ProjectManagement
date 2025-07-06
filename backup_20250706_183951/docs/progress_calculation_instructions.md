# Instructions for Calculating Project Progress

This document outlines the methodology and guidelines for calculating project progress in the Project Management Tool. The progress calculation considers both commit history and workflow step completion to provide an accurate and comprehensive measure of task and project status.

---

## Overview

Project progress is calculated by combining two key factors:

1. **Commit-Based Progress:**
   - Analyzes the Git commit history to identify commits related to specific tasks.
   - Parses commit messages to extract task identifiers.
   - Counts commits per task and normalizes the count to a 0-100% progress scale.
   - Reflects the actual development activity and code changes made for each task.

2. **Workflow-Based Progress:**
   - Considers the position of tasks within the defined project workflow.
   - Each task must complete a series of workflow steps (e.g., Coding, Testing, Documentation, Code Review, Merge and Deployment, Verification).
   - Progress is calculated based on the number of completed workflow steps relative to the total steps.
   - Ensures that tasks are not only coded but also properly tested, documented, reviewed, and deployed.

---

## Data Sources

- **Git Commit History:**
  - Retrieved using `git log` commands.
  - Commit messages are parsed to identify task IDs.

- **Workflow Definition:**
  - Stored in a JSON file (`workflow_definition.json`).
  - Defines the ordered list of workflow steps each task must complete.

---

## Calculation Methodology

1. **Extract Commit Data:**
   - Run Git commands to obtain commit hashes, messages, and affected files.
   - Parse commit messages to find task IDs using regular expressions.

2. **Calculate Commit-Based Progress:**
   - Count the number of commits per task.
   - Normalize counts to a percentage scale based on the maximum commits for any task.

3. **Calculate Workflow-Based Progress:**
   - Load the workflow definition JSON.
   - For each task, determine which workflow steps have been completed.
   - Calculate progress as the ratio of completed steps to total steps.

4. **Combine Progress Metrics:**
   - Average the commit-based and workflow-based progress percentages.
   - Optionally, apply different weights to each metric based on project needs.

---

## Implementation Notes

- The current implementation assumes equal weighting for all workflow steps.
- Workflow step completion tracking requires integration with task management and status update systems.
- The progress calculation script (`progress_data_generator.py`) can be extended to incorporate real-time workflow step completion data.
- Ensure that commit messages consistently reference task IDs to maintain accurate progress tracking.

---

## Best Practices

- Maintain clear and consistent commit message formats including task identifiers.
- Regularly update task statuses to reflect workflow step completions.
- Use automated tools and scripts to synchronize workflow progress with project management dashboards.
- Review and validate progress calculations periodically to ensure accuracy.

---

## Summary

Combining commit history with workflow step completion provides a holistic view of project progress, enabling better tracking, reporting, and decision-making. Adhering to these instructions ensures consistent and reliable progress measurement across projects.

For questions or assistance, please contact the project management office.

---
