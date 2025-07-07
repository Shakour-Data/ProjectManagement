import json
import os
import datetime

class ProgressCalculator:
    def __init__(self, input_dir='PM_Input'):
        self.input_dir = input_dir
        self.tasks = []
        self.commit_progress = {}
        self.missing_data = set()

    def load_json_file(self, filename):
        path = os.path.join(self.input_dir, filename)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return None

    def flatten_tasks(self, tasks, parent_id=None):
        flat_tasks = []
        for task in tasks:
            task_copy = task.copy()
            task_copy['parent_id'] = parent_id
            subtasks = task_copy.pop('subtasks', [])
            flat_tasks.append(task_copy)
            flat_tasks.extend(self.flatten_tasks(subtasks, task_copy.get('id')))
        return flat_tasks

    def load_inputs(self):
        tasks_hier = self.load_json_file('detailed_wbs.json') or []
        self.tasks = self.flatten_tasks(tasks_hier)
        self.commit_progress = self.load_json_file('commit_progress.json') or {}

    def calculate_commit_progress(self, task_id):
        # Since commit_progress.json is empty, we note this missing data
        if not self.commit_progress:
            self.missing_data.add('commit_progress.json is empty or missing commit data')
            return 0.0
        return self.commit_progress.get(task_id, 0.0)

    def calculate_progress(self, task):
        # Use optimistic, normal, pessimistic hours if available to estimate progress
        optimistic = task.get('optimistic_hours')
        normal = task.get('normal_hours')
        pessimistic = task.get('pessimistic_hours')
        if optimistic is None or normal is None or pessimistic is None:
            self.missing_data.add(f"Task {task.get('id')} missing time estimates")
            return 0.0
        # Simple average progress estimation placeholder
        progress = (normal - optimistic) / (pessimistic - optimistic) if pessimistic != optimistic else 0.0
        return max(0.0, min(1.0, progress))

    def enrich_tasks_with_progress(self):
        for task in self.tasks:
            task_id = task.get('id')
            commit_prog = self.calculate_commit_progress(task_id)
            estimated_prog = self.calculate_progress(task)
            # Combine commit progress and estimated progress equally
            combined_prog = (commit_prog + estimated_prog) / 2
            task['progress'] = combined_prog

    def save_missing_data_report(self):
        if not self.missing_data:
            return
        path = os.path.join(self.input_dir, 'missing_data_report.txt')
        with open(path, 'w', encoding='utf-8') as f:
            for item in sorted(self.missing_data):
                f.write(item + '\n')
        print(f"Missing data report saved to {path}")

    def get_enriched_tasks(self):
        return self.tasks
