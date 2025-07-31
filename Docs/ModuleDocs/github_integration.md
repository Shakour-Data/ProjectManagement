# GitHubIntegration Module

## Overview
The `github_integration` module provides the `GitHubIntegration` class which facilitates interaction with the GitHub API for managing issues, project boards, pull requests, and wiki pages. It supports syncing project tasks with GitHub issues and linking pull requests to issues.

## Class: GitHubIntegration

### Description
The `GitHubIntegration` class manages GitHub repository interactions using the REST API. It requires a GitHub token and repository identifier for authentication and API calls.

### Methods

- `__init__(self, token=None, repo=None)`
  - Initializes the integration with a GitHub token and repository.
  - Raises `ValueError` if token or repo is not provided.

- `get_issues(self, state='open')`
  - Retrieves issues from the repository filtered by state.

- `create_issue(self, title, body=None, labels=None)`
  - Creates a new issue with the specified title, body, and labels.

- `update_issue(self, issue_number, state=None, title=None, body=None, labels=None)`
  - Updates an existing issue's state, title, body, or labels.

- `close_issue(self, issue_number)`
  - Closes an issue by setting its state to 'closed'.

- `sync_project_board(self)`
  - Syncs the project board using the GitHub Projects API.
  - Returns a message and project data or raises an error on failure.

- `link_pull_request(self, pr_number, issue_numbers)`
  - Links a pull request to multiple issues by adding comments to the issues.

- `update_wiki(self, content, page='Home')`
  - Placeholder method to update GitHub wiki pages.

- `sync_tasks_to_github(self, tasks)`
  - Syncs a list of task objects to GitHub issues.
  - Creates new issues for tasks without linked GitHub issues.
  - Updates existing issues for tasks with linked GitHub issue numbers.

## Usage
Create an instance with a GitHub token and repository, then use methods to manage issues and sync tasks.

---

This documentation provides an overview of the `github_integration` module to assist developers in integrating project management with GitHub.
