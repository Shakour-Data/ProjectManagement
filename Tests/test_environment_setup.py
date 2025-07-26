"""
Date: 2025-07-26
Authors: GravityWavesOrg (GitHub username)
File Description: Tests for environment setup including virtual environment creation, dependency installation, and git initialization.
"""

import os
import subprocess
import unittest

class TestEnvironmentSetup(unittest.TestCase):
    def test_virtualenv_exists(self):
        """Test that the virtual environment directory exists."""
        self.assertTrue(os.path.exists('venv'), "Virtual environment directory 'venv' does not exist.")

    def test_pip_executable_exists(self):
        """Test that pip executable exists in the virtual environment."""
        pip_path = os.path.join('venv', 'bin', 'pip')
        self.assertTrue(os.path.isfile(pip_path), "pip executable not found in virtual environment.")

    def test_requirements_file_exists(self):
        """Test that requirements.txt file exists."""
        self.assertTrue(os.path.isfile('requirements.txt'), "requirements.txt file does not exist.")

    def test_git_repo_initialized(self):
        """Test that the current directory is a git repository."""
        result = subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], capture_output=True, text=True)
        self.assertEqual(result.stdout.strip(), 'true', "Current directory is not a git repository.")

if __name__ == '__main__':
    unittest.main()
