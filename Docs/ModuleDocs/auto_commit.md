# AutoCommit Module

## Overview
The `auto_commit` module provides the `AutoCommit` class which automates git operations such as detecting changes, grouping related files, generating commit messages, backing up user input JSON files, committing changes, and pushing them to a remote repository. It is designed to streamline the commit process with detailed commit messages and progress tracking.

## Class: AutoCommit

### Description
The `AutoCommit` class encapsulates methods to interact with git, manage backups, generate commit messages following conventional commit styles, and update commit progress databases.

### Methods

- `__init__(self)`
  - Initializes the `AutoCommit` instance and sets up a `BackupManager`.

- `run_git_command(self, args, cwd=None)`
  - Runs a git command with the specified arguments.
  - Parameters:
    - `args` (list): List of git command arguments.
    - `cwd` (str, optional): Directory to run the command in.
  - Returns: Tuple `(success: bool, output: str)`.

- `get_git_changes(self)`
  - Fetches the current git status and returns a list of changes.
  - Returns: List of changed files with status codes.

- `group_related_files(self, changes)`
  - Groups files based on their top-level directory.
  - Parameters:
    - `changes` (list): List of git status lines.
  - Returns: Dictionary mapping top-level directories to lists of file changes.

- `categorize_files(self, files)`
  - Categorizes files into change types such as Added, Modified, Deleted, etc.
  - Parameters:
    - `files` (list): List of tuples `(status, file)`.
  - Returns: Dictionary mapping change categories to lists of files.

- `get_file_diff_summary(self, file_path)`
  - Retrieves a short summary of the staged diff for a file.
  - Parameters:
    - `file_path` (str): Path to the file.
  - Returns: String summary of the diff.

- `generate_commit_message(self, group_name, category_name, files)`
  - Generates a conventional commit style message with emojis.
  - Parameters:
    - `group_name` (str): Group or directory name.
    - `category_name` (str): Change category.
    - `files` (list): List of file paths.
  - Returns: Commit message string.

- `load_linked_wbs_resources(self, filepath)`
  - Loads linked WBS resources from a JSON file.
  - Parameters:
    - `filepath` (str): Path to the JSON file.
  - Returns: Parsed JSON data.

- `find_task_by_file_path(self, linked_wbs, file_path)`
  - Finds the task corresponding to a file path in linked WBS resources.
  - Parameters:
    - `linked_wbs` (list): List of tasks.
    - `file_path` (str): File path to search for.
  - Returns: Task dictionary or None.

- `backup(self)`
  - Runs backup of user input JSON files before committing.

- `commit_and_push(self)`
  - Stages, commits, and pushes changes to the remote repository.
  - Updates commit progress and task databases.

## Usage
The module can be run as a script to perform backup and commit operations automatically:

```python
if __name__ == "__main__":
    auto_commit = AutoCommit()
    auto_commit.backup()
    auto_commit.commit_and_push()
```

---

This documentation provides a detailed overview of the `auto_commit` module to assist developers in understanding and using its functionality effectively.
