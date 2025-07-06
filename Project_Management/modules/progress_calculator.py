import json
from typing import List, Dict, Any

class ProgressCalculator:
    def __init__(self, input_dir: str = 'PM_Input'):
        self.input_dir = input_dir
        self.tasks = []
        self.workflow_steps = []
        self.commit_data = {}

    def load_json_file(self, filename: str) -> Any:
        path = f"{self.input_dir}/{filename}"
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return None

    def load_inputs(self):
        self.tasks = self.load_json_file('detailed_wbs.json') or []
        self.workflow_steps = self.load_json_file('workflow_definition.json') or []
        self.commit_data = self.load_json_file('commit_progress.json') or {}

    def calculate_commit_progress(self, task_id: str) -> float:
        """
        Calculate progress based on commit history for a given task.
        commit_data is expected to have task_id keys with commit counts or progress values.
        """
        return self.commit_data.get(task_id, 0.0)

    def calculate_workflow_progress(self, task_id: str) -> float:
        """
        Calculate progress based on workflow step completion for a given task.
        workflow_steps is expected to have entries with task_id and completion status.
        """
        steps = [step for step in self.workflow_steps if step.get('task_id') == task_id]
        if not steps:
            return 0.0
        completed_steps = sum(1 for step in steps if step.get('completed', False))
        return completed_steps / len(steps)

    def calculate_combined_progress(self, task_id: str, weight_commit: float = 0.5, weight_workflow: float = 0.5) -> float:
        """
        Combine commit-based and workflow-based progress with given weights.
        Also validate against actual task completion status to avoid false positives.
        """
        commit_prog = self.calculate_commit_progress(task_id)
        workflow_prog = self.calculate_workflow_progress(task_id)
        combined = (commit_prog * weight_commit) + (workflow_prog * weight_workflow)

        # Validation: check if task is marked completed in tasks list
        task = next((t for t in self.tasks if t.get('id') == task_id), None)
        if task:
            status = task.get('status', '').lower()
            if status == 'completed' and combined < 1.0:
                # If task marked completed but progress less than 100%, adjust to 100%
                combined = 1.0
            elif status != 'completed' and combined > 0.0:
                # If task not completed but progress > 0, reduce progress to 0.5 max
                combined = min(combined, 0.5)
        return combined

    def calculate_score(self, importance: float, urgency: float, weight_importance: float = 0.6, weight_urgency: float = 0.4) -> float:
        """
        Calculate combined score from importance and urgency.
        """
        return (importance * weight_importance) + (urgency * weight_urgency)

    def enrich_tasks_with_progress_and_score(self):
        """
        Enrich tasks with calculated progress and score.
        """
        for task in self.tasks:
            task_id = task.get('id')
            if not task_id:
                continue
            # Importance and urgency from wbs_scores.json or default 0
            importance = task.get('importance', 0)
            urgency = task.get('urgency', 0)
            # Calculate combined score
            score = self.calculate_score(importance, urgency)
            # Calculate combined progress
            progress = self.calculate_combined_progress(task_id)
            task['score'] = score
            task['progress'] = progress

    def get_enriched_tasks(self) -> List[Dict[str, Any]]:
        return self.tasks
