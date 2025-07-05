# Project Management System - Detailed Specification

## Overview
This project management system automates project tracking, reporting, and Scrum management by integrating JSON data, GitHub features, AI inputs, and Python scripts. It is designed with a two-layered architecture separating the current project and a general reusable framework.

## Data Sources
- JSON files (e.g., wbs_data.json, wbs_scores.json, task_progress.json) serve as the source of truth for tasks, scores, and progress.
- GitHub commit history, issues, pull requests, and project boards provide real-time updates.
- AI-generated inputs parse project manager discussions into structured tasks.

## Database Schema
- Tasks table with fields: id, title, description, importance, urgency, status, progress.
- Scrum-specific tables: sprints, backlog_items, burndown_data.
- Additional tables for resource allocation, notifications, and documentation tracking.

## Python Scripts
- Data importers: parse JSON files and populate the database.
- Progress data generator: parses git commits to calculate task progress.
- Importance and urgency calculator: computes task priority scores.
- GitHub integration: synchronizes issues, PRs, and project boards.
- AI integration: processes natural language inputs into tasks.
- Reporting: generates dashboards, changelogs, and notifications.

## Architecture
- Two-layered structure:
  - Current project: specific to this project’s activities and data.
  - General framework: reusable components and utilities for any project.
- Clear separation of source code, data, and tests.

## Reporting and Dashboards
- Real-time progress tracking.
- Importance-urgency visualizations.
- Burndown charts and sprint reports.
- Automated notifications for deadlines and stalled tasks.

## Testing Strategy
- Unit, integration, and end-to-end tests for all components.
- Separate test suites for current project and general framework.

## Next Steps
- Implement modular components per specification.
- Develop integration pipelines for GitHub and AI.
- Build user documentation and onboarding materials.
