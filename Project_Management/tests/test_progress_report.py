import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Project_Management.modules import progress_report
ProgressReport = progress_report.ProgressReport

class TestProgressReport(unittest.TestCase):
    def test_generate_progress_summary(self):
        report = ProgressReport()
        summary = report.generate_progress_summary()
        self.assertIsInstance(summary, dict)
        self.assertIn("total_tasks", summary)
        self.assertIn("completed_tasks", summary)
        self.assertIn("in_progress_tasks", summary)
        self.assertIn("pending_tasks", summary)

    def test_generate_markdown_report(self):
        report = ProgressReport()
        summary = {
            "total_tasks": 10,
            "completed_tasks": 5,
            "in_progress_tasks": 3,
            "pending_tasks": 2,
            "milestones_achieved": 1,
            "milestone_tasks": [("Milestone 1", "Completed")]
        }
        md = report.generate_markdown_report(summary)
        self.assertIn("# Project Progress Report", md)
        self.assertIn("Total Tasks: 10", md)
        self.assertIn("Milestone 1", md)

if __name__ == "__main__":
    unittest.main()
