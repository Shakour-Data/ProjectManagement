import os
import datetime
from src.task_management import TaskManagement

DASHBOARD_PATH = os.path.join('docs', 'project_management', 'detailed_progress_dashboard.md')

def generate_report(tm: TaskManagement):
    tm.calculate_urgency_importance()
    tasks = tm.prioritize_tasks()

    completed = []
    in_progress = []
    pending = []

    for task in tasks:
        status = task.status.lower()
        line = "- {} (Urgency: {:.2f}, Importance: {:.2f})".format(task.title, task.urgency, task.importance)
        if status == 'completed':
            completed.append(line)
        elif status == 'in_progress':
            in_progress.append(line)
        else:
            pending.append(line)

    report = "# Progress Report - {}\n\n".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    report += "## Completed Activities\n"
    report += "\n".join(completed) if completed else "- None"
    report += "\n\n## In-Progress Activities\n"
    report += "\n".join(in_progress) if in_progress else "- None"
    report += "\n\n## Pending Activities\n"
    report += "\n".join(pending) if pending else "- None"
    report += "\n\n*This report is generated automatically and reflects real-time project status including urgency and importance metrics.*\n"

    with open(DASHBOARD_PATH, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"Progress report updated at {DASHBOARD_PATH}")

if __name__ == "__main__":
    tm = TaskManagement()
    # For demonstration, generate WBS from example idea
    tm.generate_wbs_from_idea("Develop Project Management Tool")
    generate_report(tm)
