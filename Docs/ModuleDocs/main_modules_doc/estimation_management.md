# EstimationManagement Module

## Overview
The `estimation_management` module provides classes to manage project estimation processes. It includes a base class for handling JSON input/output and an `EstimationManagement` subclass intended to perform project estimation using parametric, COCOMO II, and Agile methods. Currently, the estimation logic is a placeholder.

## Classes

### BaseManagement

#### Description
A base class for management modules that handle JSON input loading, analysis, and output saving.

#### Methods

- `__init__(self, input_paths: dict, output_path: str)`
  - Initializes with input file paths and output file path.
  - Parameters:
    - `input_paths` (dict): Mapping of input names to file paths.
    - `output_path` (str): Path to save output JSON.

- `load_json(self, path)`
  - Loads JSON data from a file.
  - Parameters:
    - `path` (str): File path.
  - Returns: Parsed JSON data or `None` if file not found.

- `save_json(self, data, path)`
  - Saves data as JSON to a file.
  - Parameters:
    - `data`: Data to save.
    - `path` (str): File path.

- `load_inputs(self)`
  - Loads all input JSON files specified in `input_paths`.

- `analyze(self)`
  - Placeholder method to be implemented by subclasses.

- `run(self)`
  - Runs the workflow: loads inputs, performs analysis, saves output, and prints status.

### EstimationManagement (inherits BaseManagement)

#### Description
Intended to perform project estimation using parametric, COCOMO II, and Agile methods. Currently, the analysis logic is not implemented.

#### Methods

- `__init__(self, detailed_wbs_path, output_path)`
  - Initializes with default paths for detailed WBS input and output JSON.

- `analyze(self)`
  - Placeholder method for estimation logic.
  - Sets output to a summary indicating estimation methods are not yet implemented.

## Usage
Run the module as a script to execute estimation management:

```python
if __name__ == "__main__":
    manager = EstimationManagement()
    manager.run()
```

---

This documentation provides an overview of the `estimation_management` module to assist developers in managing project estimation processes.
