import subprocess
import sys
import os

def run_auto_commit_tests():
    venv_python = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'venv', 'Scripts', 'python.exe'))
    if not os.path.exists(venv_python):
        print(f"Virtual environment python not found at {venv_python}")
        sys.exit(1)
    test_script = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'project_management', 'modules', 'auto_commit.py'))
    print(f"Running auto_commit.py tests using {venv_python}")
    result = subprocess.run([venv_python, test_script], capture_output=True, text=True)
    print("Test output:")
    print(result.stdout)
    if result.returncode != 0:
        print("Test errors:")
        print(result.stderr)
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_auto_commit_tests())
