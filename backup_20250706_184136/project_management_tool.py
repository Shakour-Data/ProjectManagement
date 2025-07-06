"""
Project Management Tool Automation Script

This script automates the 10-step process for building and managing a Project Management Tool,
as described in docs/general_instructions_stepwise.md.

Each step is implemented as a modular code piece (MCP) for clarity and maintainability.

Only free and open-source Python libraries are used.
"""

import os
import json
import logging
import subprocess
from typing import List, Dict

# Step 1: Setup and Installation
class SetupInstallation:
    def __init__(self):
        self.venv_dir = "venv"

    def create_virtualenv(self):
        """Create a Python virtual environment."""
        subprocess.run(["python3", "-m", "venv", self.venv_dir], check=True)
        # Create .gitignore file to exclude venv directory from git tracking
        gitignore_path = ".gitignore"
        if os.path.exists(gitignore_path):
            with open(gitignore_path, "r") as f:
                lines = f.read().splitlines()
        else:
            lines = []
        if self.venv_dir not in lines:
            lines.append(self.venv_dir)
            with open(gitignore_path, "w") as f:
                f.write("\n".join(lines) + "\n")

    def install_dependencies(self, requirements_file="requirements.txt"):
        """Install dependencies inside the virtual environment."""
        pip_path = os.path.join(self.venv_dir, "bin", "pip")
        subprocess.run([pip_path, "install", "-r", requirements_file], check=True)

    def install_vscode_extensions(self):
        """Install essential VS Code extensions."""
        # Example: Install BLACKBOX AI extension (if available via CLI)
        # This is a placeholder; actual implementation may vary
        pass

    def run(self):
        self.create_virtualenv()
        self.install_dependencies()
        self.install_vscode_extensions()
        logging.info("Setup and installation completed.")


# Step 2: Input Handling
class InputHandler:
    def get_natural_language_input(self) -> str:
        """
        Get natural language input from user or file.
        For automation, simulate by returning a simple project description in natural language.
        The system will generate the WBS automatically from this description.
        """
        sample_input = "I want a simple calculator application."
        return sample_input.strip()

    def get_code_snippet_input(self) -> str:
        """Get code snippet input from user or file."""
        # Placeholder for actual input mechanism
        return ""

    def run(self):
        logging.info("Input handling completed.")


# Step 3: Work Breakdown Structure (WBS) Generation
import re
import datetime

class WBSGenerator:
    def generate_wbs(self, inputs: str) -> Dict:
        """
        Generate WBS from inputs using rule-based placeholder only.
        Fully free and does not use any paid or external AI APIs.
        """
        lines = inputs.strip().splitlines()
        root_tasks = []
        task_stack = []
        task_map = {}

        def create_task(id, title, level):
            return {
                "id": id,
                "title": title,
                "subtasks": [],
                "optimistic_hours": None,
                "normal_hours": None,
                "pessimistic_hours": None,
                "predecessors": []
            }

        for line in lines:
            stripped = line.lstrip()
            indent = len(line) - len(stripped)
            level = indent // 4  # assuming 4 spaces per indent
            title = stripped
            task_id = f"{level+1}.{len(task_map)+1}"
            task = create_task(task_id, title, level)
            task_map[task_id] = task

            while task_stack and task_stack[-1][1] >= level:
                task_stack.pop()
            if task_stack:
                parent_task = task_stack[-1][0]
                parent_task["subtasks"].append(task)
            else:
                root_tasks.append(task)
            task_stack.append((task, level))

        # Add milestone tasks
        start_task = {
            "id": "0",
            "title": "Start",
            "subtasks": [],
            "optimistic_hours": 0,
            "normal_hours": 0,
            "pessimistic_hours": 0,
            "predecessors": []
        }
        end_task = {
            "id": "99",
            "title": "End",
            "subtasks": [],
            "optimistic_hours": 0,
            "normal_hours": 0,
            "pessimistic_hours": 0,
            "predecessors": []
        }

        # Assign predecessors for lowest-level tasks
        def assign_predecessors(task):
            if not task["subtasks"]:
                if not task["predecessors"]:
                    task["predecessors"] = ["0"]
            else:
                for sub in task["subtasks"]:
                    assign_predecessors(sub)

        for t in root_tasks:
            assign_predecessors(t)

        wbs_json = [start_task] + root_tasks + [end_task]
        return {"wbs": wbs_json}

    def run(self):
        logging.info("WBS generation completed.")


