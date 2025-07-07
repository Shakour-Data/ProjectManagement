import os
import datetime
import sys

# Add Project_Management directory to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Project_Management')))

from modules.project_management_system import (
    InputHandler,
    GitProgressUpdater,
    ProgressCalculator,
    TaskManager,
)
from modules.dashboards_reports import DashboardReports

def run_test():
    input_dir = 'project_test/PM_Input'
    base_report_dir = 'project_test/reports'
    dashboard_dir = os.path.join(base_report_dir, 'dashboards')
    report_dir = os.path.join(base_report_dir, 'reports')
    os.makedirs(dashboard_dir, exist_ok=True)
    os.makedirs(report_dir, exist_ok=True)

    # Load inputs
    ih = InputHandler(input_dir)
    inputs = ih.read_json_files()
    print('Loaded inputs:', list(inputs.keys()))

    # Update progress from git logs
    gpu = GitProgressUpdater(inputs.get('workflow_definition', []))
    combined_progress = gpu.update_progress()
    print('Combined progress:', combined_progress)

    # Calculate progress, importance, urgency, and enrich tasks
    pc = ProgressCalculator(input_dir)
    pc.load_inputs()
    pc.commit_progress = combined_progress
    pc.enrich_tasks_with_progress_and_score()
    enriched_tasks = pc.get_enriched_tasks()
    print(f'Enriched {len(enriched_tasks)} tasks.')

    # Complete top 5 important tasks
    tm = TaskManager(enriched_tasks)
    updated_tasks = tm.complete_top_important_tasks(5)
    print(f'Completed top 5 important tasks.')

    # Generate dashboards
    dr = DashboardReports(input_dir)
    dr.load_inputs()
    progress_md = dr.progress_report_dashboard_md()
    priority_md = dr.task_priority_urgency_report_md()

    # Save dashboards and reports with timestamped filenames
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    progress_dashboard_path = os.path.join(dashboard_dir, f'progress_report_dashboard_{timestamp}.md')
    task_priority_path = os.path.join(dashboard_dir, f'task_priority_urgency_report_{timestamp}.md')

    with open(progress_dashboard_path, 'w', encoding='utf-8') as f:
        f.write(progress_md)
    with open(task_priority_path, 'w', encoding='utf-8') as f:
        f.write(priority_md)

    print(f'Dashboards saved to {dashboard_dir}/')

    # For demonstration, copy dashboards as reports as well (or generate separate reports if available)
    report_progress_path = os.path.join(report_dir, f'progress_report_{timestamp}.md')
    report_priority_path = os.path.join(report_dir, f'task_priority_urgency_report_{timestamp}.md')

    with open(report_progress_path, 'w', encoding='utf-8') as f:
        f.write(progress_md)
    with open(report_priority_path, 'w', encoding='utf-8') as f:
        f.write(priority_md)

    print(f'Reports saved to {report_dir}/')

if __name__ == '__main__':
    run_test()
