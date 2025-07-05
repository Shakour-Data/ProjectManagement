import os
import subprocess
import datetime
from collections import defaultdict

def run_git_command(args):
    """Run a git command and return (success, output)."""
    try:
        result = subprocess.run(["git"] + args, capture_output=True, text=True, check=True)
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: git {' '.join(args)}")
        print(f"Error: {e.stderr.strip()}")
        return False, e.stderr.strip()

def get_git_changes():
    """Fetch Git status and return list of changes."""
    success, output = run_git_command(["status", "--short"])
    if not success:
        return []
    return output.splitlines()

def group_related_files(changes):
    """Group files based on top-level directory (code relationship)."""
    groups = defaultdict(list)

    for change in changes:
        if not change:
            continue
        if change.startswith("??"):
            status = "??"
            file_path = change[2:].lstrip()
        else:
            parts = change.split(None, 1)
            if len(parts) == 2:
                status, file_path = parts[0], parts[1].lstrip()
            else:
                status = parts[0]
                file_path = ""

        if status == "R":
            parts = file_path.split("->")
            if len(parts) == 2:
                old_path = parts[0].strip()
                new_path = parts[1].strip()
                file_path = new_path
            else:
                file_path = file_path.strip()

        parts = file_path.split(os.sep)
        if len(parts) > 1:
            top_level_dir = parts[0]
        else:
            top_level_dir = "root"

        groups[top_level_dir].append((status, file_path))

    return groups

def categorize_files(files):
    """Categorize files into different change types."""
    categories = defaultdict(list)

    for status, file in files:
        if status == "A":
            categories["Added"].append(file)
        elif status == "M":
            categories["Modified"].append(file)
        elif status == "D":
            categories["Deleted"].append(file)
        elif status == "R":
            categories["Renamed"].append(file)
        elif status == "??":
            categories["Untracked"].append(file)
        else:
            categories["Other"].append(file)

    return categories

def get_file_diff_summary(file_path):
    """Get a short summary of changes for a file."""
    try:
        result = subprocess.run(
            ["git", "diff", "--staged", "--", file_path],
            capture_output=True,
            text=True,
            check=True,
        )
        diff_lines = result.stdout.strip().splitlines()
        summary = "\\n    ".join(diff_lines[:5]) if diff_lines else "No diff available."
        return summary
    except subprocess.CalledProcessError:
        return "Could not retrieve diff."

def generate_commit_message(group_name, category_name, files):
    """Generate a professional conventional commit style message."""
    import datetime

    type_map = {
        "Added": "feat",
        "Modified": "fix",
        "Deleted": "remove",
        "Renamed": "refactor",
        "Copied": "chore",
        "Updated but unmerged": "conflict",
        "Untracked": "docs",
        "Ignored": "chore",
        "Added and Modified": "feat",
        "Deleted and Modified": "fix",
        "Renamed and Modified": "refactor",
        "Copied and Modified": "chore",
        "Unmerged": "conflict",
        "Type Changed": "refactor",
        "Unknown": "chore",
        "Other": "chore",
        "Conflicted": "conflict",
        "Staged": "chore",
        "Unstaged": "chore",
        "Both Modified": "fix",
    }
    emoji_map = {
        "feat": "✨",
        "fix": "🐛",
        "remove": "🗑️",
        "refactor": "♻️",
        "chore": "🔧",
        "conflict": "⚠️",
        "docs": "📝",
    }
    commit_type = type_map.get(category_name, "chore")
    emoji = emoji_map.get(commit_type, "")
    scope = group_name if group_name != "root" else ""
    subject = f"{emoji} {commit_type}"
    if scope:
        subject += f"({scope})"
    subject += f": {category_name} files updated"

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    body = f"Changes included (as of {timestamp}):\\n"
    for f in files:
        desc = {
            "Added": "This file was newly added to the project and is now tracked.",
            "Modified": "This file was modified with updates or fixes.",
            "Deleted": "This file was removed from the project.",
            "Renamed": "This file was renamed or moved to a different location.",
            "Copied": "This file was copied from another file.",
            "Updated but unmerged": "This file has merge conflicts that need to be resolved.",
            "Untracked": "This file is new and not yet tracked by git.",
            "Ignored": "This file is ignored by git.",
            "Added and Modified": "This file was added and then modified before committing.",
            "Deleted and Modified": "This file was deleted and modified before committing.",
            "Renamed and Modified": "This file was renamed and modified before committing.",
            "Copied and Modified": "This file was copied and modified before committing.",
            "Unmerged": "This file has unmerged changes.",
            "Type Changed": "The file type has changed.",
            "Unknown": "This file has an unknown change status.",
            "Other": "This file has other types of changes.",
            "Conflicted": "This file has conflicts that need to be resolved.",
            "Staged": "This file is staged for commit.",
            "Unstaged": "This file has unstaged changes.",
            "Both Modified": "This file was modified in both the index and working tree.",
        }.get(category_name, "")
        diff_summary = get_file_diff_summary(f)
        body += f"- {f}: {desc}\\n  Summary:\\n    {diff_summary}\\n"

    footer = "\\nPlease describe the reason or issue addressed by these changes."

    message = f"{subject}\\n\\n{body}\\n{footer}"
    return message

