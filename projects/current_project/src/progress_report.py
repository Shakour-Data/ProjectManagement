import os
from datetime import datetime
from sqlite_db_manager import SQLiteDBManager

DASHBOARD_PATH = os.path.join('docs', 'reports', 'progress_report.md')

class ProgressReport:
    def __init__(self, db_manager=None, output_path=None):
        self.db_manager = db_manager or SQLiteDBManager()
        self.output_path = output_path or DASHBOARD_PATH
        self.db_manager.connect()

    def generate_progress_summary(self):
        cursor = self.db_manager.conn.cursor()
        cursor.execute('SELECT COUNT(*), SUM(CASE WHEN progress >= 100 THEN 1 ELSE 0 END), SUM(CASE WHEN progress > 0 AND progress < 100 THEN 1 ELSE 0 END), SUM(CASE WHEN progress = 0 THEN 1 ELSE 0 END) FROM tasks')
        total_tasks, completed_tasks, in_progress_tasks, pending_tasks = cursor.fetchone()

        # Check if 'is_milestone' column exists
        cursor.execute("PRAGMA table_info(tasks)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'is_milestone' in columns:
            cursor.execute('SELECT id, title, progress FROM tasks WHERE is_milestone = 1')
            milestones = cursor.fetchall()
        else:
            milestones = []

        milestones_achieved = sum(1 for m in milestones if m[2] >= 100)
        milestone_tasks = [(m[1], 'Completed' if m[2] >= 100 else 'Pending') for m in milestones]

        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'in_progress_tasks': in_progress_tasks,
            'pending_tasks': pending_tasks,
            'milestones_achieved': milestones_achieved,
            'milestone_tasks': milestone_tasks
        }

    def generate_markdown_report(self, summary):
        lines = []
        lines.append(f"# Project Progress Report")
        lines.append(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append(f"## Summary")
        lines.append(f"- Total Tasks: {summary['total_tasks']}")
        lines.append(f"- Completed Tasks: {summary['completed_tasks'] if summary['completed_tasks'] is not None else 0}")
        lines.append(f"- In Progress Tasks: {summary['in_progress_tasks'] if summary['in_progress_tasks'] is not None else 0}")
        lines.append(f"- Pending Tasks: {summary['pending_tasks'] if summary['pending_tasks'] is not None else 0}")
        lines.append(f"- Milestones Achieved: {summary['milestones_achieved']}")
        lines.append("")
        lines.append(f"## Completed Activities")
        lines.append(f"- Completed Tasks: {summary['completed_tasks'] if summary['completed_tasks'] is not None else 0}")
        lines.append(f"- Milestones Achieved: {summary['milestones_achieved']}")
        lines.append("")
        lines.append(f"## In-Progress Activities")
        lines.append(f"- In Progress Tasks: {summary['in_progress_tasks'] if summary['in_progress_tasks'] is not None else 0}")
        lines.append("")
        lines.append(f"## Pending Activities")
        lines.append(f"- Pending Tasks: {summary['pending_tasks'] if summary['pending_tasks'] is not None else 0}")
        lines.append("")
        lines.append(f"## Milestone Status")
        for milestone, status in summary['milestone_tasks']:
            lines.append(f"- **{milestone}**: {status}")
        lines.append("")
        lines.append(f"## Urgency and Importance Summary")
        lines.append(f"- Urgency and Importance data will be included here.")
        lines.append("")
        return "\n".join(lines)

    def save_report(self, content):
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def generate(self):
        summary = self.generate_progress_summary()
        report_md = self.generate_markdown_report(summary)
        self.save_report(report_md)
        print(f"Progress report generated at {self.output_path}")

def generate_report(task_management=None):
    report = ProgressReport()
    report.generate()

if __name__ == "__main__":
    report = ProgressReport()
    report.generate()
