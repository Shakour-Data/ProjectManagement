"""
Date: 2025-07-26
Authors: GravityWavesOrg (GitHub username)
File Description: Unit tests for the BackupManager class in project_management/modules/backup_manager.py.
"""

import unittest
from unittest.mock import patch, MagicMock
import pathlib
from pathlib import Path
import shutil
import os
import datetime
import sys

# Add project_management/modules to sys.path for import
sys.path.insert(0, str(pathlib.Path(__file__).parent.resolve().parent.joinpath('project_management/modules')))

from backup_manager import BackupManager

class TestBackupManager(unittest.TestCase):
    def setUp(self):
        self.source_dir = Path("test_source")
        self.backup_base_dir = Path("test_backup_base")
        self.source_dir.mkdir(exist_ok=True)
        self.backup_base_dir.mkdir(exist_ok=True)
        self.bm = BackupManager(str(self.source_dir), str(self.backup_base_dir))

    def tearDown(self):
        shutil.rmtree(self.source_dir, ignore_errors=True)
        shutil.rmtree(self.backup_base_dir, ignore_errors=True)

    @patch('shutil.copytree')
    def test_create_backup_success(self, mock_copytree):
        mock_copytree.return_value = None
        backup_dir = self.bm.create_backup()
        self.assertIsNotNone(backup_dir)
        self.assertTrue(str(backup_dir).startswith(str(self.backup_base_dir)))

    @patch('shutil.copytree')
    def test_create_backup_failure(self, mock_copytree):
        mock_copytree.side_effect = Exception("Copy failed")
        backup_dir = self.bm.create_backup()
        self.assertIsNone(backup_dir)

    @patch('pathlib.Path.glob')
    def test_list_backups(self, mock_glob):
        mock_glob.return_value = [Path("backup_20250726_000000"), Path("backup_20250725_000000")]
        backups = self.bm.list_backups()
        self.assertEqual(len(backups), 2)

    @patch('shutil.copytree')
    @patch('shutil.rmtree')
    @patch('pathlib.Path.exists')
    def test_restore_backup_success(self, mock_exists, mock_rmtree, mock_copytree):
        mock_exists.return_value = True
        mock_rmtree.return_value = None
        mock_copytree.return_value = None
        result = self.bm.restore_backup(str(self.backup_base_dir / "backup_20250726_000000"))
        self.assertTrue(result)

    @patch('pathlib.Path.exists')
    def test_restore_backup_nonexistent(self, mock_exists):
        mock_exists.return_value = False
        result = self.bm.restore_backup("nonexistent_backup")
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
