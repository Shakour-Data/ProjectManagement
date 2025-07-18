import argparse
import os
import subprocess
from project_management.modules.setup_initialization import initialize_git_repo, create_virtualenv, install_dependencies, create_requirements_file, ensure_gitignore_excludes_venv

def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command {command} failed with error: {e}")

def prompt_user(question, default=None):
    prompt = f"{question}"
    if default:
        prompt += f" [{default}]"
    prompt += ": "
    response = input(prompt)
    if not response and default is not None:
        return default
    return response

def setup_project():
    print("Starting project setup...")

    # Initialize git repo
    initialize_git_repo()

    # Ensure .gitignore excludes venv
    ensure_gitignore_excludes_venv()

    # Create requirements.txt
    create_requirements_file()

    # Create virtual environment
    create_virtualenv()

    # Install dependencies
    install_dependencies()

    print("\nSetup complete.")
    print("Please add your project dependencies to requirements.txt if not already done.")
    print("Place your JSON input files in the 'project_inputs/PM_JSON/user_inputs' directory.")
    print("You can then proceed with other commands.")

def status():
    print("Project Management Tool Status:")
    if os.path.exists('.git'):
        print("- Git repository initialized.")
    else:
        print("- Git repository not found.")
    if os.path.exists('venv'):
        print("- Virtual environment exists.")
    else:
        print("- Virtual environment not found.")
    if os.path.exists('requirements.txt'):
        print("- requirements.txt file exists.")
    else:
        print("- requirements.txt file not found.")
    if os.path.exists('project_inputs/PM_JSON/user_inputs'):
        print("- project_inputs/PM_JSON/user_inputs directory exists.")
    else:
        print("- project_inputs/PM_JSON/user_inputs directory not found.")

def main():
    parser = argparse.ArgumentParser(description="Project Management Tool CLI")
    parser.add_argument('command', nargs='?', help='Command to run: setup, status, etc.')

    args = parser.parse_args()

    if args.command == 'setup':
        setup_project()
    elif args.command == 'status':
        status()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
