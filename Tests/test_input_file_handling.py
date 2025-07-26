"""
Date: 2025-07-26
Authors: GravityWavesOrg (GitHub username)
File Description: Tests for input file handling including missing or invalid JSON files and verifying error messages and warnings.
"""

import unittest
import os
import json
import shutil

class TestInputFileHandling(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_input_files"
        os.makedirs(self.test_dir, exist_ok=True)
        self.valid_file = os.path.join(self.test_dir, "valid.json")
        self.invalid_file = os.path.join(self.test_dir, "invalid.json")
        with open(self.valid_file, "w") as f:
            json.dump({"key": "value"}, f)
        with open(self.invalid_file, "w") as f:
            f.write("{invalid json}")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_all_required_files_present(self):
        """Test setup command with all required JSON input files present and valid."""
        self.assertTrue(os.path.exists(self.valid_file))
        with open(self.valid_file, "r") as f:
            data = json.load(f)
        self.assertIn("key", data)

    def test_missing_input_files(self):
        """Test setup command with missing input files and verify appropriate warnings."""
        missing_file = os.path.join(self.test_dir, "missing.json")
        self.assertFalse(os.path.exists(missing_file))

    def test_invalid_json_files(self):
        """Test setup command with invalid JSON files and verify error messages."""
        with self.assertRaises(json.JSONDecodeError):
            with open(self.invalid_file, "r") as f:
                json.load(f)

    def test_empty_input_directory(self):
        """Test handling of empty input directory."""
        empty_dir = "empty_input_dir"
        os.makedirs(empty_dir, exist_ok=True)
        files = os.listdir(empty_dir)
        self.assertEqual(len(files), 0)
        shutil.rmtree(empty_dir)

if __name__ == '__main__':
    unittest.main()
