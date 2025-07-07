import unittest
import os
import json
from unittest.mock import patch
import auto_commit

class TestCommitTaskDatabase(unittest.TestCase):

    def setUp(self):
        self.db_path = "tests/temp_commit_task_database.json"
        # Ensure the test db file is removed before each test
        try:
            os.remove(self.db_path)
        except FileNotFoundError:
            pass

    def tearDown(self):
        # Clean up test db file after tests
        try:
            os.remove(self.db_path)
        except FileNotFoundError:
            pass

    @patch('auto_commit.run_git_command')
    def test_update_commit_task_database_creates_and_updates(self, mock_run_git_command):
        # Mock git command outputs for metadata
        mock_run_git_command.side_effect = [
            (True, "Test Author"),  # author
            (True, "author@example.com"),  # email
            (True, "Mon Apr 26 12:34:56 2021 +0000"),  # date
            (True, "main"),  # branch
            (True, "abc123def456"),  # parents
        ]

        commit_hash = "commit123"
        task_id = "root"
        file_path = "file1.py"
        commit_message = "feat(root): Added file1.py"

        auto_commit.update_commit_task_database(commit_hash, task_id, file_path, commit_message, self.db_path)

        # Verify file created and content
        with open(self.db_path, "r", encoding="utf-8") as f:
            db = json.load(f)

        self.assertIn(commit_hash, db)
        entry = db[commit_hash]
        self.assertEqual(entry["task_id"], task_id)
        self.assertEqual(entry["file_path"], file_path)
        self.assertEqual(entry["commit_message"], commit_message)
        self.assertEqual(entry["author"], "Test Author")
        self.assertEqual(entry["email"], "author@example.com")
        self.assertEqual(entry["date"], "Mon Apr 26 12:34:56 2021 +0000")
        self.assertEqual(entry["branch"], "main")
        self.assertEqual(entry["parent_commits"], ["abc123def456"])

    @patch('auto_commit.run_git_command')
    def test_update_commit_task_database_handles_missing_metadata(self, mock_run_git_command):
        # Simulate git command failures
        mock_run_git_command.return_value = (False, "")

        commit_hash = "commit456"
        task_id = "root"
        file_path = "file2.py"
        commit_message = "fix(root): Fixed bug in file2.py"

        auto_commit.update_commit_task_database(commit_hash, task_id, file_path, commit_message, self.db_path)

        with open(self.db_path, "r", encoding="utf-8") as f:
            db = json.load(f)

        entry = db[commit_hash]
        self.assertEqual(entry["author"], "")
        self.assertEqual(entry["email"], "")
        self.assertEqual(entry["date"], "")
        self.assertEqual(entry["branch"], "")
        self.assertEqual(entry["parent_commits"], [])

if __name__ == '__main__':
    unittest.main()
