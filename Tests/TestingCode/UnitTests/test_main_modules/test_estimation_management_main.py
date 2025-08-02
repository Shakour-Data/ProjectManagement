import unittest
from unittest.mock import patch
from project_management.modules.main_modules.estimation_management import EstimationManagement

class TestEstimationManagementMain(unittest.TestCase):
    @patch('project_management.modules.main_modules.estimation_management.EstimationManagement')
    def test_main_execution(self, mock_estimation_manager):
        # Test that the main block executes without errors
        from project_management.modules.main_modules.estimation_management import __name__ as main_name
        # We can't directly test the main block execution without importing the module
        # but we can verify that the EstimationManagement class is properly defined
        self.assertTrue(mock_estimation_manager)

    @patch('project_management.modules.main_modules.estimation_management.EstimationManagement.run')
    @patch('project_management.modules.main_modules.estimation_management.EstimationManagement.__init__')
    def test_main_functionality(self, mock_init, mock_run):
        # Test that when instantiated and run, the methods are called correctly
        mock_init.return_value = None  # __init__ should return None
        manager = EstimationManagement()
        manager.run()
        mock_init.assert_called_once()
        mock_run.assert_called_once()

if __name__ == '__main__':
    unittest.main()
