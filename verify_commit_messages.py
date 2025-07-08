import subprocess

def run_git_command(args):
    """Run a git command and return (success, output)."""
    try:
        result = subprocess.run(["git"] + args, capture_output=True, text=True, check=True)
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: git {' '.join(args)}")
        print(f"Error: {e.stderr.strip()}")
        return False, e.stderr.strip()

def get_commit_list(branch="PM01"):
    """Get list of commit hashes in the specified branch in reverse order (oldest first)."""
    success, output = run_git_command(["rev-list", "--reverse", branch])
    if not success:
        print(f"Failed to get commit list for branch {branch}.")
        return []
    return output.splitlines()

def get_commit_message(commit_hash):
    """Get the commit message of a commit."""
    success, output = run_git_command(["log", "-1", "--pretty=%B", commit_hash])
    if not success:
        print(f"Failed to get commit message for {commit_hash}")
        return ""
    return output.strip()

def check_commit_message_standard(message):
    """Check if the commit message conforms to the new standard."""
    # Example check: message starts with "[NEW STANDARD]"
    return message.startswith("[NEW STANDARD]")

def verify_commit_messages(branch="PM01"):
    commit_list = get_commit_list(branch)
    if not commit_list:
        print("No commits found to verify.")
        return

    non_conforming_commits = []

    for commit_hash in commit_list:
        message = get_commit_message(commit_hash)
        if not check_commit_message_standard(message):
            non_conforming_commits.append((commit_hash, message))

    if not non_conforming_commits:
        print(f"All commit messages in branch {branch} conform to the new standard.")
    else:
        print(f"Found {len(non_conforming_commits)} commit(s) not conforming to the new standard in branch {branch}:")
        for commit_hash, message in non_conforming_commits:
            print(f"- Commit {commit_hash}:\n{message}\n")

if __name__ == "__main__":
    verify_commit_messages()
