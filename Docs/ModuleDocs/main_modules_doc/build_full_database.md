# build_full_database Module

## Overview
The `build_full_database` module provides functions to build and initialize a SQLite database for project management data. It handles creating tables, loading JSON data, inserting tasks, updating task scores, and initializing feature tables.

## Functions

- `connect_db()`
  - Connects to the SQLite database.
  - Returns: SQLite connection object.

- `drop_tables(conn)`
  - Drops existing tables if they exist.
  - Parameters:
    - `conn`: SQLite connection object.

- `create_tables(conn)`
  - Creates necessary tables for tasks, importance features, urgency features, task progress, and resource allocation.
  - Parameters:
    - `conn`: SQLite connection object.

- `load_json_file(path)`
  - Loads JSON data from a file.
  - Parameters:
    - `path` (str): Path to the JSON file.
  - Returns: Parsed JSON data.

- `insert_task(conn, task, parent_id=None)`
  - Inserts a task and its subtasks recursively into the database.
  - Parameters:
    - `conn`: SQLite connection object.
    - `task` (dict): Task data.
    - `parent_id` (str, optional): Parent task ID.

- `update_task_scores(conn, scores)`
  - Updates importance and urgency scores for tasks.
  - Parameters:
    - `conn`: SQLite connection object.
    - `scores` (dict): Scores data.

- `initialize_feature_tables(conn)`
  - Initializes importance and urgency feature tables with example data.
  - Parameters:
    - `conn`: SQLite connection object.

- `main()`
  - Orchestrates the database build process by connecting to the database, dropping and creating tables, loading data, inserting tasks, updating scores, and initializing features.
  - This function is executed when the module is run as a script.

## Usage
Run the module as a script to build and initialize the project management database:

```python
if __name__ == "__main__":
    main()
```

---

This documentation provides a detailed overview of the `build_full_database` module to assist developers in understanding and using its database initialization functionality.
