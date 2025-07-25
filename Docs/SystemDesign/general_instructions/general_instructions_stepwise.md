General Instructions Stepwise



# Step-by-Step Instructions for Building the Project Management Tool

This document provides a detailed, ordered procedure for building, setting up, and operating the Project Management Tool. Each step specifies what to do, how to do it, when, and by whom.

---

## Step 1: Initial Setup and Installation

**What:** Install the project management tool and prepare the development environment.

**How:**
- Install the tool as a Python package/library.
- The installation process will automatically create a Python virtual environment and install all required dependencies.
- Essential VS Code extensions (e.g., BLACKBOX AI) will be installed automatically.
- Securely store GitHub authentication tokens.
- Initialize the project management state.

**When:** At the start of the project.

**Who:** DevOps engineer or project lead.

---

## Step 2: Define Project Scope and Inputs

**What:** Provide initial creative inputs describing the project goals, features, and requirements.

**How:**
- Use the VS Code chat interface to input natural language descriptions, code snippets, or images.
- Ensure inputs are clear and cover project objectives.

**When:** Immediately after setup.

**Who:** Project manager or product owner.

---

## Step 3: Generate Work Breakdown Structure (WBS)

**What:** Create a hierarchical breakdown of the project into manageable tasks.

**How:**
- Use the tool’s AI-assisted WBS generation from the creative inputs.
- Review and refine the generated WBS.
- Assign unique IDs, titles, descriptions, deadlines, dependencies, and priorities to tasks.
- Convert WBS to JSON format for programmatic use.

**When:** After defining project scope.

**Who:** Project manager and team leads.

---

## Step 4: Resource Allocation

**What:** Assign resources (human and equipment) to project tasks.

**How:**
- Define resources in JSON resource files with detailed attributes.
- Allocate resources to tasks with percentages, roles, and timeframes.
- Validate resource availability and avoid overbooking.
- Update allocations regularly as project progresses.

**When:** After WBS finalization.

**Who:** Resource manager and project manager.

---

## Step 5: Configure Task Management and Scheduling

**What:** Set up task dependencies, priorities, and schedules.

**How:**
- Use the tool to parse tasks and dependencies.
- Define task priorities based on importance and urgency.
- Schedule tasks considering dependencies and resource availability.
- Set deadlines and reminders.

**When:** After resource allocation.

**Who:** Project manager and team leads.

---

## Step 6: Development and Workflow Execution

**What:** Execute coding, testing, documentation, and review workflows.

**How:**
- Developers work on assigned tasks.
- Commit code with task IDs in commit messages.
- Complete workflow steps: coding, testing, documentation, code review, merge, deployment, verification.
- Use GitHub Issues and Project boards for status tracking.
- Automate testing and CI/CD pipelines with GitHub Actions.

**When:** Throughout project execution.

**Who:** Developers, testers, and reviewers.

---

## Step 7: Progress Tracking and Reporting

**What:** Monitor project progress and generate reports.

**How:**
- Calculate progress combining commit history and workflow step completion.
- Generate automated markdown and text-based reports.
- Use real-time dashboards in VS Code and GitHub.
- Send notifications for stalled tasks, deadlines, and reviews.

**When:** Continuously during project execution.

**Who:** Project manager and stakeholders.

---

## Step 8: Documentation and SOP Management

**What:** Manage project documentation and standard operating procedures.

**How:**
- Maintain documentation in markdown or text files within the repository.
- Version and synchronize documentation automatically.
- Integrate with GitHub Wiki for extended collaboration.

**When:** Throughout project lifecycle.

**Who:** Documentation specialists and project manager.

---

## Step 9: Security and Permissions Management

**What:** Ensure secure access and role-based permissions.

**How:**
- Encrypt and securely store authentication tokens.
- Implement role-based access control.
- Monitor compliance with GitHub API limits.

**When:** From project start and ongoing.

**Who:** Security officer and project manager.

---

## Step 10: Backup, Recovery, and Extensibility

**What:** Maintain data integrity and extend tool capabilities.

**How:**
- Automate backups of project state, documentation, and configurations.
- Implement recovery mechanisms for data loss or corruption.
- Use plugin architecture to add features or integrate external tools.
- Leverage GitHub Actions and internal bots for automation.

**When:** Continuously.

**Who:** DevOps engineer and project manager.

---

## Summary

Following these ordered steps ensures a structured, efficient, and secure approach to building and managing the Project Management Tool. Clear responsibilities and procedures enable smooth collaboration and successful project delivery.

---

## Dynamic Importance and Urgency Calculation

The project management tool calculates task importance and urgency dynamically based on multiple factors to prioritize work effectively. The calculation uses a recursive scoring approach:

* **Importance Calculation:**
* Considers deadline proximity, number of dependencies, and task priority.
* Formula:  
  `importance = w1 * (1 - normalized_time_to_deadline) + w2 * dependency_factor + w3 * priority_factor`  
  where weights sum to 1 (e.g., w1=0.5, w2=0.3, w3=0.2).
* Normalized time to deadline is calculated over a 7-day window.
* Dependency factor is the ratio of dependencies to a maximum threshold.
* Priority factor is normalized task priority.
* **Urgency Calculation:**
* Considers deadline proximity, task status, and resource availability.
* Formula:  
  `urgency = w1 * (1 - normalized_time_to_deadline) + w2 * status_factor + w3 * resource_availability_factor`  
  where weights sum to 1 (e.g., w1=0.6, w2=0.3, w3=0.1).
* Normalized time to deadline is calculated over a 3-day window.
* Status factor is 1 for pending or in-progress tasks, 0 otherwise.
* Resource availability factor is 1 if no resources assigned, else 0.
* **Implementation:**
* The tool recursively scores tasks and subtasks.
* Scores are stored and used to calculate combined task scores.
* Scores are updated dynamically as project data changes.

For detailed code implementation, see `project_inputs/modules/importance_urgency_calculator.py`.

For further assistance, please contact the project management office.

---