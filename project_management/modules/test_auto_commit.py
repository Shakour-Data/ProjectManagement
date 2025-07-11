import unittest
from unittest.mock import patch, MagicMock
from modules import auto_commit

class TestAutoCommit(unittest.TestCase):

    @patch('modules.auto_commit.run_git_command')
    @patch('modules.auto_commit.get_git_changes')
    def test_auto_commit_and_push_no_changes(self, mock_get_changes, mock_run_git):
        mock_get_changes.return_value = []
        mock_run_git.return_value = (True, "")
        with patch('builtins.print') as mock_print:
            auto_commit.auto_commit_and_push()
            mock_print.assert_any_call("No changes detected.")

    @patch('modules.auto_commit.run_git_command')
    @patch('modules.auto_commit.get_git_changes')
    def test_auto_commit_and_push_with_changes(self, mock_get_changes, mock_run_git):
        # Simulate some changes
        mock_get_changes.return_value = ["M modules/auto_commit.py"]
        # Mock git commands for add, commit, push, pull
        def side_effect(args):
            if args[0] == "pull":
                return (True, "Already up to date.")
            elif args[0] == "add":
                return (True, "")
            elif args[0] == "commit":
                return (True, "")
            elif args[0] == "push":
                return (True, "")
            elif args[0] == "status":
                return (True, " M modules/auto_commit.py")
            elif args[0] == "log":
                return (True, "commit message example")
            elif args[0] == "diff":
                return (True, "diff --git a/modules/auto_commit.py b/modules/auto_commit.py\n+some changes")
            return (True, "")
        mock_run_git.side_effect = side_effect

        with patch('builtins.print') as mock_print:
            auto_commit.auto_commit_and_push()
            mock_print.assert_any_call("Committed and pushed changes for file: modules/auto_commit.py in group: modules - Modified")

if __name__ == "__main__":
    unittest.main()
