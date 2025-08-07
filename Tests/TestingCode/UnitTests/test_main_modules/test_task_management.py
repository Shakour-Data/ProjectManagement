import unittest
import datetime
from project_management.modules.main_modules.task_management import Task, TaskManagement

class TestTaskManagement(unittest.TestCase):
    def setUp(self):
        # Setup any necessary test data or state
        self.task_manager = TaskManagement()

    # Test 1
    def test_task_creation(self):
        task = Task(id=1, title="Test Task")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.status, "pending")

    # Test 2
    def test_task_management_initialization(self):
        self.assertEqual(len(self.task_manager.tasks), 0)
        self.assertEqual(self.task_manager.next_task_id, 1)

    # Test 3
    def test_parse_creative_input(self):
        task = self.task_manager.parse_creative_input("Create a new feature")
        self.assertEqual(task.title, "Create a new feature")
        self.assertEqual(task.id, 1)
        self.assertEqual(len(self.task_manager.tasks), 1)

    # Test 4
    def test_generate_wbs_from_idea(self):
        tasks = self.task_manager.generate_wbs_from_idea("Build a website")
        self.assertGreater(len(tasks), 0)
        self.assertTrue(any(task.title == "Build a website" for task in tasks))

    # Test 5
    def test_mark_task_completed(self):
        task = self.task_manager.parse_creative_input("Test task")
        result = self.task_manager.mark_task_completed(task.id)
        self.assertTrue(result)
        self.assertEqual(self.task_manager.tasks[task.id].status, "completed")

    # Test 6
    def test_assign_task(self):
        task = self.task_manager.parse_creative_input("Test task")
        result = self.task_manager.assign_task(task.id, ["user1", "user2"])
        self.assertTrue(result)
        self.assertEqual(self.task_manager.tasks[task.id].assigned_to, ["user1", "user2"])

    # Test 7
    def test_mark_task_completed_invalid_id(self):
        result = self.task_manager.mark_task_completed(999)
        self.assertFalse(result)

    # Test 8
    def test_assign_task_invalid_id(self):
        result = self.task_manager.assign_task(999, ["user1"])
        self.assertFalse(result)

    # Test 9
    def test_task_workflow_steps(self):
        task = Task(id=1, title="Test Task")
        self.assertFalse(task.workflow_steps["Coding"])
        task.mark_workflow_step_completed("Coding")
        self.assertTrue(task.workflow_steps["Coding"])

    # Test 10
    def test_workflow_progress_percentage(self):
        task = Task(id=1, title="Test Task")
        initial_progress = task.workflow_progress_percentage()
        self.assertEqual(initial_progress, 0.0)
        
        task.mark_workflow_step_completed("Coding")
        task.mark_workflow_step_completed("Testing")
        progress = task.workflow_progress_percentage()
        expected_progress = (2/6) * 100
        self.assertEqual(progress, expected_progress)

    # Test 11
    def test_is_workflow_completed(self):
        task = Task(id=1, title="Test Task")
        self.assertFalse(task.is_workflow_completed())
        
        for step in task.workflow_steps:
            task.mark_workflow_step_completed(step)
        
        self.assertTrue(task.is_workflow_completed())

    # Test 12
    def test_detect_conflicts(self):
        task1 = Task(id=1, title="Task 1")
        task2 = Task(id=2, title="Task 2", dependencies=[1, 999])  # 999 doesn't exist
        self.task_manager.tasks[1] = task1
        self.task_manager.tasks[2] = task2
        
        conflicts = self.task_manager.detect_conflicts()
        self.assertIn("Task 2 depends on unknown task 999", conflicts)

    # Test 13
    def test_detect_conflicts_no_conflicts(self):
        task1 = Task(id=1, title="Task 1")
        task2 = Task(id=2, title="Task 2", dependencies=[1])
        self.task_manager.tasks[1] = task1
        self.task_manager.tasks[2] = task2
        
        conflicts = self.task_manager.detect_conflicts()
        self.assertEqual(len(conflicts), 0)

    # Test 14
    def test_task_with_deadline(self):
        deadline = datetime.date(2025, 12, 31)
        task = Task(id=1, title="Test Task", deadline=deadline)
        self.assertEqual(task.deadline, deadline)

    # Test 15
    def test_task_with_dependencies(self):
        task = Task(id=1, title="Test Task", dependencies=[2, 3])
        self.assertEqual(task.dependencies, [2, 3])

    # Test 16
    def test_task_with_parent(self):
        task = Task(id=1, title="Test Task", parent_id=0)
        self.assertEqual(task.parent_id, 0)

    # Test 17
    def test_task_with_github_issue(self):
        task = Task(id=1, title="Test Task", github_issue_number=123)
        self.assertEqual(task.github_issue_number, 123)

    # Test 18
    def test_update_workflow_steps_from_commit_message(self):
        task = Task(id=1, title="Test Task")
        self.task_manager.tasks[1] = task
        
        commit_message = "Task 1: Code Review done"
        self.task_manager.update_workflow_steps_from_commit_message(commit_message)
        
        self.assertTrue(task.workflow_steps["Code Review"])

    # Test 19
    def test_update_workflow_steps_from_commit_message_case_insensitive(self):
        task = Task(id=1, title="Test Task")
        self.task_manager.tasks[1] = task
        
        commit_message = "task 1: testing done"
        self.task_manager.update_workflow_steps_from_commit_message(commit_message)
        
        self.assertTrue(task.workflow_steps["Testing"])

    # Test 20
    def test_update_workflow_steps_from_commit_message_invalid_task(self):
        task = Task(id=1, title="Test Task")
        self.task_manager.tasks[1] = task
        
        commit_message = "Task 999: Code Review done"
        self.task_manager.update_workflow_steps_from_commit_message(commit_message)
        
        self.assertFalse(task.workflow_steps["Code Review"])

    # Test 21
    def test_calculate_urgency_importance(self):
        # Create a simple hierarchy
        root_task = Task(id=1, title="Root Task")
        child_task = Task(id=2, title="Child Task", parent_id=1)
        
        self.task_manager.tasks[1] = root_task
        self.task_manager.tasks[2] = child_task
        
        # This should not raise any exceptions
        self.task_manager.calculate_urgency_importance()
        
        self.assertIsNotNone(root_task.urgency)
        self.assertIsNotNone(root_task.importance)
        self.assertIsNotNone(child_task.urgency)
        self.assertIsNotNone(child_task.importance)

    # Test 22
    def test_classify_tasks_eisenhower(self):
        task1 = Task(id=1, title="High Priority", urgency=90, importance=90)
        task2 = Task(id=2, title="Low Priority", urgency=10, importance=10)
        
        self.task_manager.tasks[1] = task1
        self.task_manager.tasks[2] = task2
        
        classification = self.task_manager.classify_tasks_eisenhower()
        
        self.assertIn(task1, classification["do_now"])
        self.assertIn(task2, classification["eliminate"])

    # Test 23
    def test_prioritize_tasks(self):
        task1 = Task(id=1, title="Task 1", urgency=90, importance=90)
        task2 = Task(id=2, title="Task 2", urgency=50, importance=50)
        
        self.task_manager.tasks[1] = task1
        self.task_manager.tasks[2] = task2
        
        prioritized = self.task_manager.prioritize_tasks()
        
        self.assertEqual(prioritized[0].id, 1)  # Higher priority task should be first

    # Test 24
    def test_schedule_tasks(self):
        task1 = Task(id=1, title="Task 1", urgency=90, importance=90)
        task2 = Task(id=2, title="Task 2", urgency=50, importance=50)
        
        self.task_manager.tasks[1] = task1
        self.task_manager.tasks[2] = task2
        
        scheduled = self.task_manager.schedule_tasks()
        
        self.assertEqual(len(scheduled), 2)

    # Test 25
    def test_task_with_empty_dependencies(self):
        task = Task(id=1, title="Test Task")
        self.assertEqual(task.dependencies, [])

    # Test 26
    def test_task_with_empty_assigned_to(self):
        task = Task(id=1, title="Test Task")
        self.assertEqual(task.assigned_to, [])

    # Test 27
    def test_task_unicode_title(self):
        task = Task(id=1, title="وظیفه تست")
        self.assertEqual(task.title, "وظیفه تست")

    # Test 28
    def test_task_special_characters_title(self):
        task = Task(id=1, title="Test!@#$%^&*()")
        self.assertEqual(task.title, "Test!@#$%^&*()")

    # Test 29
    def test_task_empty_title(self):
        task = Task(id=1, title="")
        self.assertEqual(task.title, "")

    # Test 30
    def test_task_long_title(self):
        long_title = "a" * 1000
        task = Task(id=1, title=long_title)
        self.assertEqual(task.title, long_title)

    # Test 31
    def test_multiple_tasks_increment_id(self):
        task1 = self.task_manager.parse_creative_input("Task 1")
        task2 = self.task_manager.parse_creative_input("Task 2")
        
        self.assertEqual(task1.id, 1)
        self.assertEqual(task2.id, 2)
        self.assertEqual(self.task_manager.next_task_id, 3)

    # Test 32
    def test_task_equality(self):
        task1 = Task(id=1, title="Test Task")
        task2 = Task(id=1, title="Different Title")
        task3 = Task(id=2, title="Test Task")
        
        self.assertEqual(task1.id, task2.id)
        self.assertNotEqual(task1.id, task3.id)

    # Test 33
    def test_task_status_values(self):
        task = Task(id=1, title="Test Task", status="in_progress")
        self.assertEqual(task.status, "in_progress")
        
        task.status = "completed"
        self.assertEqual(task.status, "completed")

    # Test 34
    def test_task_priority_values(self):
        task = Task(id=1, title="Test Task", priority=5)
        self.assertEqual(task.priority, 5)

    # Test 35
    def test_calculate_urgency_with_deadline(self):
        task = Task(id=1, title="Test Task", deadline=datetime.date.today() + datetime.timedelta(days=7))
        urgency = self.task_manager._calculate_urgency(task)
        self.assertGreater(urgency, 0)

    # Test 36
    def test_calculate_urgency_without_deadline(self):
        task = Task(id=1, title="Test Task")
        urgency = self.task_manager._calculate_urgency(task)
        self.assertEqual(urgency, 0.1)

    # Test 37
    def test_calculate_importance_with_priority(self):
        task = Task(id=1, title="Test Task", priority=5)
        importance = self.task_manager._calculate_importance(task)
        self.assertEqual(importance, 5)

    # Test 38
    def test_calculate_importance_without_priority(self):
        task = Task(id=1, title="Test Task")
        importance = self.task_manager._calculate_importance(task)
        self.assertEqual(importance, 1.0)

    # Test 39
    def test_classify_tasks_empty(self):
        classification = self.task_manager.classify_tasks_eisenhower()
        self.assertEqual(len(classification["do_now"]), 0)
        self.assertEqual(len(classification["schedule"]), 0)
        self.assertEqual(len(classification["delegate"]), 0)
        self.assertEqual(len(classification["eliminate"]), 0)

    # Test 40
    def test_prioritize_tasks_empty(self):
        prioritized = self.task_manager.prioritize_tasks()
        self.assertEqual(len(prioritized), 0)

    # Test 41
    def test_schedule_tasks_empty(self):
        scheduled = self.task_manager.schedule_tasks()
        self.assertEqual(len(scheduled), 0)

    # Test 42
    def test_detect_conflicts_empty(self):
        conflicts = self.task_manager.detect_conflicts()
        self.assertEqual(len(conflicts), 0)

    # Test 43
    def test_load_scores_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            self.task_manager.load_scores("nonexistent.json")

    # Test 44
    def test_task_repr(self):
        task = Task(id=1, title="Test Task")
        repr_str = repr(task)
        self.assertIn("Task", repr_str)

    # Test 45
    def test_task_str(self):
        task = Task(id=1, title="Test Task")
        str_repr = str(task)
        self.assertIsInstance(str_repr, str)

    # Test 46
    def test_task_management_repr(self):
        repr_str = repr(self.task_manager)
        self.assertIn("TaskManagement", repr_str)

    # Test 47
    def test_task_with_all_parameters(self):
        deadline = datetime.date(2025, 12, 31)
        task = Task(
            id=1,
            title="Complete Project",
            description="Finish the main project",
            deadline=deadline,
            dependencies=[2, 3],
            assigned_to=["user1", "user2"],
            status="in_progress",
            priority=5,
            parent_id=0,
            urgency=75.5,
            importance=85.0,
            github_issue_number=42
        )
        
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Complete Project")
        self.assertEqual(task.description, "Finish the main project")
        self.assertEqual(task.deadline, deadline)
        self.assertEqual(task.dependencies, [2, 3])
        self.assertEqual(task.assigned_to, ["user1", "user2"])
        self.assertEqual(task.status, "in_progress")
        self.assertEqual(task.priority, 5)
        self.assertEqual(task.parent_id, 0)
        self.assertEqual(task.urgency, 75.5)
        self.assertEqual(task.importance, 85.0)
        self.assertEqual(task.github_issue_number, 42)

    # Test 48
    def test_workflow_steps_initialization(self):
        task = Task(id=1, title="Test Task")
        expected_steps = {
            "Coding": False,
            "Testing": False,
            "Documentation": False,
            "Code Review": False,
            "Merge and Deployment": False,
            "Verification": False,
        }
        self.assertEqual(task.workflow_steps, expected_steps)

    # Test 49
    def test_workflow_steps_completion_all(self):
        task = Task(id=1, title="Test Task")
        for step in task.workflow_steps:
            task.mark_workflow_step_completed(step)
        
        self.assertTrue(task.is_workflow_completed())
        self.assertEqual(task.workflow_progress_percentage(), 100.0)

    # Test 50
    def test_complex_hierarchy_propagation(self):
        # Create a 3-level hierarchy
        root = Task(id=1, title="Root")
        child1 = Task(id=2, title="Child 1", parent_id=1)
        child2 = Task(id=3, title="Child 2", parent_id=1)
        grandchild1 = Task(id=4, title="Grandchild 1", parent_id=2)
        grandchild2 = Task(id=5, title="Grandchild 2", parent_id=2)
        
        self.task_manager.tasks = {1: root, 2: child1, 3: child2, 4: grandchild1, 5: grandchild2}
        
        # This should complete without errors
        self.task_manager.calculate_urgency_importance()
        
        # Verify all tasks have urgency and importance values
        for task in self.task_manager.tasks.values():
            self.assertIsNotNone(task.urgency)
            self.assertIsNotNone(task.importance)

if __name__ == "__main__":
    unittest.main()
