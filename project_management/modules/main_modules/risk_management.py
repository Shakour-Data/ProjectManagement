from project_management.modules.services.github_integration import GitHubIntegration
from collections import defaultdict

class RiskManagement:
    def __init__(self, github_integration):
        self.github = github_integration
        self.risk_issues = []
        self.project_risk_score = 0
        self.activity_risks = defaultdict(list)
        self.wbs_risks = defaultdict(list)
        self.wbs_hierarchy = {}  # To store parent-child relationships in WBS
        self.activity_importance = {}  # Importance scores for activities
        self.activity_priority = {}  # Priority scores for activities

    def identify_risks(self):
        # Identify risks from GitHub issues labeled as 'risk'
        issues = self.github.get_issues(state="open")
        self.risk_issues = [issue for issue in issues if 'risk' in [label['name'].lower() for label in issue.get('labels', [])]]
        self._categorize_risks()
        self._calculate_project_risk_score()
        return self.risk_issues

    def _categorize_risks(self):
        # Categorize risks by activity and WBS based on issue metadata or labels
        for issue in self.risk_issues:
            labels = [label['name'].lower() for label in issue.get('labels', [])]
            activity = None
            wbs = None
            importance = 1  # Default importance
            priority = 1  # Default priority
            for label in labels:
                if label.startswith("activity:"):
                    activity = label.split("activity:")[1].strip()
                if label.startswith("wbs:"):
                    wbs = label.split("wbs:")[1].strip()
                if label.startswith("importance:"):
                    try:
                        importance = float(label.split("importance:")[1].strip())
                    except ValueError:
                        importance = 1
                if label.startswith("priority:"):
                    try:
                        priority = float(label.split("priority:")[1].strip())
                    except ValueError:
                        priority = 1
            if activity:
                self.activity_risks[activity].append(issue)
                self.activity_importance[activity] = importance
                self.activity_priority[activity] = priority
            if wbs:
                self.wbs_risks[wbs].append(issue)

    def _calculate_project_risk_score(self):
        # Calculate project risk score considering importance and priority
        score = 0
        for activity, issues in self.activity_risks.items():
            importance = self.activity_importance.get(activity, 1)
            priority = self.activity_priority.get(activity, 1)
            score += len(issues) * importance * priority
        self.project_risk_score = score

    def get_risk_summary(self):
        summary = {
            "total_risks": len(self.risk_issues),
            "project_risk_score": self.project_risk_score,
            "activity_risks": {k: len(v) for k, v in self.activity_risks.items()},
            "wbs_risks": {k: len(v) for k, v in self.wbs_risks.items()},
            "risks": [{
                "id": issue['number'],
                "title": issue['title'],
                "created_at": issue['created_at'],
                "url": issue['html_url']
            } for issue in self.risk_issues]
        }
        return summary

if __name__ == "__main__":
    repo_owner = "your_org_or_username"
    repo_name = "ProjectManagement"
    github = GitHubIntegration(repo_owner, repo_name)
    risk_manager = RiskManagement(github)
    risks = risk_manager.identify_risks()
    print(f"Identified {len(risks)} risks:")
    for risk in risks:
        print(f"- [{risk['number']}] {risk['title']} ({risk['html_url']})")
    summary = risk_manager.get_risk_summary()
    print("\nRisk Summary:")
    print(summary)
