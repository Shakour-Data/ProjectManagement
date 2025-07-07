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
        self.commit_data = self.load_json_file('commit_progress.json') or []
        self.wbs_scores = self.load_json_file('wbs_scores.json') or {}

    def calculate_commit_progress(self, task_id: str) -> float:
        """
        Calculate progress based on commit history for a given task.
        commit_data is expected to have task_id keys with commit counts or progress values.
        """
        if isinstance(self.commit_data, dict):
            return self.commit_data.get(task_id, 0.0)
        else:
            # If commit_data is a list, try to find matching task_id entry
            for entry in self.commit_data:
                if isinstance(entry, dict) and entry.get('task_id') == task_id:
                    return entry.get('progress', 0.0)
            return 0.0

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

    def calculate_dynamic_importance(self, task: dict) -> float:
        """
        Calculate importance dynamically based on task attributes.
        Example formula:
        importance = w1 * (1 - normalized_time_to_deadline) + w2 * dependency_factor + w3 * priority_factor
        where weights sum to 1.
        """
        import datetime
        w1, w2, w3 = 0.5, 0.3, 0.2
        now = datetime.datetime.now()
        deadline_str = task.get('deadline')
        if deadline_str:
            try:
                deadline = datetime.datetime.fromisoformat(deadline_str)
                total_time = (deadline - now).total_seconds()
                normalized_time = max(0, min(1, total_time / (7*24*3600)))  # normalize over 7 days
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
        """
        Calculate urgency dynamically based on task attributes.
        Example formula:
        urgency = w1 * (1 - normalized_time_to_deadline) + w2 * status_factor + w3 * resource_availability_factor
        """
        import datetime
        w1, w2, w3 = 0.6, 0.3, 0.1
        now = datetime.datetime.now()
        deadline_str = task.get('deadline')
        if deadline_str:
            try:
                deadline = datetime.datetime.fromisoformat(deadline_str)
                total_time = (deadline - now).total_seconds()
                normalized_time = max(0, min(1, total_time / (3*24*3600)))  # normalize over 3 days
                time_factor = 1 - normalized_time
            except Exception:
                time_factor = 0
        else:
            time_factor = 0
        status = task.get('status', '').lower()
        status_factor = 1 if status in ['pending', 'not started', 'in progress'] else 0
        # For resource availability, assume 1 if assigned_to is empty (urgent), else 0
        assigned_to = task.get('assigned_to', [])
        resource_availability_factor = 1 if not assigned_to else 0
        urgency = w1 * time_factor + w2 * status_factor + w3 * resource_availability_factor
        return urgency

    def enrich_tasks_with_progress_and_score(self):
        """
        Enrich tasks with calculated progress and score.
        Cache importance and urgency calculations to avoid duplicate computations.
        """
        print("Enriching tasks with progress and score...")
        importance_cache = {}
        urgency_cache = {}

        for task in self.tasks:
            task_id = task.get('id')
            if not task_id:
                continue

            if task_id in importance_cache:
                importance = importance_cache[task_id]
            else:
                importance = self.calculate_dynamic_importance(task)
                importance_cache[task_id] = importance

            if task_id in urgency_cache:
                urgency = urgency_cache[task_id]
            else:
                urgency = self.calculate_dynamic_urgency(task)
                urgency_cache[task_id] = urgency

            print(f"Task ID: {task_id}, Importance: {importance:.2f}, Urgency: {urgency:.2f}")
            # Calculate combined score
            score = self.calculate_score(importance, urgency)
            # Calculate combined progress
            progress = self.calculate_combined_progress(task_id)
            task['importance'] = importance
            task['urgency'] = urgency
            task['score'] = score
            task['progress'] = progress

    def get_enriched_tasks(self) -> List[Dict[str, Any]]:
        return self.tasks
