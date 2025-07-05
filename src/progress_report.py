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

def generate_progress_dashboard_report(tm: TaskManagement):
    """
    Generate the progress dashboard markdown file at docs/project_management/progress_dashboard.md
    """
    tm.calculate_urgency_importance()
    tasks = tm.prioritize_tasks()

    # Group tasks by phase (simulate phases based on parent_id or other logic)
    # For simplicity, group by first digit of task id as phase
    phase_summary = {}
    for task in tasks:
        phase = str(task.id)[0] if task.id else "0"
        if phase not in phase_summary:
            phase_summary[phase] = {"completed": 0, "total": 0, "description": f"Phase {phase} description"}
        phase_summary[phase]["total"] += 1
        if task.status == "completed":
            phase_summary[phase]["completed"] += 1

    # Build markdown content
    md = "# Project Management Dashboard\n\n"
    md += "## Current Progress Summary\n\n"
    md += "| Phase | Description | Completed Tasks | Total Tasks | Progress (%) |\n"
    md += "|-------|-------------|-----------------|-------------|--------------|\n"
    for phase, data in sorted(phase_summary.items()):
        progress_percent = (data["completed"] / data["total"] * 100) if data["total"] > 0 else 0
        md += f"| {phase} | {data['description']} | {data['completed']} | {data['total']} | {progress_percent:.0f}% |\n"

    md += "\n## Current Workflow Status\n\n"
    md += "- No tasks have been started yet.\n"
    md += '- Workflow steps per task are defined in "workflow_definition.txt".\n\n'

    md += "## Task Details with Urgency and Importance\n\n"
    md += "| Task ID | Title | Urgency | Importance | Status |\n"
    md += "|---------|-------|---------|------------|--------|\n"
    for task in tasks:
        md += f"| {task.id} | {task.title} | {task.urgency:.2f} | {task.importance:.2f} | {task.status} |\n"

    md += "\n## Notes\n\n"
    md += "- Update this dashboard regularly to reflect progress.\n"
    md += '- Use commit messages to update task statuses in "project_management_state.txt".\n'
    md += "- This dashboard provides a real-time overview of project progress and workflow status.\n\n"

    md += "## Test Coverage Summary\n\n"
    md += "| Module/Feature | Status |\n"
    md += "|---------------|--------|\n"
    md += "| Task Management Module | Mostly Complete |\n"
    md += "| GitHub Integration Module | Partial |\n"
    md += "| Progress Reporting | Pending |\n"
    md += "| Cross-project Compatibility | Pending |\n\n"
    md += "*See TEST_COVERAGE.txt for detailed test coverage tracking.*\n"

    with open(os.path.join('docs', 'project_management', 'progress_dashboard.md'), 'w', encoding='utf-8') as f:
        f.write(md)
    print("Progress dashboard report updated at docs/project_management/progress_dashboard.md")

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
