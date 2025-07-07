import subprocess
import json
import os
from collections import defaultdict

DB_PROGRESS_JSON_PATH = os.path.join('docs', 'project_management', 'task_progress.json')
WORKFLOW_DEFINITION_PATH = os.path.join('docs', 'db_json', 'workflow_definition.json')

def run_git_log(branch=None):
    """Run git log to get commit history with messages and files changed from specified branch.
    If branch is None, use the current checked out branch."""
    try:
        cmd = ["git", "log"]
        if branch:
            cmd.append(branch)
        cmd.extend(["--name-only", "--pretty=format:%H%n%s%n%b%n==END=="])
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Git log command failed: {e}")
        return ""

def parse_git_log(log_text):
    """
    Parse git log output into a list of commits.
    Each commit is a dict with keys: hash, message, files (list).
    """
    commits = []
    lines = log_text.splitlines()
    i = 0
    while i < len(lines):
        commit_hash = lines[i].strip()
        i += 1
        message_lines = []
        while i < len(lines) and lines[i].strip() != '' and lines[i].strip() != '==END==':
            message_lines.append(lines[i])
            i += 1
        message = "\n".join(message_lines).strip()
        files = []
        while i < len(lines) and lines[i].strip() != '==END==':
            if lines[i].strip() != '':
                files.append(lines[i].strip())
            i += 1
        # Skip the ==END== line
        i += 1
        commits.append({
            "hash": commit_hash,
            "message": message,
            "files": files
        })
    return commits

def load_workflow_definition():
    try:
        with open(WORKFLOW_DEFINITION_PATH, 'r', encoding='utf-8') as f:
            workflow = json.load(f)
        return workflow
    except Exception as e:
        print(f"Failed to load workflow definition: {e}")
        return []

def map_commits_to_tasks(commits):
    """
    Map commits to tasks based on commit messages or file paths.
    This looks for task ids in commit messages.
    """
    task_progress = defaultdict(int)  # task_id -> progress count

    for commit in commits:
        message = commit['message']
        import re
        task_ids = re.findall(r'\b\d+\.\d+\b', message)
        for task_id in task_ids:
            task_progress[task_id] += 1

    # Normalize progress counts to a 0-100 scale
    if task_progress:
        max_count = max(task_progress.values())
        for task_id in task_progress:
            task_progress[task_id] = (task_progress[task_id] / max_count) * 100
    return task_progress

def calculate_workflow_progress():
    """
    Calculate progress based on workflow steps completion.
    For simplicity, assume equal weight for each step.
    """
    workflow = load_workflow_definition()
    if not workflow:
        return {}

    step_weight = 100 / len(workflow)
    # For demonstration, assume all tasks have completed 0 steps initially.
    # This function can be extended to track actual step completion per task.
    workflow_progress = defaultdict(float)  # task_id -> progress percentage

    # Placeholder: no actual task-step mapping implemented yet.
    # In real implementation, track which steps are done per task.

    return workflow_progress

def combine_progress(commit_progress, workflow_progress):
    """
    Combine commit-based and workflow-based progress.
    For example, average the two or weight them differently.
    """
    combined_progress = defaultdict(float)
    all_task_ids = set(commit_progress.keys()) | set(workflow_progress.keys())

    for task_id in all_task_ids:
        commit_val = commit_progress.get(task_id, 0)
        workflow_val = workflow_progress.get(task_id, 0)
        combined_progress[task_id] = (commit_val + workflow_val) / 2  # simple average

    return combined_progress

def save_progress_to_json(progress_data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(progress_data, f, indent=2, ensure_ascii=False)

def main(branch='main'):
    log_text = run_git_log(branch)
    if not log_text:
        print("No git log data available.")
        return
    commits = parse_git_log(log_text)
    commit_progress = map_commits_to_tasks(commits)
    workflow_progress = calculate_workflow_progress()
    combined_progress = combine_progress(commit_progress, workflow_progress)
    save_progress_to_json(combined_progress, DB_PROGRESS_JSON_PATH)
    print(f"Task progress data saved to {DB_PROGRESS_JSON_PATH}")

if __name__ == "__main__":
    main()
