import unittest
import os
import json
from project_management.modules import quality_management

class TestQualityManagement(unittest.TestCase):
    def setUp(self):
        self.manager = quality_management.QualityManagement(
            detailed_wbs_path='project_management/data/PM_JSON/user_inputs/detailed_wbs.json',
            quality_standards_path='project_management/data/PM_JSON/user_inputs/quality_standards.json',
            output_path='project_management/tests/test_output_quality_management.json'
        )
        # Ensure output file does not exist before test
        if os.path.exists(self.manager.output_path):
            os.remove(self.manager.output_path)

    def test_load_inputs(self):
        self.manager.load_inputs()
        self.assertIsInstance(self.manager.inputs.get('detailed_wbs'), dict)
        self.assertIsInstance(self.manager.inputs.get('quality_standards'), dict)

    def test_analyze_placeholder(self):
        self.manager.load_inputs()
        self.manager.analyze()
        self.assertIn('summary', self.manager.output)
        self.assertEqual(self.manager.output['summary'], 'Quality evaluation not yet implemented')

    def test_run_creates_output_file(self):
        self.manager.run()
        self.assertTrue(os.path.exists(self.manager.output_path))
        with open(self.manager.output_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertIn('summary', data)

if __name__ == '__main__':
    unittest.main()
