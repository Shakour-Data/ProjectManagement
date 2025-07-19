import json
import os

class Reporting:
    def __init__(self,
                 detailed_wbs_path='project_inputs/PM_JSON/user_inputs/detailed_wbs.json',
                 resource_allocation_summary_path='project_inputs/PM_JSON/system_outputs/resource_allocation_summary.json',
                 time_management_path='project_inputs/PM_JSON/system_outputs/time_management.json',
                 risk_management_path='project_inputs/PM_JSON/system_outputs/risk_management.json',
                 quality_management_path='project_inputs/PM_JSON/system_outputs/quality_management.json',
                 output_path='project_inputs/PM_JSON/system_outputs/project_reports.json'):
        self.detailed_wbs_path = detailed_wbs_path
        self.resource_allocation_summary_path = resource_allocation_summary_path
        self.time_management_path = time_management_path
        self.risk_management_path = risk_management_path
        self.quality_management_path = quality_management_path
        self.output_path = output_path

        self.detailed_wbs = {}
        self.resource_allocation_summary = {}
        self.time_management = {}
        self.risk_management = {}
        self.quality_management = {}

        self.project_reports = {}

    def load_json(self, path):
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def save_json(self, data, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_inputs(self):
        self.detailed_wbs = self.load_json(self.detailed_wbs_path) or {}
        self.resource_allocation_summary = self.load_json(self.resource_allocation_summary_path) or {}
        self.time_management = self.load_json(self.time_management_path) or {}
        self.risk_management = self.load_json(self.risk_management_path) or {}
        self.quality_management = self.load_json(self.quality_management_path) or {}

    def generate_reports(self):
        """
        Generate aligned project management reports combining all data.
        This is a placeholder for actual report generation logic.
        """
        self.project_reports = {
            'summary': 'Project reports generation not yet implemented',
            'details': {}
        }

    def run(self):
        self.load_inputs()
        self.generate_reports()
        self.save_json(self.project_reports, self.output_path)
        print(f"Project reports saved to {self.output_path}")

if __name__ == "__main__":
    manager = Reporting()
    manager.run()
