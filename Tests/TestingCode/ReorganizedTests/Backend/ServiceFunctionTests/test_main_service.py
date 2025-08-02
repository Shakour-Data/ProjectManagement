import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

class TestMainServiceFunctions(unittest.TestCase):
    """Test cases for main service functions according to Unit_Testing.md standards."""

    def setUp(self):
        """Setup any necessary test data or state."""
        pass

    # Service Function Tests - Test individual backend service functions for correct output
    @patch('builtins.print')
    def test_install_function(self, mock_print):
        """Test install function."""
        # Import the main module
        from project_management.main import install
        
        install()
        
        # Verify that print was called with the expected message
        mock_print.assert_called_once_with("Installation complete. Please add your JSON input files to the input directory.")

    @patch('project_management.modules.reporting.top_n_by_importance')
    @patch('project_management.modules.reporting.top_n_by_urgency')
    @patch('project_management.modules.reporting.eisenhower_matrix')
    @patch('project_management.main.InputHandler.read_json_files')
    @patch('builtins.print')
    def test_start_function_with_valid_inputs(self, mock_print, mock_read_json_files, mock_eisenhower_matrix, 
                                               mock_top_n_by_urgency, mock_top_n_by_importance):
        """Test start function with valid inputs."""
        # Setup mocks
        mock_read_json_files.return_value = {
            'detailed_wbs.json': [
                {'title': 'Task 1', 'importance': 5, 'urgency': 3},
                {'title': 'Task 2', 'importance': 8, 'urgency': 7}
            ]
        }
        mock_top_n_by_importance.return_value = [
            {'title': 'Task 2', 'importance': 8, 'urgency': 7}
        ]
        mock_top_n_by_urgency.return_value = [
            {'title': 'Task 2', 'importance': 8, 'urgency': 7}
        ]
        mock_eisenhower_matrix.return_value = {
            'do_first': [{'title': 'Task 2', 'importance': 8, 'urgency': 7}],
            'schedule': [{'title': 'Task 1', 'importance': 5, 'urgency': 3}],
            'delegate': [],
            'eliminate': []
        }
        
        # Import the main module
        from project_management.main import start
        
        start()
        
        # Verify that the functions were called
        mock_read_json_files.assert_called_once()
        mock_top_n_by_importance.assert_called_once()
        mock_top_n_by_urgency.assert_called_once()
        mock_eisenhower_matrix.assert_called_once()
        # Verify that print was called multiple times
        self.assertGreater(mock_print.call_count, 0)

    @patch('project_management.main.InputHandler.read_json_files')
    @patch('builtins.print')
    def test_start_function_with_no_inputs(self, mock_print, mock_read_json_files):
        """Test start function with no inputs."""
        # Setup mocks
        mock_read_json_files.return_value = None
        
        # Import the main module
        from project_management.main import start
        
        start()
        
        # Verify that read_json_files was called
        mock_read_json_files.assert_called_once()
        # Verify that print was called with the error message
        mock_print.assert_any_call("Failed to load input files. Please check the input directory and JSON files.")

    @patch('project_management.main.InputHandler.read_json_files')
    @patch('builtins.print')
    def test_start_function_with_empty_inputs(self, mock_print, mock_read_json_files):
        """Test start function with empty inputs."""
        # Setup mocks
        mock_read_json_files.return_value = {
            'detailed_wbs.json': []
        }
        
        # Import the main module
        from project_management.main import start
        
        start()
        
        # Verify that read_json_files was called
        mock_read_json_files.assert_called_once()
        # Verify that print was called with the no task data message
        mock_print.assert_any_call("No task data found in input files.")

    @patch('builtins.print')
    def test_status_function(self, mock_print):
        """Test status function."""
        # Import the main module
        from project_management.main import status
        
        status()
        
        # Verify that print was called with the expected message
        mock_print.assert_called_once_with("Project Management Tool is installed and ready.")

    @patch('builtins.print')
    @patch('builtins.input')
    def test_help_function(self, mock_input, mock_print):
        """Test help function."""
        # Import the main module
        from project_management.main import help
        
        help()
        
        # Verify that print was called with the help text
        self.assertGreater(mock_print.call_count, 0)

if __name__ == "__main__":
    unittest.main()