def auto_commit_and_push():
    """Automate Git commit and push process for each changed file separately."""
    import progress_report
    from task_management import TaskManagement

    # First, pull latest changes from origin/main to sync local main branch with fast-forward only
    success_pull, output_pull = run_git_command(["pull", "--ff-only", "origin", "main"])
    if not success_pull:
        print(f"Failed to pull latest changes from origin/main: {output_pull}")
        # Optionally, handle merge conflicts or abort
        return

    changes = get_git_changes()
    if not changes or (len(changes) == 1 and changes[0] == ''):
        print("No changes detected.")
        return

    grouped_files = group_related_files(changes)

    if not grouped_files:
        print("No grouped files found. Exiting.")
        return

    for group_name, files in grouped_files.items():
        categories = categorize_files(files)

        if not categories:
            print(f"No categories found for group {group_name}. Continuing.")
            continue

        for category_name, category_files in categories.items():
            if not category_files:
                print(f"No files in category {category_name} for group {group_name}. Continuing.")
                continue

            for f in category_files:
                # Stage only this file
                success, _ = run_git_command(["add", f])
                if not success:
                    print(f"Failed to stage file {f} for {group_name} - {category_name}. Skipping commit.")
                    continue

                # Generate commit message for this file
                commit_message = generate_commit_message(group_name, category_name, [f])

                # Commit only this file
                success, _ = run_git_command(["commit", "-m", commit_message])
                if not success:
                    print(f"Failed to commit file {f} for {group_name} - {category_name}. Skipping push.")
                    continue

                # Push the commit
                success, _ = run_git_command(["push"])
                if not success:
                    print(f"Failed to push commit for file {f} in {group_name} - {category_name}.")
                    continue

                print(f"Committed and pushed changes for file: {f} in group: {group_name} - {category_name}")

    # After all commits and pushes, update workflow steps from commit messages
    try:
        tm = TaskManagement()

        # Get recent commit messages (last 10 commits)
        success_log, log_output = run_git_command(["log", "-10", "--pretty=%B"])
        if success_log:
            commit_messages = log_output.strip().split("\\n\\n")
            for msg in commit_messages:
                tm.update_workflow_steps_from_commit_message(msg)

        tm.generate_wbs_from_idea("Develop Project Management Tool")
        progress_report.generate_report(tm)
        progress_report.generate_importance_urgency_report(tm)
        progress_report.generate_progress_dashboard_report(tm)

        # Stage and commit updated reports
        report_files = [progress_report.DASHBOARD_PATH, progress_report.IMPORTANCE_URGENCY_REPORT_PATH, os.path.join('docs', 'project_management', 'progress_dashboard.md')]
        for report_file in report_files:
            print(f"Staging report file: {report_file}")
            success, _ = run_git_command(["add", report_file])
            if not success:
                print(f"Failed to stage report file {report_file}.")
                continue
            # Check git status for the file
            success_status, status_output = run_git_command(["status", "--short", report_file])
            print(f"Git status for {report_file}: {status_output}")
            if not status_output:
                print(f"No changes detected for {report_file}, skipping commit.")
                continue
            commit_msg = f"chore: update project management report {report_file}"
            success, _ = run_git_command(["commit", "-m", commit_msg])
            if not success:
                print(f"Failed to commit report file {report_file}.")
                continue
            success, _ = run_git_command(["push"])
            if not success:
                print(f"Failed to push commit for report file {report_file}.")
                continue
            print(f"Committed and pushed updated report file: {report_file}")

        print("Project management reports updated and committed after commit.")
    except Exception as e:
        print(f"Failed to update project management reports: {e}")

if __name__ == "__main__":
    auto_commit_and_push()
