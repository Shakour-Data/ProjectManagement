import unittest
import os
import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from project_management.modules import json_data_linker
JSONDataLinker = json_data_linker.JSONDataLinker

class TestJSONDataLinker(unittest.TestCase):
    def setUp(self):
        self.linker = JSONDataLinker()
        self.input_dir = self.linker.input_dir
        self.intermediate_dir = self.linker.intermediate_dir

        # Ensure input directory exists and has required files for testing
        os.makedirs(self.input_dir, exist_ok=True)
        # Create minimal input JSON files for testing
        detailed_wbs = [
            {
                "id": "1",
                "title": "Task 1",
                "subtasks": []
            }
        ]
        task_resource_allocation = [
            {
                "resource_id": "R1",
                "task_id": "1",
                "allocation_percent": 100,
                "role_in_task": "Developer",
                "start_date": "2025-06-01",
                "end_date": "2025-06-10"
            }
        ]
        with open(os.path.join(self.input_dir, "detailed_wbs.json"), "w", encoding="utf-8") as f:
            json.dump(detailed_wbs, f, indent=2, ensure_ascii=False)
        with open(os.path.join(self.input_dir, "task_resource_allocation.json"), "w", encoding="utf-8") as f:
            json.dump(task_resource_allocation, f, indent=2, ensure_ascii=False)

    def test_link_wbs_and_resources(self):
        enriched_wbs = self.linker.link_wbs_and_resources()
        self.assertIsInstance(enriched_wbs, list)
        self.assertTrue("allocations" in enriched_wbs[0])
        self.assertEqual(len(enriched_wbs[0]["allocations"]), 1)
        self.assertEqual(enriched_wbs[0]["allocations"][0]["resource_id"], "R1")

if __name__ == "__main__":
    unittest.main()
