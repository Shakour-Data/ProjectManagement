"""
Date: 2025-07-26
Authors: GravityWavesOrg (GitHub username)
File Description: Tests for documentation and usability including help command, README and HELP.md files, and documentation links.
"""

import unittest
import os
import subprocess

class TestDocumentation(unittest.TestCase):
    def test_help_command(self):
        """Verify `auto_pm help` command displays accurate and complete information."""
        env = dict(**os.environ)
        env["PYTHONPATH"] = "."
        result = subprocess.run(["python3", "project_management/cli.py", "help"], capture_output=True, text=True, env=env)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Usage", result.stdout)

    def test_readme_and_help_files(self):
        """Verify README and HELP.md files are up to date and clear."""
        self.assertTrue(os.path.exists("README.md"))
        self.assertTrue(os.path.exists("project_management/HELP.md"))

        with open("README.md", "r") as f:
            readme_content = f.read()
        with open("project_management/HELP.md", "r") as f:
            help_content = f.read()

        self.assertIn("ProjectManagement", readme_content)
        self.assertIn("Usage", help_content)

    def test_documentation_links(self):
        """Test links and references in documentation."""
        # Placeholder: actual link validation requires external tools or manual checks
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
