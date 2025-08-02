import unittest
from project_management.modules.main_modules.task_management import TaskManagement, Task
import datetime

class TestTaskManagementDataValidation(unittest.TestCase):
    """Test cases for TaskManagement data validation according to Unit_Testing.md standards."""

    def setUp(self):
        """Setup any necessary test data or state."""
        self.tm = TaskManagement()

    # Data Validation Tests - Verify data validation logic in models and services
    def test_parse_creative_input_with_special_characters(self):
        """Test parse_creative_input with special characters."""
        input_text = "Fix issue #123! @user"
        task = self.tm.parse_creative_input(input_text)
        self.assertIsInstance(task, Task)
        self.assertEqual(task.title, input_text)

    def test_parse_creative_input_with_unicode(self):
        """Test parse_creative_input with unicode characters."""
        input_text = "حل مشکل در ماژول"
        task = self.tm.parse_creative_input(input_text)
        self.assertIsInstance(task, Task)
        self.assertEqual(task.title, input_text)

    def test_parse_creative_input_with_long_text(self):
        """Test parse_creative_input with long text."""
        input_text = "a" * 1000
        task = self.tm.parse_creative_input(input_text)
        self.assertIsInstance(task, Task)
        self.assertEqual(task.title, input_text)

    def test_parse_creative_input_with_html_content(self):
        """Test parse_creative_input with HTML content."""
        input_text = "<b>Fix bug</b>"
        task = self.tm.parse_creative_input(input_text)
        self.assertIsInstance(task, Task)
        self.assertEqual(task.title, input_text)

    def test_parse_creative_input_with_sql_keywords(self):
        """Test parse_creative_input with SQL keywords."""
        input_text = "SELECT * FROM users"
        task = self.tm.parse_creative_input(input_text)
        self.assertIsInstance(task, Task)
        self.assertEqual(task.title, input_text)

    def test_parse_creative_input_with_json_like_text(self):
        """Test parse_creative_input with JSON-like text."""
        input_text = '{"key": "value"}'
        task = self.tm.parse_creative_input(input_text)
        self.assertIsInstance(task, Task)
        self.assertEqual(task.title, input_text)

    def test_parse_creative_input_with_xml_like_text(self):
        """Test parse_creative_input with XML-like text."""
        input_text = "<note><to>User</to></note>"
        task = self.tm.parse_creative_input(input_text)
        self.assertIsInstance(task, Task)
        self.assertEqual(task.title, input_text)

    def test_parse_creative_input_with_markdown(self):
        """Test parse_creative_input with markdown."""
        input_text = "**Fix bug**"
        task = self.tm.parse_creative_input(input_text)
        self.assertIsInstance(task, Task)
        self.assertEqual(task.title, input_text)

    def test_parse_creative_input_with_code_snippet(self):
        """Test parse_creative_input with code snippet."""
        input_text = "def func(): pass"
        task = self.tm.parse_creative_input(input_text)
        self.assertIsInstance(task, Task)
        self.assertEqual(task.title, input_text)

    def test_parse_creative_input_with_url(self):
        """Test parse_creative_input with URL."""
        input_text = "Fix bug http://example.com"
        task = self.tm.parse_creative_input(input_text)
        self.assertIsInstance(task, Task)
        self.assertEqual(task.title, input_text)

    def test_parse_creative_input_with_email(self):
        """Test parse_creative_input with email."""
        input_text = "Fix bug user@example.com"
        task = self.tm.parse_creative_input(input_text)
        self.assertIsInstance(task, Task)
        self.assertEqual(task.title, input_text)

    def test_parse_creative_input_with_multilingual_text(self):
        """Test parse_creative_input with multilingual text."""
        input_text = "Fix bug in English و فارسی"
        task = self.tm.parse_creative_input(input_text)
        self.assertIsInstance(task, Task)
        self.assertEqual(task.title, input_text)

    def test_assign_task_with_multiple_users(self):
        """Test assign_task with multiple users."""
        # First create a task
        task = self.tm.parse_creative_input("Test task")
        # Then assign it to multiple users
        users = ["user1", "user2", "user3"]
        result = self.tm.assign_task(task.id, users)
        self.assertTrue(result)
        self.assertEqual(self.tm.tasks[task.id].assigned_to, users)

    def test_assign_task_with_special_characters_in_usernames(self):
        """Test assign_task with special characters in usernames."""
        # First create a task
        task = self.tm.parse_creative_input("Test task")
        # Then assign it to users with special characters
        users = ["user@example.com", "user+name", "user_name"]
        result = self.tm.assign_task(task.id, users)
        self.assertTrue(result)
        self.assertEqual(self.tm.tasks[task.id].assigned_to, users)

    def test_assign_task_with_unicode_usernames(self):
        """Test assign_task with unicode usernames."""
        # First create a task
        task = self.tm.parse_creative_input("Test task")
        # Then assign it to users with unicode characters
        users = ["کاربر1", "用户2"]
        result = self.tm.assign_task(task.id, users)
        self.assertTrue(result)
        self.assertEqual(self.tm.tasks[task.id].assigned_to, users)

    def test_update_workflow_steps_from_commit_message_with_multiple_steps(self):
        """Test update_workflow_steps_from_commit_message with multiple workflow steps."""
        # First create a task
        task = self.tm.parse_creative_input("Test task")
        # Then update multiple workflow steps from commit message
        commit_message = "Task 1: Coding done. Task 1: Testing done."
        self.tm.update_workflow_steps_from_commit_message(commit_message)
        self.assertTrue(self.tm.tasks[task.id].workflow_steps["Coding"])
        self.assertTrue(self.tm.tasks[task.id].workflow_steps["Testing"])

    def test_update_workflow_steps_from_commit_message_with_special_characters(self):
        """Test update_workflow_steps_from_commit_message with special characters."""
        # First create a task
        task = self.tm.parse_creative_input("Test task")
        # Then update workflow steps from commit message with special characters
        commit_message = "Task 1: Fix issue #123 done"
        self.tm.update_workflow_steps_from_commit_message(commit_message)
        # The function should handle special characters gracefully

if __name__ == "__main__":
    unittest.main()
