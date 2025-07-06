# Test Checklist for Project_Management Package

## Initial Tests

| Test Case                  | Description                                      | Status  | Notes                                      |
|----------------------------|------------------------------------------------|---------|--------------------------------------------|
| Install Command            | Run `project_management install` to create PM_Input folder | Passed  | PM_Input folder created or already exists  |
| PM_Input Folder Creation   | Check if PM_Input folder is created after install | Passed  | Verified folder exists                      |
| Start Command With Inputs  | Run `project_management start` with sample JSON file | Passed  | Sample JSON loaded and printed              |
| Start Command With Malformed JSON | Run `project_management start` with malformed JSON file | Passed  | Detected JSON decode error and handled gracefully |
| Status Command            | Run `project_management status` command         | Passed  | Status message printed                       |

## Further Tests

| Test Case                        | Description                                      | Status  | Notes                                      |
|---------------------------------|------------------------------------------------|---------|--------------------------------------------|
| Real Project Test with project_test/PM_Input | Run start command with full project_test input folder | Passed  | Loaded all JSON input files successfully and started automation |

- To be added after initial tests.
