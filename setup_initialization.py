import os
import subprocess
import sys
import venv

def create_virtualenv(env_dir='venv'):
    """Create a virtual environment in the specified directory."""
    if not os.path.exists(env_dir):
        print(f"Creating virtual environment at {env_dir}...")
        venv.create(env_dir, with_pip=True)
        print("Virtual environment created.")
    else:
        print(f"Virtual environment already exists at {env_dir}.")

def install_dependencies(env_dir='venv', requirements_file='requirements.txt'):
    """Install dependencies from requirements.txt into the virtual environment."""
    pip_executable = os.path.join(env_dir, 'bin', 'pip')
    if not os.path.exists(pip_executable):
        print("pip not found in virtual environment. Please check the environment setup.")
        return
    if not os.path.exists(requirements_file):
        print(f"{requirements_file} not found. Skipping dependency installation.")
        return
    print(f"Installing dependencies from {requirements_file}...")
    subprocess.check_call([pip_executable, 'install', '-r', requirements_file])
    print("Dependencies installed.")

def main():
    create_virtualenv()
    install_dependencies()

if __name__ == '__main__':
    main()
