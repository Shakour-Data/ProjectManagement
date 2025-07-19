import unittest
import os
import json
from project_management.modules import reporting

class TestReporting(unittest.TestCase):
    def setUp(self):
        self.manager = reporting.Reporting(
            detailed_wbs_path='project_management/data/PM_JSON/user_inputs/detailed_wbs.json',
            resource_allocation_summary_path='project_management/data/PM_JSON/system_outputs/resource_allocation_summary.json',
            time_management_path='project_management/data/PM_JSON/system_outputs/time_management.json',
            risk_management_path='project_management/data/PM_JSON/system_outputs/risk_management.json',
            quality_management_path='project_management/data/PM_JSON/system_outputs/quality_management.json',
            output_path='project_management/tests/test_output_reporting.json'
        )
        if os.path.exists(self.manager.output_path):
            os.remove(self.manager.output_path)

    def test_load_inputs(self):
        self.manager.load_inputs()
        self.assertIsInstance(self.manager.inputs.get('detailed_wbs'), dict)

    def test_analyze_placeholder(self):
        self.manager.load_inputs()
        self.manager.analyze()
        self.assertIn('summary', self.manager.output)
        self.assertEqual(self.manager.output['summary'], 'Project reports generation not yet implemented')

    def test_run_creates_output_file(self):
        self.manager.run()
        self.assertTrue(os.path.exists(self.manager.output_path))
        with open(self.manager.output_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertIn('summary', data)

if __name__ == '__main__':
    unittest.main()
