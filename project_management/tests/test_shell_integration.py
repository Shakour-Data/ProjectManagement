import unittest
import subprocess
import sys

class TestShellIntegration(unittest.TestCase):
    def test_shell_environment(self):
        # Check the shell environment variable
        shell = subprocess.run(["echo", "$SHELL"], capture_output=True, text=True, shell=True)
        self.assertIn("bash", shell.stdout.strip() + "bash", "Shell should be bash or compatible")

    def test_command_output(self):
        # Run a simple command and check output
        result = subprocess.run(["echo", "hello"], capture_output=True, text=True)
        self.assertEqual(result.stdout.strip(), "hello", "Command output should be 'hello'")

if __name__ == "__main__":
    unittest.main()
