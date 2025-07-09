import unittest
import os
import json
from Project_Management.modules.progress_calculator import ProgressCalculator

class TestProgressCalculator(unittest.TestCase):

    def setUp(self):
        self.input_dir = "project_test/PM_Input"
        self.pc = ProgressCalculator(self.input_dir)
        self.pc.load_inputs()

    def test_load_inputs(self):
        self.assertTrue(hasattr(self.pc, 'tasks'))
        self.assertTrue(hasattr(self.pc, 'workflow_steps'))
        self.assertTrue(hasattr(self.pc, 'commit_progress'))

    def test_calculate_commit_progress(self):
        # Assuming commit_progress is a dict mapping task_id to float
        self.pc.commit_progress = {"task1": 0.5, "task2": 0.8}
        progress1 = self.pc.calculate_commit_progress("task1")
        progress2 = self.pc.calculate_commit_progress("task2")
        self.assertAlmostEqual(progress1, 0.5)
        self.assertAlmostEqual(progress2, 0.8)

    def test_calculate_workflow_progress(self):
        # Provide a dummy task_id that may or may not exist
        progress = self.pc.calculate_workflow_progress("task1")
        self.assertIsInstance(progress, float)
        self.assertGreaterEqual(progress, 0.0)
        self.assertLessEqual(progress, 1.0)

    def test_calculate_combined_progress(self):
        # Provide a dummy task_id that may or may not exist
        combined = self.pc.calculate_combined_progress("task1")
        self.assertIsInstance(combined, float)
        self.assertGreaterEqual(combined, 0.0)
        self.assertLessEqual(combined, 1.0)

    def test_calculate_dynamic_importance(self):
        if self.pc.tasks:
            importance = self.pc.calculate_dynamic_importance(self.pc.tasks[0])
            self.assertIsInstance(importance, float)

    def test_calculate_dynamic_urgency(self):
        if self.pc.tasks:
            urgency = self.pc.calculate_dynamic_urgency(self.pc.tasks[0])
            self.assertIsInstance(urgency, float)

    def test_enrich_tasks_with_progress(self):
        self.pc.enrich_tasks_with_progress()
        enriched_tasks = self.pc.get_enriched_tasks()
        self.assertIsInstance(enriched_tasks, list)
        self.assertTrue(len(enriched_tasks) > 0)

if __name__ == '__main__':
    unittest.main()
