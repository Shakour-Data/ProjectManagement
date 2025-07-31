# DashboardReports Module

## Overview
The `dashboards_reports` module provides the `DashboardReports` class which generates various project management reports in markdown format. It loads project input data, enriches tasks with progress information, and produces reports on progress, priority and urgency, resource allocation, cost management, and risk/issue tracking.

## Class: DashboardReports

### Description
The `DashboardReports` class loads input JSON files related to project tasks, resources, and workflow, and uses the `ProgressCalculator` to enrich task data with progress metrics. It provides methods to generate detailed markdown reports for project monitoring and decision-making.

### Methods

- `__init__(self, input_dir: str = 'SystemInputs/user_inputs')`
  - Initializes the class with the input directory path and creates a `ProgressCalculator` instance.

- `load_json_file(self, filename: str) -> Optional[Any]`
  - Loads a JSON file from the input directory or a fixed path for specific files.
  - Returns parsed JSON data or `None` on error.

- `load_inputs(self)`
  - Loads all required input JSON files and enriches tasks with progress data.

- `_format_task(self, task: Dict[str, Any]) -> str`
  - Formats a task's details into a markdown string including title, status, importance, urgency, score, and progress percentage.
  - Calculates a weighted score: `score = (importance * 0.6) + (urgency * 0.4)`.

- `generate_progress_report(self) -> str`
  - Generates a markdown progress report dashboard summarizing total tasks, completed, in progress, pending, and overall progress percentage.
  - Lists detailed task information.

- `generate_priority_urgency_report(self) -> str`
  - Generates a markdown report of top 10 important and urgent tasks.
  - Classifies tasks into Eisenhower matrix quadrants based on importance and urgency thresholds (0.5).
  - Includes notes if importance or urgency data is missing.

- `generate_resource_allocation_report(self) -> str`
  - Generates a markdown resource allocation dashboard listing human resources and their allocation percentages.

- `generate_cost_management_report(self) -> str`
  - Generates a markdown cost management report summarizing total costs and WBS scores.

- `generate_risk_issue_tracking_report(self) -> str`
  - Generates a markdown risk and issue tracking dashboard listing risks and issues from workflow definition.

## Usage
Create an instance and call report generation methods to obtain markdown reports:

```python
reports = DashboardReports()
reports.load_inputs()
progress_md = reports.generate_progress_report()
priority_md = reports.generate_priority_urgency_report()
resource_md = reports.generate_resource_allocation_report()
cost_md = reports.generate_cost_management_report()
risk_md = reports.generate_risk_issue_tracking_report()
```

---

This documentation provides a detailed overview of the `dashboards_reports` module to assist developers in generating comprehensive project management reports.
