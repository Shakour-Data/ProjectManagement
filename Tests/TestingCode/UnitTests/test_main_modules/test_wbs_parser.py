import unittest
from unittest.mock import patch, mock_open
import os
import re
import json

# Add the project root to the path so we can import the module
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

class TestWBSParser(unittest.TestCase):
    def setUp(self):
        # Setup any necessary test data or state
        self.test_wbs_text = """1 Project Management Tool
1.1 Requirements Analysis
1.1.1 Gather User Requirements
1.1.2 Define System Requirements
1.2 Design Phase
1.2.1 System Architecture Design
1.2.2 UI/UX Design
1.3 Implementation
1.3.1 Backend Development
1.3.2 Frontend Development
1.4 Testing
1.4.1 Unit Testing
1.4.2 Integration Testing
1.5 Deployment
1.5.1 Production Deployment
1.5.2 Post-Deployment Support"""

        self.test_wbs_text_with_empty_lines = """1 Project Management Tool

1.1 Requirements Analysis

1.1.1 Gather User Requirements
1.1.2 Define System Requirements

1.2 Design Phase

1.2.1 System Architecture Design
1.2.2 UI/UX Design"""

    # Test 1: Test parse_detailed_implementation_plan with valid data
    @patch("builtins.open", new_callable=mock_open, read_data="1 Project Management Tool\n1.1 Requirements Analysis\n1.1.1 Gather User Requirements")
    def test_parse_detailed_implementation_plan_valid_data(self, mock_open_file):
        from project_management.modules.main_modules.wbs_parser import parse_detailed_implementation_plan
        result = parse_detailed_implementation_plan('test.txt')
        
        # Verify that the result is a list
        self.assertIsInstance(result, list)
        
        # Verify that the first task has the correct structure
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], '1')
        self.assertEqual(result[0]['title'], 'Project Management Tool')
        self.assertEqual(result[0]['level'], 1)

    # Test 2: Test parse_detailed_implementation_plan with hierarchical data
    @patch("builtins.open", new_callable=mock_open, read_data="1 Project Management Tool\n1.1 Requirements Analysis\n1.1.1 Gather User Requirements")
    def test_parse_detailed_implementation_plan_hierarchical_data(self, mock_open_file):
        from project_management.modules.main_modules.wbs_parser import parse_detailed_implementation_plan
        result = parse_detailed_implementation_plan('test.txt')
        
        # Verify that the hierarchical structure is correct
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], '1')
        self.assertEqual(result[0]['title'], 'Project Management Tool')
        self.assertEqual(result[0]['level'], 1)
        
        # Verify subtasks
        self.assertIn('subtasks', result[0])
        self.assertEqual(len(result[0]['subtasks']), 1)
        self.assertEqual(result[0]['subtasks'][0]['id'], '1.1')
        self.assertEqual(result[0]['subtasks'][0]['title'], 'Requirements Analysis')
        self.assertEqual(result[0]['subtasks'][0]['level'], 2)
        
        # Verify nested subtasks
        self.assertIn('subtasks', result[0]['subtasks'][0])
        self.assertEqual(len(result[0]['subtasks'][0]['subtasks']), 1)
        self.assertEqual(result[0]['subtasks'][0]['subtasks'][0]['id'], '1.1.1')
        self.assertEqual(result[0]['subtasks'][0]['subtasks'][0]['title'], 'Gather User Requirements')
        self.assertEqual(result[0]['subtasks'][0]['subtasks'][0]['level'], 3)

    # Test 3: Test parse_detailed_implementation_plan with empty lines
    @patch("builtins.open", new_callable=mock_open, read_data="1 Project Management Tool\n\n1.1 Requirements Analysis\n\n1.1.1 Gather User Requirements")
    def test_parse_detailed_implementation_plan_empty_lines(self, mock_open_file):
        from project_management.modules.main_modules.wbs_parser import parse_detailed_implementation_plan
        result = parse_detailed_implementation_plan('test.txt')
        
        # Verify that empty lines are ignored
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], '1')
        self.assertEqual(result[0]['title'], 'Project Management Tool')
        self.assertEqual(result[0]['level'], 1)
        
        # Verify subtasks
        self.assertEqual(len(result[0]['subtasks']), 1)
        self.assertEqual(result[0]['subtasks'][0]['id'], '1.1')
        self.assertEqual(result[0]['subtasks'][0]['title'], 'Requirements Analysis')
        self.assertEqual(result[0]['subtasks'][0]['level'], 2)

    # Test 4: Test parse_detailed_implementation_plan with no data
    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_parse_detailed_implementation_plan_no_data(self, mock_open_file):
        from project_management.modules.main_modules.wbs_parser import parse_detailed_implementation_plan
        result = parse_detailed_implementation_plan('test.txt')
        
        # Verify that an empty list is returned
        self.assertEqual(result, [])

    # Test 5: Test parse_detailed_implementation_plan with invalid format
    @patch("builtins.open", new_callable=mock_open, read_data="Invalid line format\nAnother invalid line")
    def test_parse_detailed_implementation_plan_invalid_format(self, mock_open_file):
        from project_management.modules.main_modules.wbs_parser import parse_detailed_implementation_plan
        result = parse_detailed_implementation_plan('test.txt')
        
        # Verify that no tasks are parsed from invalid format
        self.assertEqual(result, [])

    # Test 6: Test parse_detailed_implementation_plan with unicode data
    @patch("builtins.open", new_callable=mock_open, read_data="1 مشروع\n1.1 تحليل المتطلبات")
    def test_parse_detailed_implementation_plan_unicode_data(self, mock_open_file):
        from project_management.modules.main_modules.wbs_parser import parse_detailed_implementation_plan
        result = parse_detailed_implementation_plan('test.txt')
        
        # Verify that unicode data is handled correctly
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], '1')
        self.assertEqual(result[0]['title'], 'مشروع')
        self.assertEqual(result[0]['level'], 1)
        
        # Verify subtasks
        self.assertEqual(len(result[0]['subtasks']), 1)
        self.assertEqual(result[0]['subtasks'][0]['id'], '1.1')
        self.assertEqual(result[0]['subtasks'][0]['title'], 'تحليل المتطلبات')
        self.assertEqual(result[0]['subtasks'][0]['level'], 2)

    # Test 7: Test parse_detailed_implementation_plan with special characters
    @patch("builtins.open", new_callable=mock_open, read_data="1 Task!@#$%^&*()\n1.1 Subtask\nwith\nnewlines")
    def test_parse_detailed_implementation_plan_special_characters(self, mock_open_file):
        from project_management.modules.main_modules.wbs_parser import parse_detailed_implementation_plan
        result = parse_detailed_implementation_plan('test.txt')
        
        # Verify that special characters are handled correctly
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], '1')
        self.assertEqual(result[0]['title'], 'Task!@#$%^&*()')
        self.assertEqual(result[0]['level'], 1)
        
        # Verify subtasks
        self.assertEqual(len(result[0]['subtasks']), 1)
        self.assertEqual(result[0]['subtasks'][0]['id'], '1.1')
        self.assertEqual(result[0]['subtasks'][0]['title'], 'Subtask')
        self.assertEqual(result[0]['subtasks'][0]['level'], 2)

    # Test 8: Test parse_detailed_implementation_plan with large data
    @patch("builtins.open", new_callable=mock_open)
    def test_parse_detailed_implementation_plan_large_data(self, mock_open_file):
        from project_management.modules.main_modules.wbs_parser import parse_detailed_implementation_plan
        
        # Create large WBS text with 100 tasks
        large_wbs_text = ""
        for i in range(100):
            large_wbs_text += f"{i+1} Task {i+1}\n"
            for j in range(5):
                large_wbs_text += f"{i+1}.{j+1} Subtask {i+1}.{j+1}\n"
        
        mock_open_file.return_value.read.return_value = large_wbs_text
        result = parse_detailed_implementation_plan('test.txt')
        
        # Verify that all tasks are parsed
        self.assertEqual(len(result), 100)
        # Verify that subtasks are parsed for the first task
        self.assertEqual(len(result[0]['subtasks']), 5)

    # Test 9: Test parse_detailed_implementation_plan with file not found
    @patch("builtins.open", side_effect=FileNotFoundError("File not found"))
    def test_parse_detailed_implementation_plan_file_not_found(self, mock_open_file):
        from project_management.modules.main_modules.wbs_parser import parse_detailed_implementation_plan
        
        # Verify that the exception is raised
        with self.assertRaises(FileNotFoundError) as context:
            parse_detailed_implementation_plan('nonexistent.txt')
        
        self.assertIn("File not found", str(context.exception))

    # Test 10: Test parse_detailed_implementation_plan with permission error
    @patch("builtins.open", side_effect=PermissionError("Permission denied"))
    def test_parse_detailed_implementation_plan_permission_error(self, mock_open_file):
        from project_management.modules.main_modules.wbs_parser import parse_detailed_implementation_plan
        
        # Verify that the exception is raised
        with self.assertRaises(PermissionError) as context:
            parse_detailed_implementation_plan('protected.txt')
        
        self.assertIn("Permission denied", str(context.exception))

    # Test 11: Test save_wbs_to_json with valid data
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_wbs_to_json_valid_data(self, mock_json_dump, mock_open_file):
        from project_management.modules.main_modules.wbs_parser import save_wbs_to_json
        
        test_wbs = [
            {
                "id": "1",
                "title": "Project Management Tool",
                "level": 1,
                "subtasks": [
                    {
                        "id": "1.1",
                        "title": "Requirements Analysis",
                        "level": 2,
                        "subtasks": []
                    }
                ]
            }
        ]
        
        save_wbs_to_json(test_wbs, 'output.json')
        
        # Verify that open was called with correct parameters
        mock_open_file.assert_called_once_with('output.json', 'w', encoding='utf-8')
        
        # Verify that json.dump was called with correct parameters
        mock_json_dump.assert_called_once()

    # Test 12: Test save_wbs_to_json with empty data
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_wbs_to_json_empty_data(self, mock_json_dump, mock_open_file):
        from project_management.modules.main_modules.wbs_parser import save_wbs_to_json
        
        save_wbs_to_json([], 'output.json')
        
        # Verify that open was called with correct parameters
        mock_open_file.assert_called_once_with('output.json', 'w', encoding='utf-8')
        
        # Verify that json.dump was called with correct parameters
        mock_json_dump.assert_called_once_with([], mock_open_file(), ensure_ascii=False, indent=2)

    # Test 13: Test save_wbs_to_json with unicode data
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_wbs_to_json_unicode_data(self, mock_json_dump, mock_open_file):
        from project_management.modules.main_modules.wbs_parser import save_wbs_to_json
        
        test_wbs = [
            {
                "id": "1",
                "title": "مشروع",  # "Project" in Arabic
                "level": 1,
                "subtasks": []
            }
        ]
        
        save_wbs_to_json(test_wbs, 'output.json')
        
        # Verify that open was called with correct parameters
        mock_open_file.assert_called_once_with('output.json', 'w', encoding='utf-8')
        
        # Verify that json.dump was called with correct parameters
        mock_json_dump.assert_called_once()

    # Test 14: Test save_wbs_to_json with special characters
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_wbs_to_json_special_characters(self, mock_json_dump, mock_open_file):
        from project_management.modules.main_modules.wbs_parser import save_wbs_to_json
        
        test_wbs = [
            {
                "id": "1",
                "title": "Task!@#$%^&*()",
                "level": 1,
                "subtasks": [
                    {
                        "id": "1.1",
                        "title": "Subtask\nwith\nnewlines",
                        "level": 2,
                        "subtasks": []
                    }
                ]
            }
        ]
        
        save_wbs_to_json(test_wbs, 'output.json')
        
        # Verify that open was called with correct parameters
        mock_open_file.assert_called_once_with('output.json', 'w', encoding='utf-8')
        
        # Verify that json.dump was called with correct parameters
        mock_json_dump.assert_called_once()

    # Test 15: Test save_wbs_to_json with permission error
    @patch("builtins.open", side_effect=PermissionError("Permission denied"))
    def test_save_wbs_to_json_permission_error(self, mock_open_file):
        from project_management.modules.main_modules.wbs_parser import save_wbs_to_json
        
        test_wbs = [
            {
                "id": "1",
                "title": "Project Management Tool",
                "level": 1,
                "subtasks": []
            }
        ]
        
        # Verify that the exception is raised
        with self.assertRaises(PermissionError) as context:
            save_wbs_to_json(test_wbs, 'protected.json')
        
        self.assertIn("Permission denied", str(context.exception))

    # Test 16: Test save_wbs_to_json with disk full error
    @patch("builtins.open", side_effect=OSError("No space left on device"))
    def test_save_wbs_to_json_disk_full_error(self, mock_open_file):
        from project_management.modules.main_modules.wbs_parser import save_wbs_to_json
        
        test_wbs = [
            {
                "id": "1",
                "title": "Project Management Tool",
                "level": 1,
                "subtasks": []
            }
        ]
        
        # Verify that the exception is raised
        with self.assertRaises(OSError) as context:
            save_wbs_to_json(test_wbs, 'full_disk.json')
        
        self.assertIn("No space left on device", str(context.exception))

    # Test 17: Test parse_detailed_implementation_plan with complex hierarchy
    @patch("builtins.open", new_callable=mock_open, read_data="1 Project\n1.1 Phase 1\n1.1.1 Task 1.1.1\n1.1.2 Task 1.1.2\n1.2 Phase 2\n1.2.1 Task 1.2.1\n1.2.1.1 Subtask 1.2.1.1\n1.3 Phase 3")
    def test_parse_detailed_implementation_plan_complex_hierarchy(self, mock_open_file):
        from project_management.modules.main_modules.wbs_parser import parse_detailed_implementation_plan
        result = parse_detailed_implementation_plan('test.txt')
        
        # Verify the complex hierarchy structure
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], '1')
        self.assertEqual(result[0]['title'], 'Project')
        
        # Verify Phase 1 and its subtasks
        phase1 = result[0]['subtasks'][0]
        self.assertEqual(phase1['id'], '1.1')
        self.assertEqual(phase1['title'], 'Phase 1')
        self.assertEqual(len(phase1['subtasks']), 2)
        
        # Verify Phase 2 and its subtasks
        phase2 = result[0]['subtasks'][1]
        self.assertEqual(phase2['id'], '1.2')
        self.assertEqual(phase2['title'], 'Phase 2')
        self.assertEqual(len(phase2['subtasks']), 1)
        
        # Verify nested subtask in Phase 2
        subtask = phase2['subtasks'][0]['subtasks'][0]
        self.assertEqual(subtask['id'], '1.2.1.1')
        self.assertEqual(subtask['title'], 'Subtask 1.2.1.1')

    # Test 18: Test parse_detailed_implementation_plan with mixed level numbering
    @patch("builtins.open", new_callable=mock_open, read_data="1 Project\n1.1 Task 1.1\n1.1.1 Task 1.1.1\n1.2 Task 1.2\n2 Another Project\n2.1 Task 2.1")
    def test_parse_detailed_implementation_plan_mixed_level_numbering(self, mock_open_file):
        from project_management.modules.main_modules.wbs_parser import parse_detailed_implementation_plan
        result = parse_detailed_implementation_plan('test.txt')
        
        # Verify that multiple top-level tasks are handled correctly
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['id'], '1')
        self.assertEqual(result[0]['title'], 'Project')
        self.assertEqual(result[1]['id'], '2')
        self.assertEqual(result[1]['title'], 'Another Project')

    # Test 19: Test parse_detailed_implementation_plan with zero-padded numbering
    @patch("builtins.open", new_callable=mock_open, read_data="01 Project\n01.01 Task 1.1\n01.01.01 Task 1.1.1")
    def test_parse_detailed_implementation_plan_zero_padded_numbering(self, mock_open_file):
        from project_management.modules.main_modules.wbs_parser import parse_detailed_implementation_plan
        result = parse_detailed_implementation_plan('test.txt')
        
        # Verify that zero-padded numbering is handled correctly
        # Note: The regex in the original code expects standard numbering format
        # So this test will verify that such lines are ignored or handled gracefully
        self.assertEqual(result, [])

    # Test 20: Test parse_detailed_implementation_plan with very long task titles
    @patch("builtins.open", new_callable=mock_open)
    def test_parse_detailed_implementation_plan_very_long_task_titles(self, mock_open_file):
        from project_management.modules.main_modules.wbs_parser import parse_detailed_implementation_plan
        
        # Create a very long task title
        long_title = "Task " + "A" * 1000  # 1000 'A' characters
        test_data = f"1 {long_title}\n1.1 Subtask"
        mock_open_file.return_value.read.return_value = test_data
        
        result = parse_detailed_implementation_plan('test.txt')
        
        # Verify that long titles are handled correctly
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], '1')
        self.assertEqual(result[0]['title'], long_title)
        self.assertEqual(len(result[0]['subtasks']), 1)

if __name__ == "__main__":
    unittest.main()
