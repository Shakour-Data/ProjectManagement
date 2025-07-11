import unittest
import os
import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules import auto_commit
collect_commit_progress = auto_commit.collect_commit_progress
update_commit_task_database = auto_commit.update_commit_task_database
generate_commit_message = auto_commit.generate_commit_message
get_git_changes = auto_commit.get_git_changes
group_changes_by_module = auto_commit.group_related_files

class TestAutoCommit(unittest.TestCase):
    def setUp(self):
        # Setup test environment paths
        self.commit_progress_path = "Project_Management/PM_JSON/system_outputs/commit_progress.json"
        self.commit_task_db_path = "Project_Management/PM_JSON/system_outputs/commit_task_database.json"

    def test_generate_commit_message(self):
        group_name = "module1"
        category_name = "Added"
        files = ["file1.py", "file2.py"]
        message = generate_commit_message(group_name, category_name, files)
        self.assertIn("feat", message)
        self.assertIn("module1", message)
        self.assertIn("Added files updated", message)

    def test_collect_commit_progress(self):
        progress_data = collect_commit_progress()
        self.assertIsInstance(progress_data, dict)
        # Further assertions can be added based on known test data

    def test_update_commit_task_database(self):
        commit_hash = "abc123"
        task_id = "module1"
        file_path = "file1.py"
        commit_message = "Test commit message"
        # Call update_commit_task_database and check if file is updated
        update_commit_task_database(commit_hash, task_id, file_path, commit_message, db_path=self.commit_task_db_path)
        self.assertTrue(os.path.exists(self.commit_task_db_path))
        with open(self.commit_task_db_path, "r", encoding="utf-8") as f:
            db = json.load(f)
        self.assertIn(commit_hash, db)
        self.assertEqual(db[commit_hash]["task_id"], task_id)
        self.assertEqual(db[commit_hash]["file_path"], file_path)
        self.assertEqual(db[commit_hash]["commit_message"], commit_message)

    def test_detect_git_changes_and_grouping(self):
        # This test assumes a git repo with some changes; here we simulate the function call
        changes = get_git_changes()
        self.assertIsInstance(changes, list)
        grouped = group_changes_by_module(changes)
        self.assertIsInstance(grouped, dict)

if __name__ == "__main__":
    unittest.main()
