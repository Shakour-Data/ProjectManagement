import os
import json
import uuid
from pathlib import Path
from project_management.modules.input_handler import InputHandler
from project_management.modules.setup_initialization import create_virtualenv, install_dependencies, ensure_gitignore_excludes_venv

REQUIRED_USER_JSON_FILES = [
    'detailed_wbs.json',
    'workflow_definition.json',
    'resource_allocation.json',
    'task_resource_allocation.json',
    'wbs_data.json',
    'wbs_scores.json'
]

GENERATED_JSON_FILES = [
    'commit_progress.json',
    'commit_task_database.json',
    'human_resources.json'  # special case, created interactively
]

def prompt_for_input_dir():
    while True:
        input_dir = input("Please enter the path to your JSON input files directory (e.g., PM_Input): ").strip()
        if not input_dir:
            print("Input directory path cannot be empty.")
            continue
        path = Path(input_dir)
        if not path.exists() or not path.is_dir():
            print(f"Directory '{input_dir}' does not exist or is not a directory. Please try again.")
            continue
        return path

def check_required_files(input_dir):
    missing_files = []
    for filename in REQUIRED_USER_JSON_FILES:
        file_path = input_dir / filename
        if not file_path.exists():
            missing_files.append(filename)
    return missing_files

def validate_json_files(input_dir):
    ih = InputHandler(input_dir)
    inputs = ih.read_json_files()
    if inputs is None:
        return False
    # Check all required files are present
    for filename in REQUIRED_USER_JSON_FILES:
        if filename not in inputs:
            print(f"Required JSON file '{filename}' is missing or invalid.")
            return False
    return True

def prompt_human_resources(input_dir):
    print("\nNow, please enter the human resources data.")
    print("For each resource, you will be prompted to enter details one by one.")
    print("The system will automatically generate a unique 'id' for each resource.")
    print("When you are done entering resources, just press Enter without typing a name.\n")

    resources = []
    while True:
        name = input("Enter resource name (or press Enter to finish): ").strip()
        if not name:
            break
        role = input("Enter resource role: ").strip()
        email = input("Enter resource email: ").strip()
        # Add more fields as needed here with prompts

        resource = {
            "id": str(uuid.uuid4()),
            "name": name,
            "role": role,
            "email": email
        }
        resources.append(resource)
        print(f"Resource '{name}' added with id {resource['id']}.\n")

    if not resources:
        print("No human resources entered. Please enter at least one resource.")
        return prompt_human_resources(input_dir)

    # Save to human_resources.json
    human_resources_path = input_dir / 'human_resources.json'
    with open(human_resources_path, 'w', encoding='utf-8') as f:
        json.dump(resources, f, indent=4, ensure_ascii=False)
    print(f"Human resources data saved to {human_resources_path}")

def main():
    print("Welcome to the interactive setup for the ProjectManagement package.\n")

    # Step 1: Prompt for input directory
    input_dir = prompt_for_input_dir()

    # Step 2: Check required JSON files presence
    missing_files = check_required_files(input_dir)
    while missing_files:
        print(f"The following required JSON files are missing in {input_dir}:")
        for f in missing_files:
            print(f" - {f}")
        print("Please add the missing files and try again.")
        input_dir = prompt_for_input_dir()
        missing_files = check_required_files(input_dir)

    # Step 3: Validate JSON files syntax
    valid = validate_json_files(input_dir)
    while not valid:
        print("One or more JSON files are invalid. Please fix the files and try again.")
        input_dir = prompt_for_input_dir()
        valid = validate_json_files(input_dir)

    # Step 4: Prompt for human_resources.json data entry
    prompt_human_resources(input_dir)

    # Step 5: Setup environment
    print("\nSetting up the project environment...")
    ensure_gitignore_excludes_venv()
    create_virtualenv()
    install_dependencies()

    print("\nSetup complete. You can now activate the virtual environment and start using the package.")
    print("To activate the virtual environment, run:")
    print("  source venv/bin/activate")

if __name__ == '__main__':
    main()
