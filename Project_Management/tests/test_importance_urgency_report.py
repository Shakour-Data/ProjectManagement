import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Project_Management.modules.reports import importance_urgency_report
ImportanceUrgencyReport = importance_urgency_report.ImportanceUrgencyReport

class TestImportanceUrgencyReport(unittest.TestCase):
    def test_generate_importance_urgency_summary(self):
        report = ImportanceUrgencyReport()
        summary = report.generate_importance_urgency_summary()
        self.assertIsInstance(summary, dict)
        self.assertIn("Important & Urgent", summary)
        self.assertIn("Important & Not Urgent", summary)
        self.assertIn("Not Important & Urgent", summary)
        self.assertIn("Not Important & Not Urgent", summary)

    def test_generate_markdown_report(self):
        report = ImportanceUrgencyReport()
        summary = {
            "Important & Urgent": [{"name": "Task 1", "status": "In Progress", "importance": 8, "urgency": 9}],
            "Important & Not Urgent": [],
            "Not Important & Urgent": [],
            "Not Important & Not Urgent": []
        }
        md = report.generate_markdown_report(summary)
        self.assertIn("# Importance and Urgency Report", md)
        self.assertIn("Task 1", md)

if __name__ == "__main__":
    unittest.main()
