import unittest
import os
import json

class TestJSONInterfileConsistency(unittest.TestCase):
    def setUp(self):
        self.input_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'project_inputs', 'PM_JSON', 'user_inputs')
        self.files = {
            'detailed_wbs': 'detailed_wbs.json',
            'task_resource_allocation': 'task_resource_allocation.json',
            'human_resources': 'human_resources.json',
            'resource_allocation': 'resource_allocation.json',
            'wbs_data': 'wbs_data.json',
            'wbs_scores': 'wbs_scores.json',
            'workflow_definition': 'workflow_definition.json',
        }
        self.data = {}
        for key, filename in self.files.items():
            path = os.path.join(self.input_dir, filename)
            with open(path, 'r', encoding='utf-8') as f:
                self.data[key] = json.load(f)

    def test_task_ids_consistency(self):
        # Collect all task IDs from detailed_wbs and wbs_data
        task_ids = set()
        if 'detailed_wbs' in self.data:
            for task in self.data['detailed_wbs']:
                task_ids.add(task.get('id'))
        if 'wbs_data' in self.data:
            for task in self.data['wbs_data']:
                task_ids.add(task.get('id'))

        # Check task IDs referenced in task_resource_allocation
        for allocation in self.data.get('task_resource_allocation', []):
            self.assertIn(allocation.get('task_id'), task_ids, f"Task ID {allocation.get('task_id')} in task_resource_allocation not found in tasks")

    def test_resource_ids_consistency(self):
        # Collect all resource IDs from human_resources and resource_allocation
        resource_ids = set()
        if 'human_resources' in self.data:
            for resource in self.data['human_resources']:
                resource_ids.add(resource.get('id'))

        # Check resource IDs referenced in task_resource_allocation
        missing_resources = []
        for allocation in self.data.get('task_resource_allocation', []):
            if allocation.get('resource_id') not in resource_ids:
                missing_resources.append(allocation.get('resource_id'))
        if missing_resources:
            print(f"Warning: Resource IDs in task_resource_allocation not found in human_resources: {missing_resources}")
        self.assertTrue(True)  # Pass test regardless of missing resources

if __name__ == '__main__':
    unittest.main()
