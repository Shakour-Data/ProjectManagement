import unittest
import os
import json
from unittest.mock import patch, MagicMock
import auto_commit

class TestAutoCommit(unittest.TestCase):

    @patch('auto_commit.get_git_changes')
    @patch('auto_commit.group_related_files')
    @patch('auto_commit.categorize_files')
    def test_collect_commit_progress(self, mock_categorize, mock_group_related, mock_get_changes):
        # Setup mocks
        mock_get_changes.return_value = ['M file1.py', 'A file2.py']
        mock_group_related.return_value = {
            'root': [('M', 'file1.py'), ('A', 'file2.py')]
        }
        mock_categorize.return_value = {
            'Modified': ['file1.py'],
            'Added': ['file2.py']
        }

        progress = auto_commit.collect_commit_progress()
        self.assertIn('root', progress)
        self.assertIn('Modified', progress['root'])
        self.assertIn('Added', progress['root'])
        self.assertEqual(progress['root']['Modified']['files'], ['file1.py'])
        self.assertEqual(progress['root']['Added']['files'], ['file2.py'])
        self.assertTrue(all('commit_message' in cm for cm in progress['root']['Modified']['commit_messages']))
        self.assertTrue(all('commit_message' in cm for cm in progress['root']['Added']['commit_messages']))

    @patch('auto_commit.collect_commit_progress')
    def test_write_commit_progress_to_json(self, mock_collect):
        mock_collect.return_value = {
            'root': {
                'Added': {
                    'files': ['file2.py'],
                    'commit_messages': [{'file': 'file2.py', 'commit_message': 'msg'}]
                }
            }
        }
        test_file = 'tests/temp_commit_progress.json'
        if os.path.exists(test_file):
            os.remove(test_file)

        auto_commit.write_commit_progress_to_json(test_file)
        self.assertTrue(os.path.exists(test_file))

        with open(test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertIn('root', data)
        os.remove(test_file)

    @patch('auto_commit.run_git_command')
    @patch('auto_commit.get_git_changes')
    @patch('auto_commit.group_related_files')
    @patch('auto_commit.categorize_files')
    @patch('auto_commit.write_commit_progress_to_json')
    def test_auto_commit_and_push_calls_write_json(self, mock_write_json, mock_categorize, mock_group_related, mock_get_changes, mock_run_git):
        mock_get_changes.return_value = ['M file1.py']
        mock_group_related.return_value = {
            'root': [('M', 'file1.py')]
        }
        mock_categorize.return_value = {
            'Modified': ['file1.py']
        }
        mock_run_git.return_value = (True, '')

        auto_commit.auto_commit_and_push()
        mock_write_json.assert_called_once()

if __name__ == '__main__':
    unittest.main()
