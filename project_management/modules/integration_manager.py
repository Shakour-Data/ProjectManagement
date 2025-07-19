import subprocess

class IntegrationManager:
    def __init__(self):
        self.modules = [
            'wbs_merger.py',
            'resource_allocation_manager.py',
            'scope_management.py',
            'time_management.py',
            'resource_management.py',
            'quality_management.py',
            'risk_management.py',
            'communication_management.py',
            'estimation_management.py',
            'commit_progress_manager.py',
            'reporting.py'
        ]

    def run_module(self, module_name):
        print(f"Running {module_name}...")
        result = subprocess.run(['python3', f'project_management/modules/{module_name}'], capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"Error running {module_name}: {result.stderr}")
            return False
        return True

    def run_all(self):
        for module in self.modules:
            success = self.run_module(module)
            if not success:
                print(f"Stopping integration due to error in {module}")
                break
        else:
            print("All modules executed successfully.")

if __name__ == "__main__":
    manager = IntegrationManager()
    manager.run_all()
