import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

class TestCliServiceFunctions(unittest.TestCase):
    """Test cases for CLI service functions according to Unit_Testing.md standards."""

    def setUp(self):
        """Setup any necessary test data or state."""
        pass

    # Service Function Tests - Test individual backend service functions for correct output
    @patch('project_management.main.install')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_cli_install_command(self, mock_parse_args, mock_install):
        """Test main_cli with install command."""
        mock_parse_args.return_value.command = 'install'
        
        # Import the cli module after mocking
        from project_management.cli import main_cli
        
        main_cli()
        
        # Verify that install was called
        mock_install.assert_called_once()

    @patch('project_management.main.start')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_cli_start_command(self, mock_parse_args, mock_start):
        """Test main_cli with start command."""
        mock_parse_args.return_value.command = 'start'
        
        # Import the cli module after mocking
        from project_management.cli import main_cli
        
        main_cli()
        
        # Verify that start was called
        mock_start.assert_called_once()

    @patch('project_management.main.status')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_cli_status_command(self, mock_parse_args, mock_status):
        """Test main_cli with status command."""
        mock_parse_args.return_value.command = 'status'
        
        # Import the cli module after mocking
        from project_management.cli import main_cli
        
        main_cli()
        
        # Verify that status was called
        mock_status.assert_called_once()

    @patch('project_management.main.setup')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_cli_setup_command(self, mock_parse_args, mock_setup):
        """Test main_cli with setup command."""
        mock_parse_args.return_value.command = 'setup'
        
        # Import the cli module after mocking
        from project_management.cli import main_cli
        
        main_cli()
        
        # Verify that setup was called
        mock_setup.assert_called_once()

    @patch('project_management.main.help')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_cli_help_command(self, mock_parse_args, mock_help):
        """Test main_cli with help command."""
        mock_parse_args.return_value.command = 'help'
        
        # Import the cli module after mocking
        from project_management.cli import main_cli
        
        main_cli()
        
        # Verify that help was called
        mock_help.assert_called_once()

    @patch('project_management.main.help')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_cli_unknown_command(self, mock_parse_args, mock_help):
        """Test main_cli with unknown command."""
        mock_parse_args.return_value.command = 'unknown'
        
        # Import the cli module after mocking
        from project_management.cli import main_cli
        
        main_cli()
        
        # Verify that help was called and sys.exit was called
        mock_help.assert_called_once()

if __name__ == "__main__":
    unittest.main()
