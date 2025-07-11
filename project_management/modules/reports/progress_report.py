import os
from datetime import datetime
from sqlite_db_manager import SQLiteDBManager

class ProgressReport:
    def __init__(self, db_manager=None, output_path=None):
        self.db_manager = db_manager or SQLiteDBManager()
        self.output_path = output_path or os.path.join('docs', 'reports', 'progress_report.md')
        self.db_manager.connect()

    def generate_progress_summary(self):
        cursor = self.db_manager.conn.cursor()
        cursor.execute('SELECT COUNT(*), SUM(CASE WHEN progress >= 100 THEN 1 ELSE 0 END), SUM(CASE WHEN progress > 0 AND progress < 100 THEN 1 ELSE 0 END), SUM(CASE WHEN progress = 0 THEN 1 ELSE 0 END) FROM tasks')
        total_tasks, completed_tasks, in_progress_tasks, pending_tasks = cursor.fetchone()

        cursor.execute('SELECT id, title, progress FROM tasks WHERE is_milestone = 1')
        milestones = cursor.fetchall()

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
        lines.append(f"- Completed Tasks: {summary['completed_tasks']}")
        lines.append(f"- In Progress Tasks: {summary['in_progress_tasks']}")
        lines.append(f"- Pending Tasks: {summary['pending_tasks']}")
        lines.append(f"- Milestones Achieved: {summary['milestones_achieved']}")
        lines.append("")
        lines.append(f"## Milestone Status")
        for milestone, status in summary['milestone_tasks']:
            lines.append(f"- **{milestone}**: {status}")
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

if __name__ == "__main__":
    report = ProgressReport()
    report.generate()
