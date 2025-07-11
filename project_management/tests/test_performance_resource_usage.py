import unittest
import os
import json
import psutil
import time
from project_management.modules.input_handler import InputHandler

class TestPerformanceResourceUsage(unittest.TestCase):
    def setUp(self):
        self.input_handler = InputHandler()
        self.test_dir = "/home/gravitywaves/GravityProject/ProjectManagement/PM_Input"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

    def tearDown(self):
        # Clean up test files
        for filename in os.listdir(self.test_dir):
            file_path = os.path.join(self.test_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    def test_memory_cpu_usage(self):
        large_data = [{"id": i, "title": f"Task {i}", "importance": i % 100, "urgency": (100 - i) % 100} for i in range(10000)]
        large_file = os.path.join(self.test_dir, "wbs_data.json")
        with open(large_file, "w") as f:
            json.dump(large_data, f)

        process = psutil.Process(os.getpid())
        start_mem = process.memory_info().rss
        start_cpu = process.cpu_percent(interval=None)

        start_time = time.time()
        inputs = self.input_handler.read_json_files()
        end_time = time.time()

        end_mem = process.memory_info().rss
        end_cpu = process.cpu_percent(interval=None)

        self.assertIsNotNone(inputs, "Should successfully read large input file")
        self.assertLess(end_mem - start_mem, 100 * 1024 * 1024, "Memory increase should be less than 100MB")
        self.assertLess(end_cpu - start_cpu, 150, "CPU usage increase should be less than 150%")
        self.assertLess(end_time - start_time, 10, "Processing should take less than 10 seconds")

if __name__ == "__main__":
    unittest.main()
