import unittest
import datetime
from modules.task_management import TaskManagement, Task

class TestTaskManagement(unittest.TestCase):
    def setUp(self):
        self.tm = TaskManagement()

    def test_generate_wbs_from_idea(self):
        tasks = self.tm.generate_wbs_from_idea("Test Project")
        self.assertTrue(len(tasks) > 0)
        root_tasks = [t for t in tasks if t.parent_id is None]
        self.assertEqual(len(root_tasks), 1)
        # Check hierarchy depth at least 2 levels
        level1_tasks = [t for t in tasks if t.parent_id == root_tasks[0].id]
        self.assertTrue(len(level1_tasks) >= 1)
        level2_tasks = [t for t in tasks if t.parent_id in [t.id for t in level1_tasks]]
        self.assertTrue(len(level2_tasks) >= 1)

    def test_urgency_importance_calculation(self):
        # Create tasks with deadlines and priorities
        root = Task(id=1, title="Root Task", priority=2)
        child1 = Task(id=2, title="Child 1", deadline=datetime.date.today() + datetime.timedelta(days=1), priority=3, parent_id=1)
        child2 = Task(id=3, title="Child 2", deadline=datetime.date.today() + datetime.timedelta(days=5), priority=1, parent_id=1)
        self.tm.tasks = {1: root, 2: child1, 3: child2}
        self.tm.calculate_urgency_importance()

        # Check urgency and importance calculated for leaf tasks
        self.assertIsNotNone(self.tm.tasks[2].urgency)
        self.assertIsNotNone(self.tm.tasks[2].importance)
        self.assertIsNotNone(self.tm.tasks[3].urgency)
        self.assertIsNotNone(self.tm.tasks[3].importance)

        # Check urgency and importance propagated to root
        self.assertAlmostEqual(self.tm.tasks[1].urgency, self.tm.tasks[2].urgency + self.tm.tasks[3].urgency)
        self.assertAlmostEqual(self.tm.tasks[1].importance, self.tm.tasks[2].importance + self.tm.tasks[3].importance)

    def test_prioritize_tasks(self):
        import datetime
        # Create tasks with urgency and importance
        t1 = Task(id=1, title="Task 1", priority=1, deadline=datetime.date.today() + datetime.timedelta(days=3))
        t2 = Task(id=2, title="Task 2", priority=5, deadline=datetime.date.today() + datetime.timedelta(days=1))
        self.tm.tasks = {1: t1, 2: t2}
        sorted_tasks = self.tm.prioritize_tasks()
        # Task 2 should have higher priority due to higher importance and urgency
        self.assertEqual(sorted_tasks[0].id, 2)

    def test_assign_task(self):
        task = Task(id=1, title="Task")
        self.tm.tasks = {1: task}
        result = self.tm.assign_task(1, ["user1", "user2"])
        self.assertTrue(result)
        self.assertEqual(self.tm.tasks[1].assigned_to, ["user1", "user2"])

        # Assign to non-existent task
        result = self.tm.assign_task(99, ["user3"])
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
