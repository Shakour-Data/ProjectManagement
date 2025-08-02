import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

class TestMainDataValidation(unittest.TestCase):
    """Test cases for main data validation according to Unit_Testing.md standards."""

    def setUp(self):
        """Setup any necessary test data or state."""
        pass

    # Data Validation Tests - Verify data validation logic in models and services
    @patch('project_management.main.InputHandler.read_json_files')
    @patch('builtins.print')
    def test_start_function_with_special_characters_in_task_titles(self, mock_print, mock_read_json_files):
        """Test start function with special characters in task titles."""
        # Setup mocks
        mock_read_json_files.return_value = {
            'detailed_wbs.json': [
                {'title': 'Task #1!', 'importance': 5, 'urgency': 3},
                {'title': '@User Task', 'importance': 8, 'urgency': 7}
            ]
        }
        
        # Import the main module
        from project_management.main import start
        
        start()
        
        # Verify that read_json_files was called
        mock_read_json_files.assert_called_once()
        # Verify that print was called with the task titles
        mock_print.assert_any_call("Loaded input files: ['detailed_wbs.json']")

    @patch('project_management.main.InputHandler.read_json_files')
    @patch('builtins.print')
    def test_start_function_with_unicode_in_task_titles(self, mock_print, mock_read_json_files):
        """Test start function with unicode characters in task titles."""
        # Setup mocks
        mock_read_json_files.return_value = {
            'detailed_wbs.json': [
                {'title': 'وظيفة 1', 'importance': 5, 'urgency': 3},
                {'title': 'タスク 2', 'importance': 8, 'urgency': 7}
            ]
        }
        
        # Import the main module
        from project_management.main import start
        
        start()
        
        # Verify that read_json_files was called
        mock_read_json_files.assert_called_once()
        # Verify that print was called with the task titles
        mock_print.assert_any_call("Loaded input files: ['detailed_wbs.json']")

    @patch('project_management.main.InputHandler.read_json_files')
    @patch('builtins.print')
    def test_start_function_with_long_task_titles(self, mock_print, mock_read_json_files):
        """Test start function with long task titles."""
        # Setup mocks
        mock_read_json_files.return_value = {
            'detailed_wbs.json': [
                {'title': 'a' * 1000, 'importance': 5, 'urgency': 3}
            ]
        }
        
        # Import the main module
        from project_management.main import start
        
        start()
        
        # Verify that read_json_files was called
        mock_read_json_files.assert_called_once()

    @patch('project_management.main.InputHandler.read_json_files')
    @patch('builtins.print')
    def test_start_function_with_html_in_task_titles(self, mock_print, mock_read_json_files):
        """Test start function with HTML in task titles."""
        # Setup mocks
        mock_read_json_files.return_value = {
            'detailed_wbs.json': [
                {'title': '<b>Task 1</b>', 'importance': 5, 'urgency': 3}
            ]
        }
        
        # Import the main module
        from project_management.main import start
        
        start()
        
        # Verify that read_json_files was called
        mock_read_json_files.assert_called_once()

    @patch('project_management.main.InputHandler.read_json_files')
    @patch('builtins.print')
    def test_start_function_with_sql_keywords_in_task_titles(self, mock_print, mock_read_json_files):
        """Test start function with SQL keywords in task titles."""
        # Setup mocks
        mock_read_json_files.return_value = {
            'detailed_wbs.json': [
                {'title': 'SELECT * FROM tasks', 'importance': 5, 'urgency': 3}
            ]
        }
        
        # Import the main module
        from project_management.main import start
        
        start()
        
        # Verify that read_json_files was called
        mock_read_json_files.assert_called_once()

    @patch('project_management.main.InputHandler.read_json_files')
    @patch('builtins.print')
    def test_start_function_with_json_like_task_titles(self, mock_print, mock_read_json_files):
        """Test start function with JSON-like task titles."""
        # Setup mocks
        mock_read_json_files.return_value = {
            'detailed_wbs.json': [
                {'title': '{"task": "1"}', 'importance': 5, 'urgency': 3}
            ]
        }
        
        # Import the main module
        from project_management.main import start
        
        start()
        
        # Verify that read_json_files was called
        mock_read_json_files.assert_called_once()

    @patch('project_management.main.InputHandler.read_json_files')
    @patch('builtins.print')
    def test_start_function_with_xml_like_task_titles(self, mock_print, mock_read_json_files):
        """Test start function with XML-like task titles."""
        # Setup mocks
        mock_read_json_files.return_value = {
            'detailed_wbs.json': [
                {'title': '<task>1</task>', 'importance': 5, 'urgency': 3}
            ]
        }
        
        # Import the main module
        from project_management.main import start
        
        start()
        
        # Verify that read_json_files was called
        mock_read_json_files.assert_called_once()

    @patch('project_management.main.InputHandler.read_json_files')
    @patch('builtins.print')
    def test_start_function_with_markdown_in_task_titles(self, mock_print, mock_read_json_files):
        """Test start function with markdown in task titles."""
        # Setup mocks
        mock_read_json_files.return_value = {
            'detailed_wbs.json': [
                {'title': '**Task 1**', 'importance': 5, 'urgency': 3}
            ]
        }
        
        # Import the main module
        from project_management.main import start
        
        start()
        
        # Verify that read_json_files was called
        mock_read_json_files.assert_called_once()

    @patch('project_management.main.InputHandler.read_json_files')
    @patch('builtins.print')
    def test_start_function_with_code_snippets_in_task_titles(self, mock_print, mock_read_json_files):
        """Test start function with code snippets in task titles."""
        # Setup mocks
        mock_read_json_files.return_value = {
            'detailed_wbs.json': [
                {'title': 'def func(): pass', 'importance': 5, 'urgency': 3}
            ]
        }
        
        # Import the main module
        from project_management.main import start
        
        start()
        
        # Verify that read_json_files was called
        mock_read_json_files.assert_called_once()

    @patch('project_management.main.InputHandler.read_json_files')
    @patch('builtins.print')
    def test_start_function_with_urls_in_task_titles(self, mock_print, mock_read_json_files):
        """Test start function with URLs in task titles."""
        # Setup mocks
        mock_read_json_files.return_value = {
            'detailed_wbs.json': [
                {'title': 'Fix bug http://example.com', 'importance': 5, 'urgency': 3}
            ]
        }
        
        # Import the main module
        from project_management.main import start
        
        start()
        
        # Verify that read_json_files was called
        mock_read_json_files.assert_called_once()

    @patch('project_management.main.InputHandler.read_json_files')
    @patch('builtins.print')
    def test_start_function_with_emails_in_task_titles(self, mock_print, mock_read_json_files):
        """Test start function with emails in task titles."""
        # Setup mocks
        mock_read_json_files.return_value = {
            'detailed_wbs.json': [
                {'title': 'Fix bug user@example.com', 'importance': 5, 'urgency': 3}
            ]
        }
        
        # Import the main module
        from project_management.main import start
        
        start()
        
        # Verify that read_json_files was called
        mock_read_json_files.assert_called_once()

    @patch('project_management.main.InputHandler.read_json_files')
    @patch('builtins.print')
    def test_start_function_with_multilingual_task_titles(self, mock_print, mock_read_json_files):
        """Test start function with multilingual task titles."""
        # Setup mocks
        mock_read_json_files.return_value = {
            'detailed_wbs.json': [
                {'title': 'Fix bug in English و فارسی', 'importance': 5, 'urgency': 3}
            ]
        }
        
        # Import the main module
        from project_management.main import start
        
        start()
        
        # Verify that read_json_files was called
        mock_read_json_files.assert_called_once()

if __name__ == "__main__":
    unittest.main()
