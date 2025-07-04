import subprocess
import sys

def test_cli_help():
    result = subprocess.run([sys.executable, 'cli_commands.py', '--help'], capture_output=True, text=True)
    assert "Project Management Tool CLI" in result.stdout

def test_cli_setup():
    result = subprocess.run([sys.executable, 'cli_commands.py', 'setup'], capture_output=True, text=True)
    assert "Setup completed successfully." in result.stdout

def test_cli_status():
    result = subprocess.run([sys.executable, 'cli_commands.py', 'status'], capture_output=True, text=True)
    assert "Configuration:" in result.stdout
