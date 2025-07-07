import subprocess
import re
from collections import defaultdict
from typing import List, Dict, Any

class GitProgressUpdater:
    def __init__(self, workflow_definition: List[Dict[str, Any]]):
        self.workflow_definition = workflow_definition
        self.task_progress = defaultdict(float)

    def run_git_log(self) -> str:
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

    def parse_git_log(self, log_text: str) -> List[Dict[str, Any]]:
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
            i += 1
            commits.append({
                "hash": commit_hash,
                "message": message,
                "files": files
            })
        return commits

    def map_commits_to_tasks(self, commits: List[Dict[str, Any]]) -> Dict[str, float]:
        task_progress_counts = defaultdict(int)
        for commit in commits:
            message = commit['message']
            # Improved regex to capture task IDs like 1, 1.1, 1.1.1 etc.
            task_ids = re.findall(r'\b\d+(?:\.\d+)*\b', message)
            for task_id in task_ids:
                task_progress_counts[task_id] += 1
        if task_progress_counts:
            max_count = max(task_progress_counts.values())
            for task_id in task_progress_counts:
                task_progress_counts[task_id] = (task_progress_counts[task_id] / max_count) * 100
        return task_progress_counts

    def calculate_workflow_progress(self) -> Dict[str, float]:
        # Placeholder for actual workflow step completion tracking
        return defaultdict(float)

    def combine_progress(self, commit_progress: Dict[str, float], workflow_progress: Dict[str, float]) -> Dict[str, float]:
        combined = defaultdict(float)
        all_task_ids = set(commit_progress.keys()) | set(workflow_progress.keys())
        for task_id in all_task_ids:
            combined[task_id] = (commit_progress.get(task_id, 0) + workflow_progress.get(task_id, 0)) / 2
        return combined

    def update_progress(self) -> Dict[str, float]:
        log_text = self.run_git_log()
        if not log_text:
            print("No git log data available.")
            return {}
        commits = self.parse_git_log(log_text)
        commit_progress = self.map_commits_to_tasks(commits)
        workflow_progress = self.calculate_workflow_progress()
        combined_progress = self.combine_progress(commit_progress, workflow_progress)
        return combined_progress
