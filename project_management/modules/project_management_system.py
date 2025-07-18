import json
import os
import subprocess
import datetime
import re
from collections import defaultdict
from typing import List, Dict, Any

class InputHandler:
    def __init__(self, input_dir='PM_UserInputs'):
        self.input_dir = os.path.abspath(input_dir)

    def ensure_input_dir(self):
        if not os.path.exists(self.input_dir):
            os.makedirs(self.input_dir)
            print(f"Created input directory at {self.input_dir}")
        else:
            print(f"Input directory already exists at {self.input_dir}")

    def read_json_files(self) -> Dict[str, Any]:
        if not os.path.exists(self.input_dir):
            print(f"Input directory {self.input_dir} does not exist.")
            return {}

        inputs = {}
        for filename in os.listdir(self.input_dir):
            if filename.endswith('.json'):
                path = os.path.join(self.input_dir, filename)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        inputs[filename] = json.load(f)
                except Exception as e:
                    print(f"Failed to read {filename}: {e}")
                    return {}
        return inputs

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
            task_ids = re.findall(r'\b\d+(\.\d+)*\b', message)
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

class ProgressCalculator:
    def __init__(self, input_dir: str = 'PM_Input'):
        self.input_dir = input_dir
        self.tasks = []
        self.workflow_steps = []
        self.commit_progress = {}
        self.importance_cache = {}
        self.urgency_cache = {}

    def load_json_file(self, filename: str) -> Any:
        path = os.path.join(self.input_dir, filename)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return None

    def load_inputs(self):
        self.tasks = self.load_json_file('detailed_wbs.json') or []
        self.workflow_steps = self.load_json_file('workflow_definition.json') or []
        self.commit_progress = self.load_json_file('commit_progress.json') or {}

    def calculate_commit_progress(self, task_id: str) -> float:
        return self.commit_progress.get(task_id, 0.0)

    def calculate_workflow_progress(self, task_id: str) -> float:
        steps = [step for step in self.workflow_steps if step.get('task_id') == task_id]
        if not steps:
            return 0.0
        completed_steps = sum(1 for step in steps if step.get('completed', False))
        return completed_steps / len(steps)

    def calculate_combined_progress(self, task_id: str, weight_commit: float = 0.5, weight_workflow: float = 0.5) -> float:
        commit_prog = self.calculate_commit_progress(task_id)
        workflow_prog = self.calculate_workflow_progress(task_id)
        combined = (commit_prog * weight_commit) + (workflow_prog * weight_workflow)
        task = next((t for t in self.tasks if t.get('id') == task_id), None)
        if task:
            status = task.get('status', '').lower()
            if status == 'completed' and combined < 1.0:
                combined = 1.0
            elif status != 'completed' and combined > 0.0:
                combined = min(combined, 0.5)
        return combined

    def calculate_dynamic_importance(self, task: dict) -> float:
        w1, w2, w3 = 0.5, 0.3, 0.2
        now = datetime.datetime.now()
        deadline_str = task.get('deadline')
        if deadline_str:
            try:
                deadline = datetime.datetime.fromisoformat(deadline_str)
                total_time = (deadline - now).total_seconds()
                normalized_time = max(0, min(1, total_time / (7*24*3600)))
                time_factor = 1 - normalized_time
            except Exception:
                time_factor = 0
        else:
            time_factor = 0
        dependencies = task.get('dependencies', [])
        dependency_factor = min(1, len(dependencies) / 10)
        priority = task.get('priority', 0)
        priority_factor = min(1, priority / 10)
        importance = w1 * time_factor + w2 * dependency_factor + w3 * priority_factor
        return importance

    def calculate_dynamic_urgency(self, task: dict) -> float:
        w1, w2, w3 = 0.6, 0.3, 0.1
        now = datetime.datetime.now()
        deadline_str = task.get('deadline')
        if deadline_str:
            try:
                deadline = datetime.datetime.fromisoformat(deadline_str)
                total_time = (deadline - now).total_seconds()
                normalized_time = max(0, min(1, total_time / (3*24*3600)))
                time_factor = 1 - normalized_time
            except Exception:
                time_factor = 0
        else:
            time_factor = 0
        status = task.get('status', '').lower()
        status_factor = 1 if status in ['pending', 'not started', 'in progress'] else 0
        assigned_to = task.get('assigned_to', [])
        resource_availability_factor = 1 if not assigned_to else 0
        urgency = w1 * time_factor + w2 * status_factor + w3 * resource_availability_factor
        return urgency

    def enrich_tasks_with_progress_and_score(self):
        self.importance_cache = {}
        self.urgency_cache = {}
        for task in self.tasks:
            task_id = task.get('id')
            if not task_id:
                continue
            if task_id in self.importance_cache:
                importance = self.importance_cache[task_id]
            else:
                importance = self.calculate_dynamic_importance(task)
                self.importance_cache[task_id] = importance
            if task_id in self.urgency_cache:
                urgency = self.urgency_cache[task_id]
            else:
                urgency = self.calculate_dynamic_urgency(task)
                self.urgency_cache[task_id] = urgency
            score = self.calculate_score(importance, urgency)
            progress = self.calculate_combined_progress(task_id)
            task['importance'] = importance
            task['urgency'] = urgency
            task['score'] = score
            task['progress'] = progress

    def calculate_score(self, importance: float, urgency: float, weight_importance: float = 0.6, weight_urgency: float = 0.4) -> float:
        return (importance * weight_importance) + (urgency * weight_urgency)

    def get_enriched_tasks(self) -> List[Dict[str, Any]]:
        return self.tasks

