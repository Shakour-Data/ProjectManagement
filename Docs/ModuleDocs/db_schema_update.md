# db_schema_update Module

## Overview
The `db_schema_update` module provides functionality to update the SQLite database schema by creating new tables as needed. Currently, it includes a function to create a `task_schedule` table for managing task schedules with resource assignments and start/end dates.

## Functions

- `create_task_schedule_table(db_path)`
  - Connects to the SQLite database at the specified path and creates the `task_schedule` table if it does not exist.
  - The `task_schedule` table schema includes:
    - `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
    - `task_id` (INTEGER NOT NULL, foreign key referencing `tasks` table)
    - `resource_id` (TEXT NOT NULL)
    - `start_date` (TEXT NOT NULL)
    - `end_date` (TEXT NOT NULL)
  - Parameters:
    - `db_path` (str): Path to the SQLite database file.

## Usage
Run the module as a script to create the `task_schedule` table:

```python
if __name__ == '__main__':
    db_path = 'projects/current_project/docs/project_management.db'
    create_task_schedule_table(db_path)
```

---

This documentation provides an overview of the `db_schema_update` module to assist developers in managing database schema updates.
