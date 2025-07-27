import unittest
from unittest.mock import patch, MagicMock, call
import sys
import os
import platform

import cross_platform_setup

class TestCrossPlatformSetup(unittest.TestCase):

    @patch('cross_platform_setup.subprocess.run')
    def test_create_virtualenv(self, mock_run):
        venv_path = 'venv_test'
        if os.path.exists(venv_path):
            os.rmdir(venv_path)
        cross_platform_setup.create_virtualenv(venv_path)
        self.assertTrue(os.path.exists(venv_path) or mock_run.called)

    @patch('cross_platform_setup.subprocess.run')
    def test_install_python_dependencies(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        cross_platform_setup.install_python_dependencies('python')
        self.assertTrue(mock_run.called)

    @patch('cross_platform_setup.subprocess.run')
    def test_install_frontend_dependencies(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        with patch('os.path.exists', return_value=True):
            cross_platform_setup.install_frontend_dependencies()
        self.assertTrue(mock_run.called)

    @patch('cross_platform_setup.subprocess.Popen')
    def test_start_backend_server(self, mock_popen):
        mock_popen.return_value = MagicMock()
        proc = cross_platform_setup.start_backend_server('python')
        self.assertIsNotNone(proc)

    @patch('cross_platform_setup.subprocess.Popen')
    def test_start_frontend_server(self, mock_popen):
        mock_popen.return_value = MagicMock()
        proc = cross_platform_setup.start_frontend_server()
        self.assertIsNotNone(proc)

    @patch('cross_platform_setup.subprocess.Popen')
    @patch('platform.system')
    def test_open_browser(self, mock_platform, mock_popen):
        mock_popen.return_value = MagicMock()
        mock_platform.return_value = 'Linux'
        cross_platform_setup.open_browser()
        mock_popen.assert_called()

    @patch('builtins.print')
    @patch('platform.system')
    @patch('os.path.expanduser')
    def test_create_desktop_shortcut_windows_missing_pywin32(self, mock_expanduser, mock_platform, mock_print):
        mock_platform.return_value = 'Windows'
        mock_expanduser.return_value = 'C:\\Users\\TestUser'
        with patch.dict('sys.modules', {'pythoncom': None, 'win32com.shell': None, 'win32com.client': None}):
            cross_platform_setup.create_desktop_shortcut()
        mock_print.assert_any_call("pywin32 is required to create Windows shortcuts. Please install it manually using 'pip install pywin32'.")

    @patch('builtins.print')
    @patch('platform.system')
    @patch('os.path.expanduser')
    def test_create_desktop_shortcut_mac(self, mock_expanduser, mock_platform, mock_print):
        mock_platform.return_value = 'Darwin'
        mock_expanduser.return_value = '/Users/testuser'
        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            cross_platform_setup.create_desktop_shortcut()
            mock_print.assert_any_call(f"Desktop shortcut created at /Users/testuser/Desktop/ProjectManagement.command")

    @patch('builtins.print')
    @patch('platform.system')
    @patch('os.path.expanduser')
    def test_create_desktop_shortcut_linux(self, mock_expanduser, mock_platform, mock_print):
        mock_platform.return_value = 'Linux'
        mock_expanduser.return_value = '/home/testuser'
        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            cross_platform_setup.create_desktop_shortcut()
            mock_print.assert_any_call(f"Desktop shortcut created at /home/testuser/Desktop/ProjectManagement.desktop")

    @patch('cross_platform_setup.create_virtualenv')
    @patch('cross_platform_setup.install_python_dependencies')
    @patch('cross_platform_setup.install_frontend_dependencies')
    @patch('cross_platform_setup.start_backend_server')
    @patch('cross_platform_setup.start_frontend_server')
    @patch('cross_platform_setup.open_browser')
    @patch('cross_platform_setup.create_desktop_shortcut')
    @patch('builtins.print')
    @patch('time.sleep', return_value=None)
    def test_main(self, mock_sleep, mock_print, mock_create_shortcut, mock_open_browser, mock_start_frontend, mock_start_backend, mock_install_frontend, mock_install_python, mock_create_venv):
        mock_create_venv.return_value = None
        mock_install_python.return_value = None
        mock_install_frontend.return_value = None
        mock_start_backend.return_value = MagicMock()
        mock_start_frontend.return_value = MagicMock()
        cross_platform_setup.main()
        mock_print.assert_any_call("\nInstallation and setup complete.")

if __name__ == '__main__':
    unittest.main()
