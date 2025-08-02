import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

class TestTaskExecutor(unittest.TestCase):
    def setUp(self):
        # Setup any necessary test data or state
        pass

    # Test 1: Test main function execution with normal flow
    @patch('project_management.modules.main_modules.task_executor.TaskManagement')
    @patch('builtins.print')
    def test_main_execution_normal_flow(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.task_executor import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock tasks with MagicMock
        mock_task1 = MagicMock()
        mock_task1.id = 1
        mock_task1.title = "Task 1"
        mock_task1.importance = 0.9
        mock_task1.urgency = 0.8
        mock_task1.status = "pending"
        
        mock_task2 = MagicMock()
        mock_task2.id = 2
        mock_task2.title = "Task 2"
        mock_task2.importance = 0.8
        mock_task2.urgency = 0.7
        mock_task2.status = "pending"
        
        # Setup prioritized tasks (20 tasks total)
        prioritized_tasks = [mock_task1, mock_task2] + [MagicMock() for _ in range(18)]
        for i, task in enumerate(prioritized_tasks[2:], 3):
            task.id = i
            task.title = f"Task {i}"
            task.importance = 1.0 - (i * 0.01)
            task.urgency = 1.0 - (i * 0.02)
            task.status = "pending"
        
        mock_tm_instance.prioritize_tasks.return_value = prioritized_tasks
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Complete Project Management Tool")
        mock_tm_instance.prioritize_tasks.assert_called_once()
        
        # Verify that print was called for top 10 tasks
        self.assertTrue(mock_print.call_count >= 20)  # At least 20 print calls

    # Test 2: Test main function with empty prioritized tasks
    @patch('project_management.modules.main_modules.task_executor.TaskManagement')
    @patch('builtins.print')
    def test_main_execution_empty_prioritized_tasks(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.task_executor import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        mock_tm_instance.prioritize_tasks.return_value = []
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Complete Project Management Tool")
        mock_tm_instance.prioritize_tasks.assert_called_once()
        
        # Verify that print was called for empty lists
        mock_print.assert_any_call("Top 10 tasks by priority (importance and urgency):")

    # Test 3: Test main function with less than 10 prioritized tasks
    @patch('project_management.modules.main_modules.task_executor.TaskManagement')
    @patch('builtins.print')
    def test_main_execution_less_than_10_prioritized_tasks(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.task_executor import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup 5 mock tasks
        tasks = []
        for i in range(5):
            mock_task = MagicMock()
            mock_task.id = i + 1
            mock_task.title = f"Task {i + 1}"
            mock_task.importance = 1.0 - (i * 0.1)
            mock_task.urgency = 1.0 - (i * 0.05)
            mock_task.status = "pending"
            tasks.append(mock_task)
        
        mock_tm_instance.prioritize_tasks.return_value = tasks
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Complete Project Management Tool")
        mock_tm_instance.prioritize_tasks.assert_called_once()

    # Test 4: Test main function with exactly 10 prioritized tasks
    @patch('project_management.modules.main_modules.task_executor.TaskManagement')
    @patch('builtins.print')
    def test_main_execution_exactly_10_prioritized_tasks(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.task_executor import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup 10 mock tasks
        tasks = []
        for i in range(10):
            mock_task = MagicMock()
            mock_task.id = i + 1
            mock_task.title = f"Task {i + 1}"
            mock_task.importance = 1.0 - (i * 0.05)
            mock_task.urgency = 1.0 - (i * 0.03)
            mock_task.status = "pending"
            tasks.append(mock_task)
        
        mock_tm_instance.prioritize_tasks.return_value = tasks
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Complete Project Management Tool")
        mock_tm_instance.prioritize_tasks.assert_called_once()

    # Test 5: Test main function with exception in generate_wbs_from_idea
    @patch('project_management.modules.main_modules.task_executor.TaskManagement')
    @patch('builtins.print')
    def test_main_execution_exception_in_generate_wbs(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.task_executor import main
        
        # Setup mock TaskManagement instance to raise exception
        mock_tm_instance = mock_task_management.return_value
        mock_tm_instance.generate_wbs_from_idea.side_effect = Exception("Failed to generate WBS")
        
        # Verify that the exception is raised
        with self.assertRaises(Exception) as context:
            main()
        
        self.assertIn("Failed to generate WBS", str(context.exception))

    # Test 6: Test main function with exception in prioritize_tasks
    @patch('project_management.modules.main_modules.task_executor.TaskManagement')
    @patch('builtins.print')
    def test_main_execution_exception_in_prioritize_tasks(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.task_executor import main
        
        # Setup mock TaskManagement instance to raise exception
        mock_tm_instance = mock_task_management.return_value
        mock_tm_instance.prioritize_tasks.side_effect = Exception("Failed to prioritize tasks")
        
        # Verify that the exception is raised
        with self.assertRaises(Exception) as context:
            main()
        
        self.assertIn("Failed to prioritize tasks", str(context.exception))

    # Test 7: Test main function with unicode task titles
    @patch('project_management.modules.main_modules.task_executor.TaskManagement')
    @patch('builtins.print')
    def test_main_execution_unicode_task_titles(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.task_executor import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock tasks with unicode titles
        mock_task1 = MagicMock()
        mock_task1.id = 1
        mock_task1.title = "مهمة 1"  # "Task 1" in Arabic
        mock_task1.importance = 0.9
        mock_task1.urgency = 0.8
        mock_task1.status = "pending"
        
        mock_task2 = MagicMock()
        mock_task2.id = 2
        mock_task2.title = "Задача 2"  # "Task 2" in Russian
        mock_task2.importance = 0.8
        mock_task2.urgency = 0.7
        mock_task2.status = "pending"
        
        # Setup prioritized tasks
        prioritized_tasks = [mock_task1, mock_task2] + [MagicMock() for _ in range(18)]
        for i, task in enumerate(prioritized_tasks[2:], 3):
            task.id = i
            task.title = f"任务 {i}"  # "Task i" in Chinese
            task.importance = 1.0 - (i * 0.01)
            task.urgency = 1.0 - (i * 0.02)
            task.status = "pending"
        
        mock_tm_instance.prioritize_tasks.return_value = prioritized_tasks
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Complete Project Management Tool")
        mock_tm_instance.prioritize_tasks.assert_called_once()

    # Test 8: Test main function with special characters in task titles
    @patch('project_management.modules.main_modules.task_executor.TaskManagement')
    @patch('builtins.print')
    def test_main_execution_special_characters_in_task_titles(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.task_executor import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock tasks with special characters
        mock_task1 = MagicMock()
        mock_task1.id = 1
        mock_task1.title = "Task!@#$%^&*()"
        mock_task1.importance = 0.9
        mock_task1.urgency = 0.8
        mock_task1.status = "pending"
        
        mock_task2 = MagicMock()
        mock_task2.id = 2
        mock_task2.title = "Task\nwith\nnewlines"
        mock_task2.importance = 0.8
        mock_task2.urgency = 0.7
        mock_task2.status = "pending"
        
        # Setup prioritized tasks
        prioritized_tasks = [mock_task1, mock_task2] + [MagicMock() for _ in range(18)]
        for i, task in enumerate(prioritized_tasks[2:], 3):
            task.id = i
            task.title = f"Task{i} with\ttabs"
            task.importance = 1.0 - (i * 0.01)
            task.urgency = 1.0 - (i * 0.02)
            task.status = "pending"
        
        mock_tm_instance.prioritize_tasks.return_value = prioritized_tasks
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Complete Project Management Tool")
        mock_tm_instance.prioritize_tasks.assert_called_once()

    # Test 9: Test main function with large number of tasks
    @patch('project_management.modules.main_modules.task_executor.TaskManagement')
    @patch('builtins.print')
    def test_main_execution_large_number_of_tasks(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.task_executor import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup 100 mock tasks
        tasks = []
        for i in range(100):
            mock_task = MagicMock()
            mock_task.id = i + 1
            mock_task.title = f"Task {i + 1}"
            mock_task.importance = 1.0 - (i * 0.005)
            mock_task.urgency = 1.0 - (i * 0.003)
            mock_task.status = "pending"
            tasks.append(mock_task)
        
        mock_tm_instance.prioritize_tasks.return_value = tasks
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Complete Project Management Tool")
        mock_tm_instance.prioritize_tasks.assert_called_once()

    # Test 10: Test main function with zero importance and urgency values
    @patch('project_management.modules.main_modules.task_executor.TaskManagement')
    @patch('builtins.print')
    def test_main_execution_zero_importance_urgency(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.task_executor import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock tasks with zero values
        mock_task1 = MagicMock()
        mock_task1.id = 1
        mock_task1.title = "Task 1"
        mock_task1.importance = 0.0
        mock_task1.urgency = 0.0
        mock_task1.status = "pending"
        
        mock_task2 = MagicMock()
        mock_task2.id = 2
        mock_task2.title = "Task 2"
        mock_task2.importance = 0.0
        mock_task2.urgency = 0.0
        mock_task2.status = "pending"
        
        # Setup prioritized tasks
        prioritized_tasks = [mock_task1, mock_task2] + [MagicMock() for _ in range(18)]
        for i, task in enumerate(prioritized_tasks[2:], 3):
            task.id = i
            task.title = f"Task {i}"
            task.importance = 0.0
            task.urgency = 0.0
            task.status = "pending"
        
        mock_tm_instance.prioritize_tasks.return_value = prioritized_tasks
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Complete Project Management Tool")
        mock_tm_instance.prioritize_tasks.assert_called_once()

    # Test 11: Test main function with negative importance and urgency values
    @patch('project_management.modules.main_modules.task_executor.TaskManagement')
    @patch('builtins.print')
    def test_main_execution_negative_importance_urgency(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.task_executor import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock tasks with negative values
        mock_task1 = MagicMock()
        mock_task1.id = 1
        mock_task1.title = "Task 1"
        mock_task1.importance = -0.5
        mock_task1.urgency = -0.3
        mock_task1.status = "pending"
        
        mock_task2 = MagicMock()
        mock_task2.id = 2
        mock_task2.title = "Task 2"
        mock_task2.importance = -0.8
        mock_task2.urgency = -0.6
        mock_task2.status = "pending"
        
        # Setup prioritized tasks
        prioritized_tasks = [mock_task1, mock_task2] + [MagicMock() for _ in range(18)]
        for i, task in enumerate(prioritized_tasks[2:], 3):
            task.id = i
            task.title = f"Task {i}"
            task.importance = -1.0 + (i * 0.01)
            task.urgency = -1.0 + (i * 0.02)
            task.status = "pending"
        
        mock_tm_instance.prioritize_tasks.return_value = prioritized_tasks
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Complete Project Management Tool")
        mock_tm_instance.prioritize_tasks.assert_called_once()

    # Test 12: Test main function with very high importance and urgency values
    @patch('project_management.modules.main_modules.task_executor.TaskManagement')
    @patch('builtins.print')
    def test_main_execution_very_high_importance_urgency(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.task_executor import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock tasks with very high values
        mock_task1 = MagicMock()
        mock_task1.id = 1
        mock_task1.title = "Task 1"
        mock_task1.importance = 100.0
        mock_task1.urgency = 99.0
        mock_task1.status = "pending"
        
        mock_task2 = MagicMock()
        mock_task2.id = 2
        mock_task2.title = "Task 2"
        mock_task2.importance = 200.0
        mock_task2.urgency = 199.0
        mock_task2.status = "pending"
        
        # Setup prioritized tasks
        prioritized_tasks = [mock_task1, mock_task2] + [MagicMock() for _ in range(18)]
        for i, task in enumerate(prioritized_tasks[2:], 3):
            task.id = i
            task.title = f"Task {i}"
            task.importance = 1000.0 - (i * 10)
            task.urgency = 999.0 - (i * 9)
            task.status = "pending"
        
        mock_tm_instance.prioritize_tasks.return_value = prioritized_tasks
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Complete Project Management Tool")
        mock_tm_instance.prioritize_tasks.assert_called_once()

    # Test 13: Test main function with task status changes
    @patch('project_management.modules.main_modules.task_executor.TaskManagement')
    @patch('builtins.print')
    def test_main_execution_task_status_changes(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.task_executor import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock tasks
        mock_task1 = MagicMock()
        mock_task1.id = 1
        mock_task1.title = "Task 1"
        mock_task1.importance = 0.9
        mock_task1.urgency = 0.8
        mock_task1.status = "pending"
        
        mock_task2 = MagicMock()
        mock_task2.id = 2
        mock_task2.title = "Task 2"
        mock_task2.importance = 0.8
        mock_task2.urgency = 0.7
        mock_task2.status = "pending"
        
        # Setup prioritized tasks
        prioritized_tasks = [mock_task1, mock_task2] + [MagicMock() for _ in range(18)]
        for i, task in enumerate(prioritized_tasks[2:], 3):
            task.id = i
            task.title = f"Task {i}"
            task.importance = 1.0 - (i * 0.01)
            task.urgency = 1.0 - (i * 0.02)
            task.status = "pending"
        
        mock_tm_instance.prioritize_tasks.return_value = prioritized_tasks
        
        main()
        
        # Verify that task statuses were changed
        self.assertEqual(mock_task1.status, "completed")
        self.assertEqual(mock_task2.status, "completed")

    # Test 14: Test main function with task status changes for all tasks
    @patch('project_management.modules.main_modules.task_executor.TaskManagement')
    @patch('builtins.print')
    def test_main_execution_task_status_changes_all_tasks(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.task_executor import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup 20 mock tasks
        tasks = []
        for i in range(20):
            mock_task = MagicMock()
            mock_task.id = i + 1
            mock_task.title = f"Task {i + 1}"
            mock_task.importance = 1.0 - (i * 0.02)
            mock_task.urgency = 1.0 - (i * 0.01)
            mock_task.status = "pending"
            tasks.append(mock_task)
        
        mock_tm_instance.prioritize_tasks.return_value = tasks
        
        main()
        
        # Verify that all task statuses were changed
        for task in tasks:
            self.assertEqual(task.status, "completed")

    # Test 15: Test main function with mixed task status values
    @patch('project_management.modules.main_modules.task_executor.TaskManagement')
    @patch('builtins.print')
    def test_main_execution_mixed_task_status_values(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.task_executor import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock tasks with different initial statuses
        mock_task1 = MagicMock()
        mock_task1.id = 1
        mock_task1.title = "Task 1"
        mock_task1.importance = 0.9
        mock_task1.urgency = 0.8
        mock_task1.status = "in_progress"
        
        mock_task2 = MagicMock()
        mock_task2.id = 2
        mock_task2.title = "Task 2"
        mock_task2.importance = 0.8
        mock_task2.urgency = 0.7
        mock_task2.status = "not_started"
        
        # Setup prioritized tasks
        prioritized_tasks = [mock_task1, mock_task2] + [MagicMock() for _ in range(18)]
        for i, task in enumerate(prioritized_tasks[2:], 3):
            task.id = i
            task.title = f"Task {i}"
            task.importance = 1.0 - (i * 0.01)
            task.urgency = 1.0 - (i * 0.02)
            task.status = "pending"
        
        mock_tm_instance.prioritize_tasks.return_value = prioritized_tasks
        
        main()
        
        # Verify that task statuses were changed to completed
        self.assertEqual(mock_task1.status, "completed")
        self.assertEqual(mock_task2.status, "completed")

    # Test 16: Test main function with None task attributes
    @patch('project_management.modules.main_modules.task_executor.TaskManagement')
    @patch('builtins.print')
    def test_main_execution_none_task_attributes(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.task_executor import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock tasks with None attributes
        mock_task1 = MagicMock()
        mock_task1.id = None
        mock_task1.title = None
        mock_task1.importance = None
        mock_task1.urgency = None
        mock_task1.status = None
        
        mock_task2 = MagicMock()
        mock_task2.id = None
        mock_task2.title = None
        mock_task2.importance = None
        mock_task2.urgency = None
        mock_task2.status = None
        
        # Setup prioritized tasks
        prioritized_tasks = [mock_task1, mock_task2] + [MagicMock() for _ in range(18)]
        for i, task in enumerate(prioritized_tasks[2:], 3):
            task.id = None
            task.title = None
            task.importance = None
            task.urgency = None
            task.status = None
        
        mock_tm_instance.prioritize_tasks.return_value = prioritized_tasks
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Complete Project Management Tool")
        mock_tm_instance.prioritize_tasks.assert_called_once()

    # Test 17: Test main function with callable task attributes
    @patch('project_management.modules.main_modules.task_executor.TaskManagement')
    @patch('builtins.print')
    def test_main_execution_callable_task_attributes(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.task_executor import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock tasks with callable attributes
        def get_id():
            return 1
            
        def get_title():
            return "Task 1"
            
        def get_importance():
            return 0.9
            
        def get_urgency():
            return 0.8
            
        def get_status():
            return "pending"
        
        mock_task1 = MagicMock()
        mock_task1.id = get_id
        mock_task1.title = get_title
        mock_task1.importance = get_importance
        mock_task1.urgency = get_urgency
        mock_task1.status = get_status
        
        # Setup prioritized tasks
        prioritized_tasks = [mock_task1] + [MagicMock() for _ in range(19)]
        for i, task in enumerate(prioritized_tasks[1:], 2):
            task.id = i
            task.title = f"Task {i}"
            task.importance = 1.0 - (i * 0.01)
            task.urgency = 1.0 - (i * 0.02)
            task.status = "pending"
        
        mock_tm_instance.prioritize_tasks.return_value = prioritized_tasks
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Complete Project Management Tool")
        mock_tm_instance.prioritize_tasks.assert_called_once()

    # Test 18: Test main function with task attributes as properties
    @patch('project_management.modules.main_modules.task_executor.TaskManagement')
    @patch('builtins.print')
    def test_main_execution_task_attributes_as_properties(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.task_executor import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock tasks with properties
        class MockTask:
            def __init__(self, id, title, importance, urgency, status):
                self._id = id
                self._title = title
                self._importance = importance
                self._urgency = urgency
                self._status = status
                
            @property
            def id(self):
                return self._id
                
            @property
            def title(self):
                return self._title
                
            @property
            def importance(self):
                return self._importance
                
            @property
            def urgency(self):
                return self._urgency
                
            @property
            def status(self):
                return self._status
        
        mock_task1 = MockTask(1, "Task 1", 0.9, 0.8, "pending")
        mock_task2 = MockTask(2, "Task 2", 0.8, 0.7, "pending")
        
        # Setup prioritized tasks
        prioritized_tasks = [mock_task1, mock_task2] + [MockTask(i, f"Task {i}", 1.0 - (i * 0.01), 1.0 - (i * 0.02), "pending") for i in range(3, 21)]
        
        mock_tm_instance.prioritize_tasks.return_value = prioritized_tasks
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Complete Project Management Tool")
        mock_tm_instance.prioritize_tasks.assert_called_once()

    # Test 19: Test main function with task attributes as descriptors
    @patch('project_management.modules.main_modules.task_executor.TaskManagement')
    @patch('builtins.print')
    def test_main_execution_task_attributes_as_descriptors(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.task_executor import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock tasks with descriptors
        class Descriptor:
            def __init__(self, value):
                self.value = value
                
            def __get__(self, obj, objtype=None):
                return self.value
                
            def __set__(self, obj, value):
                self.value = value
        
        class MockTask:
            def __init__(self, id, title, importance, urgency, status):
                self.id = Descriptor(id)
                self.title = Descriptor(title)
                self.importance = Descriptor(importance)
                self.urgency = Descriptor(urgency)
                self.status = Descriptor(status)
        
        mock_task1 = MockTask(1, "Task 1", 0.9, 0.8, "pending")
        mock_task2 = MockTask(2, "Task 2", 0.8, 0.7, "pending")
        
        # Setup prioritized tasks
        prioritized_tasks = [mock_task1, mock_task2] + [MockTask(i, f"Task {i}", 1.0 - (i * 0.01), 1.0 - (i * 0.02), "pending") for i in range(3, 21)]
        
        mock_tm_instance.prioritize_tasks.return_value = prioritized_tasks
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Complete Project Management Tool")
        mock_tm_instance.prioritize_tasks.assert_called_once()

    # Test 20: Test main function with task attributes as magic methods
    @patch('project_management.modules.main_modules.task_executor.TaskManagement')
    @patch('builtins.print')
    def test_main_execution_task_attributes_as_magic_methods(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.task_executor import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock tasks with magic methods
        class MockTask:
            def __init__(self, id, title, importance, urgency, status):
                self._id = id
                self._title = title
                self._importance = importance
                self._urgency = urgency
                self._status = status
                
            def __str__(self):
                return f"Task {self._id}"
                
            def __repr__(self):
                return f"MockTask(id={self._id}, title={self._title})"
                
            def __getattr__(self, name):
                if name == "id":
                    return self._id
                elif name == "title":
                    return self._title
                elif name == "importance":
                    return self._importance
                elif name == "urgency":
                    return self._urgency
                elif name == "status":
                    return self._status
                else:
                    raise AttributeError(f"'MockTask' object has no attribute '{name}'")
        
        mock_task1 = MockTask(1, "Task 1", 0.9, 0.8, "pending")
        mock_task2 = MockTask(2, "Task 2", 0.8, 0.7, "pending")
        
        # Setup prioritized tasks
        prioritized_tasks = [mock_task1, mock_task2] + [MockTask(i, f"Task {i}", 1.0 - (i * 0.01), 1.0 - (i * 0.02), "pending") for i in range(3, 21)]
        
        mock_tm_instance.prioritize_tasks.return_value = prioritized_tasks
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Complete Project Management Tool")
        mock_tm_instance.prioritize_tasks.assert_called_once()

if __name__ == "__main__":
    unittest.main()
