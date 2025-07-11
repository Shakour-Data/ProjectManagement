import unittest
import os
import re

class TestDocumentationLinks(unittest.TestCase):
    def setUp(self):
        self.docs_dirs = [
            "general_docs",
            "project_management/docs",
            "general_docs/general_instructions"
        ]
        self.url_pattern = re.compile(r'https?://[^\s)]+')

    def test_links_format(self):
        for docs_dir in self.docs_dirs:
            for root, _, files in os.walk(docs_dir):
                for file in files:
                    if file.endswith(".md"):
                        file_path = os.path.join(root, file)
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        urls = self.url_pattern.findall(content)
                        for url in urls:
                            self.assertTrue(url.startswith("http://") or url.startswith("https://"), f"URL {url} in {file_path} is not valid")

if __name__ == "__main__":
    unittest.main()
