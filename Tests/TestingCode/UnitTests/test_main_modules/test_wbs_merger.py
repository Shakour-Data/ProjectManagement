import unittest
from unittest.mock import patch, mock_open
import os
import json

# Add the project root to the path so we can import the module
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

class TestWBSMerger(unittest.TestCase):
    def setUp(self):
        # Setup any necessary test data or state
        self.test_wbs_part1 = {
            "id": 1,
            "name": "Project",
            "level": 0,
            "subtasks": [
                {
                    "id": 2,
                    "name": "Task 1",
                    "level": 1,
                    "subtasks": [
                        {
                            "id": 3,
                            "name": "Subtask 1.1",
                            "level": 2
                        }
                    ]
                }
            ]
        }
        
        self.test_wbs_part2 = {
            "id": 1,
            "name": "Project",
            "level": 0,
            "subtasks": [
                {
                    "id": 2,
                    "name": "Task 1 Updated",
                    "level": 1,
                    "subtasks": [
                        {
                            "id": 4,
                            "name": "Subtask 1.2",
                            "level": 2
                        }
                    ]
                },
                {
                    "id": 5,
                    "name": "Task 2",
                    "level": 1
                }
            ]
        }

    # Test 1: Test initialization with default paths
    def test_init_default_paths(self):
        from project_management.modules.main_modules.wbs_merger import WBSMerger
        merger = WBSMerger()
        self.assertEqual(merger.parts_dir, 'SystemInputs/user_inputs/wbs_parts')
        self.assertEqual(merger.output_file, 'SystemInputs/system_generated/detailed_wbs.json')

    # Test 2: Test initialization with custom paths
    def test_init_custom_paths(self):
        from project_management.modules.main_modules.wbs_merger import WBSMerger
        merger = WBSMerger('custom_parts_dir', 'custom_output.json')
        self.assertEqual(merger.parts_dir, 'custom_parts_dir')
        self.assertEqual(merger.output_file, 'custom_output.json')

    # Test 3: Test load_part method
    @patch("builtins.open", new_callable=mock_open, read_data='{"id": 1, "name": "Test"}')
    def test_load_part(self, mock_open_file):
        from project_management.modules.main_modules.wbs_merger import WBSMerger
        merger = WBSMerger()
        result = merger.load_part('test.json')
        self.assertEqual(result, {"id": 1, "name": "Test"})
        mock_open_file.assert_called_once_with('test.json', 'r', encoding='utf-8')

    # Test 4: Test merge_subtasks method with overlapping IDs
    def test_merge_subtasks_overlapping_ids(self):
        from project_management.modules.main_modules.wbs_merger import WBSMerger
        merger = WBSMerger()
        
        base_subtasks = [
            {
                "id": 1,
                "name": "Task 1"
            }
        ]
        
        additional_subtasks = [
            {
                "id": 1,
                "name": "Task 1 Updated"
            }
        ]
        
        result = merger.merge_subtasks(base_subtasks, additional_subtasks)
        
        # Verify that the task was merged (name updated)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Task 1 Updated')

    # Test 5: Test merge_subtasks method with new IDs
    def test_merge_subtasks_new_ids(self):
        from project_management.modules.main_modules.wbs_merger import WBSMerger
        merger = WBSMerger()
        
        base_subtasks = [
            {
                "id": 1,
                "name": "Task 1"
            }
        ]
        
        additional_subtasks = [
            {
                "id": 2,
                "name": "Task 2"
            }
        ]
        
        result = merger.merge_subtasks(base_subtasks, additional_subtasks)
        
        # Verify that both tasks are present
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['id'], 1)
        self.assertEqual(result[1]['id'], 2)

    # Test 6: Test merge_subtasks method with nested subtasks
    def test_merge_subtasks_nested_subtasks(self):
        from project_management.modules.main_modules.wbs_merger import WBSMerger
        merger = WBSMerger()
        
        base_subtasks = [
            {
                "id": 1,
                "name": "Task 1",
                "subtasks": [
                    {
                        "id": 2,
                        "name": "Subtask 1.1"
                    }
                ]
            }
        ]
        
        additional_subtasks = [
            {
                "id": 1,
                "name": "Task 1 Updated",
                "subtasks": [
                    {
                        "id": 3,
                        "name": "Subtask 1.2"
                    }
                ]
            }
        ]
        
        result = merger.merge_subtasks(base_subtasks, additional_subtasks)
        
        # Verify that the task was merged and subtasks were merged
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Task 1 Updated')
        self.assertEqual(len(result[0]['subtasks']), 2)
        self.assertEqual(result[0]['subtasks'][0]['id'], 2)
        self.assertEqual(result[0]['subtasks'][1]['id'], 3)

    # Test 7: Test merge_subtasks method with extended fields
    def test_merge_subtasks_extended_fields(self):
        from project_management.modules.main_modules.wbs_merger import WBSMerger
        merger = WBSMerger()
        
        base_subtasks = [
            {
                "id": 1,
                "name": "Task 1"
            }
        ]
        
        additional_subtasks = [
            {
                "id": 1,
                "name": "Task 1",
                "cost": 100,
                "quality_metrics": {"quality": "high"},
                "risk_factors": ["risk1", "risk2"],
                "resource_assignments": ["resource1"]
            }
        ]
        
        result = merger.merge_subtasks(base_subtasks, additional_subtasks)
        
        # Verify that extended fields were merged
        self.assertEqual(result[0]['cost'], 100)
        self.assertEqual(result[0]['quality_metrics'], {"quality": "high"})
        self.assertEqual(result[0]['risk_factors'], ["risk1", "risk2"])
        self.assertEqual(result[0]['resource_assignments'], ["resource1"])

    # Test 8: Test merge_all_parts method with valid data
    @patch("os.walk")
    @patch("project_management.modules.main_modules.wbs_merger.WBSMerger.load_part")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("builtins.print")
    def test_merge_all_parts_valid_data(self, mock_print, mock_json_dump, mock_open_file, mock_load_part, mock_walk):
        from project_management.modules.main_modules.wbs_merger import WBSMerger
        merger = WBSMerger()
        
        # Setup mock returns
        mock_walk.return_value = [('', [], ['part1.json', 'part2.json'])]
        mock_load_part.side_effect = [self.test_wbs_part1, self.test_wbs_part2]
        
        merger.merge_all_parts()
        
        # Verify methods were called
        mock_walk.assert_called_once_with(merger.parts_dir)
        self.assertEqual(mock_load_part.call_count, 2)
        mock_open_file.assert_called_once_with(merger.output_file, 'w', encoding='utf-8')
        mock_json_dump.assert_called_once()
        mock_print.assert_called_once_with(f"Merged detailed WBS saved to {merger.output_file}")

    # Test 9: Test merge_all_parts method with no WBS parts
    @patch("os.walk")
    @patch("builtins.print")
    def test_merge_all_parts_no_wbs_parts(self, mock_print, mock_walk):
        from project_management.modules.main_modules.wbs_merger import WBSMerger
        merger = WBSMerger()
        
        # Setup mock returns
        mock_walk.return_value = [('', [], [])]
        
        merger.merge_all_parts()
        
        # Verify methods were called
        mock_walk.assert_called_once_with(merger.parts_dir)
        mock_print.assert_called_once_with("No WBS parts found in directory.")

    # Test 10: Test merge_all_parts method with exception in load_part
    @patch("os.walk")
    @patch("project_management.modules.main_modules.wbs_merger.WBSMerger.load_part", side_effect=Exception("Failed to load part"))
    @patch("builtins.print")
    def test_merge_all_parts_exception_in_load_part(self, mock_print, mock_load_part, mock_walk):
        from project_management.modules.main_modules.wbs_merger import WBSMerger
        merger = WBSMerger()
        
        # Setup mock returns
        mock_walk.return_value = [('', [], ['part1.json'])]
        
        # Verify that the exception is raised
        with self.assertRaises(Exception) as context:
            merger.merge_all_parts()
        
        self.assertIn("Failed to load part", str(context.exception))

    # Test 11: Test merge_all_parts method with exception in json.dump
    @patch("os.walk")
    @patch("project_management.modules.main_modules.wbs_merger.WBSMerger.load_part")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump", side_effect=Exception("Failed to dump JSON"))
    @patch("builtins.print")
    def test_merge_all_parts_exception_in_json_dump(self, mock_print, mock_json_dump, mock_open_file, mock_load_part, mock_walk):
        from project_management.modules.main_modules.wbs_merger import WBSMerger
        merger = WBSMerger()
        
        # Setup mock returns
        mock_walk.return_value = [('', [], ['part1.json'])]
        mock_load_part.return_value = self.test_wbs_part1
        
        # Verify that the exception is raised
        with self.assertRaises(Exception) as context:
            merger.merge_all_parts()
        
        self.assertIn("Failed to dump JSON", str(context.exception))

    # Test 12: Test merge_all_parts method with unicode file names
    @patch("os.walk")
    @patch("project_management.modules.main_modules.wbs_merger.WBSMerger.load_part")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("builtins.print")
    def test_merge_all_parts_unicode_file_names(self, mock_print, mock_json_dump, mock_open_file, mock_load_part, mock_walk):
        from project_management.modules.main_modules.wbs_merger import WBSMerger
        merger = WBSMerger()
        
        # Setup mock returns with unicode file names
        mock_walk.return_value = [('', [], ['جزء1.json', 'جزء2.json'])]  # "part1.json" and "part2.json" in Arabic
        mock_load_part.side_effect = [self.test_wbs_part1, self.test_wbs_part2]
        
        merger.merge_all_parts()
        
        # Verify methods were called
        mock_walk.assert_called_once_with(merger.parts_dir)

    # Test 13: Test merge_all_parts method with special characters in file names
    @patch("os.walk")
    @patch("project_management.modules.main_modules.wbs_merger.WBSMerger.load_part")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("builtins.print")
    def test_merge_all_parts_special_characters_in_file_names(self, mock_print, mock_json_dump, mock_open_file, mock_load_part, mock_walk):
        from project_management.modules.main_modules.wbs_merger import WBSMerger
        merger = WBSMerger()
        
        # Setup mock returns with special characters in file names
        mock_walk.return_value = [('', [], ['part!@#.json', 'part$%^&.json'])]
        mock_load_part.side_effect = [self.test_wbs_part1, self.test_wbs_part2]
        
        merger.merge_all_parts()
        
        # Verify methods were called
        mock_walk.assert_called_once_with(merger.parts_dir)

    # Test 14: Test merge_all_parts method with large number of WBS parts
    @patch("os.walk")
    @patch("project_management.modules.main_modules.wbs_merger.WBSMerger.load_part")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("builtins.print")
    def test_merge_all_parts_large_number_of_wbs_parts(self, mock_print, mock_json_dump, mock_open_file, mock_load_part, mock_walk):
        from project_management.modules.main_modules.wbs_merger import WBSMerger
        merger = WBSMerger()
        
        # Setup mock returns with 100 WBS parts
        file_names = [f'part{i}.json' for i in range(100)]
        mock_walk.return_value = [('', [], file_names)]
        
        # Create 100 test WBS parts
        test_parts = []
        for i in range(100):
            part = {
                "id": 1,
                "name": "Project",
                "level": 0,
                "subtasks": [
                    {
                        "id": i + 2,
                        "name": f"Task {i + 1}",
                        "level": 1
                    }
                ]
            }
            test_parts.append(part)
        
        mock_load_part.side_effect = test_parts
        
        merger.merge_all_parts()
        
        # Verify methods were called
        mock_walk.assert_called_once_with(merger.parts_dir)
        self.assertEqual(mock_load_part.call_count, 100)

    # Test 15: Test merge_all_parts method with nested subtasks
    @patch("os.walk")
    @patch("project_management.modules.main_modules.wbs_merger.WBSMerger.load_part")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("builtins.print")
    def test_merge_all_parts_nested_subtasks(self, mock_print, mock_json_dump, mock_open_file, mock_load_part, mock_walk):
        from project_management.modules.main_modules.wbs_merger import WBSMerger
        merger = WBSMerger()
        
        # Setup WBS part with deeply nested subtasks
        nested_wbs_part = {
            "id": 1,
            "name": "Project",
            "level": 0,
            "subtasks": [
                {
                    "id": 2,
                    "name": "Task 1",
                    "level": 1,
                    "subtasks": [
                        {
                            "id": 3,
                            "name": "Subtask 1.1",
                            "level": 2,
                            "subtasks": [
                                {
                                    "id": 4,
                                    "name": "Subtask 1.1.1",
                                    "level": 3,
                                    "subtasks": [
                                        {
                                            "id": 5,
                                            "name": "Subtask 1.1.1.1",
                                            "level": 4
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        # Setup mock returns
        mock_walk.return_value = [('', [], ['part1.json'])]
        mock_load_part.return_value = nested_wbs_part
        
        merger.merge_all_parts()
        
        # Verify methods were called
        mock_walk.assert_called_once_with(merger.parts_dir)
        mock_load_part.assert_called_once_with(os.path.join(merger.parts_dir, 'part1.json'))
        mock_open_file.assert_called_once_with(merger.output_file, 'w', encoding='utf-8')

    # Test 16: Test merge_all_parts method with empty subtasks
    @patch("os.walk")
    @patch("project_management.modules.main_modules.wbs_merger.WBSMerger.load_part")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("builtins.print")
    def test_merge_all_parts_empty_subtasks(self, mock_print, mock_json_dump, mock_open_file, mock_load_part, mock_walk):
        from project_management.modules.main_modules.wbs_merger import WBSMerger
        merger = WBSMerger()
        
        # Setup WBS part with empty subtasks
        empty_subtasks_part = {
            "id": 1,
            "name": "Project",
            "level": 0,
            "subtasks": []
        }
        
        # Setup mock returns
        mock_walk.return_value = [('', [], ['part1.json'])]
        mock_load_part.return_value = empty_subtasks_part
        
        merger.merge_all_parts()
        
        # Verify methods were called
        mock_walk.assert_called_once_with(merger.parts_dir)
        mock_load_part.assert_called_once_with(os.path.join(merger.parts_dir, 'part1.json'))
        mock_open_file.assert_called_once_with(merger.output_file, 'w', encoding='utf-8')

    # Test 17: Test merge_all_parts method with unicode task names
    @patch("os.walk")
    @patch("project_management.modules.main_modules.wbs_merger.WBSMerger.load_part")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("builtins.print")
    def test_merge_all_parts_unicode_task_names(self, mock_print, mock_json_dump, mock_open_file, mock_load_part, mock_walk):
        from project_management.modules.main_modules.wbs_merger import WBSMerger
        merger = WBSMerger()
        
        # Setup WBS part with unicode task names
        unicode_wbs_part = {
            "id": 1,
            "name": "مشروع",  # "Project" in Arabic
            "level": 0,
            "subtasks": [
                {
                    "id": 2,
                    "name": "مهمة 1",  # "Task 1" in Arabic
                    "level": 1
                }
            ]
        }
        
        # Setup mock returns
        mock_walk.return_value = [('', [], ['part1.json'])]
        mock_load_part.return_value = unicode_wbs_part
        
        merger.merge_all_parts()
        
        # Verify methods were called
        mock_walk.assert_called_once_with(merger.parts_dir)
        mock_load_part.assert_called_once_with(os.path.join(merger.parts_dir, 'part1.json'))
        mock_open_file.assert_called_once_with(merger.output_file, 'w', encoding='utf-8')

    # Test 18: Test merge_all_parts method with special characters in task names
    @patch("os.walk")
    @patch("project_management.modules.main_modules.wbs_merger.WBSMerger.load_part")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("builtins.print")
    def test_merge_all_parts_special_characters_in_task_names(self, mock_print, mock_json_dump, mock_open_file, mock_load_part, mock_walk):
        from project_management.modules.main_modules.wbs_merger import WBSMerger
        merger = WBSMerger()
        
        # Setup WBS part with special characters in task names
        special_chars_wbs_part = {
            "id": 1,
            "name": "Task!@#$%^&*()",
            "level": 0,
            "subtasks": [
                {
                    "id": 2,
                    "name": "Subtask\nwith\nnewlines",
                    "level": 1
                }
            ]
        }
        
        # Setup mock returns
        mock_walk.return_value = [('', [], ['part1.json'])]
        mock_load_part.return_value = special_chars_wbs_part
        
        merger.merge_all_parts()
        
        # Verify methods were called
        mock_walk.assert_called_once_with(merger.parts_dir)
        mock_load_part.assert_called_once_with(os.path.join(merger.parts_dir, 'part1.json'))
        mock_open_file.assert_called_once_with(merger.output_file, 'w', encoding='utf-8')

    # Test 19: Test merge_all_parts method with mixed WBS parts
    @patch("os.walk")
    @patch("project_management.modules.main_modules.wbs_merger.WBSMerger.load_part")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("builtins.print")
    def test_merge_all_parts_mixed_wbs_parts(self, mock_print, mock_json_dump, mock_open_file, mock_load_part, mock_walk):
        from project_management.modules.main_modules.wbs_merger import WBSMerger
        merger = WBSMerger()
        
        # Setup different WBS parts
        wbs_part1 = {
            "id": 1,
            "name": "Project",
            "level": 0,
            "subtasks": [
                {
                    "id": 2,
                    "name": "Task 1",
                    "level": 1
                }
            ]
        }
        
        wbs_part2 = {
            "id": 1,
            "name": "Project",
            "level": 0,
            "subtasks": [
                {
                    "id": 3,
                    "name": "Task 2",
                    "level": 1
                }
            ]
        }
        
        # Setup mock returns
        mock_walk.return_value = [('', [], ['part1.json', 'part2.json'])]
        mock_load_part.side_effect = [wbs_part1, wbs_part2]
        
        merger.merge_all_parts()
        
        # Verify methods were called
        mock_walk.assert_called_once_with(merger.parts_dir)
        self.assertEqual(mock_load_part.call_count, 2)
        mock_open_file.assert_called_once_with(merger.output_file, 'w', encoding='utf-8')

    # Test 20: Test merge_all_parts method with duplicate task IDs
    @patch("os.walk")
    @patch("project_management.modules.main_modules.wbs_merger.WBSMerger.load_part")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("builtins.print")
    def test_merge_all_parts_duplicate_task_ids(self, mock_print, mock_json_dump, mock_open_file, mock_load_part, mock_walk):
        from project_management.modules.main_modules.wbs_merger import WBSMerger
        merger = WBSMerger()
        
        # Setup WBS parts with duplicate task IDs
        wbs_part1 = {
            "id": 1,
            "name": "Project",
            "level": 0,
            "subtasks": [
                {
                    "id": 2,
                    "name": "Task 1",
                    "level": 1
                }
            ]
        }
        
        wbs_part2 = {
            "id": 1,
            "name": "Project",
            "level": 0,
            "subtasks": [
                {
                    "id": 2,  # Same ID as part1
                    "name": "Task 1 Duplicate",
                    "level": 1
                }
            ]
        }
        
        # Setup mock returns
        mock_walk.return_value = [('', [], ['part1.json', 'part2.json'])]
        mock_load_part.side_effect = [wbs_part1, wbs_part2]
        
        merger.merge_all_parts()
        
        # Verify methods were called
        mock_walk.assert_called_once_with(merger.parts_dir)
        self.assertEqual(mock_load_part.call_count, 2)
        mock_open_file.assert_called_once_with(merger.output_file, 'w', encoding='utf-8')

if __name__ == "__main__":
    unittest.main()
