import unittest
import os
import json
from project_management.modules.input_handler import InputHandler

class TestEdgeCases(unittest.TestCase):
    def setUp(self):
        self.test_dir = "project_management/PM_Input"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
        self.input_handler = InputHandler(input_dir=self.test_dir)

    def tearDown(self):
        # Clean up test files
        for filename in os.listdir(self.test_dir):
            file_path = os.path.join(self.test_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    def test_corrupted_json_file(self):
        corrupted_file = os.path.join(self.test_dir, "wbs_data.json")
        with open(corrupted_file, "w") as f:
            f.write("{ invalid json }")

        inputs = self.input_handler.read_json_files()
        self.assertIsNone(inputs, "Should return None for corrupted JSON files")

    def test_missing_required_files(self):
        # Ensure PM_Input directory is empty
        for filename in os.listdir(self.test_dir):
            file_path = os.path.join(self.test_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

        inputs = self.input_handler.read_json_files()
        self.assertIsNone(inputs, "Should return None when required files are missing")

    def test_empty_input_directory(self):
        # Ensure PM_Input directory is empty
        for filename in os.listdir(self.test_dir):
            file_path = os.path.join(self.test_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

        inputs = self.input_handler.read_json_files()
        self.assertIsNone(inputs, "Should return None for empty input directory")

if __name__ == "__main__":
    unittest.main()
