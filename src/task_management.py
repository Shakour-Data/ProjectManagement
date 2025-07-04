import datetime
from typing import List, Dict, Optional

class Task:
    def __init__(self, id: int, title: str, description: str = "", deadline: Optional[datetime.date] = None,
                 dependencies: Optional[List[int]] = None, assigned_to: Optional[List[str]] = None,
                 status: str = "pending", priority: int = 0, parent_id: Optional[int] = None,
                 urgency: Optional[float] = None, importance: Optional[float] = None,
                 github_issue_number: Optional[int] = None):
        self.id = id
        self.title = title
        self.description = description
        self.deadline = deadline
        self.dependencies = dependencies or []
        self.assigned_to = assigned_to or []
        self.status = status  # pending, in_progress, completed
        self.priority = priority
        self.parent_id = parent_id  # For hierarchical tasks
        self.urgency = urgency
        self.importance = importance
        self.github_issue_number = github_issue_number

class TaskManagement:
    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self.next_task_id = 1

    def parse_creative_input(self, input_text: str) -> Task:
        """
        Parse creative user input text into a formal Task object.
        This is a placeholder for NLP or rule-based parsing logic.
        """
        task = Task(id=self.next_task_id, title=input_text)
        self.tasks[self.next_task_id] = task
        self.next_task_id += 1
        return task

    def generate_wbs_from_idea(self, input_text: str) -> List[Task]:
        """
        Generate a hierarchical Work Breakdown Structure (WBS) from a creative idea input.
        This is a placeholder for integration with BLACKBOX AI or other NLP tools.
        Returns a list of Tasks with parent-child relationships up to 5 levels deep.
        """
        # Placeholder implementation: create a dummy 3-level WBS for demonstration
        root_task = Task(id=self.next_task_id, title=input_text)
        self.tasks[self.next_task_id] = root_task
        self.next_task_id += 1

        # Level 1 subtasks
        for i in range(1, 4):
            level1_task = Task(id=self.next_task_id, title=f"{input_text} - Subtask Level 1.{i}", parent_id=root_task.id)
            self.tasks[self.next_task_id] = level1_task
            self.next_task_id += 1

            # Level 2 subtasks
            for j in range(1, 3):
                level2_task = Task(id=self.next_task_id, title=f"{input_text} - Subtask Level 2.{i}.{j}", parent_id=level1_task.id)
                self.tasks[self.next_task_id] = level2_task
                self.next_task_id += 1

        return list(self.tasks.values())

    def calculate_urgency_importance(self):
        """
        Calculate urgency and importance for each task at the lowest level,
        then propagate these values up the hierarchy.
        Urgency relates to time and deadlines, importance relates to task significance.
        """
        # Calculate urgency and importance for leaf tasks
        for task in self.tasks.values():
            if not any(t.parent_id == task.id for t in self.tasks.values()):
                # Leaf task
                task.urgency = self._calculate_urgency(task)
                task.importance = self._calculate_importance(task)

        # Propagate urgency and importance up the hierarchy
        def propagate(task_id):
            children = [t for t in self.tasks.values() if t.parent_id == task_id]
            if not children:
                return self.tasks[task_id].urgency, self.tasks[task_id].importance
            urgency_sum = 0
            importance_sum = 0
            for child in children:
                u, i = propagate(child.id)
                urgency_sum += u
                importance_sum += i
            # Average or weighted sum can be used; here simple sum
            self.tasks[task_id].urgency = urgency_sum
            self.tasks[task_id].importance = importance_sum
            return urgency_sum, importance_sum

        # Find root tasks (no parent)
        root_tasks = [t for t in self.tasks.values() if t.parent_id is None]
        for root in root_tasks:
            propagate(root.id)

    def _calculate_urgency(self, task: Task) -> float:
        """
        Calculate urgency based on deadline proximity and other factors.
        Urgency is distinct from importance.
        """
        if task.deadline:
            days_left = (task.deadline - datetime.date.today()).days
            urgency = max(0, 1 / (days_left + 1))  # More urgent if deadline is near
        else:
            urgency = 0.1  # Default low urgency
        # Additional factors can be added here
        return urgency

    def _calculate_importance(self, task: Task) -> float:
        """
        Calculate importance based on task priority and other attributes.
        """
        base_importance = task.priority if task.priority else 1.0
        # Additional factors can be added here
        return base_importance

    def prioritize_tasks(self):
        """
        Prioritize tasks based on calculated urgency and importance.
        """
        self.calculate_urgency_importance()

        def task_priority(task: Task):
            # Combine urgency and importance with different weights
            return (task.importance * 0.7 + task.urgency * 0.3, task.deadline or datetime.date.max)

        sorted_tasks = sorted(self.tasks.values(), key=task_priority, reverse=True)
        return sorted_tasks

    def schedule_tasks(self):
        """
        Suggest task scheduling based on priorities and dependencies.
        """
        # Placeholder: return tasks in priority order
        return self.prioritize_tasks()

    def detect_conflicts(self):
        """
        Detect conflicts in task dependencies or assignments.
        """
        conflicts = []
        for task in self.tasks.values():
            for dep_id in task.dependencies:
                if dep_id not in self.tasks:
                    conflicts.append(f"Task {task.id} depends on unknown task {dep_id}")
        return conflicts

    def assign_task(self, task_id: int, users: List[str]):
        """
        Assign task to one or more users.
        """
        if task_id in self.tasks:
            self.tasks[task_id].assigned_to = users
            return True
        return False
