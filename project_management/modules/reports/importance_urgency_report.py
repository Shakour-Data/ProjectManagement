import os
import json
from datetime import datetime

class ImportanceUrgencyReport:
    def __init__(self, input_path=None, output_path=None):
        import os
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.input_path = input_path or os.path.join(base_dir, '..', '..', '..', 'project_inputs', 'PM_JSON', 'user_inputs', 'detailed_wbs.json')
        self.output_path = output_path or os.path.join(base_dir, '..', '..', '..', 'docs', 'reports', 'importance_urgency_report.md')

    def load_tasks(self):
        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"Input JSON file not found: {self.input_path}")
        with open(self.input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Assuming tasks are in a list or dict under a key, adjust as per actual JSON structure
        if isinstance(data, dict) and 'tasks' in data:
            return data['tasks']
        return data

    def generate_importance_urgency_summary(self):
        tasks = self.load_tasks()

        importance_urgency_tasks = {
            'Important & Urgent': [],
            'Important & Not Urgent': [],
            'Not Important & Urgent': [],
            'Not Important & Not Urgent': []
        }

        for task in tasks:
            importance = task.get('importance', 0)
            urgency = task.get('urgency', 0)
            title = task.get('title', 'Untitled Task')
            status = task.get('status', 'Unknown')

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
