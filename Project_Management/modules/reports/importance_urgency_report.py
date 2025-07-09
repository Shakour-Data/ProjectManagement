import os
from datetime import datetime
from sqlite_db_manager import SQLiteDBManager

class ImportanceUrgencyReport:
    def __init__(self, db_manager=None, output_path=None):
        self.db_manager = db_manager or SQLiteDBManager()
        self.output_path = output_path or os.path.join('docs', 'reports', 'importance_urgency_report.md')
        self.db_manager.connect()

    def generate_importance_urgency_summary(self):
        cursor = self.db_manager.conn.cursor()
        cursor.execute('SELECT title, status, importance, urgency FROM tasks')
        tasks = cursor.fetchall()

        importance_urgency_tasks = {
            'Important & Urgent': [],
            'Important & Not Urgent': [],
            'Not Important & Urgent': [],
            'Not Important & Not Urgent': []
        }

        for task in tasks:
            title, status, importance, urgency = task
            category = None
            if importance >= 7 and urgency >= 7:
                category = 'Important & Urgent'
            elif importance >= 7 and urgency < 7:
                category = 'Important & Not Urgent'
            elif importance < 7 and urgency >= 7:
                category = 'Not Important & Urgent'
            else:
                category = 'Not Important & Not Urgent'
            importance_urgency_tasks[category].append({
                'name': title,
                'status': status,
                'importance': importance,
                'urgency': urgency
            })

        return importance_urgency_tasks

    def generate_markdown_report(self, summary):
        lines = []
        lines.append(f"# Importance and Urgency Report")
        lines.append(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        for category, tasks in summary.items():
            lines.append(f"## {category} ({len(tasks)} tasks)")
            for task in tasks:
                lines.append(f"- **{task['name']}** - Status: {task['status']}, Importance: {task['importance']}, Urgency: {task['urgency']}")
            lines.append("")
        return "\n".join(lines)

    def save_report(self, content):
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def generate(self):
        summary = self.generate_importance_urgency_summary()
        report_md = self.generate_markdown_report(summary)
        self.save_report(report_md)
        print(f"Importance and Urgency report generated at {self.output_path}")

if __name__ == "__main__":
    report = ImportanceUrgencyReport()
    report.generate()
