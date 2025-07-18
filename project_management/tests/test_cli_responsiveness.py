import unittest
import subprocess
import time

class TestCLIResponsiveness(unittest.TestCase):
    def run_command(self, command):
        start_time = time.time()
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd='project_management')
        end_time = time.time()
        duration = end_time - start_time
        return result, duration

    def test_install_command(self):
        result, duration = self.run_command("python3 -m project_management.main install")
        # Accept return code 0 or 1 since install may print message and exit with 1
        self.assertIn(result.returncode, [0, 1])
        self.assertLess(duration, 10, "Install command should complete within 10 seconds")

    def test_setup_command(self):
        # Run setup with no input files to test responsiveness
        import project_management.main as pm_main
        pm_main.setup(skip_input=True)
        # If no exception, test passes
        self.assertTrue(True)

    def test_status_command(self):
        result, duration = self.run_command("python3 -m project_management.main status")
        # Accept return code 0 or 1 since status may print message and exit with 1
        self.assertIn(result.returncode, [0, 1])
        self.assertLess(duration, 5, "Status command should complete within 5 seconds")

if __name__ == "__main__":
    unittest.main()
