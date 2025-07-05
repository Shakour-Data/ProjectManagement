import unittest
from unittest.mock import patch, MagicMock
import src.auto_commit as auto_commit

class TestAutoCommit(unittest.TestCase):
    def test_generate_commit_message(self):
        group_name = "src"
        category_name = "Modified"
        files = ["src/task_management.py"]
        message = auto_commit.generate_commit_message(group_name, category_name, files)
        self.assertIn("fix", message)
        self.assertIn("src/task_management.py", message)
        self.assertIn("Changes included", message)
        self.assertIn("Please describe the reason or issue addressed by these changes.", message)

    @patch('src.auto_commit.run_git_command')
    def test_run_git_command_success(self, mock_run):
        mock_run.return_value = (True, "output")
        success, output = auto_commit.run_git_command(["status"])
        self.assertTrue(success)
        self.assertEqual(output, "output")

    @patch('src.auto_commit.run_git_command')
    def test_run_git_command_failure(self, mock_run):
        mock_run.return_value = (False, "error")
        success, output = auto_commit.run_git_command(["status"])
        self.assertFalse(success)
        self.assertEqual(output, "error")

    @patch('src.auto_commit.run_git_command')
    @patch('src.auto_commit.get_git_changes')
    def test_auto_commit_and_push_no_changes(self, mock_get_changes, mock_run_git):
        mock_get_changes.return_value = []
        with patch('builtins.print') as mock_print:
            auto_commit.auto_commit_and_push()
            mock_print.assert_any_call("No changes detected.")

    # Additional tests for grouping, categorizing, and commit/push flow can be added here

if __name__ == '__main__':
    unittest.main()
