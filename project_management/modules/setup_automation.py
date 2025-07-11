import re

class SetupAutomation:
    def __init__(self, project_name='Project_Management'):
        self.project_name = project_name

    def get_standard_response(self, question: str) -> str:
        """
        Automatically answer initial setup questions with standard responses.
        Example questions: git flow, naming conventions, etc.
        """
        question_lower = question.lower()
        if 'git flow' in question_lower:
            return ("We use the standard Git Flow branching model: "
                    "feature branches prefixed with 'feature/', "
                    "release branches with 'release/', "
                    "hotfix branches with 'hotfix/', "
                    "and main branches 'main' and 'develop'.")
        elif 'naming' in question_lower or 'name' in question_lower:
            return ("All names should be prefixed with the project name "
                    f"'{self.project_name}' or suffixed with a unique number if needed.")
        else:
            return "Please follow the project standard guidelines."

    def generate_standard_name(self, base_name: str, existing_names: list) -> str:
        """
        Generate a standardized name by prefixing the project name.
        If the name exists in existing_names, append a numeric suffix.
        """
        base_standard = f"{self.project_name}_{base_name}"
        if base_standard not in existing_names:
            return base_standard
        else:
            suffix = 1
            while f"{base_standard}{suffix}" in existing_names:
                suffix += 1
            return f"{base_standard}{suffix}"
