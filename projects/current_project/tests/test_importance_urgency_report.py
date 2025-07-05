import unittest
import os
import sys
import importlib.util
from pathlib import Path

# Dynamically add src directory to sys.path for proper imports
src_path = Path(__file__).resolve().parent.parent / 'src'
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Import modules after adjusting sys.path
TaskManagement = importlib.import_module('task_management').TaskManagement
generate_importance_urgency_report = importlib.import_module('progress_report').generate_importance_urgency_report

class TestImportanceUrgencyReport(unittest.TestCase):
    def setUp(self):
        self.tm = TaskManagement()
        # Generate WBS and load scores
        self.tm.generate_wbs_from_idea('Develop Project Management Tool')
        scores_path = os.path.join('docs', 'project_management', 'wbs_scores.json')
        self.tm.load_scores(scores_path)

    def test_task_counts(self):
        tasks = list(self.tm.tasks.values())
        self.assertGreaterEqual(len(tasks), 30, "Total tasks should be at least 30 for comprehensive report")

    def test_classification_counts(self):
        classified = self.tm.classify_tasks_eisenhower()
        self.assertGreaterEqual(len(classified['do_now']), 15, "At least 15 tasks should be both important and urgent")
        self.assertGreaterEqual(len(classified['schedule']), 15, "At least 15 tasks should be only important")
        self.assertGreaterEqual(len(classified['delegate']), 15, "At least 15 tasks should be only urgent")

    def test_report_generation(self):
        generate_importance_urgency_report(self.tm)
        report_path = os.path.join('docs', 'project_management', 'importance_urgency_report.md')
        self.assertTrue(os.path.exists(report_path), "Report file should be generated")
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("Top 15 Tasks That Are Both Important and Urgent", content)
        self.assertIn("Top 15 Tasks That Are Only Important", content)
        self.assertIn("Top 15 Tasks That Are Only Urgent", content)

if __name__ == '__main__':
    unittest.main()