class TaskManager:
    def __init__(self, tasks: List[Dict[str, Any]]):
        self.tasks = tasks

    def complete_top_important_tasks(self, top_n: int = 10) -> List[Dict[str, Any]]:
        """
        Mark top N important tasks as completed with 100% progress.
        If already completed, skip but ensure progress is 100%.
        Returns the updated list of tasks.
        """
        sorted_tasks = sorted(self.tasks, key=lambda x: x.get('importance', 0), reverse=True)
        count = 0
        for task in sorted_tasks:
            if count >= top_n:
                break
            if task.get('status') != 'completed':
                task['status'] = 'completed'
                task['progress'] = 1.0
                count += 1
            else:
                task['progress'] = 1.0
                count += 1
        return self.tasks

import datetime

class ReportManager:
    def __init__(self, input_dir='project_test/PM_Input', base_report_dir='project_test/reports'):
        self.input_dir = input_dir
        self.base_report_dir = base_report_dir
        self.dashboard_dir = f"{self.base_report_dir}/dashboards"
        self.report_dir = f"{self.base_report_dir}/reports"
        self._ensure_directories()

    def _ensure_directories(self):
        import os
        os.makedirs(self.dashboard_dir, exist_ok=True)
        os.makedirs(self.report_dir, exist_ok=True)

    def _get_timestamp(self):
        return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    def save_dashboard(self, filename_prefix: str, content: str):
        timestamp = self._get_timestamp()
        filename = f"{filename_prefix}_{timestamp}.md"
        path = f"{self.dashboard_dir}/{filename}"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Dashboard saved: {path}")

    def save_report(self, filename_prefix: str, content: str):
        timestamp = self._get_timestamp()
        filename = f"{filename_prefix}_{timestamp}.md"
        path = f"{self.report_dir}/{filename}"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Report saved: {path}")

    def generate_and_save_all(self):
        ih = InputHandler(self.input_dir)
        inputs = ih.read_json_files()
        gpu = GitProgressUpdater(inputs.get('workflow_definition', []), self.input_dir)
        # Update and save commit_progress.json before loading inputs
        gpu.update_and_save_commit_progress()
        # Reload inputs after updating commit progress
        inputs = ih.read_json_files()
        combined_progress = gpu.update_progress()

        pc = ProgressCalculator(self.input_dir)
        pc.load_inputs()
        pc.commit_progress = combined_progress
        pc.enrich_tasks_with_progress()

        tm = TaskManager(pc.get_enriched_tasks())
        tm.complete_top_important_tasks(5)

        from project_management.modules.dashboards_reports import DashboardReports
        dr = DashboardReports(self.input_dir)
        dr.load_inputs()

        progress_md = dr.generate_progress_report()
        priority_md = dr.generate_priority_urgency_report()

        self.save_dashboard('progress_report_dashboard', progress_md)
        self.save_dashboard('task_priority_urgency_report', priority_md)

        # Append to archive files
        archive_dashboard_path = f"{self.base_report_dir}/dashboards/dashboard_archive.md"
        archive_report_path = f"{self.base_report_dir}/reports/report_archive.md"

        with open(archive_dashboard_path, 'a', encoding='utf-8') as f:
            f.write(f"\n\n# Archived Dashboard - {datetime.datetime.now().isoformat()}\n\n")
            f.write(progress_md)
            f.write("\n\n---\n\n")
            f.write(priority_md)
            f.write("\n\n=== End of Archived Dashboards ===\n\n")

        with open(archive_report_path, 'a', encoding='utf-8') as f:
            f.write(f"\n\n# Archived Report - {datetime.datetime.now().isoformat()}\n\n")
            # For now, just archive the priority report as example
            f.write(priority_md)
            f.write("\n\n=== End of Archived Reports ===\n\n")

if __name__ == '__main__':
    rm = ReportManager()
    rm.generate_and_save_all()
