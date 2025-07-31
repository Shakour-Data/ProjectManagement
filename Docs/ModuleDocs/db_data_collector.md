# DBDataCollector Module

## Overview
The `db_data_collector` module provides the `DBDataCollector` class which collects and stores project management data into a SQLite database. It handles task data, resource allocation summaries, progress metrics, and feature weights.

## Class: DBDataCollector

### Description
The `DBDataCollector` class interacts with a database manager to insert and update project-related data including tasks, resource usage, and progress percentages.

### Methods

- `__init__(self, db_manager=None)`
  - Initializes the collector with a database manager instance and connects to the database.

- `collect_and_store_tasks(self, tasks)`
  - Collects task data including progress and resource allocation, and stores it in the database.
  - Parameters:
    - `tasks` (list): List of task objects.

- `collect_resource_allocation(self, tasks)`
  - Analyzes resource allocation from tasks and stores a summary in the database.
  - Parameters:
    - `tasks` (list): List of task objects.
  - Aggregates task counts per user and updates the `resource_allocation` table.

- `collect_progress_metrics(self, tasks)`
  - Collects progress percentages from tasks and stores or updates them in the database.
  - Parameters:
    - `tasks` (list): List of task objects.
  - Updates the `task_progress` table with task IDs and progress percentages.

- `insert_feature_weights(self, urgency_weights, importance_weights)`
  - Inserts predefined weights for urgency and importance features into the database.
  - Parameters:
    - `urgency_weights` (dict): Weights for urgency features.
    - `importance_weights` (dict): Weights for importance features.

- `close(self)`
  - Closes the database connection.

## Usage
Create an instance with a database manager and call methods to collect and store project data.

---

This documentation provides an overview of the `db_data_collector` module to assist developers in managing project data storage in the database.
