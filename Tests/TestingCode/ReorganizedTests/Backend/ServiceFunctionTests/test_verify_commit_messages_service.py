import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

class TestVerifyCommitMessagesServiceFunctions(unittest.TestCase):
    """Test cases for verify_commit_messages service functions according to Unit_Testing.md standards."""

    def setUp(self):
        """Setup any necessary test data or state."""
        pass

    # Service Function Tests - Test individual backend service functions for correct output
    @patch('project_management.verify_commit_messages.subprocess.run')
    def test_run_git_command_success(self, mock_subprocess_run):
        """Test run_git_command with successful execution."""
        # Setup mock
        mock_result = MagicMock()
        mock_result.stdout = "success output"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_subprocess_run.return_value = mock_result
        
        # Import the module
        from project_management.verify_commit_messages import run_git_command
        
        success, output = run_git_command(["status"])
        
        # Verify results
        self.assertTrue(success)
        self.assertEqual(output, "success output")
        mock_subprocess_run.assert_called_once_with(["git", "status"], capture_output=True, text=True, check=True)

    @patch('project_management.verify_commit_messages.subprocess.run')
    def test_run_git_command_failure(self, mock_subprocess_run):
        """Test run_git_command with failed execution."""
        # Setup mock to raise exception
        mock_subprocess_run.side_effect = Exception("git command failed")
        
        # Import the module
        from project_management.verify_commit_messages import run_git_command
        
        success, output = run_git_command(["status"])
        
        # Verify results
        self.assertFalse(success)
        self.assertEqual(output, "")

    @patch('project_management.verify_commit_messages.run_git_command')
    def test_get_commit_list_success(self, mock_run_git_command):
        """Test get_commit_list with successful execution."""
        # Setup mock
        mock_run_git_command.return_value = (True, "commit1\ncommit2\ncommit3")
        
        # Import the module
        from project_management.verify_commit_messages import get_commit_list
        
        commits = get_commit_list("PM01")
        
        # Verify results
        self.assertEqual(commits, ["commit1", "commit2", "commit3"])
        mock_run_git_command.assert_called_once_with(["rev-list", "--reverse", "PM01"])

    @patch('project_management.verify_commit_messages.run_git_command')
    def test_get_commit_list_failure(self, mock_run_git_command):
        """Test get_commit_list with failed execution."""
        # Setup mock
        mock_run_git_command.return_value = (False, "error")
        
        # Import the module
        from project_management.verify_commit_messages import get_commit_list
        
        commits = get_commit_list("PM01")
        
        # Verify results
        self.assertEqual(commits, [])
        mock_run_git_command.assert_called_once_with(["rev-list", "--reverse", "PM01"])

    @patch('project_management.verify_commit_messages.run_git_command')
    def test_get_commit_message_success(self, mock_run_git_command):
        """Test get_commit_message with successful execution."""
        # Setup mock
        mock_run_git_command.return_value = (True, "commit message")
        
        # Import the module
        from project_management.verify_commit_messages import get_commit_message
        
        message = get_commit_message("commit1")
        
        # Verify results
        self.assertEqual(message, "commit message")
        mock_run_git_command.assert_called_once_with(["log", "-1", "--pretty=%B", "commit1"])

    @patch('project_management.verify_commit_messages.run_git_command')
    def test_get_commit_message_failure(self, mock_run_git_command):
        """Test get_commit_message with failed execution."""
        # Setup mock
        mock_run_git_command.return_value = (False, "error")
        
        # Import the module
        from project_management.verify_commit_messages import get_commit_message
        
        message = get_commit_message("commit1")
        
        # Verify results
        self.assertEqual(message, "")
        mock_run_git_command.assert_called_once_with(["log", "-1", "--pretty=%B", "commit1"])

    def test_check_commit_message_standard_success(self):
        """Test check_commit_message_standard with conforming message."""
        # Import the module
        from project_management.verify_commit_messages import check_commit_message_standard
        
        # Test with conforming message
        result = check_commit_message_standard("[NEW STANDARD] This is a commit message")
        self.assertTrue(result)

    def test_check_commit_message_standard_failure(self):
        """Test check_commit_message_standard with non-conforming message."""
        # Import the module
        from project_management.verify_commit_messages import check_commit_message_standard
        
        # Test with non-conforming message
        result = check_commit_message_standard("This is a commit message")
        self.assertFalse(result)

    @patch('project_management.verify_commit_messages.get_commit_list')
    @patch('project_management.verify_commit_messages.get_commit_message')
    @patch('project_management.verify_commit_messages.check_commit_message_standard')
    @patch('builtins.print')
    def test_verify_commit_messages_all_conforming(self, mock_print, mock_check_commit_message_standard, 
                                                   mock_get_commit_message, mock_get_commit_list):
        """Test verify_commit_messages when all commits conform to standard."""
        # Setup mocks
        mock_get_commit_list.return_value = ["commit1", "commit2"]
        mock_get_commit_message.return_value = "[NEW STANDARD] Commit message"
        mock_check_commit_message_standard.return_value = True
        
        # Import the module
        from project_management.verify_commit_messages import verify_commit_messages
        
        verify_commit_messages("PM01")
        
        # Verify that print was called with the success message
        mock_print.assert_any_call("All commit messages in branch PM01 conform to the new standard.")

    @patch('project_management.verify_commit_messages.get_commit_list')
    @patch('project_management.verify_commit_messages.get_commit_message')
    @patch('project_management.verify_commit_messages.check_commit_message_standard')
    @patch('builtins.print')
    def test_verify_commit_messages_some_non_conforming(self, mock_print, mock_check_commit_message_standard, 
                                                        mock_get_commit_message, mock_get_commit_list):
        """Test verify_commit_messages when some commits don't conform to standard."""
        # Setup mocks
        mock_get_commit_list.return_value = ["commit1", "commit2"]
        mock_get_commit_message.side_effect = [
            "[NEW STANDARD] Conforming message",
            "Non-conforming message"
        ]
        mock_check_commit_message_standard.side_effect = [True, False]
        
        # Import the module
        from project_management.verify_commit_messages import verify_commit_messages
        
        verify_commit_messages("PM01")
        
        # Verify that print was called with the non-conforming message info
        mock_print.assert_any_call("Found 1 commit(s) not conforming to the new standard in branch PM01:")

if __name__ == "__main__":
    unittest.main()
