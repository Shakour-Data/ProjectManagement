import os
import datetime
from task_management import TaskManagement

DASHBOARD_PATH = os.path.join('docs', 'project_management', 'detailed_progress_dashboard.md')
IMPORTANCE_URGENCY_REPORT_PATH = os.path.join('docs', 'project_management', 'importance_urgency_report.md')

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

def generate_importance_urgency_report(tm: TaskManagement):
    tm.calculate_urgency_importance()
    tasks = tm.prioritize_tasks()

    # Mapping for workflow position and files involved by task title
    workflow_positions = {
        "Develop Project Management Tool": "Initial phase, project setup and architecture design.",
        "Develop Project Management Tool - Subtask Level 1.1": "Early development, security and access control.",
        "Develop Project Management Tool - Subtask Level 1.3": "Mid development, data visualization and reporting.",
        "Develop Project Management Tool - Subtask Level 1.2": "Core functionality development.",
        "Develop Project Management Tool - Subtask Level 2.1.2": "Integration phase.",
        "Develop Project Management Tool - Subtask Level 2.3.2": "Performance tuning and optimization.",
        "Develop Project Management Tool - Subtask Level 2.1.1": "DevOps and automation.",
        "Develop Project Management Tool - Subtask Level 2.3.1": "User engagement and communication.",
        "Develop Project Management Tool - Subtask Level 2.2.1": "Backend API development.",
        "Develop Project Management Tool - Subtask Level 2.2.2": "Security and permissions.",
    }

    files_involved = {
        "Develop Project Management Tool": ["src/task_management.py", "src/progress_report.py", "src/auto_commit.py"],
        "Develop Project Management Tool - Subtask Level 1.1": ["src/task_management.py"],
        "Develop Project Management Tool - Subtask Level 1.3": ["src/progress_report.py"],
        "Develop Project Management Tool - Subtask Level 1.2": ["src/task_management.py"],
        "Develop Project Management Tool - Subtask Level 2.1.2": ["src/task_management.py"],
        "Develop Project Management Tool - Subtask Level 2.3.2": ["src/task_management.py"],
        "Develop Project Management Tool - Subtask Level 2.1.1": ["src/auto_commit.py"],
        "Develop Project Management Tool - Subtask Level 2.3.1": ["src/task_management.py"],
        "Develop Project Management Tool - Subtask Level 2.2.1": ["src/task_management.py"],
        "Develop Project Management Tool - Subtask Level 2.2.2": ["src/task_management.py"],
    }

    # Filter tasks by testing phase
    not_testing_tasks = [t for t in tasks if t.status.lower() != 'testing']
    testing_tasks = [t for t in tasks if t.status.lower() == 'testing']

    # Sort tasks by importance and urgency separately
    important_not_testing = sorted(not_testing_tasks, key=lambda t: t.importance, reverse=True)[:15]
    urgent_not_testing = sorted(not_testing_tasks, key=lambda t: t.urgency, reverse=True)[:15]
    important_testing = sorted(testing_tasks, key=lambda t: t.importance, reverse=True)[:10]
    urgent_testing = sorted(testing_tasks, key=lambda t: t.urgency, reverse=True)[:10]

    def format_task(task):
        wp = workflow_positions.get(task.title, "No workflow position available.")
        fi = files_involved.get(task.title, ["No files listed."])
        fi_str = ", ".join(fi)
        return (f"- **{task.title}** (ID: {task.id})\n"
                f"  - Importance: {task.importance:.2f}\n"
                f"  - Urgency: {task.urgency:.2f}\n"
                f"  - Status: {task.status}\n"
                f"  - Description: {task.description if hasattr(task, 'description') else 'No description available.'}\n"
                f"  - Workflow Position: {wp}\n"
                f"  - Files Involved: {fi_str}\n")

    report = f"# Importance and Urgency Report - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    report += "## Top 15 Important Tasks Not in Testing Phase\n"
    report += "\n".join(format_task(t) for t in important_not_testing) if important_not_testing else "- None"
    report += "\n\n## Top 15 Urgent Tasks Not in Testing Phase\n"
    report += "\n".join(format_task(t) for t in urgent_not_testing) if urgent_not_testing else "- None"
    report += "\n\n## Top 10 Important Tasks In Testing Phase\n"
    report += "\n".join(format_task(t) for t in important_testing) if important_testing else "- None"
    report += "\n\n## Top 10 Urgent Tasks In Testing Phase\n"
    report += "\n".join(format_task(t) for t in urgent_testing) if urgent_testing else "- None"
    report += "\n\n*This report is generated automatically and lists the top important and urgent tasks with details and current workflow status, separated by testing phase.*\n"

    with open(IMPORTANCE_URGENCY_REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"Importance and Urgency report updated at {IMPORTANCE_URGENCY_REPORT_PATH}")

if __name__ == "__main__":
    tm = TaskManagement()
    # For demonstration, generate WBS from example idea
    tm.generate_wbs_from_idea("Develop Project Management Tool")

    # Mark top 15 important tasks not in testing as completed
    tasks = tm.prioritize_tasks()
    important_not_testing = [t for t in tasks if t.status.lower() != 'testing']
    important_not_testing_sorted = sorted(important_not_testing, key=lambda t: t.importance, reverse=True)[:15]
    for task in important_not_testing_sorted:
        tm.mark_task_completed(task.id)

    generate_report(tm)
    generate_importance_urgency_report(tm)
