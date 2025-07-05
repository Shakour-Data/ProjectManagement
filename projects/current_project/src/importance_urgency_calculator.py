import json
import os

class ImportanceUrgencyCalculator:
    def __init__(self, wbs_data):
        """
        wbs_data: list of dicts representing tasks with hierarchical structure
        Each task dict should have:
            - id: unique identifier
            - title: task title
            - level: hierarchical level (int)
            - subtasks: list of subtasks (same structure)
            - other metadata as needed
        """
        self.wbs_data = wbs_data
        self.task_scores = {}

    def score_task(self, task):
        """
        Recursively score a task based on its subtasks or base criteria.
        Importance and urgency are scored 0-100.
        For leaf tasks, score based on given criteria (to be implemented).
        For parent tasks, average scores of subtasks.
        """
        if not task.get('subtasks'):
            # Leaf task scoring logic (example placeholders)
            importance = self.calculate_importance(task)
            urgency = self.calculate_urgency(task)
        else:
            importance_values = []
            urgency_values = []
            for subtask in task['subtasks']:
                sub_imp, sub_urg = self.score_task(subtask)
                importance_values.append(sub_imp)
                urgency_values.append(sub_urg)
            importance = sum(importance_values) / len(importance_values) if importance_values else 0
            urgency = sum(urgency_values) / len(urgency_values) if urgency_values else 0

        self.task_scores[task['id']] = {'importance': importance, 'urgency': urgency}
        return importance, urgency

    def calculate_importance(self, task):
        # Placeholder: Implement actual importance calculation based on criteria
        # Example factors: dependency, critical path, cost impact, stakeholder priority, etc.
        # For now, return a dummy value or parse from task metadata if available
        return task.get('importance_score', 50)

    def calculate_urgency(self, task):
        # Placeholder: Implement actual urgency calculation based on criteria
        # Example factors: deadline proximity, risk of delay, stakeholder pressure, etc.
        # For now, return a dummy value or parse from task metadata if available
        return task.get('urgency_score', 50)

    def calculate_all(self):
        for task in self.wbs_data:
            self.score_task(task)
        return self.task_scores

def load_wbs_from_file(filepath):
    import json
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def save_scores_to_json(scores, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(scores, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # Example usage
    wbs_file = os.path.join(os.path.dirname(__file__), '../docs/project_management/wbs_data.json')
    scores_file = os.path.join(os.path.dirname(__file__), '../docs/project_management/wbs_scores.json')
    wbs_data = load_wbs_from_file(wbs_file)
    calculator = ImportanceUrgencyCalculator(wbs_data)
    scores = calculator.calculate_all()
    save_scores_to_json(scores, scores_file)
    print(f"Importance and urgency scores saved to {scores_file}")
