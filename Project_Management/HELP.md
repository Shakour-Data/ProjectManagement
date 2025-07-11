# auto_pm Package Help

## Overview
The `auto_pm` package provides automated project management tools including task prioritization, progress reporting, and integration with GitHub and VS Code.

## Commands

- `install`  
  Prepare the environment and create the input directory. Use this before starting.

- `start`  
  Start the project management automation. This runs the main features of the package.

- `status`  
  Show the current status of the project management tool.

- `setup`  
  Interactive setup to help you upload and validate required JSON input files.

- `help`  
  Display help information about the package usage.

These commands provide full access to all features of the auto_pm package.

## Usage

Run commands using:

```
auto_pm <command>
```

For example, to run the interactive setup:

```
auto_pm setup
```

## Input Files

Before running `start` or `setup`, ensure you have placed the following JSON input files in the `PM_Input` directory:

- wbs_data.json
- detailed_wbs.json
- human_resources.json
- resource_allocation.json
- task_resource_allocation.json
- wbs_scores.json
- workflow_definition.json

## Notes

- The `setup` command will guide you through verifying these input files and notify you if any are missing or invalid.
- Use the `help` command to display this information anytime.

## Contact

For further assistance, please contact the package maintainer.
