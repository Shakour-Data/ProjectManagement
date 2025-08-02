import unittest
from project_management.modules.main_modules.task_management import TaskManagement, Task

class TestTaskManagementServiceFunctions(unittest.TestCase):
    """Test cases for TaskManagement service functions according to Unit_Testing.md standards."""

    def setUp(self):
        """Setup any necessary test data or state."""
        self.tm = TaskManagement()

    # Service Function Tests - Test individual backend service functions for correct output
    def test_parse_creative_input_basic(self):
        """Test parse_creative_input with basic input."""
        input_text = "Create a new feature"
        task = self.tm.parse_creative_input(input_text)
        self.assertIsInstance(task, Task)
        self.assertEqual(task.title, input_text)
        self.assertEqual(task.id, 1)

    def test_mark_task_completed_basic(self):
        """Test mark_task_completed with valid task ID."""
        # First create a task
        task = self.tm.parse_creative_input("Test task")
        # Then mark it as completed
        result = self.tm.mark_task_completed(task.id)
        self.assertTrue(result)
        self.assertEqual(self.tm.tasks[task.id].status, 'completed')

    def test_assign_task_basic(self):
        """Test assign_task with valid task ID and users."""
        # First create a task
        task = self.tm.parse_creative_input("Test task")
        # Then assign it to users
        users = ["user1", "user2"]
        result = self.tm.assign_task(task.id, users)
        self.assertTrue(result)
        self.assertEqual(self.tm.tasks[task.id].assigned_to, users)

    def test_update_workflow_steps_from_commit_message_basic(self):
        """Test update_workflow_steps_from_commit_message with valid commit message."""
        # First create a task
        task = self.tm.parse_creative_input("Test task")
        # Then update workflow steps from commit message
        commit_message = "Task 1: Coding done"
        self.tm.update_workflow_steps_from_commit_message(commit_message)
        self.assertTrue(self.tm.tasks[task.id].workflow_steps["Coding"])

if __name__ == "__main__":
    unittest.main()
