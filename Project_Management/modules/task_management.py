from typing import List, Dict, Any

class TaskManager:
    def __init__(self, tasks: List[Dict[str, Any]]):
        self.tasks = tasks

    def complete_top_important_tasks(self, top_n: int = 10) -> List[Dict[str, Any]]:
        """
        Mark top N important tasks as completed with 100% progress.
        If already completed, skip but ensure progress is 100%.
        Returns the updated list of tasks.
        """
        # Sort tasks by importance descending
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
                # Already completed, ensure progress is 100%
                task['progress'] = 1.0
                count += 1
        return self.tasks
