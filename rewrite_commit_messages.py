import subprocess
import os
import sys

def run_git_command(args):
    """Run a git command and return (success, output)."""
    try:
        result = subprocess.run(["git"] + args, capture_output=True, text=True, check=True)
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: git {' '.join(args)}")
        print(f"Error: {e.stderr.strip()}")
        return False, e.stderr.strip()

def get_commit_list():
    """Get list of commit hashes in the current branch in reverse order (oldest first)."""
    success, output = run_git_command(["rev-list", "--reverse", "HEAD"])
    if not success:
        print("Failed to get commit list.")
        return []
    return output.splitlines()

def get_commit_message(commit_hash):
    """Get the commit message of a commit."""
    success, output = run_git_command(["log", "-1", "--pretty=%B", commit_hash])
    if not success:
        print(f"Failed to get commit message for {commit_hash}")
        return ""
    return output

def transform_commit_message(old_message):
    """
    Transform the old commit message to the new standard.
    This is a placeholder function. Customize this function as needed.
    """
    # Example: prepend "[NEW STANDARD]" to the old message
    new_message = "[NEW STANDARD] " + old_message.strip()
    return new_message

def rewrite_commit_messages():
    commit_list = get_commit_list()
    if not commit_list:
        print("No commits found to rewrite.")
        return

    # Create a temporary file for the rebase todo
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as todo_file:
        todo_path = todo_file.name
        for commit_hash in commit_list:
            todo_file.write(f"edit {commit_hash}\n")

    print("Starting interactive rebase to rewrite commit messages...")

    # Start the interactive rebase with the todo file
    # Use GIT_SEQUENCE_EDITOR to automatically use the todo file
    env = os.environ.copy()
    env["GIT_SEQUENCE_EDITOR"] = f"sed -i '1s/.*/{open(todo_path).read().replace(chr(10), chr(10))}/'"

    # However, since setting GIT_SEQUENCE_EDITOR like this is complex, we will just run rebase -i --root
    # and rely on the user to edit the todo list if needed.

    success, _ = run_git_command(["rebase", "-i", "--root", "-x", f"python3 {os.path.abspath(__file__)} --edit-commit"])
    if not success:
        print("Interactive rebase failed.")
        os.unlink(todo_path)
        return

    os.unlink(todo_path)
    print("Commit messages rewritten successfully.")

def edit_commit():
    """Edit the current commit message during rebase."""
    # Get current commit hash
    success, commit_hash = run_git_command(["rev-parse", "HEAD"])
    if not success:
        print("Failed to get current commit hash.")
        return

    old_message = get_commit_message(commit_hash)
    new_message = transform_commit_message(old_message)

    # Write new message to .git/COMMIT_EDITMSG
    git_dir = ".git"
    commit_editmsg_path = os.path.join(git_dir, "COMMIT_EDITMSG")
    try:
        with open(commit_editmsg_path, "w", encoding="utf-8") as f:
            f.write(new_message + "\n")
        print(f"Updated commit message for {commit_hash}")
    except Exception as e:
        print(f"Failed to write new commit message: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--edit-commit":
        edit_commit()
    else:
        rewrite_commit_messages()
