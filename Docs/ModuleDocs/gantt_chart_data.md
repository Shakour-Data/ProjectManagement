# GanttChartData Module

## Overview
The `gantt_chart_data` module provides the `GanttChartData` class which generates Gantt chart data from project tasks. It loads detailed work breakdown structure (WBS) tasks from JSON, processes task dates and durations, and builds structured data suitable for Gantt chart visualization.

## Class: GanttChartData

### Description
The `GanttChartData` class loads task data, parses dates, calculates task durations and dependencies, and recursively processes subtasks to build comprehensive Gantt chart data.

### Methods

- `__init__(self, input_dir: str = 'project_inputs/PM_JSON/user_inputs')`
  - Initializes the class with the input directory path.

- `load_tasks(self)`
  - Loads tasks from the `detailed_wbs.json` file in the input directory.
  - Handles errors gracefully and initializes an empty task list on failure.

- `parse_date(self, date_str: Optional[str]) -> Optional[datetime.date]`
  - Parses an ISO format date string into a `datetime.date` object.
  - Returns `None` if the date string is invalid or missing.

- `build_gantt_data(self) -> List[Dict[str, Any]]`
  - Builds Gantt chart data from loaded tasks.
  - Each task dictionary includes:
    - `id`: Task identifier.
    - `name`: Task name or title.
    - `start_date`: ISO formatted start date.
    - `end_date`: Calculated end date based on start date and duration.
    - `dependencies`: List of dependent task IDs.
    - `progress`: Task progress as a percentage (0-100).
  - Recursively processes subtasks, inheriting start dates as needed.

## Usage
Run the module as a script to generate and save Gantt chart data:

```python
if __name__ == "__main__":
    generator = GanttChartData()
    generator.load_tasks()
    data = generator.build_gantt_data()
    output_path = 'SystemInputs/system_generated/gantt_chart_data.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Gantt chart data saved to {output_path}")
```

---

This documentation provides an overview of the `gantt_chart_data` module to assist developers in generating Gantt chart data for project visualization.
