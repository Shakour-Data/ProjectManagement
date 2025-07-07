import os
from Project_Management.modules.project_management_system import (
    InputHandler,
    GitProgressUpdater,
    ProgressCalculator,
    TaskManager,
    DashboardReports,
)

def run_test():
    input_dir = 'project_test/PM_Input'
    report_dir = 'project_test/reports'
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
    print('Generated dashboards.')

    # Save reports
    with open(os.path.join(report_dir, 'progress_report.md'), 'w', encoding='utf-8') as f:
        f.write(progress_md)
    with open(os.path.join(report_dir, 'priority_urgency_report.md'), 'w', encoding='utf-8') as f:
        f.write(priority_md)
    print(f'Reports saved to {report_dir}/')

if __name__ == '__main__':
    run_test()
