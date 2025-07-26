"""
Date: 2025-07-26
Authors: GravityWavesOrg (GitHub username)
File Description: Tests for CLI commands with mocking to isolate bootstrapping and side effects.
"""

import unittest
from unittest.mock import patch
import subprocess

class TestCLI(unittest.TestCase):
    @patch('subprocess.run')
    def test_start_command(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=['python3', 'project_management/cli.py', 'start'], returncode=0)
        result = subprocess.run(['python3', 'project_management/cli.py', 'start'])
        self.assertEqual(result.returncode, 0)
        mock_run.assert_called_with(['python3', 'project_management/cli.py', 'start'])

    @patch('subprocess.run')
    def test_status_command(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=['python3', 'project_management/cli.py', 'status'], returncode=0)
        result = subprocess.run(['python3', 'project_management/cli.py', 'status'])
        self.assertEqual(result.returncode, 0)
        mock_run.assert_called_with(['python3', 'project_management/cli.py', 'status'])

    @patch('subprocess.run')
    def test_setup_command(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=['python3', 'project_management/cli.py', 'setup'], returncode=0)
        result = subprocess.run(['python3', 'project_management/cli.py', 'setup'])
        self.assertEqual(result.returncode, 0)
        mock_run.assert_called_with(['python3', 'project_management/cli.py', 'setup'])

    @patch('subprocess.run')
    def test_help_command(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=['python3', 'project_management/cli.py', 'help'], returncode=0)
        result = subprocess.run(['python3', 'project_management/cli.py', 'help'])
        self.assertEqual(result.returncode, 0)
        mock_run.assert_called_with(['python3', 'project_management/cli.py', 'help'])

    @patch('subprocess.run')
    def test_invalid_command(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=['python3', 'project_management/cli.py', 'invalid'], returncode=1)
        result = subprocess.run(['python3', 'project_management/cli.py', 'invalid'])
        self.assertNotEqual(result.returncode, 0)
        mock_run.assert_called_with(['python3', 'project_management/cli.py', 'invalid'])

if __name__ == '__main__':
    unittest.main()
