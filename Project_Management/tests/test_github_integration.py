import unittest
from unittest.mock import patch, MagicMock
from src.github_integration import GitHubIntegration

class TestGitHubIntegration(unittest.TestCase):
    def setUp(self):
        self.token = "fake_token"
        self.repo = "user/repo"
        self.github = GitHubIntegration(token=self.token, repo=self.repo)

    @patch('src.github_integration.os.getenv', return_value=None)
    def test_init_without_token_raises(self, mock_getenv):
        with self.assertRaises(ValueError):
            GitHubIntegration(token=None, repo=self.repo)

    def test_init_without_repo_raises(self):
        with self.assertRaises(ValueError):
            GitHubIntegration(token=self.token, repo=None)

    @patch('src.github_integration.requests.get')
    def test_get_issues_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = [{"id": 1, "title": "Issue 1"}]
        mock_get.return_value = mock_response

        issues = self.github.get_issues(state='open')
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]['title'], "Issue 1")
        mock_get.assert_called_once()

    @patch('src.github_integration.requests.get')
    def test_get_issues_http_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("HTTP Error")
        mock_get.return_value = mock_response

        with self.assertRaises(Exception):
            self.github.get_issues(state='open')

    def test_placeholder_methods_exist(self):
        self.assertTrue(callable(self.github.create_issue))
        self.assertTrue(callable(self.github.update_issue))
        self.assertTrue(callable(self.github.close_issue))
        self.assertTrue(callable(self.github.sync_project_board))
        self.assertTrue(callable(self.github.link_pull_request))
        self.assertTrue(callable(self.github.update_wiki))

if __name__ == '__main__':
    unittest.main()
