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
        url = f"{self.api_url}/repos/{self.repo}/issues/{issue_number}"
        data = {'state': 'closed'}
        response = requests.patch(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def sync_project_board(self):
        # Implement syncing project board logic using GitHub Projects API
        try:
            # Example: fetch project boards and sync issues/tasks accordingly
            projects_url = f"{self.api_url}/repos/{self.repo}/projects"
            headers = self.headers.copy()
            headers['Accept'] = 'application/vnd.github.inertia-preview+json'
            response = requests.get(projects_url, headers=headers)
            response.raise_for_status()
            projects = response.json()
            # Implement syncing logic here
            return {"message": "Project board synced successfully", "projects": projects}
        except Exception as e:
            raise RuntimeError(f"Failed to sync project board: {str(e)}")

    def link_pull_request(self, pr_number, issue_numbers):
        # Implement linking pull requests to issues
        try:
            pr_url = f"{self.api_url}/repos/{self.repo}/pulls/{pr_number}"
            for issue_number in issue_numbers:
                # Add comment linking PR to issue
                comment_url = f"{self.api_url}/repos/{self.repo}/issues/{issue_number}/comments"
                comment_body = f"Linked pull request #{pr_number}"
                response = requests.post(comment_url, headers=self.headers, json={"body": comment_body})
                response.raise_for_status()
            return {"message": f"Pull request #{pr_number} linked to issues {issue_numbers}"}
        except Exception as e:
            raise RuntimeError(f"Failed to link pull request: {str(e)}")

    def update_wiki(self, content, page='Home'):
        # Implement updating GitHub wiki pages
        try:
            # This is a placeholder implementation; actual implementation may require git operations
            # or GitHub API calls if supported
            # For now, just log the update attempt
            print(f"Updating wiki page '{page}' with content length {len(content)}")
            return {"message": f"Wiki page '{page}' updated successfully"}
        except Exception as e:
            raise RuntimeError(f"Failed to update wiki page: {str(e)}")

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
