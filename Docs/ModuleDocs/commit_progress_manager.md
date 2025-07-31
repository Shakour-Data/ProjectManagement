# CommitProgressManager Module

## Overview
The `commit_progress_manager` module provides the `CommitProgressManager` class which manages commit progress tracking per task. It loads commit task data, calculates commit counts and progress percentages, and saves the progress data for use in project tracking.

## Class: CommitProgressManager

### Description
The `CommitProgressManager` class processes commit task data from a JSON database and generates progress metrics for each task based on commit activity.

### Methods

- `__init__(self, commit_task_db_path='project_inputs/PM_JSON/system_outputs/commit_task_database.json', commit_progress_path='project_inputs/PM_JSON/system_outputs/commit_progress.json')`
  - Initializes the manager with paths to the commit task database and commit progress output files.

- `load_commit_task_db(self)`
  - Loads commit task data from the JSON database file.

- `generate_commit_progress(self)`
  - Calculates commit progress per task.
  - Algorithm:
    - For each task, counts the number of commits.
    - Tracks the last commit date.
    - Calculates progress percentage as `min(commit_count * 10, 100)`, capping progress at 100%.
  
- `save_commit_progress(self)`
  - Saves the generated commit progress data to the output JSON file.

- `run(self)`
  - Runs the full workflow: load data, generate progress, and save results.

## Usage
Run the module as a script to generate and save commit progress data:

```python
if __name__ == "__main__":
    manager = CommitProgressManager()
    manager.run()
```

---

This documentation provides a detailed overview of the `commit_progress_manager` module to assist developers in understanding and using commit progress tracking functionality.
