"""
Date: 2025-07-26
Authors: GravityWavesOrg (GitHub username)
File Description: Unit tests for the AutoCommit class in project_management/modules/auto_commit.py.
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add project_management/modules to sys.path for import
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.resolve().parent.joinpath('project_management/modules')))

from auto_commit import AutoCommit

class TestAutoCommit(unittest.TestCase):
    def setUp(self):
        self.auto_commit = AutoCommit()

    @patch('subprocess.run')
    def test_run_git_command_success(self, mock_run):
        mock_run.return_value = MagicMock(stdout='output', returncode=0)
        success, output = self.auto_commit.run_git_command(['status'])
        self.assertTrue(success)
        self.assertEqual(output, 'output')

    @patch('subprocess.run')
    def test_run_git_command_failure(self, mock_run):
        from subprocess import CalledProcessError
        mock_run.side_effect = CalledProcessError(returncode=1, cmd='git status', stderr='Git error')
        success, output = self.auto_commit.run_git_command(['status'])
        self.assertFalse(success)
        self.assertIn("Git error", output)

    @patch.object(AutoCommit, 'run_git_command')
    def test_get_git_changes(self, mock_run_git_command):
        mock_run_git_command.return_value = (True, " M file1.py\n?? file2.py")
        changes = self.auto_commit.get_git_changes()
        self.assertIn(" M file1.py", changes)
        self.assertIn("?? file2.py", changes)

    def test_group_related_files(self):
        changes = ["M project_management/modules/auto_commit.py", "?? new_file.py"]
        groups = self.auto_commit.group_related_files(changes)
        self.assertIn('project_management', groups)
        self.assertIn('root', groups)
        self.assertIn(('M', 'project_management/modules/auto_commit.py'), groups['project_management'])
        self.assertIn(('??', 'new_file.py'), groups['root'])

    def test_categorize_files(self):
        files = [('A', 'file1.py'), ('M', 'file2.py'), ('D', 'file3.py'), ('??', 'file4.py')]
        categories = self.auto_commit.categorize_files(files)
        self.assertIn('Added', categories)
        self.assertIn('Modified', categories)
        self.assertIn('Deleted', categories)
        self.assertIn('Untracked', categories)

if __name__ == '__main__':
    unittest.main()
