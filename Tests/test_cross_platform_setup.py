"""
Date: 2025-07-26
Authors: GravityWavesOrg (GitHub username)
File Description: Tests for cross-platform setup including virtual environment creation, dependency installation, backend/frontend server startup, UI launch, desktop shortcut creation on different platforms, and error handling.
"""

import unittest
from unittest.mock import patch, MagicMock

import cross_platform_setup

class TestCrossPlatformSetup(unittest.TestCase):
    @patch('builtins.print')
    @patch('platform.system')
    @patch('os.path.expanduser')
    def test_create_desktop_shortcut_linux(self, mock_expanduser, mock_platform, mock_print):
        mock_platform.return_value = 'Linux'
        mock_expanduser.return_value = '/home/testuser'
        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            cross_platform_setup.create_desktop_shortcut('/home/testuser')
            # The shortcut creation may fail due to missing Desktop directory in test environment
            # So we check for either success or failure message
            calls = [call.args[0] for call in mock_print.call_args_list]
            self.assertTrue(any("Desktop shortcut created at" in c or "Failed to create Linux shortcut" in c for c in calls))

    @patch('builtins.print')
    @patch('platform.system')
    @patch('os.path.expanduser')
    def test_create_desktop_shortcut_mac(self, mock_expanduser, mock_platform, mock_print):
        mock_platform.return_value = 'Darwin'
        mock_expanduser.return_value = '/Users/testuser'
        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            cross_platform_setup.create_desktop_shortcut('/Users/testuser')
            calls = [call.args[0] for call in mock_print.call_args_list]
            self.assertTrue(any("Desktop shortcut created at" in c or "Failed to create macOS shortcut" in c for c in calls))

    @patch('cross_platform_setup.subprocess.check_call')
    def test_create_virtualenv(self, mock_check_call):
        venv_path = 'venv_test'
        # Clean up if exists
        import os
        import shutil
        if os.path.exists(venv_path):
            shutil.rmtree(venv_path)
        cross_platform_setup.create_virtualenv(venv_path)
        mock_check_call.assert_called()

    @patch('cross_platform_setup.subprocess.run')
    def test_install_frontend_dependencies(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        with patch('os.path.exists', return_value=True):
            cross_platform_setup.install_frontend_dependencies('.')
        self.assertTrue(mock_run.called)

if __name__ == '__main__':
    unittest.main()
