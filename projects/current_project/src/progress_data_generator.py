import subprocess
import json
import os
from collections import defaultdict

DB_PROGRESS_JSON_PATH = os.path.join('docs', 'project_management', 'task_progress.json')

def run_git_log():
    """Run git log to get commit history with messages and files changed."""
    try:
        result = subprocess.run(
            ["git", "log", "--name-only", "--pretty=format:%H%n%s%n%b%n==END=="],
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

def map_commits_to_tasks(commits):
    """
    Map commits to tasks based on commit messages or file paths.
    This is a placeholder implementation that looks for task ids in commit messages.
    """
    task_progress = defaultdict(int)  # task_id -> progress count

    for commit in commits:
        message = commit['message']
        # Example: look for task ids like "1.1", "2.3" in message
        import re
        task_ids = re.findall(r'\b\d+\.\d+\b', message)
        for task_id in task_ids:
            task_progress[task_id] += 1

    # Normalize progress counts to a 0-100 scale (example)
    if task_progress:
        max_count = max(task_progress.values())
        for task_id in task_progress:
            task_progress[task_id] = (task_progress[task_id] / max_count) * 100
    return task_progress

def save_progress_to_json(progress_data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(progress_data, f, indent=2, ensure_ascii=False)

def main():
    log_text = run_git_log()
    if not log_text:
        print("No git log data available.")
        return
    commits = parse_git_log(log_text)
    progress_data = map_commits_to_tasks(commits)
    save_progress_to_json(progress_data, DB_PROGRESS_JSON_PATH)
    print(f"Task progress data saved to {DB_PROGRESS_JSON_PATH}")

if __name__ == "__main__":
    main()
