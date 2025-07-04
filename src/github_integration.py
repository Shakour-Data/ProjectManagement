import requests
import os

class GitHubIntegration:
    def __init__(self, token=None, repo=None):
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.repo = repo
        self.api_url = 'https://api.github.com'
        if not self.token:
            raise ValueError("GitHub token must be provided via parameter or GITHUB_TOKEN environment variable.")
        if not self.repo:
            raise ValueError("GitHub repository must be specified (e.g., 'user/repo').")
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    def get_issues(self, state='open'):
        url = f"{self.api_url}/repos/{self.repo}/issues"
        params = {'state': state}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    # Placeholder methods for future implementation
    def create_issue(self, title, body=None, labels=None):
        url = f"{self.api_url}/repos/{self.repo}/issues"
        data = {'title': title}
        if body:
            data['body'] = body
        if labels:
            data['labels'] = labels
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def update_issue(self, issue_number, state=None, title=None, body=None, labels=None):
        url = f"{self.api_url}/repos/{self.repo}/issues/{issue_number}"
        data = {}
        if state:
            data['state'] = state
        if title:
            data['title'] = title
        if body:
            data['body'] = body
        if labels is not None:
            data['labels'] = labels
        response = requests.patch(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def close_issue(self, issue_number):
        pass

    def sync_project_board(self):
        pass

    def link_pull_request(self, pr_number, issue_numbers):
        pass

    def update_wiki(self, content, page='Home'):
        pass

    def sync_tasks_to_github(self, tasks):
        """
        Sync a list of Task objects to GitHub issues.
        Creates new issues for tasks without linked GitHub issues,
        updates existing issues for tasks with github_issue_number.
        """
        for task in tasks:
            title = task.title
            body = task.description or ""
            labels = []
            if task.status == "completed":
                state = "closed"
            else:
                state = "open"

            if task.github_issue_number:
                # Update existing issue
                self.update_issue(
                    issue_number=task.github_issue_number,
                    state=state,
                    title=title,
                    body=body,
                    labels=labels
                )
            else:
                # Create new issue
                issue = self.create_issue(title=title, body=body, labels=labels)
                task.github_issue_number = issue.get('number')
        return tasks