# Step 4: Resource Allocation
class ResourceAllocator:
    def load_resources(self, resource_file: str) -> Dict:
        """Load resource definitions from JSON file."""
        with open(resource_file, "r") as f:
            resources = json.load(f)
        return resources

    def allocate_resources(self, wbs: Dict, resources: Dict) -> Dict:
        """
        Allocate resources to tasks based on JSON resource allocation instructions.
        Ensures no overbooking and respects allocation percentages and roles.
        """
        allocation = {}
        resource_usage = {}

        # Flatten tasks from WBS
        def flatten_tasks(tasks):
            flat = []
            for task in tasks:
                if isinstance(task, dict):
                    flat.append(task)
                    if task.get("subtasks"):
                        flat.extend(flatten_tasks(task["subtasks"]))
            return flat

        tasks = flatten_tasks(wbs.get("wbs", []))

        for task in tasks:
            task_id = task.get("id")
            allocation[task_id] = []
            for res in resources:
                # Check if resource is allocated to this task
                if res.get("task_id") == task_id:
                    resource_id = res.get("resource_id")
                    percent = res.get("allocation_percent", 100)
                    # Check resource availability
                    used = resource_usage.get(resource_id, 0)
                    if used + percent <= 100:
                        allocation[task_id].append({
                            "resource_id": resource_id,
                            "allocation_percent": percent,
                            "role_in_task": res.get("role_in_task"),
                            "start_date": res.get("start_date"),
                            "end_date": res.get("end_date"),
                            "notes": res.get("notes")
                        })
                        resource_usage[resource_id] = used + percent
                    else:
                        logging.warning(f"Resource {resource_id} overbooked for task {task_id}")
        return allocation

    def run(self):
        logging.info("Resource allocation completed.")


# Step 5: Task Management and Scheduling
class TaskScheduler:
    def schedule_tasks(self, wbs: Dict, allocations: Dict) -> Dict:
        """Schedule tasks considering dependencies and priorities."""
        # Placeholder for scheduling logic
        schedule = {}
        return schedule

    def run(self):
        logging.info("Task scheduling completed.")


# Step 6: Development Workflow Automation
class DevelopmentWorkflow:
    def setup_commit_hooks(self):
        """Setup commit hooks for task ID enforcement."""
        # Placeholder for hook setup
        pass

    def setup_ci_cd(self):
        """Setup CI/CD pipelines."""
        # Placeholder for CI/CD setup
        pass

    def run(self):
        logging.info("Development workflow automation completed.")


# Step 7: Progress Tracking and Reporting
import subprocess
import json
import re

class ProgressTracker:
    def track_progress(self):
        """
        Track progress from commit history and workflow steps as per docs/progress_calculation_instructions.md.
        Combines commit-based and workflow-based progress.
        """
        # Extract commit messages
        try:
            result = subprocess.run(
                ["git", "log", "--pretty=format:%H %s"],
                capture_output=True,
                text=True,
                check=True
            )
            commits = result.stdout.strip().split("\n")
        except subprocess.CalledProcessError as e:
            logging.error(f"Git log failed: {e}")
            commits = []

        # Parse task IDs from commit messages (assuming format includes task IDs like [TASK-123])
        task_commit_counts = {}
        task_id_pattern = re.compile(r"\[([^\]]+)\]")
        for commit in commits:
            match = task_id_pattern.search(commit)
            if match:
                task_id = match.group(1)
                task_commit_counts[task_id] = task_commit_counts.get(task_id, 0) + 1

        # Normalize commit counts to 0-100%
        max_commits = max(task_commit_counts.values()) if task_commit_counts else 1
        commit_progress = {task: (count / max_commits) * 100 for task, count in task_commit_counts.items()}

        # Load workflow definition
        workflow_file = "workflow_definition.json"
        try:
            with open(workflow_file, "r") as f:
                workflow = json.load(f)
        except FileNotFoundError:
            logging.warning(f"Workflow definition file {workflow_file} not found.")
            workflow = {}

        # Placeholder: Assume all workflow steps completed for all tasks
        workflow_progress = {task: 100 for task in commit_progress.keys()}

        # Combine progress (equal weighting)
        combined_progress = {}
        for task in commit_progress.keys():
            combined_progress[task] = (commit_progress.get(task, 0) + workflow_progress.get(task, 0)) / 2

        self.progress_data = combined_progress

    def generate_reports(self):
        """Generate markdown and text-based reports of progress."""
        if not hasattr(self, "progress_data"):
            self.progress_data = {}
        report_lines = ["# Project Progress Report\n"]
        for task, progress in self.progress_data.items():
            report_lines.append(f"- Task {task}: {progress:.2f}% complete\n")
        report_content = "\n".join(report_lines)
        with open("progress_report.md", "w") as f:
            f.write(report_content)
        logging.info("Progress report generated at progress_report.md")

    def run(self):
        self.track_progress()
        self.generate_reports()
        logging.info("Progress tracking and reporting completed.")


