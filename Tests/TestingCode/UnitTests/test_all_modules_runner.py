import unittest

# Import all test modules from main_modules
from Tests.TestingCode.UnitTests.test_main_modules import (
    test_estimation_management,
    test_feature_weights,
    test_gantt_chart_data,
    test_git_progress_updater,
    test_importance_urgency_calculator_refactored,
    test_input_handler,
    test_progress_calculator_refactored,
    test_progress_data_generator_refactored,
    test_progress_report,
    test_project_management_system,
    test_quality_management,
    test_reporting,
    test_resource_allocation_manager,
    test_risk_management,
    test_task_management,
)

# Import all test modules from services
from Tests.TestingCode.UnitTests.test_services import (
    test_auto_commit,
    test_backup_manager,
    test_check_progress_dashboard_update,
    test_commit_progress_manager,
    test_communication_management,
    test_communication_risk_doc_integration,
    test_dashboards_reports,
    test_db_data_collector,
    test_do_important_tasks,
    test_do_urgent_tasks,
)

def load_all_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add main_modules tests
    suite.addTests(loader.loadTestsFromModule(test_estimation_management))
    suite.addTests(loader.loadTestsFromModule(test_feature_weights))
    suite.addTests(loader.loadTestsFromModule(test_gantt_chart_data))
    suite.addTests(loader.loadTestsFromModule(test_git_progress_updater))
    suite.addTests(loader.loadTestsFromModule(test_importance_urgency_calculator_refactored))
    suite.addTests(loader.loadTestsFromModule(test_input_handler))
    suite.addTests(loader.loadTestsFromModule(test_progress_calculator_refactored))
    suite.addTests(loader.loadTestsFromModule(test_progress_data_generator_refactored))
    suite.addTests(loader.loadTestsFromModule(test_progress_report))
    suite.addTests(loader.loadTestsFromModule(test_project_management_system))
    suite.addTests(loader.loadTestsFromModule(test_quality_management))
    suite.addTests(loader.loadTestsFromModule(test_reporting))
    suite.addTests(loader.loadTestsFromModule(test_resource_allocation_manager))
    suite.addTests(loader.loadTestsFromModule(test_risk_management))
    suite.addTests(loader.loadTestsFromModule(test_task_management))

    # Add services tests
    suite.addTests(loader.loadTestsFromModule(test_auto_commit))
    suite.addTests(loader.loadTestsFromModule(test_backup_manager))
    suite.addTests(loader.loadTestsFromModule(test_check_progress_dashboard_update))
    suite.addTests(loader.loadTestsFromModule(test_commit_progress_manager))
    suite.addTests(loader.loadTestsFromModule(test_communication_management))
    suite.addTests(loader.loadTestsFromModule(test_communication_risk_doc_integration))
    suite.addTests(loader.loadTestsFromModule(test_dashboards_reports))
    suite.addTests(loader.loadTestsFromModule(test_db_data_collector))
    suite.addTests(loader.loadTestsFromModule(test_do_important_tasks))
    suite.addTests(loader.loadTestsFromModule(test_do_urgent_tasks))

    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(load_all_tests())
