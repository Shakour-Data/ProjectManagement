import unittest
import os
from Project_Management.modules.project_management_system import ReportManager
from Project_Management.modules.progress_calculator import ProgressCalculator
from Project_Management.modules.git_progress_updater import GitProgressUpdater
from Project_Management.modules.dashboards_reports import DashboardReports

class TestProjectManagementSystem(unittest.TestCase):
    def setUp(self):
        self.input_dir = 'project_test/PM_Input'
        self.report_manager = ReportManager(input_dir=self.input_dir, base_report_dir='project_test/reports')
        self.progress_calculator = ProgressCalculator(input_dir=self.input_dir)
        self.dashboard_reports = DashboardReports(input_dir=self.input_dir)

    def test_load_inputs(self):
        self.assertTrue(os.path.exists(self.input_dir))
        files = os.listdir(self.input_dir)
        self.assertIn('detailed_wbs.json', files)
        self.assertIn('commit_progress.json', files)

    def test_git_progress_updater(self):
        gpu = GitProgressUpdater(workflow_definition=[], input_dir=self.input_dir)
        task_progress = gpu.update_and_save_commit_progress()
        self.assertIsInstance(task_progress, dict)
        self.assertTrue(all('progress_percent' in v and 'status' in v for v in task_progress.values()))

    def test_progress_calculation(self):
        self.progress_calculator.load_inputs()
        self.progress_calculator.enrich_tasks_with_progress()
        tasks = self.progress_calculator.get_enriched_tasks()
        self.assertTrue(len(tasks) > 0)
        for task in tasks:
            self.assertIn('progress', task)
            self.assertIn('importance', task)
            self.assertIn('urgency', task)
            self.assertIn('status', task)

    def test_report_generation(self):
        self.dashboard_reports.load_inputs()
        progress_report = self.dashboard_reports.generate_progress_report()
        priority_report = self.dashboard_reports.generate_priority_urgency_report()
        self.assertIn('# Progress Report Dashboard', progress_report)
        self.assertIn('# Task Priority and Urgency Report', priority_report)

    def test_generate_and_save_all(self):
        self.report_manager.generate_and_save_all()
        dashboard_dir = self.report_manager.dashboard_dir
        report_dir = self.report_manager.report_dir
        self.assertTrue(os.path.exists(dashboard_dir))
        self.assertTrue(os.path.exists(report_dir))
        dashboard_files = os.listdir(dashboard_dir)
        report_files = os.listdir(report_dir)
        self.assertTrue(any(f.endswith('.md') for f in dashboard_files))
        self.assertTrue(any(f.endswith('.md') for f in report_files))

if __name__ == '__main__':
    unittest.main()
