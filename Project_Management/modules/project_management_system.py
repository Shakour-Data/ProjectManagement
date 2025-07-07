import json
import os
import subprocess
import datetime
import re
from collections import defaultdict
from typing import List, Dict, Any

class InputHandler:
    def __init__(self, input_dir='PM_Input'):
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

class DashboardReports:
    def __init__(self, input_dir: str = 'PM_Input'):
        self.input_dir = input_dir
        self.data = {}
        self.load_inputs()

    def load_json_file(self, filename: str) -> Any:
        path = os.path.join(self.input_dir, filename)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return None

    def load_inputs(self):
        self.data['detailed_wbs'] = self.load_json_file('detailed_wbs.json')
        self.data['human_resources'] = self.load_json_file('human_resources.json')
        self.data['resource_allocation'] = self.load_json_file('resource_allocation.json')
        self.data['task_resource_allocation'] = self.load_json_file('task_resource_allocation.json')
        self.data['wbs_data'] = self.load_json_file('wbs_data.json')
        self.data['wbs_scores'] = self.load_json_file('wbs_scores.json')
        self.data['workflow_definition'] = self.load_json_file('workflow_definition.json')

        from Project_Management.modules.project_management_system import ProgressCalculator
        pc = ProgressCalculator(self.input_dir)
        pc.load_inputs()
        pc.enrich_tasks_with_progress_and_score()
        self.data['detailed_wbs'] = pc.get_enriched_tasks()

    def _format_task(self, task: Dict[str, Any]) -> str:
        title = task.get('title', 'No Title')
        status = task.get('status', 'unknown')
        importance = task.get('importance', 0)
        urgency = task.get('urgency', 0)
        score = (importance * 0.6) + (urgency * 0.4)
        progress = task.get('progress', 0)
        progress_percent = progress * 100 if isinstance(progress, (int, float)) else 0
        return f"- **{title}** (Status: {status}, Importance: {importance:.2f}, Urgency: {urgency:.2f}, Score: {score:.2f}, Progress: {progress_percent:.1f}%)"

    def progress_report_dashboard_md(self) -> str:
        tasks = self.data.get('detailed_wbs') or self.data.get('wbs_data') or []
        total_tasks = len(tasks)
        completed = sum(1 for t in tasks if t.get('status') == 'completed')
        in_progress = sum(1 for t in tasks if t.get('status') == 'in_progress')
        pending = total_tasks - completed - in_progress
        progress_percent = (completed / total_tasks * 100) if total_tasks > 0 else 0

        md = f"# Progress Report Dashboard\n\n"
        md += f"- Total Tasks: {total_tasks}\n"
        md += f"- Completed: {completed}\n"
        md += f"- In Progress: {in_progress}\n"
        md += f"- Pending: {pending}\n"
        md += f"- Progress Percentage: {progress_percent:.2f}%\n\n"
        md += "## Task Details\n"
        for task in tasks:
            md += self._format_task(task) + "\n"
        return md

    def task_priority_urgency_report_md(self) -> str:
        tasks = self.data.get('detailed_wbs') or self.data.get('wbs_data') or []
        important_tasks = sorted(tasks, key=lambda x: x.get('importance', 0), reverse=True)[:10]
        urgent_tasks = sorted(tasks, key=lambda x: x.get('urgency', 0), reverse=True)[:10]

        matrix = {
            'Urgent & Important': [],
            'Urgent & Not Important': [],
            'Not Urgent & Important': [],
            'Not Urgent & Not Important': []
        }
        for task in tasks:
            urgent = task.get('urgency', 0) >= 0.5
            important = task.get('importance', 0) >= 0.5
            if urgent and important:
                matrix['Urgent & Important'].append(task)
            elif urgent and not important:
                matrix['Urgent & Not Important'].append(task)
            elif not urgent and important:
                matrix['Not Urgent & Important'].append(task)
            else:
                matrix['Not Urgent & Not Important'].append(task)

        md = "# Task Priority and Urgency Report\n\n"
        md += "## Top 10 Important Tasks\n"
        for task in important_tasks:
            md += self._format_task(task) + "\n"
        md += "\n## Top 10 Urgent Tasks\n"
        for task in urgent_tasks:
            md += self._format_task(task) + "\n"

        md += "\n## Eisenhower Matrix\n"
        for quadrant, tasks_list in matrix.items():
            md += f"\n### {quadrant} ({len(tasks_list)} tasks)\n"
            for task in tasks_list:
                md += self._format_task(task) + "\n"
        return md
