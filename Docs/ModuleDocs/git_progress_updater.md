# GitProgressUpdater Module

## Overview
The `git_progress_updater` module provides the `GitProgressUpdater` class which analyzes git commit logs to track task progress. It maps commits to tasks based on commit messages, calculates normalized progress percentages, and combines commit progress with workflow progress.

## Class: GitProgressUpdater

### Description
The `GitProgressUpdater` class processes git logs to extract commit information, associate commits with tasks using regex on commit messages, and calculate progress metrics for project tasks.

### Methods

- `__init__(self, workflow_definition: List[Dict[str, Any]])`
  - Initializes the updater with a workflow definition.

- `run_git_log(self) -> str`
  - Runs the `git log` command to retrieve commit hashes, messages, and changed files.
  - Returns: Raw git log text.

- `parse_git_log(self, log_text: str) -> List[Dict[str, Any]]`
  - Parses the raw git log text into a list of commit dictionaries containing hash, message, and files.

- `map_commits_to_tasks(self, commits: List[Dict[str, Any]]) -> Dict[str, float]`
  - Uses regex to extract task IDs from commit messages.
  - Counts commits per task and normalizes counts to a 0-100 scale.

- `calculate_workflow_progress(self) -> Dict[str, float]`
  - Placeholder method for workflow step completion tracking.

- `combine_progress(self, commit_progress: Dict[str, float], workflow_progress: Dict[str, float]) -> Dict[str, float]`
  - Combines commit progress and workflow progress by averaging values per task.

- `update_progress(self) -> Dict[str, float]`
  - Runs the full update process: runs git log, parses commits, maps commits to tasks, calculates workflow progress, and combines results.
  - Returns: Combined progress dictionary.

## Usage
Create an instance with a workflow definition and call `update_progress()` to get task progress data.

---

This documentation provides an overview of the `git_progress_updater` module to assist developers in tracking task progress from git commits.
