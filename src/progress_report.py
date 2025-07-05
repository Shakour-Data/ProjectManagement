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
    import re

    tm.calculate_urgency_importance()
    tasks = tm.prioritize_tasks()

    # Group tasks by phase using parent_id to reflect hierarchy
    phase_summary = {}
    phase_descriptions = {
        None: "Initial phase, project setup and architecture design.",
        1: "Early development, security and access control.",
        2: "Core functionality development.",
        3: "Integration and testing.",
        4: "Documentation and reporting.",
        5: "User engagement and communication.",
        6: "Performance tuning and optimization.",
        7: "DevOps and automation.",
        8: "Backup and recovery.",
        9: "Final testing and deployment.",
    }

    for task in tasks:
        phase = task.parent_id if task.parent_id in phase_descriptions else None
        if phase not in phase_summary:
            phase_summary[phase] = {
                "total": 0,
                "progress_sum": 0,
                "completed": 0,
                "description": phase_descriptions.get(phase, "No description available.")
            }
        phase_summary[phase]["total"] += 1
        progress = getattr(task, "workflow_progress_percentage", lambda: 0)()
        phase_summary[phase]["progress_sum"] += progress
        if task.status.lower() == "completed":
            phase_summary[phase]["completed"] += 1

    # Build markdown content
    md = "# Project Management Dashboard\n\n"
    md += "## Current Progress Summary\n\n"
    md += "| Phase | Description | Completed Tasks | Total Tasks | Progress (%) |\n"
    md += "|-------|-------------|-----------------|-------------|--------------|\n"
    for phase, data in sorted(phase_summary.items(), key=lambda x: (x[0] is None, x[0])):
        # Calculate average workflow progress percentage per phase
        progress_percent = (data["progress_sum"] / data["total"]) if data["total"] > 0 else 0
        phase_name = f"Phase {phase}" if phase is not None else "Unassigned"
        md += f"| {phase_name} | {data['description']} | {data['completed']} | {data['total']} | {progress_percent:.0f}% |\n"

    md += "\n## Task Details with Urgency and Importance\n\n"
    md += "| Task ID | Title | Urgency | Importance | Status |\n"
    md += "|---------|-------|---------|------------|--------|\n"
    for task in tasks:
        md += f"| {task.id} | {task.title} | {task.urgency:.2f} | {task.importance:.2f} | {task.status} |\n"

    md += "\n## Notes\n\n"
    md += "- Update this dashboard regularly to reflect progress.\n"
    md += "- Use commit messages to update task statuses in \"project_management_state.txt\".\n"
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

    # Ensure tasks are loaded and valid
    if not tasks:
        print("Warning: No tasks found to generate report.")
        return

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

    # Classify tasks into Eisenhower matrix quadrants
    do_now = []
    schedule = []
    delegate = []
    eliminate = []

    for task in tasks:
        if task.importance is None or task.urgency is None:
            continue
        if task.importance >= 70 and task.urgency >= 70:
            do_now.append(task)
        elif task.importance >= 70 and task.urgency < 70:
            schedule.append(task)
        elif task.importance < 70 and task.urgency >= 70:
            delegate.append(task)
        else:
            eliminate.append(task)

    # Sort each quadrant by importance and urgency
    do_now_sorted = sorted(do_now, key=lambda t: (t.importance, t.urgency), reverse=True)
    schedule_sorted = sorted(schedule, key=lambda t: t.importance, reverse=True)
    delegate_sorted = sorted(delegate, key=lambda t: t.urgency, reverse=True)

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
    report += "## 1. Top 15 Tasks That Are Both Important and Urgent\n"
    report += "\n".join(format_task(t) for t in do_now_sorted) if do_now_sorted else "- None"
    report += "\n\n## 2. Top 15 Tasks That Are Only Important\n"
    report += "\n".join(format_task(t) for t in schedule_sorted) if schedule_sorted else "- None"
    report += "\n\n## 3. Top 15 Tasks That Are Only Urgent\n"
    report += "\n".join(format_task(t) for t in delegate_sorted) if delegate_sorted else "- None"
    report += "\n\n*This report is generated automatically and lists the top important and urgent tasks with details and current workflow status, separated by Eisenhower matrix quadrants.*\n"

    with open(IMPORTANCE_URGENCY_REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"Importance and Urgency report updated at {IMPORTANCE_URGENCY_REPORT_PATH}")

if __name__ == "__main__":
    import openpyxl
    from openpyxl.styles import Font, Alignment

    def generate_comprehensive_excel_report(tm: TaskManagement, output_path="docs/project_management/comprehensive_report.xlsx"):
        """
        Generate a comprehensive Excel report with columns:
        Level (لول), Description (شرح), Priority (اولویت), Urgency (فوریت), Status (وضعیت), Progress Percentage (درصد پیشرفت)
        """
        tasks = tm.prioritize_tasks()

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Comprehensive Report"

        headers = ["Level", "Description", "Priority", "Urgency", "Status", "Progress Percentage"]
        ws.append(headers)

        # Set header styles
        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal="center")

        for task in tasks:
            # Extract level from task title if possible, e.g. "Subtask Level 1.1" -> "1.1"
            level = "1"
            import re
            match = re.search(r"Level ([\\d\\.]+)", task.title)
            if match:
                level = match.group(1)

            description = getattr(task, "description", "") or ""
            priority = round(task.importance, 2) if hasattr(task, "importance") else ""
            urgency = round(task.urgency, 2) if hasattr(task, "urgency") else ""
            status = task.status if hasattr(task, "status") else ""
            progress = 0
            if hasattr(task, "workflow_progress_percentage"):
                if callable(task.workflow_progress_percentage):
                    progress = task.workflow_progress_percentage()
                else:
                    progress = task.workflow_progress_percentage

            row = [level, description, priority, urgency, status, progress]
            ws.append(row)

        # Adjust column widths
        column_widths = [10, 50, 15, 15, 15, 20]
        for i, width in enumerate(column_widths, 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width

        wb.save(output_path)
        print(f"Comprehensive Excel report generated at {output_path}")

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
    generate_progress_dashboard_report(tm)
    generate_comprehensive_excel_report(tm)
