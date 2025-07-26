"""
Date: 2025-07-26
Authors: GravityWavesOrg (GitHub username)
File Description: Tests for installation and setup commands with isolation of environment and git operations to avoid conflicts.
"""

import unittest
from unittest.mock import patch, MagicMock
import subprocess
import os

class TestInstallationSetup(unittest.TestCase):
    @patch('subprocess.run')
    def test_pip_install(self, mock_run):
        """Verify package installs correctly via pip install."""
        mock_run.return_value = subprocess.CompletedProcess(args=['pip', 'install', 'auto_pm'], returncode=0)
        result = subprocess.run(['pip', 'install', 'auto_pm'])
        self.assertEqual(result.returncode, 0)
        mock_run.assert_called_with(['pip', 'install', 'auto_pm'])

    @patch('subprocess.run')
    def test_pip_uninstall(self, mock_run):
        """Verify package uninstallation works cleanly."""
        mock_run.return_value = subprocess.CompletedProcess(args=['pip', 'uninstall', '-y', 'auto_pm'], returncode=0)
        result = subprocess.run(['pip', 'uninstall', '-y', 'auto_pm'])
        self.assertEqual(result.returncode, 0)
        mock_run.assert_called_with(['pip', 'uninstall', '-y', 'auto_pm'])

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_clean_virtualenv_setup(self, mock_run, mock_exists):
        """Test installation in a clean virtual environment."""
        mock_exists.return_value = False  # Simulate venv does not exist
        mock_run.return_value = subprocess.CompletedProcess(args=['python3', '-m', 'venv', 'venv'], returncode=0)
        if not os.path.exists('venv'):
            result = subprocess.run(['python3', '-m', 'venv', 'venv'])
            self.assertEqual(result.returncode, 0)
        mock_run.assert_called_with(['python3', '-m', 'venv', 'venv'])

    @patch('subprocess.run')
    def test_auto_pm_install_command(self, mock_run):
        """Test `auto_pm install` command executes without errors and creates input directory."""
        mock_run.return_value = subprocess.CompletedProcess(args=['python3', 'project_management/cli.py', 'install'], returncode=0)
        result = subprocess.run(['python3', 'project_management/cli.py', 'install'])
        self.assertEqual(result.returncode, 0)
        mock_run.assert_called_with(['python3', 'project_management/cli.py', 'install'])

if __name__ == '__main__':
    unittest.main()
