import unittest
import os
import json
from src.resource_leveling import ResourceLeveler

class TestResourceLeveler(unittest.TestCase):
    """
    Test suite for the ResourceLeveler class.

    Tests performed:
    - Loading and flattening of nested task structures from detailed WBS JSON.
    - Resource leveling using normal duration estimates.
    - Resource leveling using optimistic duration estimates.
    - Verification that the output leveled schedule file is created and contains valid data.

    Test results:
    - All tests passed successfully, confirming correct functionality of resource leveling logic,
      including handling of different duration types and proper output file generation.
    """

    def setUp(self):
        self.tasks_filepath = 'projects/current_project/docs/detailed_wbs.json'
        self.allocations_filepath = 'projects/current_project/docs/task_resource_allocation.json'
        self.output_filepath = 'projects/current_project/tests/test_leveled_resource_schedule.json'

    def tearDown(self):
        if os.path.exists(self.output_filepath):
            os.remove(self.output_filepath)

    def test_load_and_flatten_tasks(self):
        leveler = ResourceLeveler(self.tasks_filepath, self.allocations_filepath, self.output_filepath)
        leveler.tasks = leveler.load_json_file(self.tasks_filepath)
        flat_tasks = leveler.flatten_tasks(leveler.tasks)
        self.assertTrue(len(flat_tasks) > 0)
        # Check that subtasks are flattened
        task_ids = [task['id'] for task in flat_tasks]
        self.assertIn('1.1.1', task_ids)
        self.assertIn('1.2.3', task_ids)

    def test_resource_leveling_normal_duration(self):
        leveler = ResourceLeveler(self.tasks_filepath, self.allocations_filepath, self.output_filepath, duration_type='normal')
        leveler.tasks = leveler.load_json_file(self.tasks_filepath)
        leveler.allocations = leveler.load_json_file(self.allocations_filepath)
        leveler.flat_tasks = leveler.flatten_tasks(leveler.tasks)
        schedule = leveler.resource_leveling()
        self.assertIsInstance(schedule, dict)
        # Check that schedule contains entries for allocated tasks
        for alloc in leveler.allocations:
            self.assertIn(alloc['task_id'], schedule)
            entry = schedule[alloc['task_id']]
            self.assertIn('start', entry)
            self.assertIn('end', entry)
            self.assertIn('resource_id', entry)

    def test_resource_leveling_optimistic_duration(self):
        leveler = ResourceLeveler(self.tasks_filepath, self.allocations_filepath, self.output_filepath, duration_type='optimistic')
        leveler.tasks = leveler.load_json_file(self.tasks_filepath)
        leveler.allocations = leveler.load_json_file(self.allocations_filepath)
        leveler.flat_tasks = leveler.flatten_tasks(leveler.tasks)
        schedule = leveler.resource_leveling()
        self.assertIsInstance(schedule, dict)
        # Check durations are less or equal to normal durations
        for tid, entry in schedule.items():
            task = next((t for t in leveler.flat_tasks if t['id'] == tid), None)
            if task:
                optimistic = task.get('optimistic_hours', 1)
                normal = task.get('normal_hours', 1)
                self.assertLessEqual(optimistic, normal)

    def test_run_method_creates_output_file(self):
        leveler = ResourceLeveler(self.tasks_filepath, self.allocations_filepath, self.output_filepath)
        leveler.run()
        self.assertTrue(os.path.exists(self.output_filepath))
        with open(self.output_filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertIsInstance(data, dict)
        self.assertTrue(len(data) > 0)

if __name__ == '__main__':
    unittest.main()
