# BackupManager Module

## Overview
The `backup_manager` module provides the `BackupManager` class which manages backups of user input JSON files. It supports creating backups, listing existing backups, and restoring backups to the original location. This module helps ensure data safety by maintaining versioned backups.

## Class: BackupManager

### Description
The `BackupManager` class handles backup operations for user input data directories. It uses Python's `pathlib` and `shutil` modules to perform file system operations.

### Methods

- `__init__(self, source_dir: str = "project_management/data/PM_JSON/user_inputs", backup_base_dir: str = "project_management/PM_Backups/user_inputs_backup")`
  - Initializes the `BackupManager` with source and backup directories.
  - Parameters:
    - `source_dir` (str): Directory containing user input files to back up.
    - `backup_base_dir` (str): Directory where backups are stored.

- `create_backup(self)`
  - Creates a timestamped backup of the source directory.
  - Returns: Path to the created backup directory or `None` if failed.

- `list_backups(self)`
  - Lists existing backups sorted by newest first.
  - Returns: List of backup directory paths.

- `restore_backup(self, backup_dir: str)`
  - Restores a specified backup to the source directory.
  - Parameters:
    - `backup_dir` (str): Path to the backup directory to restore.
  - Returns: `True` if successful, `False` otherwise.

## Usage
The module can be run as a script to create a backup:

```python
if __name__ == "__main__":
    bm = BackupManager()
    print("Creating backup...")
    bm.create_backup()
```

---

This documentation provides a clear overview of the `backup_manager` module to assist developers in managing backups effectively.
