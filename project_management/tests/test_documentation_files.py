import unittest
import os

class TestDocumentationFiles(unittest.TestCase):
    def test_readme_exists_and_not_empty(self):
        readme_path = "ProjectManagement_Module/general_docs/README.md"
        self.assertTrue(os.path.exists(readme_path), "README.md file should exist")
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        self.assertTrue(len(content) > 0, "README.md file should not be empty")

    def test_help_exists_and_not_empty(self):
        help_path = "ProjectManagement_Module/project_management/HELP.md"
        self.assertTrue(os.path.exists(help_path), "HELP.md file should exist")
        with open(help_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        self.assertTrue(len(content) > 0, "HELP.md file should not be empty")

if __name__ == "__main__":
    unittest.main()
