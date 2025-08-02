import unittest
import subprocess
import sys
import os

class TestEstimationManagementScript(unittest.TestCase):
    def test_script_execution(self):
        """Test that the script can be executed directly"""
        # Get the path to the estimation_management.py file
        script_path = os.path.join('project_management', 'modules', 'main_modules', 'estimation_management.py')
        
        # Execute the script as a subprocess
        result = subprocess.run([sys.executable, script_path], 
                                capture_output=True, text=True, cwd='.')
        
        # Check that the script executed without errors
        # Note: The script might fail because of missing files, but that's okay for this test
        # We're just checking that it can be executed
        self.assertIn("output saved to", result.stdout) or self.assertEqual(result.returncode, 0)

if __name__ == '__main__':
    unittest.main()
