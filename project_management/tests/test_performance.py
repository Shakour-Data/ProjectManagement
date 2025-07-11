import unittest
import os
import json
from project_management.modules.input_handler import InputHandler

class TestPerformance(unittest.TestCase):
    def setUp(self):
        self.input_handler = InputHandler()
        self.test_dir = "/home/gravitywaves/GravityProject/ProjectManagement/PM_Input"
        # Ensure test directory exists
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

    def tearDown(self):
        # Clean up test files
        for filename in os.listdir(self.test_dir):
            file_path = os.path.join(self.test_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    def test_large_input_file(self):
        large_data = [{"id": i, "title": f"Task {i}", "importance": i % 100, "urgency": (100 - i) % 100} for i in range(10000)]
        large_file = os.path.join(self.test_dir, "wbs_data.json")
        with open(large_file, "w") as f:
            json.dump(large_data, f)

        inputs = self.input_handler.read_json_files()
        self.assertIsNotNone(inputs, "Should successfully read large input file")
        self.assertIn("wbs_data.json", inputs)
        self.assertEqual(len(inputs["wbs_data.json"]), 10000)

if __name__ == "__main__":
    unittest.main()
