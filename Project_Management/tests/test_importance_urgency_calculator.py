import unittest
import os
import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Project_Management.modules import importance_urgency_calculator
ImportanceUrgencyCalculator = importance_urgency_calculator.ImportanceUrgencyCalculator

class TestImportanceUrgencyCalculator(unittest.TestCase):
    def setUp(self):
        self.test_wbs = [
            {
                "id": "1",
                "title": "Task 1",
                "importance_score": 80,
                "urgency_score": 70,
                "subtasks": []
            },
            {
                "id": "2",
                "title": "Task 2",
                "importance_score": 60,
                "urgency_score": 50,
                "subtasks": [
                    {
                        "id": "2.1",
                        "title": "Subtask 2.1",
                        "importance_score": 90,
                        "urgency_score": 85,
                        "subtasks": []
                    }
                ]
            }
        ]

    def test_calculate_all(self):
        calculator = ImportanceUrgencyCalculator(self.test_wbs)
        scores = calculator.calculate_all()
        self.assertIn("1", scores)
        self.assertIn("2", scores)
        self.assertIn("2.1", scores)
        self.assertAlmostEqual(scores["1"]["importance"], 80)
        self.assertAlmostEqual(scores["1"]["urgency"], 70)
        self.assertAlmostEqual(scores["2"]["importance"], 90)  # Should match subtask importance
        self.assertAlmostEqual(scores["2"]["urgency"], 85)   # Should match subtask urgency

if __name__ == "__main__":
    unittest.main()
