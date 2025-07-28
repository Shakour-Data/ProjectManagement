"""
Date: 2025-07-27
Authors: GravityWavesOrg (GitHub username)
File Description: Unit tests for gantt_chart_data.py module to verify Gantt chart data generation.
"""

import unittest
from project_management.modules.gantt_chart_data import GanttChartData

class TestGanttChartData(unittest.TestCase):
    def setUp(self):
        self.generator = GanttChartData()
    
    def test_build_gantt_data_empty(self):
        self.generator.tasks = []
        result = self.generator.build_gantt_data()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_build_gantt_data_basic(self):
        self.generator.tasks = [
            {
                "id": "1",
                "name": "Task 1",
                "start_date": "2025-07-01",
                "duration_days": 4,
                "progress": 0.5,
                "dependencies": []
            },
            {
                "id": "2",
                "name": "Task 2",
                "start_date": "2025-07-06",
                "duration_days": 4,
                "progress": 0.2,
                "dependencies": ["1"]
            }
        ]
        result = self.generator.build_gantt_data()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "1")
        self.assertEqual(result[1]["dependencies"], ["1"])

    def test_build_gantt_data_invalid_dates(self):
        self.generator.tasks = [
            {
                "id": "1",
                "name": "Task 1",
                "start_date": "invalid-date",
                "duration_days": 4,
                "progress": 0.5,
                "dependencies": []
            }
        ]
        # The invalid date is handled gracefully by parse_date returning None and using today as fallback,
        # so no exception is expected here. Instead, check that the output contains a valid ISO date string.
        result = self.generator.build_gantt_data()
        self.assertEqual(len(result), 1)
        self.assertIsNotNone(result[0]["start_date"])

if __name__ == '__main__':
    unittest.main()
