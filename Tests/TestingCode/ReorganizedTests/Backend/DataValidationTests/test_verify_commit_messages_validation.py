import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

class TestVerifyCommitMessagesDataValidation(unittest.TestCase):
    """Test cases for verify_commit_messages data validation according to Unit_Testing.md standards."""

    def setUp(self):
        """Setup any necessary test data or state."""
        pass

    # Data Validation Tests - Verify data validation logic in models and services
    def test_check_commit_message_standard_with_special_characters(self):
        """Test check_commit_message_standard with special characters."""
        # Import the module
        from project_management.verify_commit_messages import check_commit_message_standard
        
        # Test with special characters
        result = check_commit_message_standard("[NEW STANDARD] Fix issue #123!")
        self.assertTrue(result)

    def test_check_commit_message_standard_with_unicode(self):
        """Test check_commit_message_standard with unicode characters."""
        # Import the module
        from project_management.verify_commit_messages import check_commit_message_standard
        
        # Test with unicode characters
        result = check_commit_message_standard("[NEW STANDARD] حل مشکل در ماژول")
        self.assertTrue(result)

    def test_check_commit_message_standard_with_long_message(self):
        """Test check_commit_message_standard with long message."""
        # Import the module
        from project_management.verify_commit_messages import check_commit_message_standard
        
        # Test with long message
        long_message = "[NEW STANDARD] " + "a" * 1000
        result = check_commit_message_standard(long_message)
        self.assertTrue(result)

    def test_check_commit_message_standard_with_empty_message(self):
        """Test check_commit_message_standard with empty message."""
        # Import the module
        from project_management.verify_commit_messages import check_commit_message_standard
        
        # Test with empty message (just the prefix)
        result = check_commit_message_standard("[NEW STANDARD] ")
        self.assertTrue(result)

    def test_check_commit_message_standard_with_whitespace_only(self):
        """Test check_commit_message_standard with whitespace only after prefix."""
        # Import the module
        from project_management.verify_commit_messages import check_commit_message_standard
        
        # Test with whitespace only after prefix
        result = check_commit_message_standard("[NEW STANDARD]    ")
        self.assertTrue(result)

    def test_check_commit_message_standard_with_html_content(self):
        """Test check_commit_message_standard with HTML content."""
        # Import the module
        from project_management.verify_commit_messages import check_commit_message_standard
        
        # Test with HTML content
        result = check_commit_message_standard("[NEW STANDARD] <b>Fix bug</b>")
        self.assertTrue(result)

    def test_check_commit_message_standard_with_sql_keywords(self):
        """Test check_commit_message_standard with SQL keywords."""
        # Import the module
        from project_management.verify_commit_messages import check_commit_message_standard
        
        # Test with SQL keywords
        result = check_commit_message_standard("[NEW STANDARD] SELECT * FROM users")
        self.assertTrue(result)

    def test_check_commit_message_standard_with_json_like_content(self):
        """Test check_commit_message_standard with JSON-like content."""
        # Import the module
        from project_management.verify_commit_messages import check_commit_message_standard
        
        # Test with JSON-like content
        result = check_commit_message_standard('[NEW STANDARD] {"key": "value"}')
        self.assertTrue(result)

    def test_check_commit_message_standard_with_xml_like_content(self):
        """Test check_commit_message_standard with XML-like content."""
        # Import the module
        from project_management.verify_commit_messages import check_commit_message_standard
        
        # Test with XML-like content
        result = check_commit_message_standard("[NEW STANDARD] <note><to>User</to></note>")
        self.assertTrue(result)

    def test_check_commit_message_standard_with_markdown_content(self):
        """Test check_commit_message_standard with markdown content."""
        # Import the module
        from project_management.verify_commit_messages import check_commit_message_standard
        
        # Test with markdown content
        result = check_commit_message_standard("[NEW STANDARD] **Fix bug**")
        self.assertTrue(result)

    def test_check_commit_message_standard_with_code_snippet(self):
        """Test check_commit_message_standard with code snippet."""
        # Import the module
        from project_management.verify_commit_messages import check_commit_message_standard
        
        # Test with code snippet
        result = check_commit_message_standard("[NEW STANDARD] def func(): pass")
        self.assertTrue(result)

    def test_check_commit_message_standard_with_url(self):
        """Test check_commit_message_standard with URL."""
        # Import the module
        from project_management.verify_commit_messages import check_commit_message_standard
        
        # Test with URL
        result = check_commit_message_standard("[NEW STANDARD] Fix bug http://example.com")
        self.assertTrue(result)

    def test_check_commit_message_standard_with_email(self):
        """Test check_commit_message_standard with email."""
        # Import the module
        from project_management.verify_commit_messages import check_commit_message_standard
        
        # Test with email
        result = check_commit_message_standard("[NEW STANDARD] Fix bug user@example.com")
        self.assertTrue(result)

    def test_check_commit_message_standard_with_multilingual_content(self):
        """Test check_commit_message_standard with multilingual content."""
        # Import the module
        from project_management.verify_commit_messages import check_commit_message_standard
        
        # Test with multilingual content
        result = check_commit_message_standard("[NEW STANDARD] Fix bug in English و فارسی")
        self.assertTrue(result)

    def test_check_commit_message_standard_case_sensitivity(self):
        """Test check_commit_message_standard case sensitivity."""
        # Import the module
        from project_management.verify_commit_messages import check_commit_message_standard
        
        # Test with lowercase prefix (should fail)
        result = check_commit_message_standard("[new standard] This is a commit message")
        self.assertFalse(result)
        
        # Test with mixed case prefix (should fail)
        result = check_commit_message_standard("[New Standard] This is a commit message")
        self.assertFalse(result)
        
        # Test with exact prefix (should pass)
        result = check_commit_message_standard("[NEW STANDARD] This is a commit message")
        self.assertTrue(result)

    def test_check_commit_message_standard_with_prefix_in_middle(self):
        """Test check_commit_message_standard with prefix in middle of message."""
        # Import the module
        from project_management.verify_commit_messages import check_commit_message_standard
        
        # Test with prefix in middle (should fail)
        result = check_commit_message_standard("This is [NEW STANDARD] a commit message")
        self.assertFalse(result)

    def test_check_commit_message_standard_with_prefix_at_end(self):
        """Test check_commit_message_standard with prefix at end of message."""
        # Import the module
        from project_management.verify_commit_messages import check_commit_message_standard
        
        # Test with prefix at end (should fail)
        result = check_commit_message_standard("This is a commit message [NEW STANDARD]")
        self.assertFalse(result)

    @patch('project_management.verify_commit_messages.run_git_command')
    def test_get_commit_list_with_special_branch_names(self, mock_run_git_command):
        """Test get_commit_list with special branch names."""
        # Setup mock with special branch names
        mock_run_git_command.return_value = (True, "commit1\ncommit2")
        
        # Import the module
        from project_management.verify_commit_messages import get_commit_list
        
        # Test with branch name containing special characters
        commits = get_commit_list("feature/branch#123")
        mock_run_git_command.assert_called_with(["rev-list", "--reverse", "feature/branch#123"])
        
        # Test with branch name containing unicode
        commits = get_commit_list("وظيفة/فرع")
        mock_run_git_command.assert_called_with(["rev-list", "--reverse", "وظيفة/فرع"])

    @patch('project_management.verify_commit_messages.run_git_command')
    def test_get_commit_message_with_special_commit_hashes(self, mock_run_git_command):
        """Test get_commit_message with special commit hashes."""
        # Setup mock with special commit hashes
        mock_run_git_command.return_value = (True, "commit message")
        
        # Import the module
        from project_management.verify_commit_messages import get_commit_message
        
        # Test with commit hash containing special characters
        message = get_commit_message("commit#123")
        mock_run_git_command.assert_called_with(["log", "-1", "--pretty=%B", "commit#123"])
        
        # Test with commit hash containing unicode
        message = get_commit_message("التزام123")
        mock_run_git_command.assert_called_with(["log", "-1", "--pretty=%B", "التزام123"])

    @patch('project_management.verify_commit_messages.run_git_command')
    def test_get_commit_message_with_special_characters_in_message(self, mock_run_git_command):
        """Test get_commit_message with special characters in commit message."""
        # Setup mock with special characters in message
        special_message = "Fix issue #123! @user"
        mock_run_git_command.return_value = (True, special_message)
        
        # Import the module
        from project_management.verify_commit_messages import get_commit_message
        
        message = get_commit_message("commit1")
        
        # Verify results
        self.assertEqual(message, special_message)

if __name__ == "__main__":
    unittest.main()
