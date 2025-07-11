import unittest
import os
import json

class TestOutputJSONFields(unittest.TestCase):
    def setUp(self):
        self.output_dir = os.path.join(os.path.dirname(__file__), '..', 'project_management', 'PM_JSON', 'system_outputs')
        self.commit_progress_path = os.path.join(self.output_dir, 'commit_progress.json')
        self.commit_task_db_path = os.path.join(self.output_dir, 'commit_task_database.json')

    def test_commit_progress_fields(self):
        import os
        if not os.path.exists(self.commit_progress_path):
            self.skipTest(f"{self.commit_progress_path} does not exist, skipping test.")
        with open(self.commit_progress_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for key, value in data.items():
            self.assertIn('progress_change', value, f"Missing 'progress_change' in commit_progress for {key}")
            self.assertIsInstance(value['progress_change'], (int, float), f"'progress_change' should be numeric for {key}")
            self.assertLessEqual(value['progress_change'], 5, f"'progress_change' should be capped at 5 for {key}")

    def test_commit_task_database_fields(self):
        import os
        if not os.path.exists(self.commit_task_db_path):
            self.skipTest(f"{self.commit_task_db_path} does not exist, skipping test.")
        with open(self.commit_task_db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for key, value in data.items():
            self.assertIn('workflow_stage', value, f"Missing 'workflow_stage' in commit_task_database for {key}")
            self.assertIn('importance_change', value, f"Missing 'importance_change' in commit_task_database for {key}")
            self.assertIn('priority_change', value, f"Missing 'priority_change' in commit_task_database for {key}")

if __name__ == '__main__':
    unittest.main()