# Step 8: Documentation Management
import shutil

class DocumentationManager:
    def sync_documentation(self):
        """
        Synchronize documentation files in markdown or text format within the repository.
        For simplicity, copy docs/ content to a docs_sync/ folder to simulate sync.
        """
        src_dir = "docs"
        dest_dir = "docs_sync"
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)
        shutil.copytree(src_dir, dest_dir)
        logging.info(f"Documentation synchronized from {src_dir} to {dest_dir}")

    def integrate_github_wiki(self):
        """
        Integrate with GitHub Wiki by pushing documentation files to the wiki repository.
        Placeholder: actual implementation requires GitHub API or git commands.
        """
        logging.info("GitHub Wiki integration placeholder executed.")

    def run(self):
        self.sync_documentation()
        self.integrate_github_wiki()
        logging.info("Documentation management completed.")


# Step 9: Security and Permissions Management
from cryptography.fernet import Fernet

class SecurityManager:
    def __init__(self):
        self.key_file = "secret.key"
        self.token_file = "token.enc"
        self.key = None
        self.load_or_create_key()

    def load_or_create_key(self):
        """Load encryption key from file or create a new one."""
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(self.key)

    def encrypt_tokens(self, token: str):
        """Encrypt and securely store authentication tokens."""
        if not hasattr(self, "fernet") or not self.fernet:
            self.setup_fernet()
        encrypted = self.fernet.encrypt(token.encode())
        with open(self.token_file, "wb") as f:
            f.write(encrypted)
        logging.info("Token encrypted and stored securely.")

    def decrypt_tokens(self) -> str:
        """Decrypt and return the stored authentication token."""
        if not os.path.exists(self.token_file):
            logging.error("Encrypted token file not found.")
            return ""
        if not hasattr(self, "fernet") or not self.fernet:
            self.setup_fernet()
        with open(self.token_file, "rb") as f:
            encrypted = f.read()
        decrypted = self.fernet.decrypt(encrypted).decode()
        return decrypted

    def setup_role_based_access(self):
        """Implement role-based access control."""
        # Placeholder for access control implementation
        logging.info("Role-based access control placeholder executed.")

    def run(self):
        logging.info("Security and permissions management completed.")


# Step 10: Backup, Recovery, and Extensibility
import datetime
import shutil

class BackupRecoveryManager:
    def automate_backups(self):
        """
        Automate backups of project state, documentation, and configurations.
        For simplicity, copy key files to a backup folder with timestamp.
        """
        backup_dir = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(backup_dir, exist_ok=True)
        files_to_backup = ["project_management_tool.py", "docs", ".gitignore"]
        for item in files_to_backup:
            if os.path.exists(item):
                dest = os.path.join(backup_dir, os.path.basename(item))
                if os.path.isdir(item):
                    shutil.copytree(item, dest)
                else:
                    shutil.copy2(item, dest)
        logging.info(f"Backup completed to {backup_dir}")

    def implement_recovery(self):
        """Implement recovery mechanisms for data loss or corruption."""
        # Placeholder for recovery logic
        logging.info("Recovery mechanism placeholder executed.")

    def setup_plugin_architecture(self):
        """Setup plugin architecture for extensibility."""
        # Placeholder for plugin setup
        logging.info("Plugin architecture setup placeholder executed.")

    def run(self):
        self.automate_backups()
        self.implement_recovery()
        self.setup_plugin_architecture()
        logging.info("Backup, recovery, and extensibility completed.")


# Main orchestrator
class ProjectManagementTool:
    def __init__(self):
        self.setup = SetupInstallation()
        self.input_handler = InputHandler()
        self.wbs_generator = WBSGenerator()
        self.resource_allocator = ResourceAllocator()
        self.task_scheduler = TaskScheduler()
        self.dev_workflow = DevelopmentWorkflow()
        self.progress_tracker = ProgressTracker()
        self.documentation_manager = DocumentationManager()
        self.security_manager = SecurityManager()
        self.backup_manager = BackupRecoveryManager()

    def run_all(self):
        self.setup.run()
        self.input_handler.run()
        self.wbs_generator.run()
        self.resource_allocator.run()
        self.task_scheduler.run()
        self.dev_workflow.run()
        self.progress_tracker.run()
        self.documentation_manager.run()
        self.security_manager.run()
        self.backup_manager.run()
        logging.info("Project Management Tool automation completed.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    tool = ProjectManagementTool()
    tool.run_all()
